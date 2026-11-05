#!/usr/bin/env python3
"""
Sincronizador Oficial de Pasajes Aéreos y Comitivas desde la API de Mercado Público (ChileCompra).
Plataforma: VuelosPúblicos (vuelospublicos.evegat.cl) - P167.

Flujo de 2 fases:
1. Consulta diaria por fecha (DDMMAAAA) para obtener listado de órdenes de compra del Estado.
2. Consulta detallada por código OC para las órdenes de transporte/pasajes aéreos no registradas.
"""

import os
import sys
import json
import re
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

DEFAULT_TICKET = "2CB3E6C4-789E-495F-898B-90FF6748149C"

AIRPORT_DB = {
    # Internacionales
    "GINEBRA": {"code": "GVA", "city": "Ginebra", "country": "Suiza", "lon": 6.109, "lat": 46.238, "airport": "Aeropuerto de Ginebra (GVA)"},
    "GENEVA": {"code": "GVA", "city": "Ginebra", "country": "Suiza", "lon": 6.109, "lat": 46.238, "airport": "Aeropuerto de Ginebra (GVA)"},
    "MADRID": {"code": "MAD", "city": "Madrid", "country": "España", "lon": -3.567, "lat": 40.483, "airport": "Adolfo Suárez Madrid-Barajas (MAD)"},
    "BARCELONA": {"code": "BCN", "city": "Barcelona", "country": "España", "lon": 2.078, "lat": 41.297, "airport": "Josep Tarradellas Barcelona-El Prat (BCN)"},
    "ESPANA": {"code": "MAD", "city": "Madrid", "country": "España", "lon": -3.567, "lat": 40.483, "airport": "Adolfo Suárez Madrid-Barajas (MAD)"},
    "ESPAÑA": {"code": "MAD", "city": "Madrid", "country": "España", "lon": -3.567, "lat": 40.483, "airport": "Adolfo Suárez Madrid-Barajas (MAD)"},
    "WASHINGTON": {"code": "IAD", "city": "Washington D.C.", "country": "EE.UU.", "lon": -77.455, "lat": 38.953, "airport": "Dulles International (IAD)"},
    "NUEVA YORK": {"code": "JFK", "city": "Nueva York", "country": "EE.UU.", "lon": -73.778, "lat": 40.639, "airport": "John F. Kennedy (JFK)"},
    "NEW YORK": {"code": "JFK", "city": "Nueva York", "country": "EE.UU.", "lon": -73.778, "lat": 40.639, "airport": "John F. Kennedy (JFK)"},
    "PARIS": {"code": "CDG", "city": "París", "country": "Francia", "lon": 2.550, "lat": 49.009, "airport": "Charles de Gaulle (CDG)"},
    "FRANCIA": {"code": "CDG", "city": "París", "country": "Francia", "lon": 2.550, "lat": 49.009, "airport": "Charles de Gaulle (CDG)"},
    "LONDRES": {"code": "LHR", "city": "Londres", "country": "Reino Unido", "lon": -0.454, "lat": 51.470, "airport": "Heathrow (LHR)"},
    "TOKIO": {"code": "NRT", "city": "Tokio", "country": "Japón", "lon": 140.392, "lat": 35.772, "airport": "Narita International (NRT)"},
    "TOKYO": {"code": "NRT", "city": "Tokio", "country": "Japón", "lon": 140.392, "lat": 35.772, "airport": "Narita International (NRT)"},
    "OSAKA": {"code": "KIX", "city": "Osaka", "country": "Japón", "lon": 135.233, "lat": 34.434, "airport": "Kansai International (KIX)"},
    "PEKIN": {"code": "PEK", "city": "Pekín", "country": "China", "lon": 116.584, "lat": 40.079, "airport": "Beijing Capital (PEK)"},
    "BEIJING": {"code": "PEK", "city": "Pekín", "country": "China", "lon": 116.584, "lat": 40.079, "airport": "Beijing Capital (PEK)"},
    "FUZHOU": {"code": "FOC", "city": "Fuzhou", "country": "China", "lon": 119.663, "lat": 25.935, "airport": "Fuzhou Changle (FOC)"},
    "PANAMA": {"code": "PTY", "city": "Ciudad de Panamá", "country": "Panamá", "lon": -79.383, "lat": 9.071, "airport": "Tocumen International (PTY)"},
    "SIDNEY": {"code": "SYD", "city": "Sídney", "country": "Australia", "lon": 151.177, "lat": -33.946, "airport": "Kingsford Smith (SYD)"},
    "SYDNEY": {"code": "SYD", "city": "Sídney", "country": "Australia", "lon": 151.177, "lat": -33.946, "airport": "Kingsford Smith (SYD)"},
    "BUENOS AIRES": {"code": "EZE", "city": "Buenos Aires", "country": "Argentina", "lon": -58.535, "lat": -34.822, "airport": "Ezeiza Ministro Pistarini (EZE)"},
    "LIMA": {"code": "LIM", "city": "Lima", "country": "Perú", "lon": -77.114, "lat": -12.021, "airport": "Jorge Chávez (LIM)"},
    "BOGOTA": {"code": "BOG", "city": "Bogotá", "country": "Colombia", "lon": -74.146, "lat": 4.701, "airport": "El Dorado (BOG)"},
    "MEXICO": {"code": "MEX", "city": "Ciudad de México", "country": "México", "lon": -99.072, "lat": 19.436, "airport": "Benito Juárez (MEX)"},
    "ROMA": {"code": "FCO", "city": "Roma", "country": "Italia", "lon": 12.238, "lat": 41.800, "airport": "Leonardo da Vinci Fiumicino (FCO)"},
    "ITALIA": {"code": "FCO", "city": "Roma", "country": "Italia", "lon": 12.238, "lat": 41.800, "airport": "Leonardo da Vinci Fiumicino (FCO)"},
    "BERLIN": {"code": "BER", "city": "Berlín", "country": "Alemania", "lon": 13.503, "lat": 52.366, "airport": "Berlin Brandenburg (BER)"},
    "ALEMANIA": {"code": "FRA", "city": "Fráncfort", "country": "Alemania", "lon": 8.570, "lat": 50.037, "airport": "Frankfurt Airport (FRA)"},
    "BRUSELAS": {"code": "BRU", "city": "Bruselas", "country": "Bélgica", "lon": 4.484, "lat": 50.901, "airport": "Brussels Airport (BRU)"},
    "MIAMI": {"code": "MIA", "city": "Miami", "country": "EE.UU.", "lon": -80.287, "lat": 25.795, "airport": "Miami International (MIA)"},
    "SAO PAULO": {"code": "GRU", "city": "São Paulo", "country": "Brasil", "lon": -46.473, "lat": -23.435, "airport": "Guarulhos (GRU)"},
    "SÃO PAULO": {"code": "GRU", "city": "São Paulo", "country": "Brasil", "lon": -46.473, "lat": -23.435, "airport": "Guarulhos (GRU)"},
    "RIO DE JANEIRO": {"code": "GIG", "city": "Río de Janeiro", "country": "Brasil", "lon": -43.250, "lat": -22.808, "airport": "Galeão (GIG)"},
    "BRASIL": {"code": "GRU", "city": "São Paulo", "country": "Brasil", "lon": -46.473, "lat": -23.435, "airport": "Guarulhos (GRU)"},
    "MONTEVIDEO": {"code": "MVD", "city": "Montevideo", "country": "Uruguay", "lon": -56.030, "lat": -34.838, "airport": "Carrasco (MVD)"},
    "ASUNCION": {"code": "ASU", "city": "Asunción", "country": "Paraguay", "lon": -57.519, "lat": -25.240, "airport": "Silvio Pettirossi (ASU)"},
    "ASUNCIÓN": {"code": "ASU", "city": "Asunción", "country": "Paraguay", "lon": -57.519, "lat": -25.240, "airport": "Silvio Pettirossi (ASU)"},
    "QUITO": {"code": "UIO", "city": "Quito", "country": "Ecuador", "lon": -78.357, "lat": -0.129, "airport": "Mariscal Sucre (UIO)"},
    "SAN JOSE": {"code": "SJO", "city": "San José", "country": "Costa Rica", "lon": -84.208, "lat": 9.993, "airport": "Juan Santamaría (SJO)"},
    "SAN JOSÉ": {"code": "SJO", "city": "San José", "country": "Costa Rica", "lon": -84.208, "lat": 9.993, "airport": "Juan Santamaría (SJO)"},
    "PUERTO NATALES": {"code": "PNT", "city": "Puerto Natales", "country": "Chile", "lon": -72.527, "lat": -51.679, "airport": "Teniente Gallardo (PNT)"},
    # Nacionales (Chile)
    "ISLA DE PASCUA": {"code": "IPC", "city": "Isla de Pascua", "country": "Chile", "lon": -109.421, "lat": -27.164, "airport": "Mataveri (IPC)"},
    "RAPA NUI": {"code": "IPC", "city": "Isla de Pascua", "country": "Chile", "lon": -109.421, "lat": -27.164, "airport": "Mataveri (IPC)"},
    "EASTER ISLAND": {"code": "IPC", "city": "Isla de Pascua", "country": "Chile", "lon": -109.421, "lat": -27.164, "airport": "Mataveri (IPC)"},
    "PUNTA ARENAS": {"code": "PUQ", "city": "Punta Arenas", "country": "Chile", "lon": -70.854, "lat": -53.002, "airport": "Pdte. Carlos Ibáñez del Campo (PUQ)"},
    "IQUIQUE": {"code": "IQQ", "city": "Iquique", "country": "Chile", "lon": -70.181, "lat": -20.535, "airport": "Diego Aracena (IQQ)"},
    "ANTOFAGASTA": {"code": "ANF", "city": "Antofagasta", "country": "Chile", "lon": -70.445, "lat": -23.444, "airport": "Andrés Sabella (ANF)"},
    "CALAMA": {"code": "CJC", "city": "Calama", "country": "Chile", "lon": -68.904, "lat": -22.498, "airport": "El Loa (CJC)"},
    "ARICA": {"code": "ARI", "city": "Arica", "country": "Chile", "lon": -70.338, "lat": -18.348, "airport": "Chacalluta (ARI)"},
    "COPIAPO": {"code": "CPO", "city": "Copiapó", "country": "Chile", "lon": -70.779, "lat": -27.261, "airport": "Desierto de Atacama (CPO)"},
    "COPIAPÓ": {"code": "CPO", "city": "Copiapó", "country": "Chile", "lon": -70.779, "lat": -27.261, "airport": "Desierto de Atacama (CPO)"},
    "LA SERENA": {"code": "LSC", "city": "La Serena", "country": "Chile", "lon": -71.200, "lat": -29.916, "airport": "La Florida (LSC)"},
    "CONCEPCION": {"code": "CCP", "city": "Concepción", "country": "Chile", "lon": -73.063, "lat": -36.772, "airport": "Carriel Sur (CCP)"},
    "CONCEPCIÓN": {"code": "CCP", "city": "Concepción", "country": "Chile", "lon": -73.063, "lat": -36.772, "airport": "Carriel Sur (CCP)"},
    "TEMUCO": {"code": "ZCO", "city": "Temuco", "country": "Chile", "lon": -72.770, "lat": -38.925, "airport": "La Araucanía (ZCO)"},
    "VALDIVIA": {"code": "ZAL", "city": "Valdivia", "country": "Chile", "lon": -73.086, "lat": -39.650, "airport": "Pichoy (ZAL)"},
    "OSORNO": {"code": "ZOS", "city": "Osorno", "country": "Chile", "lon": -73.060, "lat": -40.611, "airport": "Cañal Bajo (ZOS)"},
    "PUERTO MONTT": {"code": "PMC", "city": "Puerto Montt", "country": "Chile", "lon": -73.094, "lat": -41.439, "airport": "El Tepual (PMC)"},
    "CASTRO": {"code": "MHC", "city": "Castro", "country": "Chile", "lon": -73.714, "lat": -42.340, "airport": "Mocopulli (MHC)"},
    "CHILOE": {"code": "MHC", "city": "Castro", "country": "Chile", "lon": -73.714, "lat": -42.340, "airport": "Mocopulli (MHC)"},
    "CHILOÉ": {"code": "MHC", "city": "Castro", "country": "Chile", "lon": -73.714, "lat": -42.340, "airport": "Mocopulli (MHC)"},
    "BALMACEDA": {"code": "BBA", "city": "Balmaceda", "country": "Chile", "lon": -71.689, "lat": -45.916, "airport": "Balmaceda Aysén (BBA)"}
}

