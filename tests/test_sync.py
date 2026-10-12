import os
import sys
import tempfile
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from sync_mercadopublico import sync_orders, process_raw_order, detect_destination, detect_cabin

class TestSyncMercadoPublico(unittest.TestCase):

    def test_destination_detection(self):
        d1 = detect_destination("Pasaje aéreo Santiago - Ginebra Misión OIT")
        self.assertIsNotNone(d1)
        self.assertEqual(d1["code"], "GVA")
        self.assertEqual(d1["city"], "Ginebra")

        d2 = detect_destination("Traslado comitiva París Francia cumbre OCDE")
        self.assertIsNotNone(d2)
        self.assertEqual(d2["code"], "CDG")

        d_none = detect_destination("Compra de computadores para oficina")
        self.assertIsNone(d_none)

    def test_cabin_detection(self):
        self.assertEqual(detect_cabin("Pasaje Clase Business intercontinental"), "Business")
        self.assertEqual(detect_cabin("Tarifa Turista regular económica"), "Turista")
        self.assertEqual(detect_cabin("Vuelo comitiva ejecutiva"), "Business")

    def test_deduplication_and_sync(self):
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json', encoding='utf-8') as tf:
            initial_data = [
                {
                    "id": "FL-0001",
                    "monthIndex": 200,
                    "year": 2023,
                    "month": 9,
                    "date": "2023-09-15",
                    "origin": {"code": "SCL"},
                    "dest": {"code": "JFK", "city": "Nueva York"},
                    "entity": "Presidencia",
                    "role": "Comitiva",
                    "cost": 5000000,
                    "cabin": "Business",
                    "oc": "724-10-CM23"
                }
            ]
            json.dump(initial_data, tf)
            temp_path = tf.name

        try:
            mock_orders = [
                # 1. Orden duplicada (debe ser ignorada)
                {
                    "Codigo": "724-10-CM23",
                    "Nombre": "Pasaje aéreo Santiago - Nueva York",
                    "OrganismoPublico": "Presidencia",
                    "MontoTotalOC_PesosChilenos": "5000000"
                },
                # 2. Orden nueva válida
                {
                    "Codigo": "999-55-CM26",
                    "Nombre": "Pasajes Tokio Japón Misión Comercial",
                    "EspecificacionComprador": "Juan Pérez Cancillería",
                    "OrganismoPublico": "Ministerio de Relaciones Exteriores",
                    "NombreProveedor": "Turismo Cocha",
                    "MontoTotalOC_PesosChilenos": "4200000",
                    "FechaEnvio": "2026-10-10"
                }
            ]

            added = sync_orders(data_path=temp_path, mock_orders=mock_orders)
            self.assertEqual(added, 1, "Debe agregar exactamente 1 orden nueva ignorando la duplicada")

            with open(temp_path, 'r', encoding='utf-8') as f:
                updated = json.load(f)

            self.assertEqual(len(updated), 2, "El catálogo debe tener 2 vuelos en total")
            new_flight = updated[-1]
            self.assertEqual(new_flight["oc"], "999-55-CM26")
            self.assertEqual(new_flight["dest"]["code"], "NRT")
            self.assertEqual(new_flight["dest"]["city"], "Tokio")
            self.assertEqual(new_flight["provider"], "Cocha")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
