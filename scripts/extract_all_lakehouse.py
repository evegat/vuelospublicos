#!/usr/bin/env python3
"""
Extractor Histórico Integral de Vuelos Públicos (2007–2026).
Procesa los 236 archivos mensuales de órdenes de compra del Data Lakehouse (DataCompleta)
utilizando DuckDB en memoria y geocodificación automática.
"""

import os
import sys
import glob
import json
import re
import time
from datetime import datetime
import duckdb

# Importar utilidades del sincronizador existente
sys.path.insert(0, os.path.dirname(__file__))
from sync_mercadopublico import (
    AIRPORT_DB, 
    SCL, 
    detect_destination, 
    detect_cabin, 
    clean_provider, 
    extract_passenger_name,
    load_existing_flights,
    save_flights_atomically,
    safe_replace
)

LAKEHOUSE_DIR = r"D:\Proyectos\P049 - Compras publicas tecnologicas e IA publica\DataCompleta"

QUERY_TEMPLATE = """
SELECT 
    Codigo,
    FIRST(Nombre) as Nombre,
    FIRST("Descripcion/Obervaciones") as Descripcion,
    MAX(TRY_CAST("MontoTotalOC_PesosChilenos" AS DOUBLE)) as Monto,
    FIRST(OrganismoPublico) as OrganismoPublico,
    FIRST(NombreProveedor) as NombreProveedor,
    FIRST(FechaEnvio) as FechaEnvio,
    STRING_AGG(EspecificacionComprador, ' ') as ItemsEspecificacion
FROM read_csv(
    ?,
    delim=';',
    header=true,
    all_varchar=true,
    ignore_errors=true
)
WHERE 
    (
        upper(Nombre) LIKE '%PASAJE%' 
        OR upper(Nombre) LIKE '%AEREO%' 
        OR upper(Nombre) LIKE '%AÉREO%' 
        OR upper(Nombre) LIKE '%VUELO%'
        OR upper(Nombre) LIKE '%BOLETO%'
        OR upper(NombreProveedor) LIKE '%COCHA%'
        OR upper(NombreProveedor) LIKE '%TURAVION%'
        OR upper(NombreProveedor) LIKE '%LATAM%'
        OR upper(NombreProveedor) LIKE '%LAN%'
        OR upper(NombreProveedor) LIKE '%SKY AIR%'
        OR upper(NombreProveedor) LIKE '%CORTE INGLES%'
        OR upper(NombreProveedor) LIKE '%CORTE INGLÉS%'
    )
    AND NOT (upper(Nombre) LIKE '%TERRESTRE%' OR upper(Nombre) LIKE '%PULLMAN%' OR upper(Nombre) LIKE '%BUS INTERURBANO%')
GROUP BY Codigo
HAVING MAX(TRY_CAST("MontoTotalOC_PesosChilenos" AS DOUBLE)) >= 250000
"""

