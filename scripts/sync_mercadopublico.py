import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta

AIRPORT_DB = {
    "GINEBRA": {"code": "GVA", "city": "Ginebra", "country": "Suiza", "lon": 6.109, "lat": 46.238, "airport": "Aeropuerto de Ginebra (GVA)"},
    "GENEVA": {"code": "GVA", "city": "Ginebra", "country": "Suiza", "lon": 6.109, "lat": 46.238, "airport": "Aeropuerto de Ginebra (GVA)"},
    "MADRID": {"code": "MAD", "city": "Madrid", "country": "España", "lon": -3.567, "lat": 40.483, "airport": "Adolfo Suárez Madrid-Barajas (MAD)"},
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
    "PEKIN": {"code": "PEK", "city": "Pekín", "country": "China", "lon": 116.584, "lat": 40.079, "airport": "Beijing Capital (PEK)"},
    "BEIJING": {"code": "PEK", "city": "Pekín", "country": "China", "lon": 116.584, "lat": 40.079, "airport": "Beijing Capital (PEK)"},
    "SIDNEY": {"code": "SYD", "city": "Sídney", "country": "Australia", "lon": 151.177, "lat": -33.946, "airport": "Kingsford Smith (SYD)"},
    "SYDNEY": {"code": "SYD", "city": "Sídney", "country": "Australia", "lon": 151.177, "lat": -33.946, "airport": "Kingsford Smith (SYD)"},
    "BUENOS AIRES": {"code": "EZE", "city": "Buenos Aires", "country": "Argentina", "lon": -58.535, "lat": -34.822, "airport": "Ezeiza Ministro Pistarini (EZE)"},
    "LIMA": {"code": "LIM", "city": "Lima", "country": "Perú", "lon": -77.114, "lat": -12.021, "airport": "Jorge Chávez (LIM)"},
    "BOGOTA": {"code": "BOG", "city": "Bogotá", "country": "Colombia", "lon": -74.146, "lat": 4.701, "airport": "El Dorado (BOG)"},
    "MEXICO": {"code": "MEX", "city": "Ciudad de México", "country": "México", "lon": -99.072, "lat": 19.436, "airport": "Benito Juárez (MEX)"},
    "SAN ANTONIO": {"code": "SAT", "city": "San Antonio TX", "country": "EE.UU.", "lon": -98.469, "lat": 29.533, "airport": "San Antonio International (SAT)"},
    "TAMPA": {"code": "TPA", "city": "Tampa FL", "country": "EE.UU.", "lon": -82.533, "lat": 27.975, "airport": "Tampa International (TPA)"},
    "MIAMI": {"code": "MIA", "city": "Miami FL", "country": "EE.UU.", "lon": -80.287, "lat": 25.795, "airport": "Miami International (MIA)"},
    "BERLIN": {"code": "BER", "city": "Berlín", "country": "Alemania", "lon": 13.503, "lat": 52.366, "airport": "Berlin Brandenburg (BER)"},
    "ALEMANIA": {"code": "FRA", "city": "Fráncfort", "country": "Alemania", "lon": 8.570, "lat": 50.037, "airport": "Frankfurt Airport (FRA)"},
    "BRUSELAS": {"code": "BRU", "city": "Bruselas", "country": "Bélgica", "lon": 4.484, "lat": 50.901, "airport": "Brussels Airport (BRU)"},
    "ROMA": {"code": "FCO", "city": "Roma", "country": "Italia", "lon": 12.238, "lat": 41.800, "airport": "Leonardo da Vinci Fiumicino (FCO)"},
    "ITALIA": {"code": "FCO", "city": "Roma", "country": "Italia", "lon": 12.238, "lat": 41.800, "airport": "Leonardo da Vinci Fiumicino (FCO)"},
    "PUNTA ARENAS": {"code": "PUQ", "city": "Punta Arenas", "country": "Chile", "lon": -70.854, "lat": -53.002, "airport": "Pdte. Carlos Ibáñez del Campo (PUQ)"},
    "IQUIQUE": {"code": "IQQ", "city": "Iquique", "country": "Chile", "lon": -70.181, "lat": -20.535, "airport": "Diego Aracena (IQQ)"},
    "ANTOFAGASTA": {"code": "ANF", "city": "Antofagasta", "country": "Chile", "lon": -70.445, "lat": -23.444, "airport": "Andrés Sabella (ANF)"},
    "CONCEPCION": {"code": "CCP", "city": "Concepción", "country": "Chile", "lon": -73.063, "lat": -36.772, "airport": "Carriel Sur (CCP)"},
    "ISLA DE PASCUA": {"code": "IPC", "city": "Isla de Pascua", "country": "Chile", "lon": -109.421, "lat": -27.164, "airport": "Mataveri (IPC)"},
    "EASTER ISLAND": {"code": "IPC", "city": "Isla de Pascua", "country": "Chile", "lon": -109.421, "lat": -27.164, "airport": "Mataveri (IPC)"},
    "BALMACEDA": {"code": "BBA", "city": "Balmaceda", "country": "Chile", "lon": -71.689, "lat": -45.916, "airport": "Balmaceda Aysén (BBA)"},
    "ARICA": {"code": "ARI", "city": "Arica", "country": "Chile", "lon": -70.338, "lat": -18.348, "airport": "Chacalluta (ARI)"}
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
    if "COCHA" in p:
        return "Cocha"
    if "TURAVION" in p:
        return "Turavion"
    if "LATAM" in p or "LAN" in p:
        return "LATAM"
    if "SKY" in p:
        return "Sky"
    if "CORTE INGLES" in p or "CORTE INGLÉS" in p:
        return "El Corte Inglés"
    return "Otras Agencias"

def extract_passenger_name(text):
    if not text or not isinstance(text, str):
        return "Comitiva Oficial"
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3]
    for line in lines:
        if any(w in line.upper() for w in ["PASAJE", "VALOR", "TARIFA", "CONTRATO", "ORDEN"]):
            continue
        if re.search(r'^[A-ZÁÉÍÓÚÑ\s\.\-]{5,35}$', line):
            return line.title()
    return "Comitiva Oficial"

