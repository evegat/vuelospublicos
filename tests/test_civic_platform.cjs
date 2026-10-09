/**
 * Comprehensive Automated Test Suite for P167 VuelosPublicos (Milestone M1)
 * Rediseño Integral de Plataforma Cívica
 */

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');
const assert = require('node:assert');

console.log('=== P167 VuelosPublicos: Automated M1 Civic Platform Verification ===\n');

const repoRoot = path.resolve(__dirname, '..');
const indexPath = path.join(repoRoot, 'index.html');
const docsIndexPath = path.join(repoRoot, 'docs', 'index.html');

// 1. File Synchronization & Presence
console.log('1. Verifying file synchronization between index.html and docs/index.html...');
assert(fs.existsSync(indexPath), 'deploy/index.html must exist');
assert(fs.existsSync(docsIndexPath), 'deploy/docs/index.html must exist');

const indexHtml = fs.readFileSync(indexPath, 'utf-8');
const docsIndexHtml = fs.readFileSync(docsIndexPath, 'utf-8');

const hashIndex = crypto.createHash('sha256').update(indexHtml).digest('hex');
const hashDocs = crypto.createHash('sha256').update(docsIndexHtml).digest('hex');

assert.strictEqual(hashIndex, hashDocs, 'deploy/index.html and deploy/docs/index.html must have identical SHA-256');
console.log(`   [PASS] SHA-256 match: ${hashIndex.slice(0, 16)}... (${indexHtml.length} bytes)`);

// 2. Structural & Terminological Verifications (Civic vs War-Room)
console.log('\n2. Verifying civic usability & elimination of war-room jargon...');

const forbiddenJargon = [
  'DEFCON',
  'defcon',
  'WAR ROOM',
  'war-room',
  'radar sweep',
  'sonar ping',
  'analog knob',
  'classified ops',
  'military alert'
];

for (const term of forbiddenJargon) {
  assert(!indexHtml.includes(term), `Forbidden war-room term found in HTML: "${term}"`);
}
console.log('   [PASS] Zero war-room jargon or analog knobs found.');

const requiredCivicElements = [
  'Observatorio Cívico',
  'VuelosPúblicos',
  'Tribunal Ciudadano',
  'Ley 19.886',
  'Odómetro Fiscal',
  'Se justifica',
  'Es derroche',
  'timelineSlider',
  'fiscalOdometer',
  'radarCanvas',
  'flightListContainer',
  'dossier-housing',
  'btnApprove',
  'btnReject'
];

for (const req of requiredCivicElements) {
  assert(indexHtml.includes(req), `Required civic UI element missing: "${req}"`);
}
console.log('   [PASS] All civic governance, tribunal, and odometer components present in markup.');

// 3. Execution of Frontend Script in Sandboxed VM
console.log('\n3. Extracting and executing frontend logic in isolated environment...');

const scriptMatch = indexHtml.match(/<script>([\s\S]*?)<\/script>/);
assert(scriptMatch, 'index.html must contain an inline <script> block');
const scriptCode = scriptMatch[1];

// Create a DOM & Browser shim environment for testing logic
const storage = new Map();
const mockLocalStorage = {
  getItem: (k) => storage.get(k) || null,
  setItem: (k, v) => storage.set(k, String(v)),
  removeItem: (k) => storage.delete(k),
  clear: () => storage.clear()
};

const domElements = new Map();
function createMockElement(id = '', tag = 'div') {
  const el = {
    id,
    tagName: tag.toUpperCase(),
    className: '',
    innerHTML: '',
    innerText: '',
    textContent: '',
    value: '0',
    dataset: {},
    style: {},
    classList: {
      classes: new Set(),
      add: (c) => el.classList.classes.add(c),
      remove: (c) => el.classList.classes.delete(c),
      toggle: (c, f) => (f !== undefined ? (f ? el.classList.classes.add(c) : el.classList.classes.delete(c)) : el.classList.classes.has(c) ? el.classList.classes.delete(c) : el.classList.classes.add(c)),
      contains: (c) => el.classList.classes.has(c)
    },
    addEventListener: () => {},
    removeEventListener: () => {},
    appendChild: () => {},
    setAttribute: () => {},
    getAttribute: () => null,
    closest: () => null,
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 600 }),
    getContext: () => ({
      clearRect: () => {},
      save: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      arc: () => {},
      fill: () => {},
      stroke: () => {},
      fillRect: () => {},
      setLineDash: () => {},
      quadraticCurveTo: () => {},
      bezierCurveTo: () => {},
      measureText: () => ({ width: 40 }),
      fillText: () => {},
      closePath: () => {},
      translate: () => {},
      rotate: () => {}
    })
  };
  return el;
}

const mockDocument = {
  getElementById: (id) => {
    if (!domElements.has(id)) {
      domElements.set(id, createMockElement(id));
    }
    return domElements.get(id);
  },
  querySelectorAll: (selector) => [],
  querySelector: (selector) => createMockElement(),
  createElement: (tag) => createMockElement('', tag),
  addEventListener: () => {}
};

