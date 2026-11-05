import re
import os

def update_build_frontend():
    file_path = os.path.join(os.path.dirname(__file__), "build_frontend.py")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update <head> metadata in template
    old_meta = """  <title>VuelosPúblicos — Observatorio Cívico del Gasto en Pasajes Aéreos del Estado de Chile</title>
  <meta name="description" content="Observatorio ciudadano y auditoría del gasto en pasajes aéreos y comitivas oficiales de la administración del Estado de Chile (2007-2026). Trazabilidad oficial con Mercado Público (Ley 19.886) y Transparencia Activa (Ley 20.285).">
  <meta property="og:title" content="VuelosPúblicos — Observatorio Cívico de Pasajes del Estado">
  <meta property="og:description" content="Auditoría ciudadana y visualización geoespacial de 459 compras públicas de pasajes aéreos en comitivas oficiales de Chile.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://vuelospublicos.evegat.cl/">"""

    new_meta = """  <title>VuelosPúblicos — Observatorio Cívico del Gasto en Pasajes Aéreos del Estado de Chile</title>
  <meta name="description" content="Observatorio ciudadano y auditoría del gasto en pasajes aéreos y comitivas oficiales de la administración del Estado de Chile (2007-2026). Trazabilidad oficial con Mercado Público (Ley 19.886) y Transparencia Activa (Ley 20.285).">
  <meta name="author" content="Eduardo Vega Toledo">
  <meta name="keywords" content="ChileCompra, Mercado Público, Pasajes Aéreos, Comitivas Oficiales, Transparencia, Datos Abiertos, GovTech, Auditoría Cívica, Estado de Chile, Open Data">

  <!-- Open Graph / LinkedIn / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://vuelospublicos.evegat.cl/">
  <meta property="og:site_name" content="VuelosPúblicos">
  <meta property="og:title" content="VuelosPúblicos — Observatorio Cívico de Pasajes del Estado">
  <meta property="og:description" content="Auditoría ciudadana y visualización geoespacial de compras públicas de pasajes aéreos en comitivas oficiales de Chile (2007-2026). Datos oficiales de ChileCompra (Ley 19.886) y Transparencia Activa.">
  <meta property="og:image" content="https://vuelospublicos.evegat.cl/og-image.png">
  <meta property="og:image:secure_url" content="https://vuelospublicos.evegat.cl/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Observatorio Cívico VuelosPúblicos con cartografía 2.5D y odómetro fiscal">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="VuelosPúblicos — Observatorio Cívico de Pasajes del Estado">
  <meta name="twitter:description" content="Auditoría ciudadana y radar táctico de compras públicas en comitivas oficiales del Estado de Chile.">
  <meta name="twitter:image" content="https://vuelospublicos.evegat.cl/og-image.png">"""

    if old_meta in content:
        content = content.replace(old_meta, new_meta)
        print("[+] Meta tags actualizados.")
    else:
        print("[-] old_meta no encontrado exactamente, verificando variantes...")

    # 2. Add .btn-linkedin-pill CSS
    old_btn_help_css = """.btn-help-modal:hover {
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }"""
    
    # Notice double braces in Python f-string
    new_btn_help_css = """.btn-help-modal:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .btn-linkedin-pill {{
      background: rgba(10, 102, 194, 0.18) !important;
      border-color: rgba(10, 102, 194, 0.45) !important;
      color: #70b5f9 !important;
    }}
    .btn-linkedin-pill:hover {{
      background: #0a66c2 !important;
      border-color: #0a66c2 !important;
      color: #ffffff !important;
    }}"""

    old_btn_help_target = """.btn-help-modal:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}"""

    if old_btn_help_target in content:
        content = content.replace(old_btn_help_target, new_btn_help_css)
        print("[+] CSS .btn-linkedin-pill agregado.")

    # 3. Add .share-box and social buttons CSS
    old_share_css = """    /* Compartir Expediente */
    .share-box {{
      border-top: 1px solid var(--border-subtle);
      padding: 8px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
    }}

    .btn-share-expediente {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .btn-share-expediente:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
      color: #ffffff;
    }}

    .share-toast {{
      display: none;
      font-size: 0.7rem;
      color: #38bdf8;
      text-align: center;
      font-weight: 600;
    }}"""

    new_share_css = """    /* Compartir Expediente y Redes */
    .share-box {{
      border-top: 1px solid var(--border-subtle);
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      position: relative;
      background: rgba(12, 20, 32, 0.4);
    }}

    .share-actions-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }}

    .btn-share-social {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 6px 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.15s ease;
      text-decoration: none;
    }}

    .btn-share-social:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
      color: #ffffff;
    }}

    .btn-share-social.btn-linkedin {{
      border-color: rgba(10, 102, 194, 0.45);
      background: rgba(10, 102, 194, 0.15);
      color: #70b5f9;
    }}
    .btn-share-social.btn-linkedin:hover {{
      background: #0a66c2;
      border-color: #0a66c2;
      color: #ffffff;
    }}

    .btn-share-social.btn-wa {{
      border-color: rgba(37, 211, 102, 0.4);
      background: rgba(37, 211, 102, 0.12);
      color: #4ade80;
    }}
    .btn-share-social.btn-wa:hover {{
      background: #16a34a;
      border-color: #16a34a;
      color: #ffffff;
    }}

    .btn-share-social.btn-x:hover {{
      background: #000000;
      border-color: #ffffff;
      color: #ffffff;
    }}

    .btn-share-expediente {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 7px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
      width: 100%;
    }}

    .btn-share-expediente:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
      color: #ffffff;
    }}

    .share-toast {{
      display: none;
      font-size: 0.7rem;
      color: #38bdf8;
      text-align: center;
      font-weight: 600;
      padding: 4px;
      border-radius: var(--radius-sm);
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.2);
    }}"""

    if old_share_css in content:
        content = content.replace(old_share_css, new_share_css)
        print("[+] CSS .share-box y botones sociales actualizado.")

    # 4. Header action button: Add Ficha LinkedIn
    old_header_btn = """        <button class="btn-help-modal" id="btnOpenHelp" aria-label="Abrir fuentes y metodología">
          <span>ℹ️ Metodología</span>
        </button>"""
    
    new_header_btn = """        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn-help-modal btn-linkedin-pill" id="btnOpenLinkedInModal" aria-label="Abrir Ficha Ejecutiva para LinkedIn">
            <span>💼 Ficha LinkedIn</span>
          </button>
          <button class="btn-help-modal" id="btnOpenHelp" aria-label="Abrir fuentes y metodología">
            <span>📖 Metodología</span>
          </button>
        </div>"""

    if old_header_btn in content:
        content = content.replace(old_header_btn, new_header_btn)
        print("[+] Botón Ficha LinkedIn agregado en Header.")

    # 5. Expediente share box HTML
    old_share_html = """        <!-- Compartir Expediente -->
        <div class="share-box">
          <button class="btn-share-expediente" id="btnShareExpediente" title="Compartir este expediente oficial">
            <span>📤 Compartir Expediente (WhatsApp / X)</span>
          </button>
          <div class="share-toast" id="shareToast">Enlace directo copiado al portapapeles ✓</div>
        </div>"""

    new_share_html = """        <!-- Compartir Expediente -->
        <div class="share-box">
          <div class="share-actions-row">
            <button class="btn-share-social btn-linkedin" id="btnShareLinkedIn" title="Compartir este expediente en LinkedIn">
              <span>💼 LinkedIn</span>
            </button>
            <button class="btn-share-social btn-wa" id="btnShareWhatsApp" title="Compartir por WhatsApp">
              <span>💬 WhatsApp</span>
            </button>
            <button class="btn-share-social btn-x" id="btnShareX" title="Compartir en X">
              <span>𝕏 Post</span>
            </button>
          </div>
          <button class="btn-share-expediente" id="btnShareExpediente" title="Copiar Ficha Cívica oficial para LinkedIn">
            <span>📋 Copiar Ficha Cívica (LinkedIn)</span>
          </button>
          <div class="share-toast" id="shareToast">Enlace directo copiado al portapapeles ✓</div>
        </div>"""

    if old_share_html in content:
        content = content.replace(old_share_html, new_share_html)
        print("[+] HTML share-box actualizado con suite social.")

    # 6. LinkedIn Modal HTML
    linkedin_modal_html = """
  <!-- Modal: Ficha Ejecutiva para LinkedIn -->
  <div class="modal-overlay" id="linkedinModal">
    <div class="modal-box" style="max-width: 720px;">
      <div class="modal-header">
        <div class="modal-title">💼 FICHA EJECUTIVA & PITCH PARA LINKEDIN</div>
        <button class="btn-close-modal" id="btnCloseLinkedIn" aria-label="Cerrar modal">&times;</button>
      </div>

      <div class="modal-body">
        <p><strong>VuelosPúblicos</strong> transforma miles de órdenes de compra de pasajes en una experiencia cartográfica y de rendición de cuentas. Utiliza esta ficha para citar datos consolidados o compartir el observatorio en redes profesionales:</p>

        <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 12px 16px; margin: 12px 0;">
          <div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">📊 Radiografía Consolidada (2007–Octubre 2026)</div>
          <ul style="padding-left: 18px; display: flex; flex-direction: column; gap: 4px; font-size: 0.8rem; color: var(--text-secondary);">
            <li><strong>Gasto Auditado Total:</strong> $3.188.672.723 CLP en 465 compras públicas geocodificadas.</li>
            <li><strong>Línea de Tiempo:</strong> 240 meses cronológicos continuos (Enero 2007 a Octubre 2026).</li>
            <li><strong>Top Destinos Internacionales:</strong> París (39 vuelos), Madrid (38), Washington D.C. (30), Ginebra (10), Osaka (Gab. Ministerial).</li>
            <li><strong>Destino Insular Líder:</strong> Rapa Nui / Isla de Pascua (67 delegaciones y comitivas).</li>
            <li><strong>Concentración de Agencias:</strong> Cocha ($1.167M), LATAM ($1.111M), Turavion ($699M), Sky ($139M).</li>
            <li><strong>Trazabilidad Legal:</strong> 100% órdenes de compra de ChileCompra (Ley 19.886) y Transparencia Activa (Ley 20.285).</li>
          </ul>
        </div>

        <div style="font-size: 0.72rem; font-weight: 700; color: #f59e0b; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">📝 Borrador de Post para LinkedIn (Listo para usar)</div>
        <textarea id="linkedinPostText" readonly style="width: 100%; height: 185px; background: #060b11; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); color: var(--text-primary); font-family: var(--font-sans); font-size: 0.78rem; padding: 10px; resize: vertical; line-height: 1.45;">🇨🇱 ¿Cuánto gasta el Estado de Chile en pasajes aéreos y comitivas oficiales?

Para responder a esta pregunta con evidencia y sin sesgos partidistas, construí VuelosPúblicos: un observatorio cívico interactivo que procesa y visualiza más de 20 años de órdenes de compra oficiales de ChileCompra (2007–2026).

📊 Hallazgos clave del Data Lakehouse:
• $3.188 millones de pesos (CLP) auditados en 465 compras públicas geocodificadas.
• 240 meses cronológicos continuos a través de 5 administraciones de gobierno.
• Top destinos: Rapa Nui (67 vuelos), París (39), Madrid (38) y Washington D.C. (30).
• 4 proveedores concentran la mayor parte de las compras vía Convenio Marco: Cocha, LATAM, Turavion y Sky.

🛠️ Innovación y tecnología cívica:
1. Cartografía 2.5D interactiva a 60 FPS con curvas geodésicas balísticas desde Santiago (SCL).
2. Odómetro fiscal mensual y scrubber temporal con sparkline de densidad de gasto.
3. Expediente fiscal por vuelo con ID oficial de Orden de Compra (OC), distancia geodésica y tiempo estimado de vuelo.
4. Tribunal Ciudadano reactivo: la ciudadanía puede evaluar si cada viaje se justifica por razones de servicio o constituye un derroche fiscal.

Los datos abiertos solo tienen valor cuando se convierten en información accesible, comprensible y auditable para cualquier persona.

👉 Explora la plataforma interactiva y audita las órdenes de compra:
https://vuelospublicos.evegat.cl/

#GovTech #ChileCompra #Transparencia #DatosAbiertos #Chile #ComprasPublicas #DataCivica #OpenData</textarea>

        <div style="display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
          <button class="btn-help-modal" id="btnCopyLinkedInPost" style="flex: 1; background: #0a66c2; color: #fff; border-color: #0a66c2; justify-content: center;">
            <span>📋 Copiar Post al Portapapeles</span>
          </button>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fvuelospublicos.evegat.cl%2F" target="_blank" rel="noopener noreferrer" class="btn-help-modal" style="background: var(--bg-card); color: var(--text-primary); border-color: var(--border-subtle); justify-content: center; text-decoration: none;">
            <span>🚀 Abrir LinkedIn para Publicar</span>
          </a>
        </div>
        <div class="share-toast" id="linkedinToast" style="margin-top: 8px;">¡Post copiado con éxito! Listo para pegar en tu perfil de LinkedIn ✓</div>
      </div>

      <div class="modal-footer">
        <button class="btn-help-modal" id="btnModalLinkedInClose">CERRAR</button>
      </div>
    </div>
  </div>
"""

    old_modal_target = """    </div>
  </div>

  <script>"""

    if old_modal_target in content:
        content = content.replace(old_modal_target, f"    </div>\n  </div>{linkedin_modal_html}\n  <script>")
        print("[+] Modal LinkedIn agregado.")

    # 7. JavaScript event listeners & handlers
    old_share_js = """    /* =====================================================================
       COMPARTIR EXPEDIENTE Y DEEP LINKING POR HASH
       ===================================================================== */
    if (btnShareExpediente) {{
      btnShareExpediente.addEventListener('click', () => {{
        if (!selectedFlight) return;
        const url = `${{window.location.origin}}${{window.location.pathname}}#${{selectedFlight.id}}`;
        const texto = `🇨🇱 [VuelosPúblicos] El Estado gastó $${{selectedFlight.cost.toLocaleString('es-CL')}} CLP en viaje a ${{selectedFlight.dest.city}} (${{selectedFlight.cabin}}) para ${{selectedFlight.entity}}. OC: ${{selectedFlight.oc}}. ¿Se justifica o es derroche? Vota aquí: ${{url}}`;

        if (navigator.clipboard) {{
          navigator.clipboard.writeText(texto).then(() => {{
            if (shareToast) {{
              shareToast.style.display = 'block';
              setTimeout(() => {{ shareToast.style.display = 'none'; }}, 2500);
            }}
          }});
        }}
        if (navigator.share) {{
          navigator.share({{
            title: `VuelosPúblicos — ${{selectedFlight.dest.city}}`,
            text: texto,
            url: url
          }}).catch(() => {{}});
        }}
      }});
    }}"""

    new_share_js = """    /* =====================================================================
       COMPARTIR EXPEDIENTE, SUITE SOCIAL Y MODAL LINKEDIN
       ===================================================================== */
    const linkedinModal = document.getElementById('linkedinModal');
    const btnOpenLinkedInModal = document.getElementById('btnOpenLinkedInModal');
    const btnCloseLinkedIn = document.getElementById('btnCloseLinkedIn');
    const btnModalLinkedInClose = document.getElementById('btnModalLinkedInClose');
    const btnCopyLinkedInPost = document.getElementById('btnCopyLinkedInPost');
    const linkedinPostText = document.getElementById('linkedinPostText');
    const linkedinToast = document.getElementById('linkedinToast');

    if (btnOpenLinkedInModal && linkedinModal) {{
      btnOpenLinkedInModal.addEventListener('click', () => linkedinModal.classList.add('open'));
    }}
    if (btnCloseLinkedIn && linkedinModal) {{
      btnCloseLinkedIn.addEventListener('click', () => linkedinModal.classList.remove('open'));
    }}
    if (btnModalLinkedInClose && linkedinModal) {{
      btnModalLinkedInClose.addEventListener('click', () => linkedinModal.classList.remove('open'));
    }}
    if (linkedinModal) {{
      linkedinModal.addEventListener('click', (e) => {{
        if (e.target === linkedinModal) linkedinModal.classList.remove('open');
      }});
    }}
    if (btnCopyLinkedInPost && linkedinPostText) {{
      btnCopyLinkedInPost.addEventListener('click', () => {{
        if (navigator.clipboard) {{
          navigator.clipboard.writeText(linkedinPostText.value).then(() => {{
            if (linkedinToast) {{
              linkedinToast.style.display = 'block';
              setTimeout(() => {{ linkedinToast.style.display = 'none'; }}, 3000);
            }}
          }});
        }}
      }});
    }}

    const btnShareLinkedIn = document.getElementById('btnShareLinkedIn');
    if (btnShareLinkedIn) {{
      btnShareLinkedIn.addEventListener('click', () => {{
        if (!selectedFlight) return;
        const url = `${{window.location.origin}}${{window.location.pathname}}#${{selectedFlight.id}}`;
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${{encodeURIComponent(url)}}`, '_blank', 'width=620,height=620');
      }});
    }}

    const btnShareWhatsApp = document.getElementById('btnShareWhatsApp');
    if (btnShareWhatsApp) {{
      btnShareWhatsApp.addEventListener('click', () => {{
        if (!selectedFlight) return;
        const url = `${{window.location.origin}}${{window.location.pathname}}#${{selectedFlight.id}}`;
        const texto = `🇨🇱 *VuelosPúblicos* | El Estado gastó $${{selectedFlight.cost.toLocaleString('es-CL')}} CLP en viaje a ${{selectedFlight.dest.city}} (${{selectedFlight.cabinDesc}}) para ${{selectedFlight.entity}}. OC: ${{selectedFlight.oc}}. ¿Se justifica o es derroche? Vota aquí: ${{url}}`;
        window.open(`https://api.whatsapp.com/send?text=${{encodeURIComponent(texto)}}`, '_blank');
      }});
    }}

    const btnShareX = document.getElementById('btnShareX');
    if (btnShareX) {{
      btnShareX.addEventListener('click', () => {{
        if (!selectedFlight) return;
        const url = `${{window.location.origin}}${{window.location.pathname}}#${{selectedFlight.id}}`;
        const texto = `🇨🇱 VuelosPúblicos: El Estado pagó $${{selectedFlight.cost.toLocaleString('es-CL')}} CLP en viaje a ${{selectedFlight.dest.city}} (${{selectedFlight.cabin}}) para ${{selectedFlight.entity}} (OC: ${{selectedFlight.oc}}). ¿Se justifica o es derroche fiscal? Audita y vota:`;
        window.open(`https://twitter.com/intent/tweet?text=${{encodeURIComponent(texto)}}&url=${{encodeURIComponent(url)}}`, '_blank');
      }});
    }}

    if (btnShareExpediente) {{
      btnShareExpediente.addEventListener('click', () => {{
        if (!selectedFlight) return;
        const url = `${{window.location.origin}}${{window.location.pathname}}#${{selectedFlight.id}}`;
        const texto = `🇨🇱 [VuelosPúblicos — Observatorio Cívico]
✈️ Expediente: ${{selectedFlight.id}} • ${{selectedFlight.dest.city}} (${{selectedFlight.dest.code}}), ${{selectedFlight.dest.country}}
🏛️ Organismo: ${{selectedFlight.entity}}
👤 Pasajero / Comitiva: ${{selectedFlight.role}}
💰 Costo Fiscal: $${{selectedFlight.cost.toLocaleString('es-CL')}} CLP (${{selectedFlight.cabinDesc}})
📄 Orden de Compra: ${{selectedFlight.oc}} (Mercado Público / Ley 19.886)
🔍 Motivo: ${{selectedFlight.reason}}
🗳️ ¿Se justifica o es derroche fiscal? Vota y audita aquí:
${{url}}`;

        if (navigator.clipboard) {{
          navigator.clipboard.writeText(texto).then(() => {{
            if (shareToast) {{
              shareToast.innerText = "¡Ficha copiada al portapapeles! Lista para pegar en LinkedIn ✓";
              shareToast.style.display = 'block';
              setTimeout(() => {{ shareToast.style.display = 'none'; }}, 3000);
            }}
          }});
        }}
      }});
    }}"""

    if old_share_js in content:
        content = content.replace(old_share_js, new_share_js)
        print("[+] JavaScript social handlers actualizados.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] build_frontend.py actualizado exitosamente.")

if __name__ == '__main__':
    update_build_frontend()