def load_existing_flights(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_flights_atomically(filepath, flights):
    tmp_path = filepath + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, filepath)

def process_raw_order(order, existing_ocs, next_id):
    oc_code = order.get('Codigo') or order.get('order_id')
    if not oc_code or oc_code in existing_ocs:
        return None

    item_name = order.get('Nombre') or order.get('item_title', '')
    espec = order.get('EspecificacionComprador') or order.get('item_description', '')
    organismo = order.get('OrganismoPublico') or order.get('buyer_name', 'Servicio Público')
    prov_raw = order.get('NombreProveedor') or order.get('supplier_name', 'Agencia de Viajes')
    fecha_raw = order.get('FechaEnvio') or order.get('issue_date') or datetime.now().strftime("%Y-%m-%d")

    combined_text = f"{item_name} {espec}"
    dest = detect_destination(combined_text)
    if not dest:
        return None

    monto_clean = 0
    monto_raw = order.get('MontoTotalOC_PesosChilenos') or order.get('amount_clp', 0)
    try:
        m_str = re.sub(r'[^\d,]', '', str(monto_raw))
        if ',' in m_str:
            monto_clean = int(float(m_str.replace(',', '.')))
        else:
            monto_clean = int(m_str) if m_str else 0
    except:
        monto_clean = 1500000

    if monto_clean < 300000:
        return None

    cabin = detect_cabin(combined_text)
    provider = clean_provider(prov_raw)
    passenger = extract_passenger_name(espec)

    date_str = str(fecha_raw)[:10]
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        year = dt.year
        month = dt.month
    except:
        year = 2026
        month = 10

    month_index = (year - 2007) * 12 + (month - 1)

    return {
        "id": f"FL-{next_id:04d}",
        "monthIndex": month_index,
        "year": year,
        "month": month,
        "date": date_str,
        "origin": SCL,
        "dest": dest,
        "entity": organismo.title() if isinstance(organismo, str) else "Servicio Público",
        "role": passenger,
        "cost": monto_clean,
        "cabin": cabin,
        "cabinDesc": f"Clase {cabin} • Vía {provider}",
        "airline": "Vuelo Comercial",
        "oc": oc_code,
        "provider": provider,
        "reason": (item_name[:90] if len(item_name) > 10 else f"Comitiva oficial a {dest['city']} por razones de servicio").strip(),
        "votes": {"approve": 45, "reject": 35}
    }

def sync_orders(ticket=None, fecha=None, data_path=None, mock_orders=None):
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vuelos_2007_2026.json")
    
    docs_path = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "vuelos_2007_2026.json")

    flights = load_existing_flights(data_path)
    existing_ocs = set(f.get('oc') for f in flights if f.get('oc'))
    next_id = len(flights) + 1

    print(f"[*] Catálogo base: {len(flights)} vuelos. OCs registradas: {len(existing_ocs)}")

    new_flights = []
    if mock_orders:
        orders_to_process = mock_orders
    else:
        import urllib.request
        import urllib.error

        if not ticket:
            ticket = os.environ.get("CHILECOMPRA_TICKET", "2CB3E6C4-789E-495F-898B-90FF6748149C")

        if not fecha:
            yesterday = datetime.now() - timedelta(days=1)
            fecha = yesterday.strftime("%d%m%Y")

        url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha={fecha}&ticket={ticket}"
        print(f"[*] Consultando API Mercado Público para fecha: {fecha}...")

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VuelosPublicos-Sync/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    orders_to_process = data.get('Listado', [])
                else:
                    print(f"[-] API respondió con estado HTTP {resp.status}")
                    return 0
        except Exception as e:
            print(f"[!] Error consultando API de Mercado Público (red o cuota): {e}")
            print("[*] Dataset local conservado intacto sin corrupción.")
            return 0

    for order in orders_to_process:
        flight_obj = process_raw_order(order, existing_ocs, next_id)
        if flight_obj:
            new_flights.append(flight_obj)
            existing_ocs.add(flight_obj['oc'])
            next_id += 1

    if new_flights:
        print(f"[+] Incorporando {len(new_flights)} nuevos vuelos detectados...")
        flights.extend(new_flights)
        save_flights_atomically(data_path, flights)
        if os.path.exists(os.path.dirname(docs_path)):
            save_flights_atomically(docs_path, flights)
        print(f"[OK] Catálogo actualizado a {len(flights)} vuelos en total.")
    else:
        print("[*] No se detectaron nuevas compras de pasajes para el período (0 cambios).")

    return len(new_flights)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincronizador diario de pasajes aéreos desde Mercado Público")
    parser.add_argument("--fecha", help="Fecha a consultar en formato DDMMAAAA (ej. 10102026)")
    parser.add_argument("--ticket", help="Ticket de API Mercado Público")
    parser.add_argument("--data", help="Ruta al archivo vuelos_2007_2026.json")
    args = parser.parse_args()

    sync_orders(ticket=args.ticket, fecha=args.fecha, data_path=args.data)