SCL = {
    "code": "SCL",
    "city": "Santiago",
    "country": "Chile",
    "airport": "Arturo Merino Benítez (SCL)",
    "lon": -70.7858,
    "lat": -33.393
}

def detect_destination(text):
    if not text or not isinstance(text, str):
        return None
    up = text.upper()
    for key, dest in AIRPORT_DB.items():
        if key in up:
            return dest
    return None

def detect_cabin(text):
    if not text or not isinstance(text, str):
        return "Turista"
    up = text.upper()
    if any(w in up for w in ["BUSINESS", "EJECUTIVA", "PRIMERA", "FIRST", "VIP"]):
        return "Business"
    return "Turista"

def clean_provider(prov_name):
    if not prov_name or not isinstance(prov_name, str):
        return "Otras Agencias"
    p = prov_name.upper()
    if "COCHA" in p: return "Cocha"
    if "TURAVION" in p: return "Turavion"
    if "LATAM" in p or "LAN" in p: return "LATAM"
    if "SKY" in p: return "Sky"
    if "CORTE INGLES" in p or "CORTE INGLÉS" in p: return "El Corte Inglés"
    return "Otras Agencias"

def extract_passenger_name(text):
    if not text or not isinstance(text, str):
        return "Comitiva Oficial"
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3]
    for line in lines:
        if any(w in line.upper() for w in ["PASAJE", "VALOR", "TARIFA", "CONTRATO", "ORDEN", "SUMINISTRO", "TELEFONO", "CORREO"]):
            continue
        if re.search(r'^[A-ZÁÉÍÓÚÑ\s\.\-]{5,35}$', line):
            return line.title()
    return "Comitiva Oficial"