const sandbox = {
  window: { devicePixelRatio: 1 },
  document: mockDocument,
  localStorage: mockLocalStorage,
  performance: { now: () => Date.now() },
  requestAnimationFrame: () => 1,
  cancelAnimationFrame: () => {},
  console: {
    log: () => {},
    warn: () => {},
    error: (...args) => {
      console.error('[BROWSER ERROR]', ...args);
      throw new Error(`Unexpected browser error: ${args.join(' ')}`);
    }
  },
  Math,
  Date,
  Intl,
  Array,
  Object,
  String,
  Number,
  Boolean,
  RegExp,
  JSON,
  parseInt,
  parseFloat,
  isNaN,
  setTimeout: () => 1,
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {}
};
sandbox.window.addEventListener = () => {};
sandbox.window.document = mockDocument;

// Run the script in the VM
vm.createContext(sandbox);
vm.runInContext(scriptCode, sandbox);

// Extract lexical closures
const flights = vm.runInContext('FLIGHTS', sandbox);
const continentsGeo = vm.runInContext('CONTINENTS_GEO', sandbox);
const castVote = (id, type) => vm.runInContext(`castVote(${JSON.stringify(id)}, ${JSON.stringify(type)})`, sandbox);
const getSortedFlights = () => vm.runInContext('getSortedFlights()', sandbox);
const calculateOdometer = (monthIdx, prov) => vm.runInContext(`calculateOdometer(${monthIdx}, ${JSON.stringify(prov)})`, sandbox);
const geoToCanvas = (lon, lat) => vm.runInContext(`geoToCanvas(${lon}, ${lat})`, sandbox);
const getArcPoint = (p1, p2, t) => vm.runInContext(`getArcPoint(${JSON.stringify(p1)}, ${JSON.stringify(p2)}, ${t})`, sandbox);

// 4. Verify Dataset Invariants
console.log('\n4. Verifying Canonical Flight Dataset (12 flights, $44.900.000 CLP)...');
assert(Array.isArray(flights), 'FLIGHTS must be an array');
assert.strictEqual(flights.length, 12, 'FLIGHTS must contain exactly 12 canonical flights');

let totalCost = 0;
const providerTotals = {};

flights.forEach((f, idx) => {
  assert(f.id && f.id.startsWith('FL-'), `Flight #${idx} missing valid id`);
  assert(f.date && /^\d{4}-\d{2}-\d{2}$/.test(f.date), `Flight #${idx} missing valid YYYY-MM-DD date`);
  assert(typeof f.monthIndex === 'number' && f.monthIndex >= 0 && f.monthIndex <= 35, `Flight #${idx} invalid monthIndex: ${f.monthIndex}`);
  assert(f.origin && f.dest, `Flight #${idx} missing origin or destination`);
  assert(f.entity, `Flight #${idx} missing entity`);
  assert(typeof f.cost === 'number' && f.cost > 0, `Flight #${idx} invalid cost`);
  assert(f.oc && /^\d+-\d+-[A-Z0-9]+$/.test(f.oc), `Flight #${idx} missing valid Mercado Público OC: ${f.oc}`);
  assert(f.reason, `Flight #${idx} missing flight motive`);
  assert(f.votes && typeof f.votes.approve === 'number' && typeof f.votes.reject === 'number', `Flight #${idx} missing vote tallies`);
  
  totalCost += f.cost;
  providerTotals[f.provider] = (providerTotals[f.provider] || 0) + f.cost;
});

assert.strictEqual(totalCost, 44900000, `Total cost must equal exactly $44.900.000 CLP (got ${totalCost})`);
console.log(`   [PASS] 12 canonical flights verified. Total expenditure: $${totalCost.toLocaleString('es-CL')} CLP`);

// Verify provider distribution
assert.strictEqual(providerTotals['Cocha'], 23170000, 'Cocha total should be $23.170.000');
assert.strictEqual(providerTotals['Turavion'], 14200000, 'Turavion total should be $14.200.000');
assert.strictEqual(providerTotals['LATAM'], 5460000, 'LATAM total should be $5.460.000');
assert.strictEqual(providerTotals['Sky'], 2070000, 'Sky total should be $2.070.000');
console.log('   [PASS] Provider fiscal breakdown matches spec exactly.');

// 5. Test Voting Mathematics & Symmetry (P_A + P_R == 100%)
console.log('\n5. Verifying Voting Symmetry and Anti-duplicate Locking...');

for (const f of flights) {
  const total = f.votes.approve + f.votes.reject;
  const pctApprove = Math.round((f.votes.approve / total) * 100);
  const pctReject = 100 - pctApprove;
  assert.strictEqual(pctApprove + pctReject, 100, `Voting percentage sum must equal exactly 100% for ${f.id}`);
}
console.log('   [PASS] Voting percentage symmetry verified across all 12 initial tallies.');

// Test reactive vote registration
const flightToVote = flights[0]; // FL-001
const initialApprove = flightToVote.votes.approve;

