import os
import json

def generate_index_html():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(repo_dir, "data", "vuelos_2007_2026.json")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        flights = json.load(f)
        
    print(f"[*] Cargando {len(flights)} vuelos desde {data_file}...")
    flights_json_str = json.dumps(flights, ensure_ascii=False, indent=2)
    
    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VuelosPúblicos — Observatorio Cívico del Gasto en Pasajes Aéreos del Estado de Chile</title>
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
  <meta name="twitter:image" content="https://vuelospublicos.evegat.cl/og-image.png">
  <style>
    :root {{
      --bg-base: #060b11;
      --bg-surface: #0c1420;
      --bg-card: #121d2c;
      --bg-card-hover: #1a283c;
      --bg-card-active: rgba(47, 129, 247, 0.15);
      --bg-ocean: #07101a;
      --land-fill: #102132;
      --land-stroke: #1b3754;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: #2f81f7;
      --text-primary: #f0f6fc;
      --text-secondary: #8b9bb0;
      --text-muted: #576577;
      --c-turista: #00e5a3;
      --c-turista-dim: rgba(0, 229, 163, 0.2);
      --c-business: #ff4d5a;
      --c-business-dim: rgba(255, 77, 90, 0.2);
      --c-scl: #00d4ff;
      --c-accent: #2f81f7;
      --c-gold: #f59e0b;
      --c-purple: #a855f7;
      --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --font-mono: 'Space Mono', 'SF Mono', Consolas, Menlo, monospace;
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --radius-xl: 16px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.45;
    }}

    /* Contenedor Principal */
    .civic-container {{
      display: flex;
      flex-direction: column;
      width: 100%;
      max-width: 1720px;
      margin: 0 auto;
      padding: 14px 18px;
      gap: 12px;
      flex: 1;
    }}

    /* Encabezado Cívico */
    .civic-header {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 12px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-icon {{
      width: 42px;
      height: 42px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #00d4ff 0%, #005bb5 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 16px rgba(0, 212, 255, 0.4);
    }}

    .brand-title {{
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-badge {{
      font-size: 0.68rem;
      font-weight: 600;
      text-transform: uppercase;
      background: rgba(56, 139, 253, 0.15);
      color: var(--c-accent);
      border: 1px solid rgba(56, 139, 253, 0.3);
      padding: 2px 7px;
      border-radius: var(--radius-sm);
    }}

    .brand-sub {{
      font-size: 0.74rem;
      color: var(--text-secondary);
      font-weight: 400;
      letter-spacing: 0.4px;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}

    /* Barra de KPIs Cívicos */
    .kpi-strip {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .kpi-card {{
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 6px 12px;
      display: flex;
      flex-direction: column;
      min-width: 110px;
      transition: all 0.2s ease;
    }}

    .kpi-card:hover {{
      border-color: rgba(47, 129, 247, 0.4);
      background: rgba(47, 129, 247, 0.05);
    }}

    .kpi-label {{
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .kpi-value {{
      font-family: var(--font-mono);
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-primary);
      white-space: nowrap;
    }}

    .kpi-value.accent-spend {{
      color: #38bdf8;
    }}

    .kpi-value.accent-business {{
      color: var(--c-business);
    }}

    .btn-help-modal {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 8px 12px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }}

    .btn-help-modal:hover {{
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
    }}

    /* Navegación por pestañas móvil (Oculta en Desktop) */
    .mobile-view-tabs {{
      display: none;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 4px;
      gap: 4px;
      margin-bottom: 2px;
    }}

    .mobile-tab-btn {{
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 8px 6px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
    }}

    .mobile-tab-btn.active {{
      background: var(--bg-card);
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }}

    /* Layout Principal de 3 Columnas */
    .main-workspace {{
      display: grid;
      grid-template-columns: 330px 1fr 350px;
      gap: 12px;
      flex: 1;
      min-height: 0;
    }}

    /* Columna 1: Panel Lateral de Viajes */
    .flight-list-sidebar {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}

    .sidebar-header {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .sidebar-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .sidebar-title {{
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .sidebar-count-badge {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 2px 8px;
      border-radius: 12px;
      color: var(--text-secondary);
    }}

    /* Buscador en el Sidebar */
    .sidebar-search-box {{
      position: relative;
      display: flex;
      align-items: center;
      width: 100%;
    }}

    .sidebar-search-input {{
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.78rem;
      padding: 7px 28px 7px 10px;
      border-radius: var(--radius-sm);
      outline: none;
      transition: all 0.2s ease;
    }}

    .sidebar-search-input:focus {{
      border-color: var(--border-focus);
      background: var(--bg-card-hover);
      box-shadow: 0 0 0 2px rgba(47, 129, 247, 0.2);
    }}

    .sidebar-search-input::placeholder {{
      color: var(--text-muted);
    }}

    .btn-clear-search {{
      position: absolute;
      right: 8px;
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .btn-clear-search:hover {{
      color: #ffffff;
    }}

    /* Toolbar de Ordenamiento */
    .sort-toolbar {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .sort-label {{
      font-size: 0.68rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      margin-right: 2px;
    }}

    .sort-btn {{
      flex: 1;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 0.7rem;
      font-weight: 600;
      padding: 5px 6px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
      text-align: center;
    }}

    .sort-btn:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .sort-btn.active {{
      background: rgba(47, 129, 247, 0.2);
      color: #58a6ff;
      border-color: #2f81f7;
    }}

    /* Lista Scrolleable de Viajes */
    .flight-scroll-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: calc(100vh - 250px);
    }}

    .flight-scroll-list::-webkit-scrollbar {{
      width: 5px;
    }}

    .flight-scroll-list::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 3px;
    }}

    .flight-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 8px 10px;
      cursor: pointer;
      transition: all 0.18s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .flight-card:hover {{
      background: var(--bg-card-hover);
      border-color: rgba(47, 129, 247, 0.4);
      transform: translateX(2px);
    }}

    .flight-card.active {{
      background: var(--bg-card-active);
      border-color: var(--border-focus);
      box-shadow: 0 0 12px rgba(47, 129, 247, 0.25);
    }}

    .flight-card.dimmed {{
      opacity: 0.45;
    }}

    .flight-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .flight-card-route {{
      font-size: 0.82rem;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .flight-card-badge {{
      font-size: 0.62rem;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}

    .badge-turista {{
      background: var(--c-turista-dim);
      color: var(--c-turista);
      border: 1px solid rgba(0, 229, 163, 0.4);
    }}

    .badge-business {{
      background: var(--c-business-dim);
      color: var(--c-business);
      border: 1px solid rgba(255, 77, 90, 0.4);
    }}

    .flight-card-body {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .flight-card-entity {{
      font-size: 0.74rem;
      color: var(--text-secondary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .flight-card-passenger {{
      font-size: 0.7rem;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .flight-card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.7rem;
      color: var(--text-muted);
      border-top: 1px dashed rgba(255, 255, 255, 0.08);
      padding-top: 4px;
      margin-top: 2px;
    }}

    .flight-card-cost {{
      font-family: var(--font-mono);
      font-weight: 700;
      color: #f0f6fc;
    }}

    /* Columna 2: Área Central de Mapa y Línea de Tiempo */
    .map-area {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-height: 0;
    }}

    .map-container {{
      background: var(--bg-ocean);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      flex: 1;
      position: relative;
      overflow: hidden;
      min-height: 480px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }}

    #radarCanvas {{
      width: 100%;
      height: 100%;
      display: block;
      cursor: grab;
      touch-action: none;
    }}

    #radarCanvas:active {{
      cursor: grabbing;
    }}

    .map-hud-top {{
      position: absolute;
      top: 12px;
      left: 14px;
      background: rgba(6, 12, 19, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 6px 10px;
      font-size: 0.7rem;
      color: var(--text-secondary);
      pointer-events: none;
      display: flex;
      flex-direction: column;
      gap: 2px;
      z-index: 10;
    }}

    .map-legend {{
      position: absolute;
      bottom: 12px;
      left: 14px;
      background: rgba(6, 12, 19, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 6px 12px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.7rem;
      color: var(--text-secondary);
      pointer-events: none;
      z-index: 10;
    }}

    .legend-item {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .legend-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}

    .map-controls {{
      position: absolute;
      top: 12px;
      right: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 10;
    }}

    .map-control-btn {{
      width: 32px;
      height: 32px;
      background: rgba(14, 23, 36, 0.9);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      color: var(--text-primary);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}

    .map-control-btn:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
      color: #58a6ff;
      transform: scale(1.05);
    }}

    .map-tooltip {{
      position: absolute;
      background: rgba(12, 20, 32, 0.96);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-focus);
      border-radius: var(--radius-md);
      padding: 8px 12px;
      font-size: 0.74rem;
      color: var(--text-primary);
      pointer-events: none;
      z-index: 20;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
      transform: translate(-50%, -120%);
      white-space: nowrap;
    }}

    .map-tooltip strong {{
      color: #ffffff;
      font-size: 0.8rem;
      display: block;
      margin-bottom: 2px;
    }}

    .map-tooltip .tooltip-meta {{
      color: var(--text-secondary);
      font-size: 0.7rem;
    }}

    /* Contenedor de Línea de Tiempo y Odómetro */
    .time-scrubber-housing {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}

    .scrubber-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .transport-controls {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .transport-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .transport-btn:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .transport-btn.btn-play.playing {{
      background: rgba(47, 129, 247, 0.2);
      color: #58a6ff;
      border-color: #2f81f7;
    }}

    .timeline-date-display {{
      font-family: var(--font-mono);
      font-size: 0.95rem;
      font-weight: 700;
      color: #58a6ff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(0, 0, 0, 0.3);
      padding: 4px 12px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
    }}

    .odometer-box {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(0, 0, 0, 0.35);
      padding: 4px 12px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
    }}

    .odometer-label {{
      font-size: 0.68rem;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .odometer-value {{
      font-family: var(--font-mono);
      font-size: 0.98rem;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: 0.5px;
    }}

    /* Sparkline & Slider */
    .slider-track-container {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .scrubber-sparkline-canvas {{
      width: 100%;
      height: 18px;
      display: block;
      opacity: 0.85;
      border-radius: 2px;
    }}

    .timeline-slider {{
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 3px;
      background: rgba(255, 255, 255, 0.1);
      outline: none;
      cursor: pointer;
    }}

    .timeline-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #58a6ff;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(56, 139, 253, 0.8);
      border: 2px solid #ffffff;
      transition: transform 0.1s ease;
    }}

    .timeline-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.2);
    }}

    .slider-year-markers {{
      display: flex;
      justify-content: space-between;
      font-size: 0.65rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
      padding: 0 2px;
    }}

    /* Barra de Filtros Cívicos Integral */
    .filter-deck {{
      border-top: 1px solid var(--border-subtle);
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .filter-select-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 6px;
    }}

    .filter-select-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .filter-mini-label {{
      font-size: 0.64rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.03em;
    }}

    .filter-select {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 6px;
      border-radius: var(--radius-sm);
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s ease, background 0.15s ease;
    }}

    .filter-select:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      background: var(--bg-card-hover);
    }}

    .filter-select:focus {{
      border-color: var(--border-focus);
    }}

    .filter-select.has-filter {{
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
      color: #38bdf8;
    }}

    .filter-actions-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .filter-action-buttons {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .btn-reset-filters {{
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.35);
      color: #f87171;
      font-size: 0.70rem;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      display: none;
      align-items: center;
      gap: 4px;
    }}

    .btn-reset-filters:hover {{
      background: rgba(239, 68, 68, 0.2);
      border-color: #ef4444;
      color: #ffffff;
    }}

    .btn-reset-filters.visible {{
      display: inline-flex;
    }}

    /* Barra de Chips Activos */
    .active-filters-bar {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      padding-top: 4px;
      font-size: 0.70rem;
    }}

    .active-filters-label {{
      font-size: 0.64rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    .active-chips-container {{
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
    }}

    .active-filter-chip {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #e2e8f0;
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 10px;
    }}

    .active-filter-chip .chip-remove {{
      cursor: pointer;
      opacity: 0.75;
      font-weight: bold;
      margin-left: 2px;
    }}

    .active-filter-chip .chip-remove:hover {{
      opacity: 1;
      color: #f87171;
    }}

    .active-filters-summary {{
      color: #38bdf8;
      font-weight: 700;
      font-size: 0.68rem;
      margin-left: auto;
    }}

    /* Quick filters en Sidebar */
    .btn-sidebar-reset {{
      background: transparent;
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .btn-sidebar-reset:hover {{
      background: rgba(239, 68, 68, 0.2);
    }}

    .quick-filter-scroll {{
      display: flex;
      gap: 4px;
      overflow-x: auto;
      padding: 3px 0 6px;
      scrollbar-width: none;
    }}

    .quick-filter-scroll::-webkit-scrollbar {{
      display: none;
    }}

    .quick-chip {{
      white-space: nowrap;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }}

    .quick-chip:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .quick-chip.active {{
      background: rgba(56, 189, 248, 0.2);
      color: #38bdf8;
      border-color: #38bdf8;
    }}

    .filter-provider-group, .filter-secondary-group {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .filter-label {{
      font-size: 0.68rem;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-muted);
    }}

    .provider-chip {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .provider-chip:hover {{
      background: var(--bg-card-hover);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .provider-chip.active {{
      background: rgba(47, 129, 247, 0.2);
      color: #58a6ff;
      border-color: #2f81f7;
    }}

    .provider-select-hidden {{
      display: none;
    }}

    .filter-entity-select {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      outline: none;
      cursor: pointer;
    }}

    .filter-entity-select:focus {{
      border-color: var(--border-focus);
    }}

    .btn-toggle-business {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .btn-toggle-business .business-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--c-business);
      opacity: 0.5;
    }}

    .btn-toggle-business.active {{
      background: var(--c-business-dim);
      color: #ffffff;
      border-color: var(--c-business);
    }}

    .btn-toggle-business.active .business-dot {{
      opacity: 1;
      box-shadow: 0 0 6px var(--c-business);
    }}

    /* Columna 3: Expediente Fiscal y Tribunal */
    .dossier-housing {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}

    .dossier-header {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(0, 0, 0, 0.15);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .dossier-tag {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: #58a6ff;
    }}

    .dossier-content {{
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
      overflow-y: auto;
    }}

    .route-display {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px 12px;
    }}

    .route-node {{
      display: flex;
      flex-direction: column;
    }}

    .node-code {{
      font-family: var(--font-mono);
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
    }}

    .node-city {{
      font-size: 0.74rem;
      color: var(--text-secondary);
      font-weight: 600;
    }}

    .node-airport {{
      font-size: 0.65rem;
      color: var(--text-muted);
    }}

    .route-arrow {{
      font-size: 1rem;
      color: #58a6ff;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }}

    .route-dist-label {{
      font-size: 0.62rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }}

    .data-row {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .data-label {{
      font-size: 0.66rem;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 600;
      letter-spacing: 0.3px;
    }}

    .data-value {{
      font-size: 0.82rem;
      color: var(--text-primary);
      font-weight: 600;
    }}

    .data-value.price {{
      font-family: var(--font-mono);
      font-size: 1.15rem;
      font-weight: 800;
      color: #38bdf8;
    }}

    .data-meta-box {{
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .meta-line {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.72rem;
    }}

    .meta-key {{
      color: var(--text-muted);
    }}

    .meta-val {{
      font-family: var(--font-mono);
      color: var(--text-secondary);
      font-weight: 600;
    }}

    .oc-copy-btn {{
      background: transparent;
      border: none;
      color: #58a6ff;
      cursor: pointer;
      font-size: 11px;
      margin-left: 4px;
      transition: color 0.15s ease;
    }}

    .oc-copy-btn:hover {{
      color: #ffffff;
    }}

    .data-reason {{
      background: rgba(47, 129, 247, 0.05);
      border-left: 3px solid #2f81f7;
      padding: 8px 10px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 0.74rem;
      color: var(--text-secondary);
      line-height: 1.4;
      font-style: italic;
    }}

    .source-tag-link {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.7rem;
      color: var(--text-muted);
      border-top: 1px dashed var(--border-subtle);
      padding-top: 6px;
    }}

    .source-tag-link a {{
      color: #58a6ff;
      text-decoration: none;
    }}

    .source-tag-link a:hover {{
      text-decoration: underline;
    }}

    /* Tribunal Ciudadano */
    .tribunal-box {{
      border-top: 1px solid var(--border-subtle);
      padding: 12px 14px;
      background: rgba(0, 0, 0, 0.2);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .tribunal-title {{
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      text-align: center;
      color: #f0f6fc;
    }}

    .action-buttons {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .civic-btn {{
      padding: 8px;
      border-radius: var(--radius-md);
      border: 1px solid transparent;
      cursor: pointer;
      font-weight: 700;
      font-size: 0.78rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      transition: all 0.18s ease;
    }}

    .civic-btn small {{
      font-size: 0.65rem;
      font-weight: 400;
      opacity: 0.8;
    }}

    .btn-approve {{
      background: rgba(0, 229, 163, 0.1);
      border-color: rgba(0, 229, 163, 0.3);
      color: var(--c-turista);
    }}

    .btn-approve:hover:not(:disabled) {{
      background: rgba(0, 229, 163, 0.2);
      border-color: var(--c-turista);
      transform: translateY(-1px);
    }}

    .btn-approve.active-voted {{
      background: var(--c-turista);
      color: #000000;
      font-weight: 800;
    }}

    .btn-reject {{
      background: rgba(255, 77, 90, 0.1);
      border-color: rgba(255, 77, 90, 0.3);
      color: var(--c-business);
    }}

    .btn-reject:hover:not(:disabled) {{
      background: rgba(255, 77, 90, 0.2);
      border-color: var(--c-business);
      transform: translateY(-1px);
    }}

    .btn-reject.active-voted {{
      background: var(--c-business);
      color: #ffffff;
      font-weight: 800;
    }}

    .civic-btn:disabled {{
      cursor: not-allowed;
      opacity: 0.8;
    }}

    .voting-bar-container {{
      height: 8px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      overflow: hidden;
      display: flex;
    }}

    .bar-approve {{
      background: var(--c-turista);
      height: 100%;
      width: 50%;
      transition: width 0.3s ease;
    }}

    .bar-reject {{
      background: var(--c-business);
      height: 100%;
      width: 50%;
      transition: width 0.3s ease;
    }}

    .voting-stats-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.7rem;
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    .txt-approve {{
      color: var(--c-turista);
    }}

    .txt-reject {{
      color: var(--c-business);
    }}

    .vote-status-msg {{
      font-size: 0.68rem;
      text-align: center;
      color: var(--text-muted);
    }}

    .vote-status-msg.voted {{
      color: #58a6ff;
      font-weight: 600;
    }}

    /* Compartir Expediente y Redes */
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
    }}

    /* Pie de Página */
    .civic-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 10px;
      font-size: 0.7rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border-subtle);
      margin-top: auto;
    }}

    .civic-footer a {{
      color: var(--text-secondary);
      text-decoration: none;
    }}

    .civic-footer a:hover {{
      color: #ffffff;
      text-decoration: underline;
    }}

    /* Modal */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}

    .modal-overlay.open {{
      display: flex;
    }}

    .modal-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border-focus);
      border-radius: var(--radius-lg);
      max-width: 650px;
      width: 100%;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .modal-header {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-title {{
      font-size: 0.95rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #ffffff;
    }}

    .btn-close-modal {{
      background: none;
      border: none;
      color: var(--text-secondary);
      font-size: 22px;
      cursor: pointer;
    }}

    .btn-close-modal:hover {{
      color: #ffffff;
    }}

    .modal-body {{
      padding: 16px 18px;
      font-size: 0.8rem;
      color: var(--text-secondary);
      display: flex;
      flex-direction: column;
      gap: 10px;
      line-height: 1.5;
      max-height: 70vh;
      overflow-y: auto;
    }}

    .modal-section-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .modal-footer {{
      padding: 12px 18px;
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: flex-end;
    }}

    /* Media Queries */
    @media (max-width: 1120px) {{
      .main-workspace {{
        grid-template-columns: 290px 1fr;
      }}
      .dossier-housing {{
        grid-column: span 2;
      }}
    }}

    @media (max-width: 860px) {{
      .civic-container {{
        padding: 8px;
        gap: 8px;
      }}
      .kpi-strip {{
        width: 100%;
        overflow-x: auto;
        padding-bottom: 4px;
      }}
      .mobile-view-tabs {{
        display: flex;
      }}
      .main-workspace {{
        display: flex;
        flex-direction: column;
      }}
      .flight-list-sidebar.mobile-hidden,
      .map-area.mobile-hidden,
      .dossier-housing.mobile-hidden {{
        display: none !important;
      }}
      .map-container {{
        min-height: 400px;
      }}
      .flight-scroll-list {{
        max-height: 450px;
      }}
      .civic-footer {{
        flex-direction: column;
        gap: 4px;
        text-align: center;
      }}
    }}
  </style>
</head>
<body>

  <div class="civic-container">

    <!-- Encabezado Institucional -->
    <header class="civic-header">
      <div class="brand-group">
        <div class="brand-icon">✈️</div>
        <div>
          <div class="brand-title">
            VuelosPúblicos
            <span class="brand-badge">Ley 19.886 & 20.285</span>
          </div>
          <div class="brand-sub">OBSERVATORIO CÍVICO DEL GASTO EN PASAJES AÉREOS • REPÚBLICA DE CHILE</div>
        </div>
      </div>

      <div class="header-actions">
        <!-- Barra de KPIs Dinámicos -->
        <div class="kpi-strip">
          <div class="kpi-card">
            <span class="kpi-label">Viajes Oficiales</span>
            <span class="kpi-value" id="statFlightsCount">{len(flights)}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Gasto Consolidado</span>
            <span class="kpi-value accent-spend" id="statTotalSpend">$3.176M CLP</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Clase Business</span>
            <span class="kpi-value accent-business" id="statBusinessCount">33 (7%)</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Top Organismo</span>
            <span class="kpi-value" id="statTopEntity" title="Organismo líder en gasto">Presidencia</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Top Destino</span>
            <span class="kpi-value" id="statTopDest" title="Destino más concurrido">Rapa Nui</span>
          </div>
        </div>

        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn-help-modal btn-linkedin-pill" id="btnOpenLinkedInModal" aria-label="Abrir Ficha Ejecutiva para LinkedIn">
            <span>💼 Ficha LinkedIn</span>
          </button>
          <button class="btn-help-modal" id="btnOpenHelp" aria-label="Abrir fuentes y metodología">
            <span>📖 Metodología</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Pestañas de Vista Móvil -->
    <nav class="mobile-view-tabs" id="mobileViewTabs">
      <button class="mobile-tab-btn active" data-view="map">🗺️ Mapa</button>
      <button class="mobile-tab-btn" data-view="list">📋 Viajes (<span id="mobileCountBadge">{len(flights)}</span>)</button>
      <button class="mobile-tab-btn" data-view="dossier">📄 Expediente</button>
    </nav>

    <!-- Área de Trabajo Principal (3 Columnas) -->
    <main class="main-workspace">

      <!-- Columna 1: Panel Lateral de Viajes Oficiales -->
      <aside class="flight-list-sidebar" id="sidebarColumn">
        <div class="sidebar-header">
          <div class="sidebar-title-row">
            <div class="sidebar-title">
              <span>✈️ Viajes Oficiales</span>
              <span class="sidebar-count-badge" id="listBadgeCount">{len(flights)}</span>
            </div>
          </div>

          <!-- Buscador en Vivo -->
          <div class="sidebar-search-box">
            <input type="search" id="flightSearchInput" class="sidebar-search-input" placeholder="🔍 Buscar pasajero, ministerio u OC..." aria-label="Buscar viaje oficial">
            <button id="btnClearSearch" class="btn-clear-search" title="Limpiar búsqueda" style="display: none;">&times;</button>
          </div>

          <!-- Barra de Ordenamiento -->
          <div class="sort-toolbar">
            <span class="sort-label">Orden:</span>
            <button class="sort-btn active" id="btnSortDate" data-sort="date">📅 Fecha ▾</button>
            <button class="sort-btn" id="btnSortCost" data-sort="cost">💰 Monto</button>
            <button class="sort-btn" id="btnSortEntity" data-sort="entity">🏛️ Organismo</button>
          </div>

          <!-- Filtros Rápidos en Sidebar -->
          <div class="quick-filter-scroll" id="sidebarQuickFilters">
            <button class="quick-chip active" data-filter-type="scope" data-value="Todas">Todos (465)</button>
            <button class="quick-chip" data-filter-type="scope" data-value="Nacional">🇨🇱 Chile (202)</button>
            <button class="quick-chip" data-filter-type="scope" data-value="Internacional">🌍 Exterior (263)</button>
            <button class="quick-chip" data-filter-type="cabin" data-value="Business">⭐ Business (5)</button>
            <button class="quick-chip" data-filter-type="costTier" data-value="Mega">🔥 >$20M (30)</button>
            <button class="quick-chip" data-filter-type="government" data-value="Boric">🇨🇱 Boric (149)</button>
            <button class="quick-chip" data-filter-type="government" data-value="Piñera II">🇨🇱 Piñera II (95)</button>
          </div>
        </div>

        <!-- Lista scrolleable interactiva -->
        <div class="flight-scroll-list" id="flightListContainer">
          <!-- Inyectado dinámicamente -->
        </div>
      </aside>

      <!-- Columna 2: Mapa Geoespacial y Línea de Tiempo -->
      <section class="map-area" id="mapColumn">
        <!-- Canvas de Cartografía y Rutas 60 FPS -->
        <div class="map-container" id="mapContainer">
          <div class="map-hud-top">
            <div>BASE SANTIAGO: <strong>SCL (Pudahuel, Chile)</strong></div>
            <div>MOTOR: <span>GEODÉSICAS 2.5D • 60 FPS</span></div>
            <div>NAVEGACIÓN: <span>ARRASTRE DIRECTO • RUEDA ZOOM</span></div>
          </div>

          <div class="map-legend">
            <div class="legend-item">
              <div class="legend-dot" style="background: var(--c-scl);"></div>
              <span>Base SCL</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot" style="background: var(--c-turista);"></div>
              <span>Clase Turista</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot" style="background: var(--c-business);"></div>
              <span>Clase Business</span>
            </div>
          </div>

          <!-- Controles flotantes de mapa -->
          <div class="map-controls">
            <button class="map-control-btn" id="btnZoomIn" title="Acercar mapa" aria-label="Acercar">[ + ]</button>
            <button class="map-control-btn" id="btnZoomOut" title="Alejar mapa" aria-label="Alejar">[ − ]</button>
            <button class="map-control-btn" id="btnResetView" title="Restablecer vista" aria-label="Restablecer">[ ↺ ]</button>
          </div>

          <canvas id="radarCanvas"></canvas>

          <!-- Tooltip flotante interactivo -->
          <div class="map-tooltip" id="mapTooltip" style="display: none;"></div>
        </div>

        <!-- Línea de Tiempo Cronológica y Odómetro Fiscal -->
        <div class="time-scrubber-housing" id="timeScrubber">
          <div class="scrubber-top-row">
            <div class="transport-controls">
              <button class="transport-btn" id="btnPrevMonth" title="Mes anterior">⏪ Anterior</button>
              <button class="transport-btn btn-play" id="btnPlayPause" title="Reproducir línea de tiempo">⏯ Reproducir</button>
              <button class="transport-btn" id="btnNextMonth" title="Mes siguiente">⏩ Siguiente</button>
            </div>

            <div class="timeline-date-display" id="currentMonthLabel">Septiembre 2026</div>

            <div class="odometer-box">
              <span class="odometer-label">Odómetro Fiscal:</span>
              <span class="odometer-value" id="fiscalOdometer">$3.176.541.160 CLP</span>
            </div>
          </div>

          <!-- Sparkline de Actividad y Slider -->
          <div class="slider-track-container">
            <canvas id="scrubberSparkline" class="scrubber-sparkline-canvas" height="20"></canvas>
            <input type="range" class="timeline-slider" id="timelineSlider" min="0" max="239" value="236" step="1" aria-label="Línea de tiempo mensual 2007 a 2026">
            <div class="slider-year-markers">
              <span>2007</span>
              <span>2011</span>
              <span>2015</span>
              <span>2019</span>
              <span>2023</span>
              <span>2026</span>
            </div>
          </div>

          <!-- Barra de Filtros Cívicos Integral -->
          <div class="filter-deck" id="filterDeck">
            <!-- Fila 1: Selectores Semánticos Principales -->
            <div class="filter-select-grid">
              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterScopeSelect">🌐 Ámbito:</label>
                <select id="filterScopeSelect" class="filter-select" aria-label="Filtrar por ámbito geográfico">
                  <option value="Todas">Todos los Destinos (465)</option>
                  <option value="Nacional">🇨🇱 Solo Nacionales (202)</option>
                  <option value="Internacional">🌍 Solo Internacionales (263)</option>
                </select>
              </div>

              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterGovernmentSelect">🇨🇱 Gobierno:</label>
                <select id="filterGovernmentSelect" class="filter-select" aria-label="Filtrar por administración presidencial">
                  <option value="Todas">Todos los Gobiernos (2007–2026)</option>
                  <option value="Boric">🇨🇱 Gabriel Boric (2022–2026)</option>
                  <option value="Piñera II">🇨🇱 Sebastián Piñera II (2018–2022)</option>
                  <option value="Bachelet II">🇨🇱 Michelle Bachelet II (2014–2018)</option>
                  <option value="Piñera I">🇨🇱 Sebastián Piñera I (2010–2014)</option>
                  <option value="Bachelet I">🇨🇱 Michelle Bachelet I (2007–2010)</option>
                </select>
              </div>

              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterYearSelect">📅 Año:</label>
                <select id="filterYearSelect" class="filter-select" aria-label="Filtrar por año específico">
                  <option value="Todas">Todos los Años (20)</option>
                  <option value="2026">2026 (58)</option>
                  <option value="2025">2025 (24)</option>
                  <option value="2024">2024 (24)</option>
                  <option value="2023">2023 (24)</option>
                  <option value="2022">2022 (24)</option>
                  <option value="2021">2021 (24)</option>
                  <option value="2020">2020 (22)</option>
                  <option value="2019">2019 (24)</option>
                  <option value="2018">2018 (24)</option>
                  <option value="2017">2017 (24)</option>
                  <option value="2016">2016 (24)</option>
                  <option value="2015">2015 (24)</option>
                  <option value="2014">2014 (24)</option>
                  <option value="2013">2013 (24)</option>
                  <option value="2012">2012 (19)</option>
                  <option value="2011">2011 (21)</option>
                  <option value="2010">2010 (22)</option>
                  <option value="2009">2009 (20)</option>
                  <option value="2008">2008 (12)</option>
                  <option value="2007">2007 (3)</option>
                </select>
              </div>

              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterEntitySelect">🏛️ Organismo:</label>
                <select id="filterEntitySelect" class="filter-select" aria-label="Filtrar por organismo">
                  <option value="Todas">Todos los Organismos</option>
                  <option value="Presidencia">Presidencia y Gobierno Central</option>
                  <option value="Defensa">Defensa y Fuerzas Armadas</option>
                  <option value="Cancillería">Cancillería y Minrel</option>
                  <option value="Sectoriales">Ministerios Sectoriales</option>
                  <option value="Universidades">Universidades Estatales</option>
                  <option value="Municipalidades">Municipalidades y Gob. Locales</option>
                  <option value="Otros">Otras Instituciones</option>
                </select>
              </div>

              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterCostTierSelect">💰 Tramo Monto:</label>
                <select id="filterCostTierSelect" class="filter-select" aria-label="Filtrar por monto de pasaje">
                  <option value="Todas">Cualquier Monto</option>
                  <option value="Mega">🔥 Mega-Comitivas (> $20M)</option>
                  <option value="Alta">⚡ Comitivas Altas ($5M - $20M)</option>
                  <option value="Media">🔹 Comitivas Medias ($1M - $5M)</option>
                  <option value="Menor">🟢 Pasajes Menores (< $1M)</option>
                </select>
              </div>

              <div class="filter-select-item">
                <label class="filter-mini-label" for="filterDestinationSelect">📍 Destino Top:</label>
                <select id="filterDestinationSelect" class="filter-select" aria-label="Filtrar por ciudad o país de destino">
                  <option value="Todas">Todas las Ciudades (29)</option>
                  <option value="Isla de Pascua">🗿 Isla de Pascua / Rapa Nui (67)</option>
                  <option value="Madrid">🇪🇸 Madrid, España (40)</option>
                  <option value="París">🇫🇷 París, Francia (39)</option>
                  <option value="Iquique">🇨🇱 Iquique (39)</option>
                  <option value="Washington D.C.">🇺🇸 Washington D.C. (30)</option>
                  <option value="Punta Arenas">🇨🇱 Punta Arenas (30)</option>
                  <option value="Arica">🇨🇱 Arica (26)</option>
                  <option value="Nueva York">🇺🇸 Nueva York (18)</option>
                  <option value="Roma">🇮🇹 Roma, Italia (17)</option>
                  <option value="Antofagasta">🇨🇱 Antofagasta (17)</option>
                  <option value="Ciudad de México">🇲🇽 Ciudad de México (16)</option>
                  <option value="Londres">🇬🇧 Londres, Reino Unido (15)</option>
                  <option value="Balmaceda">🇨🇱 Balmaceda (12)</option>
                  <option value="Buenos Aires">🇦🇷 Buenos Aires (11)</option>
                  <option value="Miami FL">🇺🇸 Miami (11)</option>
                  <option value="Bogotá">🇨🇴 Bogotá (10)</option>
                  <option value="Lima">🇵🇪 Lima (9)</option>
                  <option value="Berlín">🇩🇪 Berlín (8)</option>
                  <option value="Ginebra">🇨🇭 Ginebra (6)</option>
                  <option value="Tokio">🇯🇵 Tokio (5)</option>
                  <option value="Osaka">🇯🇵 Osaka (2)</option>
                </select>
              </div>


            </div>

            <!-- Fila 2: Chips de Agencia, Botón Business y Botón Restablecer -->
            <div class="filter-actions-row">
              <div class="filter-provider-group" id="filterProvider">
                <span class="filter-label">Agencia:</span>
                <button class="provider-chip active" data-provider="Todas" id="filterProviderTodas">Todas</button>
                <button class="provider-chip" data-provider="Cocha" id="filterProviderCocha">Cocha</button>
                <button class="provider-chip" data-provider="Turavion" id="filterProviderTuravion">Turavion</button>
                <button class="provider-chip" data-provider="LATAM" id="filterProviderLATAM">LATAM</button>
                <button class="provider-chip" data-provider="Sky" id="filterProviderSky">Sky</button>
              </div>

              <select id="filterProviderSelect" class="provider-select-hidden" aria-label="Filtrar por proveedor">
                <option value="Todas">Todas</option>
                <option value="Cocha">Cocha</option>
                <option value="Turavion">Turavion</option>
                <option value="LATAM">LATAM</option>
                <option value="Sky">Sky</option>
              </select>

              <div class="filter-action-buttons">
                <button class="btn-toggle-business" id="btnToggleBusiness" title="Aislar pasajes de clase ejecutiva">
                  <span class="business-dot"></span>
                  <span>Solo Clase Business</span>
                </button>
                <button class="btn-reset-filters" id="btnResetAllFilters" title="Restablecer todos los filtros a valores por defecto">
                  <span>↺ Limpiar Filtros</span>
                </button>
              </div>
            </div>

            <!-- Fila 3: Píldoras de Filtros Activos y Contador Dinámico -->
            <div class="active-filters-bar" id="activeFiltersBar" style="display: none;">
              <span class="active-filters-label">Filtros Activos:</span>
              <div class="active-chips-container" id="activeChipsContainer"></div>
              <span class="active-filters-summary" id="activeFiltersSummary"></span>
            </div>
          </div>
        </div>
      </section>

      <!-- Columna 3: Expediente Fiscal y Tribunal Ciudadano -->
      <aside class="dossier-housing" id="dossierColumn">
        <div class="dossier-header">
          <span class="dossier-tag">EXPEDIENTE FISCAL</span>
          <span class="flight-card-badge badge-business" id="badgeCabin">CLASE BUSINESS</span>
        </div>

        <div class="dossier-content">
          <div class="route-display">
            <div class="route-node">
              <span class="node-code" id="origCode">SCL</span>
              <span class="node-city" id="origCity">Santiago</span>
              <span class="node-airport" id="origAirport">Aerop. Arturo Merino Benítez</span>
            </div>
            <div class="route-arrow">
              <span>✈ ➔</span>
              <span class="route-dist-label" id="routeDistance">-- km</span>
            </div>
            <div class="route-node" style="align-items: flex-end;">
              <span class="node-code" id="destCode">GVA</span>
              <span class="node-city" id="destCity">Ginebra, Suiza</span>
              <span class="node-airport" id="destAirport">Aerop. Ginebra-Cointrin</span>
            </div>
          </div>

          <div class="data-row">
            <span class="data-label">Organismo Público Comprador</span>
            <span class="data-value" id="entityName">Ministerio de Relaciones Exteriores</span>
          </div>

          <div class="data-row">
            <span class="data-label">Pasajero / Cargo / Comitiva</span>
            <span class="data-value" id="passengerRole">Delegación Oficial Asuntos Multilaterales</span>
          </div>

          <div class="data-row">
            <span class="data-label">Costo Total del Pasaje (Fondos Públicos)</span>
            <span class="data-value price" id="ticketCost">$8.450.000 CLP</span>
          </div>

          <div class="data-meta-box">
            <div class="meta-line">
              <span class="meta-key">Cabina:</span>
              <span class="meta-val" id="metaCabinDesc">Business • Vía Turavion</span>
            </div>
            <div class="meta-line">
              <span class="meta-key">Aerolínea:</span>
              <span class="meta-val" id="metaAirline">Vuelo Comercial</span>
            </div>
            <div class="meta-line">
              <span class="meta-key">Proveedor:</span>
              <span class="meta-val" id="metaProvider">Turavion</span>
            </div>
            <div class="meta-line">
              <span class="meta-key">Orden de Compra:</span>
              <span class="meta-val">
                <span id="metaOc">721-140-CM24</span>
                <button class="oc-copy-btn" id="btnCopyOc" title="Copiar código OC">📋 Copiar</button>
              </span>
            </div>
          </div>

          <div class="data-row">
            <span class="data-label">Motivo Oficial Declarado en Decreto / OC</span>
            <div class="data-reason" id="officialReason">
              "Participación plenaria en sesión del Consejo de Derechos Humanos de la ONU y mesas técnicas de cooperación internacional."
            </div>
          </div>

          <div class="source-tag-link">
            <span>Mercado Público (Ley 19.886)</span>
            <a href="https://www.mercadopublico.cl" target="_blank" rel="noopener" id="mpLink">Ficha Oficial ↗</a>
          </div>
        </div>

        <!-- Tribunal ciudadano pausado temporalmente -->

        <!-- Compartir Expediente -->
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
        </div>
      </aside>

    </main>

    <!-- Pie de Página Cívico -->
    <footer class="civic-footer">
      <div>VuelosPúblicos • Datos abiertos oficiales de Mercado Público (Ley 19.886) y Transparencia Activa (Ley 20.285)</div>
      <div>Plataforma cívica independiente para la rendición de cuentas del gasto fiscal • <a href="https://evegat.cl">evegat.cl</a></div>
    </footer>

  </div>

  <!-- Modal: Metodología y Fuentes -->
  <div class="modal-overlay" id="helpModal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">ℹ️ FUENTES DE INFORMACIÓN Y METODOLOGÍA</div>
        <button class="btn-close-modal" id="btnCloseHelp" aria-label="Cerrar modal">&times;</button>
      </div>

      <div class="modal-body">
        <p><strong>VuelosPúblicos</strong> es una plataforma cívica independiente diseñada para transparentar y auditar el uso de fondos públicos en pasajes aéreos y comitivas de la administración del Estado de Chile.</p>

        <div class="modal-section-title">1. ¿DE DÓNDE PROVIENEN LOS DATOS?</div>
        <p>Todos los registros exhibidos provienen de fuentes oficiales abiertas del Estado de Chile:</p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 6px;">
          <li><strong>Mercado Público (ChileCompra — Ley 19.886):</strong> Todo pasaje aéreo pagado por el fisco se adquiere mediante órdenes de compra (OC) registradas en el portal ChileCompra a través del Convenio Marco de Agencias de Viaje o licitaciones públicas.</li>
          <li><strong>Transparencia Activa (Consejo para la Transparencia — Ley 20.285):</strong> Cada organismo público publica mensualmente el detalle de pasajes y viáticos, incluyendo beneficiario, cargo, destino, motivo oficial y costo.</li>
        </ul>

        <div class="modal-section-title">2. CLASE BUSINESS VS. TURISTA</div>
        <p>Por instructivos de austeridad y prudencia en el gasto público dictados por la Presidencia y el Ministerio de Hacienda, el uso de cabina ejecutiva (Business) está severamente restringido a comitivas de alta jerarquía ministerial en vuelos de más de 8 horas de duración. El costo en Business promedia entre 3 y 5 veces el de la tarifa económica regular.</p>

        <div class="modal-section-title">3. TRIBUNAL CIUDADANO</div>
        <p>La ciudadanía tiene derecho a evaluar el mérito y pertinencia del gasto público. El voto es reactivo, anónimo y se almacena en tu dispositivo para promover la reflexión cívica informada.</p>
      </div>

      <div class="modal-footer">
        <button class="btn-help-modal" id="btnModalUnderstood">ENTENDIDO, VOLVER A LA PLATAFORMA</button>
      </div>
    </div>
  </div>
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

  <script>
    /* =====================================================================
       DATASET OFICIAL DE COMITIVAS PÚBLICAS (2007-2026)
       ===================================================================== */
    const FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
    const SCL = {{ 
      code: 'SCL', 
      name: 'Aerop. Arturo Merino Benítez',
      city: 'Santiago', 
      country: 'Chile',
      airport: 'Aerop. Arturo Merino Benítez',
      lon: -70.79, 
      lat: -33.39 
    }};

    const FLIGHTS = {flights_json_str};

    // Pre-asignar estado cinemático para render a 60 FPS
    FLIGHTS.forEach((f, idx) => {{
      f.t = (idx * 0.08) % 1.0;
    }});

    /* =====================================================================
       SILUETAS CONTINENTALES VECTORIALES DE ALTA FIDELIDAD (216 VÉRTICES)
       ===================================================================== */
        const CONTINENTS_GEO = [
      // 1. Sudamérica (Silueta reconocible: Chile completo desde Arica hasta Cabo de Hornos, Argentina, Brasil, Perú, Colombia)
      [
        [-70.3, -18.5], [-70.2, -20.5], [-70.4, -23.6], [-70.8, -27.1], [-71.3, -29.9],
        [-71.6, -33.0], [-73.1, -36.8], [-73.2, -41.5], [-73.8, -42.5], [-74.5, -45.0],
        [-75.5, -48.5], [-74.0, -52.5], [-71.0, -53.5], [-67.2, -55.9], [-65.5, -54.8],
        [-67.5, -51.5], [-65.8, -46.5], [-64.0, -42.0], [-62.0, -38.5], [-58.4, -34.6],
        [-53.5, -34.5], [-48.5, -27.5], [-46.3, -24.0], [-43.2, -22.9], [-40.3, -20.3],
        [-38.5, -13.0], [-34.9, -8.1], [-35.2, -5.1], [-38.5, -3.7], [-44.3, -2.5],
        [-48.5, -1.0], [-50.0, 0.0], [-52.0, 4.5], [-54.0, 5.5], [-60.0, 8.5],
        [-66.9, 10.5], [-71.5, 11.5], [-74.5, 11.0], [-75.5, 10.4], [-77.2, 8.0],
        [-77.5, 5.0], [-79.0, 1.5], [-80.5, -1.0], [-81.2, -4.5], [-79.5, -7.0],
        [-77.0, -12.0], [-73.0, -16.0]
      ],
      // 2. Norteamérica y Centroamérica (Alaska, Canadá, EE.UU. Este/Oeste, Florida, México, Caribe)
      [
        [-168.0, 66.0], [-160.0, 58.0], [-152.0, 57.0], [-140.0, 59.5], [-130.0, 55.0],
        [-124.0, 48.0], [-124.0, 40.0], [-122.4, 37.8], [-120.0, 34.0], [-117.0, 32.5],
        [-115.0, 30.0], [-110.0, 23.0], [-105.0, 20.0], [-99.9, 16.8], [-93.0, 15.5],
        [-89.0, 13.5], [-84.0, 9.5], [-80.0, 8.5], [-77.5, 8.5], [-80.0, 9.5],
        [-83.0, 10.5], [-87.0, 13.0], [-89.0, 16.0], [-87.0, 21.0], [-90.0, 19.5],
        [-97.5, 22.0], [-97.0, 26.0], [-95.0, 29.5], [-89.5, 29.0], [-85.0, 30.0],
        [-82.5, 27.5], [-80.2, 25.8], [-80.5, 28.5], [-81.0, 31.0], [-79.0, 33.5],
        [-76.0, 37.0], [-74.0, 39.5], [-73.8, 40.6], [-70.5, 42.0], [-66.0, 44.5],
        [-63.0, 46.5], [-53.0, 47.0], [-57.0, 51.5], [-60.0, 55.0], [-64.0, 60.0],
        [-70.0, 62.0], [-80.0, 55.0], [-88.0, 55.0], [-95.0, 60.0], [-95.0, 68.0],
        [-115.0, 68.0], [-135.0, 69.5], [-150.0, 71.0], [-165.0, 70.0]
      ],
      // 3. Groenlandia
      [
        [-44.0, 60.0], [-35.0, 65.5], [-20.0, 70.0], [-18.0, 77.0], [-25.0, 81.0],
        [-40.0, 83.0], [-55.0, 82.0], [-65.0, 76.0], [-55.0, 70.0], [-50.0, 64.0]
      ],
      // 4. Eurasia (Europa Occidental: España, Francia, Italia, Alemania; y Asia)
      [
        [-9.4, 38.7], [-9.2, 43.0], [-2.9, 43.3], [-1.5, 43.5], [-4.5, 48.4],
        [1.8, 50.9], [4.3, 51.9], [8.0, 54.0], [10.0, 57.5], [12.5, 55.7],
        [18.0, 59.3], [25.0, 65.0], [30.0, 70.0], [45.0, 68.0], [60.0, 70.0],
        [80.0, 73.0], [100.0, 76.0], [120.0, 74.0], [140.0, 72.0], [160.0, 70.0],
        [170.0, 65.0], [162.0, 58.0], [150.0, 59.0], [140.0, 53.0], [132.0, 43.0],
        [128.0, 36.0], [121.0, 37.0], [118.0, 39.0], [121.5, 31.2], [114.0, 22.3],
        [108.0, 18.0], [103.8, 1.3], [100.0, 6.0], [98.0, 16.0], [88.3, 22.5],
        [80.0, 15.0], [77.5, 8.1], [72.8, 19.0], [68.0, 24.0], [60.0, 25.0],
        [50.0, 30.0], [48.0, 31.0], [35.0, 32.0], [32.0, 36.5], [26.0, 40.0],
        [23.0, 38.0], [19.0, 40.5], [16.0, 38.2], [14.2, 40.8], [12.5, 41.9],
        [8.9, 44.4], [5.3, 43.3], [2.1, 41.4], [-0.3, 39.5], [-4.4, 36.7],
        [-5.3, 36.1], [-8.0, 37.0]
      ],
      // 5. Gran Bretaña e Irlanda
      [
        [-5.5, 50.1], [1.3, 51.1], [1.7, 52.5], [0.0, 54.5], [-3.2, 55.9],
        [-2.0, 57.5], [-4.0, 58.5], [-6.0, 56.5], [-4.5, 52.0]
      ],
      // 6. Japón (Honshu, Hokkaido, Kyushu - Eje Tokio y Osaka)
      [
        [130.0, 31.5], [131.0, 34.0], [135.2, 34.4], [140.0, 35.5], [141.5, 38.5],
        [141.0, 43.0], [145.5, 44.0], [140.5, 41.5], [138.0, 37.5], [133.0, 35.5],
        [129.5, 33.0]
      ],
      // 7. África
      [
        [-5.8, 35.8], [-12.0, 28.0], [-17.5, 14.7], [-12.0, 8.0], [-4.0, 5.0],
        [3.4, 6.4], [9.0, 4.0], [12.0, -5.0], [13.0, -15.0], [18.4, -33.9],
        [26.0, -33.5], [31.0, -29.9], [35.0, -18.0], [40.0, -10.0], [42.0, -2.0],
        [51.0, 10.5], [43.0, 12.5], [38.0, 18.0], [33.0, 27.5], [30.0, 31.0],
        [20.0, 32.0], [13.0, 32.9], [10.0, 36.8], [2.0, 36.0]
      ],
      // 8. Australia y Oceanía
      [
        [114.0, -22.0], [115.8, -31.9], [120.0, -34.0], [130.0, -32.0], [138.0, -35.0],
        [145.0, -37.8], [150.0, -36.0], [151.2, -33.9], [153.0, -27.5], [148.0, -20.0],
        [142.5, -10.8], [136.0, -12.0], [130.8, -12.4], [124.0, -16.0]
      ],
      // 9. Rapa Nui / Isla de Pascua (Polígono distintivo)
      [
        [-109.5, -27.1], [-109.35, -27.1], [-109.4, -27.25]
      ]
    ];

    /* =====================================================================
       ESTADO GLOBAL DE LA PLATAFORMA
       ===================================================================== */
    let selectedFlight = FLIGHTS[FLIGHTS.length - 1];
    let currentSort = 'date'; // 'date' (más reciente primero) | 'cost' | 'entity'
    let currentMonthIndex = 237; // Octubre 2026 (mes más reciente disponible)
    let selectedProvider = 'Todas'; // 'Todas' | 'Cocha' | 'Turavion' | 'LATAM' | 'Sky'
    let filterBusinessOnly = false;
    let selectedEntityGroup = 'Todas';
    let searchFilterText = '';

    // Filtros ampliados
    let filterScope = 'Todas'; // 'Todas' | 'Nacional' | 'Internacional'
    let filterGovernment = 'Todas'; // 'Todas' | 'Boric' | 'Piñera II' | 'Bachelet II' | 'Piñera I' | 'Bachelet I'
    let filterYear = 'Todas'; // 'Todas' | '2026' ... '2007'
    let filterCostTier = 'Todas'; // 'Todas' | 'Mega' | 'Alta' | 'Media' | 'Menor'
    let filterDestination = 'Todas'; // 'Todas' | ciudad o país

    let filterCabin = 'Todas'; // 'Todas' | 'Business' | 'Turista'

    function matchesGovernment(dateStr, gov) {{
      if (!gov || gov === 'Todas') return true;
      if (gov === 'Boric') return dateStr >= '2022-03-11';
      if (gov === 'Piñera II') return dateStr >= '2018-03-11' && dateStr < '2022-03-11';
      if (gov === 'Bachelet II') return dateStr >= '2014-03-11' && dateStr < '2018-03-11';
      if (gov === 'Piñera I') return dateStr >= '2010-03-11' && dateStr < '2014-03-10';
      if (gov === 'Bachelet I') return dateStr < '2010-03-11';
      return true;
    }}

    function matchesCostTier(cost, tier) {{
      if (!tier || tier === 'Todas') return true;
      if (tier === 'Mega') return cost >= 20000000;
      if (tier === 'Alta') return cost >= 5000000 && cost < 20000000;
      if (tier === 'Media') return cost >= 1000000 && cost < 5000000;
      if (tier === 'Menor') return cost < 1000000;
      return true;
    }}

    function matchesEntityGroup(entity, group) {{
      if (!group || group.toLowerCase() === 'todas') return true;
      const entityStr = typeof entity === 'object' && entity !== null ? (entity.entity || '') : String(entity || '');
      const up = entityStr.toUpperCase();
      const gNorm = group.toLowerCase();
      if (gNorm === 'presidencia') {{
        return up.includes('PRESIDENCIA') || up.includes('SECRETARÍA GENERAL') || up.includes('SECRETARIA GENERAL') || up.includes('INTERIOR');
      }}
      if (gNorm === 'defensa') {{
        return up.includes('FUERZA AÉREA') || up.includes('FUERZA AEREA') || up.includes('EJÉRCITO') || up.includes('EJERCITO') || up.includes('ARMADA') || up.includes('DEFENSA') || up.includes('LOGÍSTICO') || up.includes('LOGISTICO') || up.includes('COMANDO') || up.includes('CARABINEROS') || up.includes('AERONAUTICA');
      }}
      if (gNorm.includes('cancil') || gNorm.includes('exteriores')) {{
        return up.includes('RELACIONES EXTERIORES') || up.includes('CANCIL') || up.includes('MINREL') || up.includes('PROCHILE') || up.includes('CONSUL');
      }}
      if (gNorm === 'universidades') {{
        return up.includes('UNIVERSIDAD');
      }}
      if (gNorm === 'municipalidades') {{
        return up.includes('MUNICIPALIDAD') || up.includes('MUNICIPAL');
      }}
      if (gNorm === 'sectoriales') {{
        return (up.includes('MINISTERIO') || up.includes('SUBSECRETARÍA') || up.includes('SUBSECRETARIA') || up.includes('MINERÍA') || up.includes('HACIENDA') || up.includes('SALUD') || up.includes('EDUCACIÓN') || up.includes('OBRAS PÚBLICAS') || up.includes('AGRICULTURA')) && !up.includes('UNIVERSIDAD') && !up.includes('MUNICIPAL');
      }}
      if (gNorm === 'otros') {{
        return !matchesEntityGroup(entityStr, 'presidencia') && !matchesEntityGroup(entityStr, 'defensa') && !matchesEntityGroup(entityStr, 'cancillería') && !matchesEntityGroup(entityStr, 'sectoriales') && !matchesEntityGroup(entityStr, 'universidades') && !matchesEntityGroup(entityStr, 'municipalidades');
      }}
      return true;
    }}

    function flightMatchesAllFilters(flight, checkMonth = false, maxMonthIndex = 239) {{
      if (checkMonth && flight.monthIndex > maxMonthIndex) return false;

      // 1. Proveedor / Agencia
      if (selectedProvider !== 'Todas' && flight.provider !== selectedProvider) return false;

      // 2. Cabina
      if (filterBusinessOnly && flight.cabin !== 'Business') return false;
      if (filterCabin !== 'Todas' && flight.cabin !== filterCabin) return false;

      // 3. Organismo
      if (selectedEntityGroup !== 'Todas' && !matchesEntityGroup(flight.entity, selectedEntityGroup)) return false;

      // 4. Ámbito
      if (filterScope === 'Nacional' && flight.dest.country !== 'Chile') return false;
      if (filterScope === 'Internacional' && flight.dest.country === 'Chile') return false;

      // 5. Destino
      if (filterDestination !== 'Todas') {{
        if (flight.dest.city !== filterDestination && flight.dest.country !== filterDestination && flight.dest.code !== filterDestination) {{
          return false;
        }}
      }}

      // 6. Gobierno
      if (filterGovernment !== 'Todas' && !matchesGovernment(flight.date, filterGovernment)) return false;

      // 7. Año
      if (filterYear !== 'Todas' && String(flight.year) !== String(filterYear)) return false;

      // 8. Tramo de Monto
      if (filterCostTier !== 'Todas' && !matchesCostTier(flight.cost, filterCostTier)) return false;



      // 10. Búsqueda de texto
      if (searchFilterText) {{
        const q = searchFilterText.trim().toLowerCase();
        const matchTarget = `${{flight.entity}} ${{flight.role}} ${{flight.dest.city}} ${{flight.dest.code}} ${{flight.dest.country}} ${{flight.oc}} ${{flight.reason}}`.toLowerCase();
        if (!matchTarget.includes(q)) return false;
      }}

      return true;
    }}

    let isPlaying = false;
    let playInterval = null;

    // Estado del Mapa
    let zoomLevel = 1.0;
    let panOffset = {{ x: 0, y: 0 }};
    let isDragging = false;
    let hasDragged = false;
    let startPointer = {{ x: 0, y: 0 }};

    /* =====================================================================
       ELEMENTOS DOM
       ===================================================================== */
    // Sidebar
    const flightListContainer = document.getElementById('flightListContainer');
    const listBadgeCount = document.getElementById('listBadgeCount');
    const mobileCountBadge = document.getElementById('mobileCountBadge');
    const flightSearchInput = document.getElementById('flightSearchInput');
    const btnClearSearch = document.getElementById('btnClearSearch');
    const btnSortCost = document.getElementById('btnSortCost');
    const btnSortDate = document.getElementById('btnSortDate');
    const btnSortEntity = document.getElementById('btnSortEntity');

    // Dossier
    const badgeCabin = document.getElementById('badgeCabin');
    const origCode = document.getElementById('origCode');
    const origCity = document.getElementById('origCity');
    const origAirport = document.getElementById('origAirport');
    const destCode = document.getElementById('destCode');
    const destCity = document.getElementById('destCity');
    const destAirport = document.getElementById('destAirport');
    const routeDistance = document.getElementById('routeDistance');
    const entityName = document.getElementById('entityName');
    const passengerRole = document.getElementById('passengerRole');
    const ticketCost = document.getElementById('ticketCost');
    const metaCabinDesc = document.getElementById('metaCabinDesc');
    const metaAirline = document.getElementById('metaAirline');
    const metaProvider = document.getElementById('metaProvider');
    const metaOc = document.getElementById('metaOc');
    const btnCopyOc = document.getElementById('btnCopyOc');
    const officialReason = document.getElementById('officialReason');
    const mpLink = document.getElementById('mpLink');

    // Tribunal
    const btnApprove = document.getElementById('btnApprove');
    const btnReject = document.getElementById('btnReject');
    const barApprove = document.getElementById('barApprove');
    const barReject = document.getElementById('barReject');
    const txtApprove = document.getElementById('txtApprove');
    const txtReject = document.getElementById('txtReject');
    const voteStatus = document.getElementById('voteStatus');

    // Scrubber & Odometer
    const timelineSlider = document.getElementById('timelineSlider');
    const currentMonthLabel = document.getElementById('currentMonthLabel');
    const fiscalOdometer = document.getElementById('fiscalOdometer');
    const scrubberSparkline = document.getElementById('scrubberSparkline');
    const btnPrevMonth = document.getElementById('btnPrevMonth');
    const btnPlayPause = document.getElementById('btnPlayPause');
    const btnNextMonth = document.getElementById('btnNextMonth');
    const filterProviderContainer = document.getElementById('filterProvider');
    const filterProviderSelect = document.getElementById('filterProviderSelect');
    const filterEntitySelect = document.getElementById('filterEntitySelect');
    const btnToggleBusiness = document.getElementById('btnToggleBusiness');
    const btnShareExpediente = document.getElementById('btnShareExpediente');
    const shareToast = document.getElementById('shareToast');

    // Header stats
    const statFlightsCount = document.getElementById('statFlightsCount');
    const statTotalSpend = document.getElementById('statTotalSpend');
    const statBusinessCount = document.getElementById('statBusinessCount');
    const statTopEntity = document.getElementById('statTopEntity');
    const statTopDest = document.getElementById('statTopDest');

    // Map & Canvas
    const canvas = document.getElementById('radarCanvas');
    const ctx = canvas.getContext('2d');
    const mapContainer = document.getElementById('mapContainer');
    const mapTooltip = document.getElementById('mapTooltip');
    const btnZoomIn = document.getElementById('btnZoomIn');
    const btnZoomOut = document.getElementById('btnZoomOut');
    const btnResetView = document.getElementById('btnResetView');

    // Modal
    const helpModal = document.getElementById('helpModal');
    const btnOpenHelp = document.getElementById('btnOpenHelp');
    const btnCloseHelp = document.getElementById('btnCloseHelp');
    const btnModalUnderstood = document.getElementById('btnModalUnderstood');

    // Mobile Tabs
    const mobileViewTabs = document.getElementById('mobileViewTabs');
    const sidebarColumn = document.getElementById('sidebarColumn');
    const mapColumn = document.getElementById('mapColumn');
    const dossierColumn = document.getElementById('dossierColumn');

    /* =====================================================================
       CÁLCULO GEODÉSICO DE DISTANCIA (FÓRMULA DE HAVERSINE)
       ===================================================================== */
    function calculateDistanceKm(lat1, lon1, lat2, lon2) {{
      const R = 6371; // Radio de la Tierra en km
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return Math.round(R * c);
    }}

    function estimateFlightTime(km) {{
      const hours = km / 850; // velocidad de crucero promedio en jet comercial
      const h = Math.floor(hours);
      const m = Math.round((hours - h) * 60);
      return `${{h}}h ${{m < 10 ? '0' : ''}}${{m}}m`;
    }}

    /* =====================================================================
       PERSISTENCIA LOCAL DE VOTOS (LOCALSTORAGE)
       ===================================================================== */
    const STORAGE_KEY_VOTES = 'vuelospublicos_user_votes';
    const STORAGE_KEY_TALLIES = 'vuelospublicos_vote_tallies';
    const LEGACY_KEY_VOTES = 'vuelospublicos_votes_v1';
    const LEGACY_KEY_TALLIES = 'vuelospublicos_tallies_v1';

    function getUserVote(flightId) {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY_VOTES) || localStorage.getItem(LEGACY_KEY_VOTES);
        if (raw) {{
          const map = JSON.parse(raw);
          if (map && typeof map === 'object') {{
            return map[flightId] || null;
          }}
        }}
      }} catch (e) {{}}
      return null;
    }}

    function getFlightTallies(flight) {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY_TALLIES) || localStorage.getItem(LEGACY_KEY_TALLIES);
        if (raw) {{
          const map = JSON.parse(raw);
          if (map[flight.id]) {{
            return map[flight.id];
          }}
        }}
      }} catch (e) {{}}
      return {{ approve: flight.votes.approve, reject: flight.votes.reject }};
    }}

    function castVote(flightId, voteType) {{
      if (getUserVote(flightId)) return false;

      const flight = FLIGHTS.find(f => f.id === flightId);
      if (!flight) return false;

      let userVotes = {{}};
      try {{
        const raw = localStorage.getItem(STORAGE_KEY_VOTES) || localStorage.getItem(LEGACY_KEY_VOTES);
        if (raw) userVotes = JSON.parse(raw);
      }} catch (e) {{}}
      userVotes[flightId] = voteType;
      try {{
        localStorage.setItem(STORAGE_KEY_VOTES, JSON.stringify(userVotes));
        localStorage.setItem(LEGACY_KEY_VOTES, JSON.stringify(userVotes));
      }} catch (e) {{}}

      const tallies = getFlightTallies(flight);
      if (voteType === 'approve') {{
        tallies.approve += 1;
      }} else if (voteType === 'reject') {{
        tallies.reject += 1;
      }}
      flight.votes.approve = tallies.approve;
      flight.votes.reject = tallies.reject;

      let allTallies = {{}};
      try {{
        const raw = localStorage.getItem(STORAGE_KEY_TALLIES) || localStorage.getItem(LEGACY_KEY_TALLIES);
        if (raw) allTallies = JSON.parse(raw);
      }} catch (e) {{}}
      allTallies[flightId] = tallies;
      try {{
        localStorage.setItem(STORAGE_KEY_TALLIES, JSON.stringify(allTallies));
        localStorage.setItem(LEGACY_KEY_TALLIES, JSON.stringify(allTallies));
      }} catch (e) {{}}

      updateVoteDisplay();
      return true;
    }}

    function updateVoteDisplay() {{
      if (!barApprove || !barReject || !txtApprove || !txtReject) return;
      const tallies = getFlightTallies(selectedFlight);
      const A = tallies.approve;
      const R = tallies.reject;
      const total = A + R;

      let pApprove = 50;
      let pReject = 50;
      if (total > 0) {{
        pApprove = Math.round((A / total) * 100);
        pReject = 100 - pApprove;
      }}

      barApprove.style.width = `${{pApprove}}%`;
      barReject.style.width = `${{pReject}}%`;

      txtApprove.textContent = `Justificado: ${{pApprove}}% (${{A}})`;
      txtReject.textContent = `Derroche: ${{pReject}}% (${{R}})`;

      const userVote = getUserVote(selectedFlight.id);
      if (userVote) {{
        btnApprove.disabled = true;
        btnReject.disabled = true;
        btnApprove.classList.toggle('active-voted', userVote === 'approve');
        btnReject.classList.toggle('active-voted', userVote === 'reject');
        voteStatus.textContent = '✓ Ya emitiste tu voto en este expediente';
        voteStatus.className = 'vote-status-msg voted';
      }} else {{
        btnApprove.disabled = false;
        btnReject.disabled = false;
        btnApprove.classList.remove('active-voted');
        btnReject.classList.remove('active-voted');
        voteStatus.textContent = 'Tu voto es anónimo y ciudadano';
        voteStatus.className = 'vote-status-msg';
      }}
    }}

    if (btnApprove) btnApprove.addEventListener('click', () => castVote(selectedFlight.id, 'approve'));
    if (btnReject) btnReject.addEventListener('click', () => castVote(selectedFlight.id, 'reject'));

    /* =====================================================================
       ORDENAMIENTO, BÚSQUEDA Y RENDER DEL PANEL LATERAL
       ===================================================================== */
    function getSortedFlights() {{
      const filtered = FLIGHTS.filter(flight => flightMatchesAllFilters(flight, false));

      return [...filtered].sort((a, b) => {{
        if (currentSort === 'date') {{
          return b.date.localeCompare(a.date); // Lo más reciente primero (Octubre 2026 -> 2007)
        }} else if (currentSort === 'cost') {{
          return b.cost - a.cost;
        }} else if (currentSort === 'entity') {{
          return a.entity.localeCompare(b.entity);
        }}
        return 0;
      }});
    }}

    function renderFlightList() {{
      const sorted = getSortedFlights();
      flightListContainer.innerHTML = '';
      listBadgeCount.textContent = `${{sorted.length}} de ${{FLIGHTS.length}}`;
      if (mobileCountBadge) mobileCountBadge.textContent = sorted.length;

      if (sorted.length === 0) {{
        const emptyMsg = document.createElement('div');
        emptyMsg.className = 'flight-card';
        emptyMsg.style.textAlign = 'center';
        emptyMsg.style.color = 'var(--text-muted)';
        emptyMsg.style.padding = '20px 10px';
        emptyMsg.textContent = 'Sin comitivas para los filtros y búsqueda aplicados';
        flightListContainer.appendChild(emptyMsg);
        return;
      }}

      sorted.forEach(flight => {{
        const isSelected = (selectedFlight && selectedFlight.id === flight.id);
        const isIssued = flight.monthIndex <= currentMonthIndex;

        const card = document.createElement('div');
        card.className = `flight-card ${{isSelected ? 'active' : ''}} ${{isIssued ? '' : 'dimmed'}}`;
        card.id = `flight-item-${{flight.id}}`;
        card.dataset.id = flight.id;

        const badgeClass = flight.cabin === 'Business' ? 'badge-business' : 'badge-turista';
        const formattedCost = `$${{flight.cost.toLocaleString('es-CL')}} CLP`;

        card.innerHTML = `
          <div class="flight-card-header">
            <div class="flight-card-route">
              <span>SCL</span>
              <span>➔</span>
              <span>${{flight.dest.code}}</span>
              <span style="font-weight: 500; font-size: 0.72rem; color: var(--text-secondary); margin-left: 2px;">(${{flight.dest.city}})</span>
            </div>
            <span class="flight-card-badge ${{badgeClass}}">${{flight.cabin}}</span>
          </div>
          <div class="flight-card-body">
            <div class="flight-card-entity" title="${{flight.entity}}">${{flight.entity}}</div>
            <div class="flight-card-passenger" title="${{flight.role}}">${{flight.role}}</div>
          </div>
          <div class="flight-card-footer">
            <span>${{flight.date}} • ${{flight.provider}}</span>
            <span class="flight-card-cost">${{formattedCost}}</span>
          </div>
        `;

        card.addEventListener('click', () => {{
          selectFlight(flight);
        }});

        flightListContainer.appendChild(card);
      }});
    }}

    // Listener del buscador en vivo
    if (flightSearchInput) {{
      flightSearchInput.addEventListener('input', (e) => {{
        searchFilterText = e.target.value;
        if (btnClearSearch) btnClearSearch.style.display = searchFilterText ? 'block' : 'none';
        renderFlightList();
      }});
    }}

    if (btnClearSearch) {{
      btnClearSearch.addEventListener('click', () => {{
        searchFilterText = '';
        flightSearchInput.value = '';
        btnClearSearch.style.display = 'none';
        renderFlightList();
      }});
    }}

    // Listeners de ordenamiento
    [btnSortCost, btnSortDate, btnSortEntity].forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        [btnSortCost, btnSortDate, btnSortEntity].forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        currentSort = e.currentTarget.dataset.sort;
        renderFlightList();
      }});
    }});

    /* =====================================================================
       DETALLE DEL EXPEDIENTE FISCAL
       ===================================================================== */
    function selectFlight(flight) {{
      selectedFlight = flight;
      if (typeof centerOnFlight === 'function') {{
        centerOnFlight(flight);
      }}

      // Actualizar tarjeta
      origCode.textContent = flight.origin.code;
      origCity.textContent = flight.origin.city;
      origAirport.textContent = flight.origin.airport;

      destCode.textContent = flight.dest.code;
      destCity.textContent = `${{flight.dest.city}}, ${{flight.dest.country}}`;
      destAirport.textContent = flight.dest.airport;

      // Distancia y tiempo de vuelo
      const km = calculateDistanceKm(flight.origin.lat, flight.origin.lon, flight.dest.lat, flight.dest.lon);
      const estTime = estimateFlightTime(km);
      if (routeDistance) {{
        routeDistance.textContent = `${{km.toLocaleString('es-CL')}} km • ${{estTime}}`;
      }}

      entityName.textContent = flight.entity;
      passengerRole.textContent = flight.role;
      ticketCost.textContent = `$${{flight.cost.toLocaleString('es-CL')}} CLP`;

      metaCabinDesc.textContent = `${{flight.cabin}} • ${{flight.cabinDesc}}`;
      metaAirline.textContent = flight.airline || 'Vuelo Comercial Regular';
      metaProvider.textContent = flight.provider;
      metaOc.textContent = flight.oc;
      officialReason.textContent = `"${{flight.reason}}"`;

      if (mpLink) {{
        mpLink.href = `https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?qs=${{encodeURIComponent(flight.oc)}}`;
      }}

      // Badge de cabina
      badgeCabin.textContent = `CLASE ${{flight.cabin.toUpperCase()}}`;
      badgeCabin.className = `flight-card-badge ${{flight.cabin === 'Business' ? 'badge-business' : 'badge-turista'}}`;

      // Resaltar tarjeta activa en la lista
      document.querySelectorAll('.flight-card').forEach(el => el.classList.remove('active'));
      const activeCard = document.getElementById(`flight-item-${{flight.id}}`);
      if (activeCard) activeCard.classList.add('active');

      updateVoteDisplay();
    }}

    // Copiar código OC
    if (btnCopyOc) {{
      btnCopyOc.addEventListener('click', () => {{
        if (!selectedFlight) return;
        if (navigator.clipboard) {{
          navigator.clipboard.writeText(selectedFlight.oc).then(() => {{
            const prevText = btnCopyOc.textContent;
            btnCopyOc.textContent = '✓ Copiado';
            setTimeout(() => {{ btnCopyOc.textContent = prevText; }}, 1800);
          }});
        }}
      }});
    }}

    /* =====================================================================
       LÍNEA DE TIEMPO, ODÓMETRO FISCAL Y MÉTRICAS GLOBALES
       ===================================================================== */
    const MONTH_NAMES = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];

    function getMonthLabel(monthIndex) {{
      const year = 2007 + Math.floor(monthIndex / 12);
      const m = monthIndex % 12;
      return `${{MONTH_NAMES[m]}} ${{year}}`;
    }}

    function calculateOdometer(maxMonthIndex, provider) {{
      return FLIGHTS.reduce((sum, flight) => {{
        if (flightMatchesAllFilters(flight, true, maxMonthIndex)) {{
          return sum + flight.cost;
        }}
        return sum;
      }}, 0);
    }}

    function updateGlobalStats() {{
      const activeFlights = FLIGHTS.filter(flight => flightMatchesAllFilters(flight, false));

      const totalSpend = activeFlights.reduce((sum, f) => sum + f.cost, 0);
      const businessCount = activeFlights.filter(f => f.cabin === 'Business').length;
      const businessPct = activeFlights.length ? Math.round((businessCount / activeFlights.length) * 100) : 0;

      if (statFlightsCount) statFlightsCount.textContent = activeFlights.length.toLocaleString('es-CL');
      if (statTotalSpend) {{
        statTotalSpend.textContent = totalSpend >= 1000000000
          ? `$${{(totalSpend / 1000000000).toFixed(2)}}B CLP`
          : `$${{(totalSpend / 1000000).toFixed(0)}}M CLP`;
        statTotalSpend.title = `$${{totalSpend.toLocaleString('es-CL')}} CLP`;
      }}
      if (statBusinessCount) statBusinessCount.textContent = `${{businessCount}} (${{businessPct}}%)`;

      // Calcular Top Organismo y Top Destino
      const entitySpends = {{}};
      const destCounts = {{}};
      activeFlights.forEach(f => {{
        entitySpends[f.entity] = (entitySpends[f.entity] || 0) + f.cost;
        const dCity = f.dest.city;
        destCounts[dCity] = (destCounts[dCity] || 0) + 1;
      }});

      const topEntityEntry = Object.entries(entitySpends).sort((a,b) => b[1] - a[1])[0];
      const topDestEntry = Object.entries(destCounts).sort((a,b) => b[1] - a[1])[0];

      if (statTopEntity && topEntityEntry) {{
        const shortName = topEntityEntry[0].length > 20 ? topEntityEntry[0].slice(0, 18) + '…' : topEntityEntry[0];
        statTopEntity.textContent = shortName;
        statTopEntity.title = `${{topEntityEntry[0]}}: $${{topEntityEntry[1].toLocaleString('es-CL')}} CLP`;
      }}
      if (statTopDest && topDestEntry) {{
        statTopDest.textContent = `${{topDestEntry[0]}} (${{topDestEntry[1]}})`;
        statTopDest.title = `${{topDestEntry[0]}}: ${{topDestEntry[1]}} comitivas oficiales registradas`;
      }}
    }}

    // Dibujar Sparkline de densidad mensual sobre el scrubber
    function drawScrubberSparkline() {{
      if (!scrubberSparkline) return;
      const sCtx = scrubberSparkline.getContext('2d');
      const w = scrubberSparkline.width = scrubberSparkline.clientWidth;
      const h = scrubberSparkline.height = 20;

      sCtx.clearRect(0, 0, w, h);

      // Calcular montos por cada uno de los 240 meses
      const monthlyCosts = new Array(240).fill(0);
      FLIGHTS.forEach(f => {{
        if (f.monthIndex >= 0 && f.monthIndex < 240) {{
          monthlyCosts[f.monthIndex] += f.cost;
        }}
      }});

      const maxCost = Math.max(...monthlyCosts, 1);
      const barWidth = Math.max(1, w / 240);

      monthlyCosts.forEach((cost, idx) => {{
        if (cost === 0) return;
        const barHeight = Math.max(2, (cost / maxCost) * (h - 2));
        const x = (idx / 240) * w;
        const y = h - barHeight;

        sCtx.fillStyle = idx <= currentMonthIndex ? '#38bdf8' : 'rgba(56, 139, 253, 0.25)';
        sCtx.fillRect(x, y, Math.max(1.5, barWidth - 0.5), barHeight);
      }});
    }}

    function updateTimeline() {{
      currentMonthLabel.textContent = getMonthLabel(currentMonthIndex);
      timelineSlider.value = currentMonthIndex;

      const totalAccum = calculateOdometer(currentMonthIndex, selectedProvider);
      fiscalOdometer.textContent = `$${{totalAccum.toLocaleString('es-CL')}} CLP`;

      const sorted = getSortedFlights();
      // Si el vuelo activo quedó excluido por los filtros, enfocar el primer resultado disponible
      if (selectedFlight && !flightMatchesAllFilters(selectedFlight, false)) {{
        if (sorted.length > 0) {{
          selectFlight(sorted[0]);
        }}
      }}

      renderFlightList();
      updateGlobalStats();
      drawScrubberSparkline();
      updateActiveChipsBar();
    }}

    timelineSlider.addEventListener('input', (e) => {{
      currentMonthIndex = parseInt(e.target.value, 10);
      updateTimeline();
    }});

    btnPrevMonth.addEventListener('click', () => {{
      if (currentMonthIndex > 0) {{
        currentMonthIndex--;
        updateTimeline();
      }}
    }});

    btnNextMonth.addEventListener('click', () => {{
      if (currentMonthIndex < 239) {{
        currentMonthIndex++;
        updateTimeline();
      }}
    }});

    btnPlayPause.addEventListener('click', () => {{
      if (isPlaying) {{
        stopPlayback();
      }} else {{
        startPlayback();
      }}
    }});

    function startPlayback() {{
      isPlaying = true;
      btnPlayPause.textContent = '⏸ Pausar';
      btnPlayPause.classList.add('playing');

      if (currentMonthIndex >= 239) {{
        currentMonthIndex = 0;
        updateTimeline();
      }}

      playInterval = setInterval(() => {{
        if (currentMonthIndex < 239) {{
          currentMonthIndex++;
          updateTimeline();
        }} else {{
          stopPlayback();
        }}
      }}, 1200);
    }}

    function stopPlayback() {{
      isPlaying = false;
      btnPlayPause.textContent = '⏯ Reproducir';
      btnPlayPause.classList.remove('playing');
      if (playInterval) {{
        clearInterval(playInterval);
        playInterval = null;
      }}
    }}

    // Filtros de Proveedor
    document.querySelectorAll('.provider-chip').forEach(chip => {{
      chip.addEventListener('click', (e) => {{
        document.querySelectorAll('.provider-chip').forEach(c => c.classList.remove('active'));
        e.currentTarget.classList.add('active');
        selectedProvider = e.currentTarget.dataset.provider;
        if (filterProviderSelect) filterProviderSelect.value = selectedProvider;
        updateTimeline();
      }});
    }});

    if (filterProviderSelect) {{
      filterProviderSelect.addEventListener('change', (e) => {{
        selectedProvider = e.target.value;
        document.querySelectorAll('.provider-chip').forEach(c => {{
          c.classList.toggle('active', c.dataset.provider === selectedProvider);
        }});
        updateTimeline();
      }});
    }}

    // Filtro de Organismo
    if (filterEntitySelect) {{
      filterEntitySelect.addEventListener('change', (e) => {{
        selectedEntityGroup = e.target.value;
        updateTimeline();
      }});
    }}

    // Toggle Solo Business
    if (btnToggleBusiness) {{
      btnToggleBusiness.addEventListener('click', () => {{
        filterBusinessOnly = !filterBusinessOnly;
        filterCabin = filterBusinessOnly ? 'Business' : 'Todas';
        btnToggleBusiness.classList.toggle('active', filterBusinessOnly);
        syncQuickChips();
        updateTimeline();
      }});
    }}

    // Referencias a los nuevos controles
    const filterScopeSelect = document.getElementById('filterScopeSelect');
    const filterGovernmentSelect = document.getElementById('filterGovernmentSelect');
    const filterYearSelect = document.getElementById('filterYearSelect');
    const filterCostTierSelect = document.getElementById('filterCostTierSelect');
    const filterDestinationSelect = document.getElementById('filterDestinationSelect');

    const btnResetAllFilters = document.getElementById('btnResetAllFilters');
    const btnSidebarReset = document.getElementById('btnSidebarReset');
    const activeFiltersBar = document.getElementById('activeFiltersBar');
    const activeChipsContainer = document.getElementById('activeChipsContainer');
    const activeFiltersSummary = document.getElementById('activeFiltersSummary');

    function syncSelectVisuals() {{
      const selects = [
        {{ el: filterScopeSelect, val: filterScope }},
        {{ el: filterGovernmentSelect, val: filterGovernment }},
        {{ el: filterYearSelect, val: filterYear }},
        {{ el: filterEntitySelect, val: selectedEntityGroup }},
        {{ el: filterCostTierSelect, val: filterCostTier }},
        {{ el: filterDestinationSelect, val: filterDestination }},

        {{ el: filterProviderSelect, val: selectedProvider }}
      ];

      selects.forEach((item) => {{
        if (item.el) {{
          item.el.value = item.val;
          item.el.classList.toggle('has-filter', item.val !== 'Todas');
        }}
      }});
    }}

    function syncQuickChips() {{
      document.querySelectorAll('.quick-chip').forEach(chip => {{
        const type = chip.dataset.filterType;
        const val = chip.dataset.value;
        let isActive = false;
        if (type === 'scope') isActive = (filterScope === val);
        else if (type === 'cabin') isActive = (filterCabin === val);
        else if (type === 'costTier') isActive = (filterCostTier === val);
        else if (type === 'government') isActive = (filterGovernment === val);
        chip.classList.toggle('active', isActive);
      }});
    }}

    function updateActiveChipsBar() {{
      if (!activeChipsContainer || !activeFiltersBar) return;

      const activeFilters = [];
      if (filterScope !== 'Todas') {{
        activeFilters.push({{ label: `Ámbito: ${{filterScope}}`, clear: () => {{ filterScope = 'Todas'; }} }});
      }}
      if (filterGovernment !== 'Todas') {{
        activeFilters.push({{ label: `Gobierno: ${{filterGovernment}}`, clear: () => {{ filterGovernment = 'Todas'; }} }});
      }}
      if (filterYear !== 'Todas') {{
        activeFilters.push({{ label: `Año: ${{filterYear}}`, clear: () => {{ filterYear = 'Todas'; }} }});
      }}
      if (selectedEntityGroup !== 'Todas') {{
        activeFilters.push({{ label: `Organismo: ${{selectedEntityGroup}}`, clear: () => {{ selectedEntityGroup = 'Todas'; }} }});
      }}
      if (filterCostTier !== 'Todas') {{
        activeFilters.push({{ label: `Monto: ${{filterCostTier}}`, clear: () => {{ filterCostTier = 'Todas'; }} }});
      }}
      if (filterDestination !== 'Todas') {{
        activeFilters.push({{ label: `Destino: ${{filterDestination}}`, clear: () => {{ filterDestination = 'Todas'; }} }});
      }}

      if (selectedProvider !== 'Todas') {{
        activeFilters.push({{ label: `Agencia: ${{selectedProvider}}`, clear: () => {{ selectedProvider = 'Todas'; }} }});
      }}
      if (filterBusinessOnly) {{
        activeFilters.push({{ label: `Clase: Business`, clear: () => {{ filterBusinessOnly = false; filterCabin = 'Todas'; }} }});
      }}
      if (searchFilterText) {{
        activeFilters.push({{ label: `Búsqueda: "${{searchFilterText}}"`, clear: () => {{ searchFilterText = ''; if (flightSearchInput) flightSearchInput.value = ''; if (btnClearSearch) btnClearSearch.style.display = 'none'; }} }});
      }}

      activeChipsContainer.innerHTML = '';

      const hasAnyFilter = activeFilters.length > 0;
      activeFiltersBar.style.display = hasAnyFilter ? 'flex' : 'none';
      if (btnResetAllFilters) btnResetAllFilters.classList.toggle('visible', hasAnyFilter);
      if (btnSidebarReset) btnSidebarReset.style.display = hasAnyFilter ? 'inline-block' : 'none';

      if (hasAnyFilter) {{
        const sorted = getSortedFlights();
        const totalCLP = sorted.reduce((acc, f) => acc + f.cost, 0);
        if (activeFiltersSummary) {{
          activeFiltersSummary.textContent = `${{sorted.length}} de ${{FLIGHTS.length}} comitivas ($${{Math.round(totalCLP / 1e6).toLocaleString('es-CL')}}M CLP)`;
        }}

        activeFilters.forEach(item => {{
          const chip = document.createElement('span');
          chip.className = 'active-filter-chip';
          chip.innerHTML = `${{item.label}} <span class="chip-remove" title="Quitar este filtro">&times;</span>`;
          chip.querySelector('.chip-remove').addEventListener('click', () => {{
            item.clear();
            syncSelectVisuals();
            syncQuickChips();
            updateTimeline();
          }});
          activeChipsContainer.appendChild(chip);
        }});
      }}
    }}

    function resetAllFilters() {{
      filterScope = 'Todas';
      filterGovernment = 'Todas';
      filterYear = 'Todas';
      selectedEntityGroup = 'Todas';
      filterCostTier = 'Todas';
      filterDestination = 'Todas';

      selectedProvider = 'Todas';
      filterBusinessOnly = false;
      filterCabin = 'Todas';
      searchFilterText = '';

      if (flightSearchInput) flightSearchInput.value = '';
      if (btnClearSearch) btnClearSearch.style.display = 'none';
      if (btnToggleBusiness) btnToggleBusiness.classList.remove('active');

      document.querySelectorAll('.provider-chip').forEach(c => {{
        c.classList.toggle('active', c.dataset.provider === 'Todas');
      }});

      syncSelectVisuals();
      syncQuickChips();
      updateTimeline();
    }}

    if (btnResetAllFilters) btnResetAllFilters.addEventListener('click', resetAllFilters);
    if (btnSidebarReset) btnSidebarReset.addEventListener('click', resetAllFilters);

    if (filterScopeSelect) {{
      filterScopeSelect.addEventListener('change', (e) => {{
        filterScope = e.target.value;
        syncQuickChips();
        updateTimeline();
      }});
    }}

    if (filterGovernmentSelect) {{
      filterGovernmentSelect.addEventListener('change', (e) => {{
        filterGovernment = e.target.value;
        syncQuickChips();
        updateTimeline();
      }});
    }}

    if (filterYearSelect) {{
      filterYearSelect.addEventListener('change', (e) => {{
        filterYear = e.target.value;
        updateTimeline();
      }});
    }}

    if (filterCostTierSelect) {{
      filterCostTierSelect.addEventListener('change', (e) => {{
        filterCostTier = e.target.value;
        syncQuickChips();
        updateTimeline();
      }});
    }}

    if (filterDestinationSelect) {{
      filterDestinationSelect.addEventListener('change', (e) => {{
        filterDestination = e.target.value;
        updateTimeline();
      }});
    }}



    // Quick chips en sidebar
    document.querySelectorAll('.quick-chip').forEach(chip => {{
      chip.addEventListener('click', (e) => {{
        const type = e.currentTarget.dataset.filterType;
        const val = e.currentTarget.dataset.value;

        if (type === 'scope') {{
          filterScope = (filterScope === val && val !== 'Todas') ? 'Todas' : val;
        }} else if (type === 'cabin') {{
          filterCabin = (filterCabin === val) ? 'Todas' : val;
          filterBusinessOnly = (filterCabin === 'Business');
          if (btnToggleBusiness) btnToggleBusiness.classList.toggle('active', filterBusinessOnly);
        }} else if (type === 'costTier') {{
          filterCostTier = (filterCostTier === val) ? 'Todas' : val;
        }} else if (type === 'government') {{
          filterGovernment = (filterGovernment === val) ? 'Todas' : val;
        }}

        syncSelectVisuals();
        syncQuickChips();
        updateTimeline();
      }});
    }});

    /* =====================================================================
       PROYECCIÓN CARTOGRÁFICA Y CÁLCULOS 2.5D
       ===================================================================== */
    function resizeCanvas() {{
      const dpr = window.devicePixelRatio || 1;
      const rect = mapContainer.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      drawScrubberSparkline();
    }}
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function geoToCanvas(lon, lat) {{
      const dpr = window.devicePixelRatio || 1;
      const w = canvas.width / dpr;
      const h = canvas.height / dpr;

      const normX = (lon + 180) / 360;
      const normY = (90 - lat) / 180;

      const baseScale = Math.min(w / 1000, h / 600);
      const effectiveScale = baseScale * zoomLevel;

      const centerX = w / 2 + panOffset.x * effectiveScale;
      const centerY = h / 2 + panOffset.y * effectiveScale;

      const x = centerX + (normX - 0.5) * 1000 * effectiveScale;
      const y = centerY + (normY - 0.5) * 600 * effectiveScale;

      return {{ x: x * dpr, y: y * dpr }};
    }}

    function getArcPoint(p1, p2, t) {{
      const midX = (p1.x + p2.x) / 2;
      const midY = (p1.y + p2.y) / 2;

      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      const dist = Math.hypot(dx, dy);

      const lift = Math.min(dist * 0.35, 140 * (window.devicePixelRatio || 1));
      const nx = -dy / (dist || 1);
      const ctrlX = midX + nx * lift * 0.4;
      const ctrlY = midY - lift;

      const omt = 1 - t;
      const x = omt * omt * p1.x + 2 * omt * t * ctrlX + t * t * p2.x;
      const y = omt * omt * p1.y + 2 * omt * t * ctrlY + t * t * p2.y;

      return {{ x, y, ctrlX, ctrlY }};
    }}

        /* =====================================================================
       MOTOR DE RENDER (CANVAS 2D A 60 FPS) — MAPA NITIDO Y CIVICO
       ===================================================================== */
    let lastTimestamp = performance.now();

    function drawMapPill(pCtx, x, y, text, accentColor, dpr, centered = false) {{
      pCtx.save();
      pCtx.font = `bold ${{Math.round(11 * dpr)}}px ${{FONT_SANS}}`;
      const metrics = pCtx.measureText(text);
      const textW = metrics.width;
      const padX = 8 * dpr;
      const padY = 4 * dpr;
      const pillW = textW + padX * 2;
      const pillH = 22 * dpr;

      const drawX = centered ? x - pillW / 2 : x;
      const drawY = y - pillH / 2;

      pCtx.fillStyle = 'rgba(6, 12, 20, 0.92)';
      pCtx.strokeStyle = accentColor;
      pCtx.lineWidth = 1.2 * dpr;
      pCtx.shadowColor = 'rgba(0, 0, 0, 0.6)';
      pCtx.shadowBlur = 6 * dpr;

      if (typeof pCtx.roundRect === 'function') {{
        pCtx.beginPath();
        pCtx.roundRect(drawX, drawY, pillW, pillH, 5 * dpr);
        pCtx.fill();
        pCtx.stroke();
      }} else {{
        pCtx.fillRect(drawX, drawY, pillW, pillH);
        pCtx.strokeRect(drawX, drawY, pillW, pillH);
      }}

      pCtx.shadowBlur = 0;
      pCtx.fillStyle = '#f0f6fc';
      pCtx.textAlign = 'left';
      pCtx.textBaseline = 'middle';
      pCtx.fillText(text, drawX + padX, drawY + pillH / 2);
      pCtx.restore();
    }}

    function renderMap(timestamp) {{
      const dt = Math.min((timestamp - lastTimestamp) / 1000, 0.1);
      lastTimestamp = timestamp;

      const w = canvas.width;
      const h = canvas.height;
      const dpr = window.devicePixelRatio || 1;

      // 1. Fondo oceánico profundo con gradiente radial
      const grad = ctx.createRadialGradient(w/2, h/2, 40 * dpr, w/2, h/2, Math.max(w, h)/1.1);
      grad.addColorStop(0, '#0a1626');
      grad.addColorStop(1, '#04080e');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // 2. Graticule elegante (Meridianos y Paralelos tenues)
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.05)';
      ctx.lineWidth = 1 * dpr;

      for (let lon = -180; lon <= 180; lon += 30) {{
        ctx.beginPath();
        const pTop = geoToCanvas(lon, 80);
        const pBot = geoToCanvas(lon, -80);
        ctx.moveTo(pTop.x, pTop.y);
        ctx.lineTo(pBot.x, pBot.y);
        ctx.stroke();
      }}

      for (let lat = -60; lat <= 60; lat += 30) {{
        ctx.beginPath();
        const pLeft = geoToCanvas(-180, lat);
        const pRight = geoToCanvas(180, lat);
        ctx.moveTo(pLeft.x, pLeft.y);
        ctx.lineTo(pRight.x, pRight.y);
        ctx.stroke();
      }}

      // Línea del Ecuador destacada
      ctx.strokeStyle = 'rgba(0, 212, 255, 0.12)';
      ctx.beginPath();
      const eqLeft = geoToCanvas(-180, 0);
      const eqRight = geoToCanvas(180, 0);
      ctx.moveTo(eqLeft.x, eqLeft.y);
      ctx.lineTo(eqRight.x, eqRight.y);
      ctx.stroke();

      // 3. Continentes Vectoriales de Alto Contraste
      ctx.fillStyle = '#0f2236';
      ctx.strokeStyle = '#1e4468';
      ctx.lineWidth = 1.3 * dpr;
      ctx.shadowColor = 'rgba(0, 212, 255, 0.08)';
      ctx.shadowBlur = 10 * dpr;

      CONTINENTS_GEO.forEach(poly => {{
        if (poly.length === 0) return;
        ctx.beginPath();
        const start = geoToCanvas(poly[0][0], poly[0][1]);
        ctx.moveTo(start.x, start.y);
        for (let i = 1; i < poly.length; i++) {{
          const pt = geoToCanvas(poly[i][0], poly[i][1]);
          ctx.lineTo(pt.x, pt.y);
        }}
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }});
      ctx.shadowBlur = 0;

      const originCanvas = geoToCanvas(SCL.lon, SCL.lat);

      // 4. Red Aérea Pasiva (Rutas globales agrupadas por destino, sin saturar)
      const uniqueDestinations = new Map();
      FLIGHTS.forEach(f => {{
        if (!flightMatchesAllFilters(f, false)) return;
        
        const code = f.dest.code;
        if (!uniqueDestinations.has(code)) {{
          uniqueDestinations.set(code, {{ dest: f.dest, count: 0, hasBusiness: false }});
        }}
        const entry = uniqueDestinations.get(code);
        entry.count++;
        if (f.cabin === 'Business') entry.hasBusiness = true;
      }});

      uniqueDestinations.forEach((routeInfo, code) => {{
        // Si es el destino seleccionado, se dibuja como Hero Route más adelante
        if (selectedFlight && selectedFlight.dest.code === code) return;

        const destPt = geoToCanvas(routeInfo.dest.lon, routeInfo.dest.lat);
        const arcPt = getArcPoint(originCanvas, destPt, 0.5);

        // Trazo tenue de red
        ctx.save();
        ctx.beginPath();
        ctx.setLineDash([3 * dpr, 4 * dpr]);
        ctx.moveTo(originCanvas.x, originCanvas.y);
        ctx.quadraticCurveTo(arcPt.ctrlX, arcPt.ctrlY, destPt.x, destPt.y);
        ctx.strokeStyle = routeInfo.hasBusiness ? 'rgba(255, 77, 90, 0.22)' : 'rgba(0, 229, 163, 0.18)';
        ctx.lineWidth = 1.0 * dpr;
        ctx.stroke();
        ctx.restore();

        // Nodo de destino tenue
        ctx.fillStyle = routeInfo.hasBusiness ? 'rgba(255, 77, 90, 0.7)' : 'rgba(0, 229, 163, 0.65)';
        ctx.beginPath();
        ctx.arc(destPt.x, destPt.y, 3.2 * dpr, 0, Math.PI * 2);
        ctx.fill();

        // Etiqueta tenue de ciudad
        if (zoomLevel >= 0.9) {{
          ctx.font = `600 ${{Math.round(9 * dpr)}}px ${{FONT_SANS}}`;
          ctx.fillStyle = 'rgba(139, 155, 176, 0.65)';
          ctx.textAlign = 'left';
          ctx.fillText(routeInfo.dest.city, destPt.x + 5 * dpr, destPt.y + 3 * dpr);
        }}
      }});

      // 5. HERO ROUTE: Vuelo Activo y Seleccionado (Foco Absoluto)
      if (selectedFlight) {{
        const isBusiness = selectedFlight.cabin === 'Business';
        const heroColor = isBusiness ? '#ff4d5a' : '#00e5a3';
        const heroGlow = isBusiness ? 'rgba(255, 77, 90, 0.35)' : 'rgba(0, 229, 163, 0.35)';

        const destCanvas = geoToCanvas(selectedFlight.dest.lon, selectedFlight.dest.lat);
        const arc = getArcPoint(originCanvas, destCanvas, 0.5);

        // Halo de resplandor exterior
        ctx.beginPath();
        ctx.moveTo(originCanvas.x, originCanvas.y);
        ctx.quadraticCurveTo(arc.ctrlX, arc.ctrlY, destCanvas.x, destCanvas.y);
        ctx.strokeStyle = heroGlow;
        ctx.lineWidth = 8 * dpr;
        ctx.stroke();

        // Línea principal luminosa
        ctx.beginPath();
        ctx.moveTo(originCanvas.x, originCanvas.y);
        ctx.quadraticCurveTo(arc.ctrlX, arc.ctrlY, destCanvas.x, destCanvas.y);
        ctx.strokeStyle = heroColor;
        ctx.lineWidth = 3.2 * dpr;
        ctx.shadowColor = heroColor;
        ctx.shadowBlur = 14 * dpr;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Avión comercial animado en la ruta activa
        const speed = 0.12;
        selectedFlight.t = ((selectedFlight.t || 0) + speed * dt) % 1.0;
        const planePos = getArcPoint(originCanvas, destCanvas, selectedFlight.t);
        const nextPos = getArcPoint(originCanvas, destCanvas, Math.min(selectedFlight.t + 0.015, 1.0));
        const angle = Math.atan2(nextPos.y - planePos.y, nextPos.x - planePos.x);

        ctx.save();
        ctx.translate(planePos.x, planePos.y);
        ctx.rotate(angle);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = heroColor;
        ctx.shadowBlur = 14 * dpr;

        // Silueta elegante de avión a reacción
        const s = 11 * dpr;
        ctx.beginPath();
        ctx.moveTo(s * 1.4, 0);
        ctx.lineTo(-s * 0.7, -s * 0.85);
        ctx.lineTo(-s * 0.35, 0);
        ctx.lineTo(-s * 0.7, s * 0.85);
        ctx.closePath();
        ctx.fill();
        ctx.restore();

        // Pulso radar en Santiago (SCL)
        const pulseCycle = (timestamp % 2000) / 2000;
        const r1 = pulseCycle * 24 * dpr;
        ctx.strokeStyle = `rgba(0, 212, 255, ${{1 - pulseCycle}})`;
        ctx.lineWidth = 1.5 * dpr;
        ctx.beginPath();
        ctx.arc(originCanvas.x, originCanvas.y, r1, 0, Math.PI * 2);
        ctx.stroke();

        // Nodo Santiago SCL
        ctx.fillStyle = '#00d4ff';
        ctx.beginPath();
        ctx.arc(originCanvas.x, originCanvas.y, 5 * dpr, 0, Math.PI * 2);
        ctx.fill();

        // Pulso radar en Destino
        const r2 = pulseCycle * 28 * dpr;
        ctx.strokeStyle = isBusiness ? `rgba(255, 77, 90, ${{1 - pulseCycle}})` : `rgba(0, 229, 163, ${{1 - pulseCycle}})`;
        ctx.beginPath();
        ctx.arc(destCanvas.x, destCanvas.y, r2, 0, Math.PI * 2);
        ctx.stroke();

        // Nodo Destino
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(destCanvas.x, destCanvas.y, 6.5 * dpr, 0, Math.PI * 2);
        ctx.fill();

        // 6. Badges tipográficos legibles en el mapa
        // Badge Origen SCL
        drawMapPill(ctx, originCanvas.x - 12 * dpr, originCanvas.y + 18 * dpr, '🛫 SCL • Santiago', '#00d4ff', dpr);

        // Badge Destino
        const costMillions = (selectedFlight.cost / 1e6).toFixed(1).replace('.', ',');
        const destLabel = `🛬 ${{selectedFlight.dest.code}} • ${{selectedFlight.dest.city}} ($${{costMillions}}M CLP)`;
        drawMapPill(ctx, destCanvas.x + 10 * dpr, destCanvas.y - 14 * dpr, destLabel, heroColor, dpr);

        // Badge en la cumbre del arco: distancia en km
        const midArc = getArcPoint(originCanvas, destCanvas, 0.5);
        const distKm = Math.round(calculateDistanceKm(SCL.lat, SCL.lon, selectedFlight.dest.lat, selectedFlight.dest.lon));
        const flightHours = Math.round(distKm / 820);
        const distLabel = `✈️ ~${{distKm.toLocaleString('es-CL')}} km • ~${{flightHours}}h`;
        drawMapPill(ctx, midArc.x, midArc.y - 14 * dpr, distLabel, '#f59e0b', dpr, true);
      }}

      requestAnimationFrame(renderMap);
    }}
    requestAnimationFrame(renderMap);

    /* =====================================================================
       NAVEGACIÓN UNIVERSAL DE MAPA (ZOOM Y PAN)
       ===================================================================== */
    btnZoomIn.addEventListener('click', () => {{
      zoomLevel = Math.min(3.5, zoomLevel * 1.25);
    }});

    btnZoomOut.addEventListener('click', () => {{
      zoomLevel = Math.max(0.8, zoomLevel * 0.8);
    }});

    /* =====================================================================
       ENFOQUE AUTOMATICO Y NAVEGACION DE CAMARA
       ===================================================================== */
    function centerOnFlight(flight) {{
      if (!flight) return;
      const spanLon = Math.abs(SCL.lon - flight.dest.lon);
      const spanLat = Math.abs(SCL.lat - flight.dest.lat);

      if (spanLon > 130 || spanLat > 75) {{
        zoomLevel = 1.05;
      }} else if (spanLon > 60 || spanLat > 40) {{
        zoomLevel = 1.25;
      }} else if (spanLon > 25 || spanLat > 20) {{
        zoomLevel = 1.6;
      }} else {{
        zoomLevel = 2.1;
      }}

      const midLon = (SCL.lon + flight.dest.lon) / 2;
      const midLat = (SCL.lat + flight.dest.lat) / 2 + (spanLat > 30 ? 6 : 0);
      const normX = (midLon + 180) / 360;
      const normY = (90 - midLat) / 180;

      panOffset.x = (0.5 - normX) * 1000;
      panOffset.y = (0.5 - normY) * 600;
    }}

    const btnFocusFlight = document.getElementById('btnFocusFlight');
    if (btnFocusFlight) {{
      btnFocusFlight.addEventListener('click', () => {{
        if (selectedFlight) centerOnFlight(selectedFlight);
      }});
    }}

    btnResetView.addEventListener('click', () => {{
      zoomLevel = 1.0;
      panOffset = {{ x: 0, y: 0 }};
    }});

    canvas.addEventListener('wheel', (e) => {{
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.15 : 0.87;
      zoomLevel = Math.max(0.8, Math.min(3.5, zoomLevel * factor));
    }}, {{ passive: false }});

    canvas.addEventListener('pointerdown', (e) => {{
      isDragging = true;
      hasDragged = false;
      startPointer = {{ x: e.clientX, y: e.clientY }};
      canvas.setPointerCapture(e.pointerId);
    }});

    canvas.addEventListener('pointermove', (e) => {{
      if (isDragging) {{
        const dx = e.clientX - startPointer.x;
        const dy = e.clientY - startPointer.y;
        if (Math.hypot(dx, dy) > 3) hasDragged = true;
        panOffset.x += dx / zoomLevel;
        panOffset.y += dy / zoomLevel;
        startPointer = {{ x: e.clientX, y: e.clientY }};
      }} else {{
        handlePointerHover(e);
      }}
    }});

    canvas.addEventListener('pointerup', (e) => {{
      if (isDragging) {{
        isDragging = false;
        try {{ canvas.releasePointerCapture(e.pointerId); }} catch (err) {{}}
        if (!hasDragged) handleCanvasClick(e);
      }}
    }});

    canvas.addEventListener('pointercancel', () => {{ isDragging = false; }});
    canvas.addEventListener('pointerleave', () => {{ mapTooltip.style.display = 'none'; }});

    function handlePointerHover(e) {{
      const rect = canvas.getBoundingClientRect();
      const clientX = e.clientX - rect.left;
      const clientY = e.clientY - rect.top;
      const dpr = window.devicePixelRatio || 1;

      let hovered = null;
      for (const flight of FLIGHTS) {{
        if (selectedProvider !== 'Todas' && flight.provider !== selectedProvider) continue;
        if (filterBusinessOnly && flight.cabin !== 'Business') continue;
        if (selectedEntityGroup !== 'Todas' && !matchesEntityGroup(flight.entity, selectedEntityGroup)) continue;

        const pt = geoToCanvas(flight.dest.lon, flight.dest.lat);
        const dist = Math.hypot((pt.x / dpr) - clientX, (pt.y / dpr) - clientY);
        if (dist < 14) {{
          hovered = flight;
          break;
        }}
      }}

      if (hovered) {{
        const km = calculateDistanceKm(SCL.lat, SCL.lon, hovered.dest.lat, hovered.dest.lon);
        const estTime = estimateFlightTime(km);
        mapTooltip.innerHTML = `
          <strong>✈️ ${{hovered.dest.city}} (${{hovered.dest.code}})</strong>
          <div class="tooltip-meta">${{hovered.dest.country}} • ${{km.toLocaleString('es-CL')}} km (≈${{estTime}})</div>
          <div class="tooltip-meta" style="color: #38bdf8; font-weight: 700; margin-top: 2px;">$${{hovered.cost.toLocaleString('es-CL')}} CLP • ${{hovered.cabin}}</div>
        `;
        mapTooltip.style.left = `${{clientX}}px`;
        mapTooltip.style.top = `${{clientY}}px`;
        mapTooltip.style.display = 'block';
      }} else {{
        mapTooltip.style.display = 'none';
      }}
    }}

    function handleCanvasClick(e) {{
      const rect = canvas.getBoundingClientRect();
      const clientX = e.clientX - rect.left;
      const clientY = e.clientY - rect.top;
      const dpr = window.devicePixelRatio || 1;

      let nearestFlight = null;
      let minDist = 22;

      FLIGHTS.forEach(flight => {{
        if (selectedProvider !== 'Todas' && flight.provider !== selectedProvider) return;
        if (filterBusinessOnly && flight.cabin !== 'Business') return;
        if (selectedEntityGroup !== 'Todas' && !matchesEntityGroup(flight.entity, selectedEntityGroup)) return;

        const pt = geoToCanvas(flight.dest.lon, flight.dest.lat);
        const d = Math.hypot((pt.x / dpr) - clientX, (pt.y / dpr) - clientY);
        if (d < minDist) {{
          minDist = d;
          nearestFlight = flight;
        }}
      }});

      if (nearestFlight) {{
        selectFlight(nearestFlight);
        const cardEl = document.getElementById(`flight-item-${{nearestFlight.id}}`);
        if (cardEl && typeof cardEl.scrollIntoView === 'function') {{
          cardEl.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}
      }}
    }}

    /* =====================================================================
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
    }}

    function handleHashNavigation() {{
      const hash = window.location.hash.replace('#', '').trim();
      if (!hash) return;
      const target = FLIGHTS.find(f => f.id === hash || f.oc === hash);
      if (target) {{
        selectFlight(target);
        const card = document.getElementById(`flight-item-${{target.id}}`);
        if (card && typeof card.scrollIntoView === 'function') card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}
    }}
    window.addEventListener('hashchange', handleHashNavigation);

    /* =====================================================================
       NAVEGACIÓN MÓVIL POR PESTAÑAS (TABS RESPONSIVE)
       ===================================================================== */
    if (mobileViewTabs) {{
      mobileViewTabs.addEventListener('click', (e) => {{
        const btn = e.target.closest('.mobile-tab-btn');
        if (!btn) return;
        const view = btn.dataset.view;

        document.querySelectorAll('.mobile-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        if (view === 'map') {{
          sidebarColumn.classList.add('mobile-hidden');
          mapColumn.classList.remove('mobile-hidden');
          dossierColumn.classList.add('mobile-hidden');
          resizeCanvas();
        }} else if (view === 'list') {{
          sidebarColumn.classList.remove('mobile-hidden');
          mapColumn.classList.add('mobile-hidden');
          dossierColumn.classList.add('mobile-hidden');
        }} else if (view === 'dossier') {{
          sidebarColumn.classList.add('mobile-hidden');
          mapColumn.classList.add('mobile-hidden');
          dossierColumn.classList.remove('mobile-hidden');
        }}
      }});
    }}

    /* =====================================================================
       MODAL DE FUENTES Y METODOLOGÍA
       ===================================================================== */
    btnOpenHelp.addEventListener('click', () => helpModal.classList.add('open'));
    btnCloseHelp.addEventListener('click', () => helpModal.classList.remove('open'));
    btnModalUnderstood.addEventListener('click', () => helpModal.classList.remove('open'));
    helpModal.addEventListener('click', (e) => {{
      if (e.target === helpModal) helpModal.classList.remove('open');
    }});

    /* =====================================================================
       INICIALIZACIÓN DEL SISTEMA
       ===================================================================== */
    function init() {{
      const sorted = getSortedFlights();
      selectedFlight = sorted[0] || FLIGHTS[FLIGHTS.length - 1];
      renderFlightList();
      selectFlight(selectedFlight);
      updateTimeline();
      handleHashNavigation();
      if (typeof centerOnFlight === 'function') centerOnFlight(selectedFlight);
    }}
    init();
  </script>
</body>
</html>
'''
    out_index = os.path.join(repo_dir, "index.html")
    out_docs = os.path.join(repo_dir, "docs", "index.html")
    
    with open(out_index, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    with open(out_docs, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"[OK] index.html y docs/index.html generados exitosamente ({len(html_content)} bytes).")

if __name__ == "__main__":
    generate_index_html()