def load_existing_flights(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def safe_replace(src, dst, max_retries=6, base_delay=0.2):
    """
    Reemplazo atómico tolerante a bloqueos transitorios de sincronización (OneDrive/antivirus) en Windows.
    """
    import shutil
    for attempt in range(max_retries):
        try:
            os.replace(src, dst)
            return
        except (PermissionError, OSError):
            time.sleep(base_delay * (attempt + 1))
    try:
        shutil.copyfile(src, dst)
        if os.path.exists(src):
            try:
                os.remove(src)
            except Exception:
                pass
    except Exception:
        pass

def save_flights_atomically(filepath, flights):
    tmp_path = filepath + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)
    safe_replace(tmp_path, filepath)

def query_api_with_retry(url, timeout=12, max_retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VuelosPublicos/1.0"})
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 2.5 * (attempt + 1)
                time.sleep(wait_time)
                continue
            return None
        except Exception:
            return None
    return None

def load_audited_cache(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_audited_cache(filepath, cache_data):
    tmp_path = filepath + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    safe_replace(tmp_path, filepath)

def fetch_day_candidates(date_str, ticket):
    url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha={date_str}&ticket={ticket}"
    data = query_api_with_retry(url, timeout=15)
    if not data or 'Listado' not in data:
        return []

    items = data.get('Listado', [])
    candidates = []
    keywords = ['PASAJE', 'VUELO', 'AEREO', 'AÉREO', 'COMITIVA', 'BOLETO', 'AEROLINEA', 'AEROLÍNEA', 'TICKET']
    for it in items:
        name = (it.get('Nombre') or '').upper()
        if any(w in name for w in keywords):
            candidates.append(it)
    return candidates

def fetch_oc_detail(code, ticket):
    url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?codigo={code}&ticket={ticket}"
    data = query_api_with_retry(url, timeout=12)
    if not data or 'Listado' not in data or not data['Listado']:
        return None
    return data['Listado'][0]

def process_raw_order(oc, next_id=1, default_date=None):
    """
    Procesa y normaliza una orden de compra (sea mock o de la API de Mercado Público).
    Retorna el diccionario estructurado del vuelo o None si no califica.
    """
    if not isinstance(oc, dict):
        return None

    code = oc.get('Codigo')
    if not code:
        return None

    name = oc.get('Nombre') or ''
    desc = oc.get('Descripcion') or oc.get('EspecificacionComprador') or ''
    
    items = []
    if isinstance(oc.get('Items'), dict):
        items = oc.get('Items', {}).get('Listado', [])
    items_text = " ".join([f"{item.get('Producto','')} {item.get('EspecificacionComprador','')}" for item in items])
    if oc.get('EspecificacionComprador'):
        items_text += f" {oc.get('EspecificacionComprador')}"
    
    full_text = f"{name} {desc} {items_text}"
    upper_full = full_text.upper()

    # Descartar pasajes terrestres si no indican transporte aéreo
    if any(w in upper_full for w in ["TERRESTRE", "BUS INTERURBANO", "PULLMAN", "TUR BUS", "TURBUS"]):
        if not any(w in upper_full for w in ["AEREO", "AÉREO", "VUELO", "AVION", "AVIÓN", "LATAM", "SKY", "JETSMART", "AEROLINEA", "AEROLÍNEA"]):
            return None

    dest = detect_destination(full_text)
    if not dest:
        return None

    monto = 0
    raw_monto = oc.get('Total') if oc.get('Total') is not None else oc.get('MontoTotalOC_PesosChilenos')
    try:
        monto = int(float(raw_monto or 0))
    except (ValueError, TypeError):
        monto = 0

    if monto < 300000:
        return None

    comprador = oc.get('Comprador')
    if isinstance(comprador, dict):
        organismo = comprador.get('NombreOrganismo') or "Servicio Público"
    else:
        organismo = oc.get('OrganismoPublico') or "Servicio Público"

    proveedor_raw = None
    proveedor_obj = oc.get('Proveedor')
    if isinstance(proveedor_obj, dict):
        proveedor_raw = proveedor_obj.get('Nombre')
    elif oc.get('NombreProveedor'):
        proveedor_raw = oc.get('NombreProveedor')
    proveedor = clean_provider(proveedor_raw)

    fechas = oc.get('Fechas')
    fecha_envio = None
    if isinstance(fechas, dict):
        fecha_envio = fechas.get('FechaEnvio')
    elif oc.get('FechaEnvio'):
        fecha_envio = oc.get('FechaEnvio')
    elif default_date:
        fecha_envio = f"{default_date[4:]}-{default_date[2:4]}-{default_date[:2]}"
    else:
        fecha_envio = datetime.now().strftime("%Y-%m-%d")

    date_str = str(fecha_envio)[:10]
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        year = dt.year
        month = dt.month
    except ValueError:
        year = datetime.now().year
        month = datetime.now().month

    month_index = (year - 2007) * 12 + (month - 1)
    cabin = detect_cabin(full_text)
    passenger = extract_passenger_name(desc or name)

    return {
        "id": f"FL-{next_id:04d}",
        "monthIndex": month_index,
        "year": year,
        "month": month,
        "date": date_str,
        "origin": SCL,
        "dest": dest,
        "entity": organismo.title(),
        "role": passenger,
        "cost": monto,
        "cabin": cabin,
        "cabinDesc": f"Clase {cabin} • Vía {proveedor}",
        "airline": "Vuelo Comercial",
        "oc": code,
        "provider": proveedor,
        "reason": (desc[:90] if len(desc) > 10 else name[:90]).strip(),
        "votes": {"approve": 45, "reject": 35}
    }

def sync_orders(ticket=None, fecha=None, fechas=None, data_path=None, commit=False, max_orders=0, mock_orders=None):
    if not ticket:
        ticket = os.environ.get("CHILECOMPRA_TICKET", DEFAULT_TICKET)

    is_default_target = (data_path is None)
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vuelos_2007_2026.json")
    docs_path = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "vuelos_2007_2026.json")
    audit_path = os.path.join(os.path.dirname(__file__), "..", "data", "audited_ocs.json")

    flights = load_existing_flights(data_path)
    existing_ocs = set(f.get('oc') for f in flights if f.get('oc'))
    audited_cache = load_audited_cache(audit_path) if is_default_target else {}
    next_id = len(flights) + 1

    print(f"[*] Catálogo local: {len(flights)} vuelos. OCs deduplicadas: {len(existing_ocs)}. En caché auditada: {len(audited_cache)}", flush=True)

    new_flights = []

    # Caso Mock / Tests Unitarios
    if mock_orders is not None:
        for oc in mock_orders:
            code = oc.get('Codigo')
            if not code or code in existing_ocs:
                continue
            flight_obj = process_raw_order(oc, next_id=next_id)
            if flight_obj:
                new_flights.append(flight_obj)
                existing_ocs.add(code)
                next_id += 1
        commit = True
        flights.extend(new_flights)
        save_flights_atomically(data_path, flights)
        if is_default_target and os.path.exists(os.path.dirname(docs_path)):
            save_flights_atomically(docs_path, flights)
        return len(new_flights)

    # Caso API en Vivo Mercado Público
    dates_to_process = []
    if fechas:
        dates_to_process = [d.strip() for d in fechas.split(',') if d.strip()]
    elif fecha:
        dates_to_process = [fecha.strip()]
    else:
        yesterday = datetime.now() - timedelta(days=1)
        dates_to_process = [yesterday.strftime("%d%m%Y")]

    for curr_fecha in dates_to_process:
        print(f"\n[*] Conectando a API de Mercado Público para fecha: {curr_fecha}...", flush=True)
        candidates = fetch_day_candidates(curr_fecha, ticket)
        print(f"[+] Órdenes candidatas de transporte/pasajes detectadas: {len(candidates)}", flush=True)

        unseen_candidates = [c for c in candidates if c.get('Codigo') and c.get('Codigo') not in existing_ocs and c.get('Codigo') not in audited_cache]
        print(f"[+] OCs nuevas pendientes de auditar: {len(unseen_candidates)} (de {len(candidates)} totales)", flush=True)

        target_list = unseen_candidates if (max_orders <= 0) else unseen_candidates[:max_orders]
        total_eval = len(target_list)

        for idx, it in enumerate(target_list, 1):
            code = it.get('Codigo')
            time.sleep(1.3) # Rate limit preventivo

            oc = fetch_oc_detail(code, ticket)
            if not oc:
                audited_cache[code] = {"status": "error_or_empty"}
                continue

            flight_obj = process_raw_order(oc, next_id=next_id, default_date=curr_fecha)
            if not flight_obj:
                audited_cache[code] = {"status": "discarded"}
                if commit and (idx % 20 == 0):
                    save_audited_cache(audit_path, audited_cache)
                continue

            new_flights.append(flight_obj)
            existing_ocs.add(code)
            audited_cache[code] = {"status": "flight", "id": flight_obj["id"]}
            next_id += 1

            print(f"  [{idx}/{total_eval}] GUARDADO: {flight_obj['id']} | {flight_obj['date']} | {flight_obj['dest']['city']} ({flight_obj['dest']['country']}) | ${flight_obj['cost']:,} CLP | {flight_obj['entity'][:28]} (Total catálogo: {len(flights) + len(new_flights)})", flush=True)

            if commit:
                # Guardado progresivo atómico inmediato
                save_flights_atomically(data_path, flights + new_flights)
                if is_default_target and os.path.exists(os.path.dirname(docs_path)):
                    save_flights_atomically(docs_path, flights + new_flights)
                save_audited_cache(audit_path, audited_cache)

        if commit and is_default_target:
            save_audited_cache(audit_path, audited_cache)

    print(f"\n[+] Total nuevos vuelos extraídos en esta sesión: {len(new_flights)}", flush=True)
    if not commit:
        print("[*] Modo simulación (dry-run). Usa --commit para persistir progresivamente en el catálogo.", flush=True)

    return len(new_flights)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extractor de pasajes oficiales desde Mercado Público")
    parser.add_argument("--fecha", help="Fecha individual a consultar en formato DDMMAAAA (ej. 04112026)")
    parser.add_argument("--fechas", help="Lista de fechas separadas por coma (ej. 04112026,03112026)")
    parser.add_argument("--ticket", help="Ticket de API Mercado Público")
    parser.add_argument("--data", help="Ruta a vuelos_2007_2026.json")
    parser.add_argument("--commit", action="store_true", help="Persistir progresivamente los nuevos vuelos")
    parser.add_argument("--max", type=int, default=0, help="Máximo de órdenes a detallar por fecha (0 = todas)")
    args = parser.parse_args()

    sync_orders(ticket=args.ticket, fecha=args.fecha, fechas=args.fechas, data_path=args.data, commit=args.commit, max_orders=args.max)