def run_full_lakehouse_extraction(data_dir=None, commit=True):
    start_total = time.time()
    
    if not os.path.exists(LAKEHOUSE_DIR):
        print(f"[!] Directorio Lakehouse no encontrado: {LAKEHOUSE_DIR}")
        return 0

    csv_files = sorted(glob.glob(os.path.join(LAKEHOUSE_DIR, "oc_*.csv")))
    total_files = len(csv_files)
    print(f"[*] Data Lakehouse encontrado: {total_files} archivos mensuales (2007–2026).", flush=True)

    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(repo_dir, "data", "vuelos_2007_2026.json")
    docs_path = os.path.join(repo_dir, "docs", "data", "vuelos_2007_2026.json")

    # Cargar vuelos actuales para no duplicar
    flights = load_existing_flights(data_path)
    existing_ocs = set(f.get('oc') for f in flights if f.get('oc'))
    next_id = len(flights) + 1
    initial_count = len(flights)

    print(f"[*] Base actual cargada: {initial_count} vuelos. OCs deduplicadas: {len(existing_ocs)}", flush=True)

    conn = duckdb.connect()
    new_flights = []
    
    current_year = ""
    year_count = 0
    year_monto = 0

    for idx, csv_file in enumerate(csv_files, 1):
        filename = os.path.basename(csv_file)
        # Extraer año de oc_YYYY-MM.csv
        m_year = re.search(r'oc_(\d{4})-\d{2}', filename)
        file_year = m_year.group(1) if m_year else "Desconocido"

        if file_year != current_year:
            if current_year != "":
                print(f"  [>] Resumen {current_year}: {year_count} vuelos nuevos extraídos (${year_monto:,.0f} CLP). Total catálogo: {len(flights) + len(new_flights)}", flush=True)
                if commit and new_flights:
                    save_flights_atomically(data_path, flights + new_flights)
                    save_flights_atomically(docs_path, flights + new_flights)
            current_year = file_year
            year_count = 0
            year_monto = 0

        t0 = time.time()
        try:
            df = conn.execute(QUERY_TEMPLATE, [csv_file]).fetchdf()
        except Exception as e:
            print(f"[!] Error leyendo {filename}: {e}", flush=True)
            continue

        file_added = 0
        for _, row in df.iterrows():
            code = row['Codigo']
            if not code or code in existing_ocs:
                continue

            full_text = f"{row['Nombre']} {row['Descripcion']} {row['ItemsEspecificacion']}"
            dest = detect_destination(full_text)
            if not dest:
                continue

            monto = int(row['Monto'] or 0)
            if monto < 250000:
                continue

            organismo = row['OrganismoPublico'] or "Servicio Público"
            proveedor = clean_provider(row['NombreProveedor'])
            date_raw = str(row['FechaEnvio'] or '')[:10]

            try:
                dt = datetime.strptime(date_raw, "%Y-%m-%d")
                year = dt.year
                month = dt.month
            except ValueError:
                try:
                    year = int(file_year)
                    month = int(filename.split('-')[1].split('.')[0])
                    date_raw = f"{year}-{month:02d}-01"
                except:
                    year = 2026
                    month = 1
                    date_raw = "2026-01-01"

            month_index = (year - 2007) * 12 + (month - 1)
            cabin = detect_cabin(full_text)
            passenger = extract_passenger_name(row['Descripcion'] or row['Nombre'])

            flight_obj = {
                "id": f"FL-{next_id:04d}",
                "monthIndex": month_index,
                "year": year,
                "month": month,
                "date": date_raw,
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
                "reason": (row['Descripcion'][:90] if row['Descripcion'] and len(row['Descripcion']) > 10 else row['Nombre'][:90]).strip(),
                "votes": {"approve": 45, "reject": 35}
            }

            new_flights.append(flight_obj)
            existing_ocs.add(code)
            next_id += 1
            file_added += 1
            year_count += 1
            year_monto += monto

        t_diff = time.time() - t0
        if file_added > 0:
            print(f"[{idx}/{total_files}] {filename}: +{file_added} vuelos ({t_diff:.1f}s)", flush=True)

    # Resumen del último año
    if current_year != "":
        print(f"  [>] Resumen {current_year}: {year_count} vuelos nuevos extraídos (${year_monto:,.0f} CLP).", flush=True)

    total_final = len(flights) + len(new_flights)
    print(f"\n=======================================================", flush=True)
    print(f"[OK] Extracción masiva completada en {time.time() - start_total:.1f}s.", flush=True)
    print(f"[*] Vuelos iniciales: {initial_count}", flush=True)
    print(f"[*] Nuevos vuelos incorporados: {len(new_flights)}", flush=True)
    print(f"[*] Catálogo total consolidado: {total_final} vuelos.", flush=True)
    total_gasto = sum(f.get('cost', 0) for f in flights + new_flights)
    print(f"[*] Gasto total acumulado histórico: ${total_gasto:,.0f} CLP", flush=True)
    print(f"=======================================================\n", flush=True)

    if commit and new_flights:
        all_flights = flights + new_flights
        # Ordenar cronológicamente descendente
        all_flights.sort(key=lambda x: (x.get('date', ''), x.get('id', '')), reverse=True)
        # Re-indexar IDs
        for i, f in enumerate(all_flights, 1):
            f['id'] = f"FL-{i:04d}"

        save_flights_atomically(data_path, all_flights)
        save_flights_atomically(docs_path, all_flights)
        print(f"[OK] Dataset reindexado y persistido con éxito ({len(all_flights)} vuelos).", flush=True)

    return len(new_flights)

if __name__ == "__main__":
    run_full_lakehouse_extraction(commit=True)