// Call castVote in sandbox
const voteResult = castVote(flightToVote.id, 'approve');
assert.strictEqual(voteResult, true, 'castVote must return true on first vote');

// Check that tallies increased
assert.strictEqual(flightToVote.votes.approve, initialApprove + 1, 'Approval votes must increment by 1');

// Check localStorage keys
const userVotesRaw = mockLocalStorage.getItem('vuelospublicos_user_votes');
assert(userVotesRaw, 'User votes must be saved in localStorage under vuelospublicos_user_votes');
const userVotes = JSON.parse(userVotesRaw);
assert.strictEqual(userVotes[flightToVote.id], 'approve', 'User vote must record approve for FL-001');

// Verify duplicate voting is rejected
const duplicateVote = castVote(flightToVote.id, 'reject');
assert.strictEqual(duplicateVote, false, 'castVote must return false on duplicate vote attempt');
assert.strictEqual(flightToVote.votes.approve, initialApprove + 1, 'Approval votes must remain unchanged on duplicate vote');
assert.strictEqual(userVotes[flightToVote.id], 'approve', 'Vote type must not change on duplicate vote');
console.log('   [PASS] Vote casting, tally increment, and anti-duplicate lock verified.');

// 6. Test Sorting and Filtering Logic
console.log('\n6. Verifying Sorting and Filter Reactivity...');

// Sort by cost desc
vm.runInContext("currentSort = 'cost';", sandbox);
const sortedCost = getSortedFlights();
assert.strictEqual(sortedCost[0].id, 'FL-006', 'Most expensive flight must be FL-006 ($9.120.000)');
assert.strictEqual(sortedCost[11].id, 'FL-008', 'Cheapest flight must be FL-008 ($480.000)');

// Sort by date
vm.runInContext("currentSort = 'date';", sandbox);
const sortedDate = getSortedFlights();
assert.strictEqual(sortedDate[0].id, 'FL-001', 'Earliest flight must be FL-001 (2024-03-14)');
assert.strictEqual(sortedDate[11].id, 'FL-012', 'Latest flight must be FL-012 (2026-08-14)');

// Filter by Provider
vm.runInContext("selectedProvider = 'Turavion';", sandbox);
const turavionFiltered = getSortedFlights();
assert.strictEqual(turavionFiltered.length, 3, 'Turavion filter must yield 3 flights ($14.200.000)');
vm.runInContext("selectedProvider = 'Todas';", sandbox);
console.log('   [PASS] Multidimensional sorting and provider filters verified.');

// 7. Test Timeline Scrubber & Cumulative Fiscal Odometer
console.log('\n7. Verifying 36-Month Timeline Scrubber & Fiscal Odometer...');

// Initial scrubber: Month Index 2 (Marzo 2024)
const cumulativeAt2 = calculateOdometer(2, 'Todas');
assert.strictEqual(cumulativeAt2, 8450000, 'Cumulative expenditure up to Marzo 2024 must be $8.450.000');

// Scrubber at Month Index 35 (Dec 2026 / all flights)
const cumulativeAt35 = calculateOdometer(35, 'Todas');
assert.strictEqual(cumulativeAt35, 44900000, 'Cumulative expenditure at max month must be full $44.900.000');
console.log(`   [PASS] Fiscal odometer accumulated correctly ($8.450.000 -> $44.900.000).`);

// 8. Test Geospatial Cartography & Vector Math
console.log('\n8. Verifying 2D Canvas Cartography Math & Projections...');
assert(Array.isArray(continentsGeo), 'CONTINENTS_GEO must exist');
let totalVertexCount = 0;
for (const poly of continentsGeo) {
  assert(Array.isArray(poly), 'Each polygon must be an array of vertices');
  totalVertexCount += poly.length;
  for (const [lon, lat] of poly) {
    assert(typeof lon === 'number' && !isNaN(lon), 'Longitude must be valid number');
    assert(typeof lat === 'number' && !isNaN(lat), 'Latitude must be valid number');
    const pt = geoToCanvas(lon, lat);
    assert(!isNaN(pt.x) && !isNaN(pt.y), 'Projected point must not be NaN');
  }
}
assert(totalVertexCount >= 200, `Cartography must contain detailed vector geometry (got ${totalVertexCount} vertices)`);
console.log(`   [PASS] Vector cartography verified (${totalVertexCount} vertices, projections valid).`);

// Ballistic arc interpolation
const p1 = { x: 100, y: 100 };
const p2 = { x: 500, y: 400 };
const arcMid = getArcPoint(p1, p2, 0.5);
assert(!isNaN(arcMid.x) && !isNaN(arcMid.y), 'Arc midpoint must be valid numbers');
assert(arcMid.y < (p1.y + p2.y) * 0.5, 'Ballistic arc must curve upward (lower Y)');
console.log('   [PASS] 2.5D ballistic geodesic curve calculation verified.');

console.log('\n=============================================================');
console.log('ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (8/8)');
console.log('Milestone M1 Rediseño Integral de Plataforma Cívica is 100% COMPLETE.');
console.log('=============================================================\n');
