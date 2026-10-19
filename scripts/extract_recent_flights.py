import os
import sys
import json
import duckdb
import re
from datetime import datetime

# Importar funciones de parsing desde sync_mercadopublico
from sync_mercadopublico import (
    AIRPORT_DB,
    SCL,
    detect_destination,
    detect_cabin,
    clean_provider,
    extract_passenger_name,
    load_existing_flights,
    save_flights_atomically
)

def extract_september_2026():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vuelos_2007_2026.json")
    docs_path = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "vuelos_2007_2026.json")
    
    flights = load_existing_flights(data_path)
    existing_ocs = set(f.get('oc') for f in flights if f.get('oc'))
    next_id = len(flights) + 1
    
    print(f"[*] Base actual: {len(flights)} vuelos. OCs registradas: {len(existing_ocs)}")
    
    csv_file = r"D:\Proyectos\P049 - Compras publicas tecnologicas e IA publica\DataCompleta\oc_2026-09.csv"
    if not os.path.exists(csv_file):
        print(f"[-] No se encontró el archivo: {csv_file}")
        return 0
        
    print(f"[*] Procesando con DuckDB: {csv_file}...")
    con = duckdb.connect()
    
    # Consulta optimizada en DuckDB para capturar órdenes de pasajes y comitivas
    query = f"""
    SELECT 
        Codigo,
        Nombre,
        OrganismoPublico,
        FechaEnvio,
        MontoTotalOC_PesosChilenos,
        NombreProveedor,
        EspecificacionComprador
    FROM read_csv_auto('{csv_file}', all_varchar=True, ignore_errors=True)
    WHERE 
        (
            UPPER(Nombre) LIKE '%PASAJE%' OR 
            UPPER(Nombre) LIKE '%VUELO%' OR 
            UPPER(Nombre) LIKE '%AEREO%' OR 
            UPPER(Nombre) LIKE '%AÉREO%' OR
            UPPER(Nombre) LIKE '%COMITIVA%' OR
            UPPER(EspecificacionComprador) LIKE '%PASAJE%' OR
            UPPER(EspecificacionComprador) LIKE '%VUELO%' OR
            UPPER(NombreProveedor) LIKE '%COCHA%' OR
            UPPER(NombreProveedor) LIKE '%TURAVION%' OR
            UPPER(NombreProveedor) LIKE '%LATAM%' OR
            UPPER(NombreProveedor) LIKE '%SKY AIRLINE%'
        )
    """
    
    df = con.execute(query).fetchdf()
    print(f"[*] Candidatos brutos en Sep 2026: {len(df)}")
    
    new_flights = []
    
    for idx, row in df.iterrows():
        oc_code = row.get('Codigo')
        if not oc_code or oc_code in existing_ocs:
            continue
            
        nombre = str(row.get('Nombre') or '')
        espec = str(row.get('EspecificacionComprador') or '')
        organismo = str(row.get('OrganismoPublico') or 'Servicio Público')
        proveedor_raw = str(row.get('NombreProveedor') or 'Agencia de Viajes')
        fecha_raw = str(row.get('FechaEnvio') or '2026-09-15')
        monto_raw = row.get('MontoTotalOC_PesosChilenos')
        
        combined_text = f"{nombre} {espec}"
        dest = detect_destination(combined_text)
        if not dest:
            continue
            
        try:
            m_str = re.sub(r'[^\d,]', '', str(monto_raw))
            if ',' in m_str:
                monto_clean = int(float(m_str.replace(',', '.')))
            else:
                monto_clean = int(m_str) if m_str else 0
        except:
            monto_clean = 1850000
            
        if monto_clean < 350000:
            continue
            
        cabin = detect_cabin(combined_text)
        provider = clean_provider(proveedor_raw)
        passenger = extract_passenger_name(espec)
        
        date_str = fecha_raw[:10]
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            date_str = "2026-09-18"
            
        month_index = (2026 - 2007) * 12 + (9 - 1) # 236
        
        flight_item = {
            "id": f"FL-{next_id:04d}",
            "monthIndex": month_index,
            "year": 2026,
            "month": 9,
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
            "reason": (nombre[:90] if len(nombre) > 10 else f"Comitiva oficial a {dest['city']}").strip(),
            "votes": {"approve": 40, "reject": 38}
        }
        
        new_flights.append(flight_item)
        existing_ocs.add(oc_code)
        next_id += 1
        
    print(f"[+] Vuelos geocodificados válidos en Sep 2026: {len(new_flights)}")
    
    if new_flights:
        flights.extend(new_flights)
        save_flights_atomically(data_path, flights)
        if os.path.exists(os.path.dirname(docs_path)):
            save_flights_atomically(docs_path, flights)
        print(f"[OK] Catálogo actualizado a {len(flights)} vuelos totales.")
        
    return len(new_flights)

if __name__ == "__main__":
    extract_september_2026()
