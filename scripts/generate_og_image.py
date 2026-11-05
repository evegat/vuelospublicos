import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_og_image(output_path):
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), color=(6, 11, 17))
    draw = ImageDraw.Draw(img)

    # 1. Gradient Background
    for y in range(height):
        ratio = y / height
        r = int(6 + (14 - 6) * ratio)
        g = int(11 + (24 - 11) * ratio)
        b = int(17 + (38 - 17) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Tech Grid Lines
    grid_color = (20, 36, 56)
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 3. Radar Circles (Origin roughly at SCL: 820, 440)
    ox, oy = 820, 440
    for radius in [70, 150, 240, 340, 460]:
        draw.ellipse([ox - radius, oy - radius, ox + radius, oy + radius], outline=(25, 48, 75), width=1)

    # Destination nodes and arcs from SCL (ox, oy)
    destinations = [
        {"name": "Madrid (MAD)", "x": 920, "y": 180, "color": (255, 77, 90), "cabin": "Business"},
        {"name": "París (CDG)", "x": 960, "y": 140, "color": (255, 77, 90), "cabin": "Business"},
        {"name": "Washington (IAD)", "x": 760, "y": 200, "color": (0, 212, 255), "cabin": "Turista"},
        {"name": "Osaka (KIX)", "x": 1100, "y": 210, "color": (255, 77, 90), "cabin": "Business"},
        {"name": "Rapa Nui (IPC)", "x": 620, "y": 380, "color": (0, 229, 163), "cabin": "Turista"},
        {"name": "Arica (ARI)", "x": 800, "y": 330, "color": (0, 229, 163), "cabin": "Turista"},
        {"name": "Punta Arenas (PUQ)", "x": 810, "y": 550, "color": (0, 229, 163), "cabin": "Turista"}
    ]

    # Draw curved arcs
    for dest in destinations:
        dx, dy = dest["x"], dest["y"]
        # Quadratic Bézier control point pulled upward
        cx = (ox + dx) / 2 - 40
        cy = min(oy, dy) - 60
        
        points = []
        for t_step in range(41):
            t = t_step / 40.0
            px = (1 - t)**2 * ox + 2 * (1 - t) * t * cx + t**2 * dx
            py = (1 - t)**2 * oy + 2 * (1 - t) * t * cy + t**2 * dy
            points.append((px, py))
            
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=dest["color"], width=2)
            
        # Draw node circle
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=dest["color"], outline=(255, 255, 255), width=1)

    # Origin SCL pulse
    draw.ellipse([ox - 9, oy - 9, ox + 9, oy + 9], fill=(0, 212, 255), outline=(255, 255, 255), width=2)

    # 4. Fonts
    font_bold_lg = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
    font_bold_md = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
    font_bold_sm = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    font_mono_lg = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 46)
    font_mono_md = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)

    # 5. Left Content Box (Dark Card Overlay for High Legibility)
    box_w = 640
    card_fill = (12, 20, 32, 240)
    draw.rounded_rectangle([36, 36, 36 + box_w, 594], radius=16, fill=(10, 18, 28), outline=(47, 129, 247), width=2)

    # Badge: Observatorio Cívico
    badge_x, badge_y = 66, 62
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 330, badge_y + 32], radius=16, fill=(20, 42, 68), outline=(56, 189, 248), width=1)
    draw.text((badge_x + 14, badge_y + 5), "OBSERVATORIO CÍVICO INDEPENDIENTE", font=font_bold_sm, fill=(56, 189, 248))

    # Main Brand Title
    draw.text((66, 108), "VuelosPúblicos", font=font_bold_lg, fill=(240, 246, 252))

    # Subtitle
    draw.text((66, 172), "Radar Táctico y Scrollytelling de Pasajes del Estado", font=font_sub, fill=(139, 155, 176))
    draw.text((66, 202), "Trazabilidad oficial de compras públicas de Chile (2007–2026)", font=font_regular, fill=(87, 101, 119))

    # Separator Line
    draw.line([(66, 238), (66 + box_w - 60, 238)], fill=(30, 50, 75), width=1)

    # Fiscal Odometer Highlight
    draw.text((66, 252), "GASTO CONSOLIDADO EN COMITIVAS AUDITADAS", font=font_mono_md, fill=(139, 155, 176))
    draw.text((66, 280), "$3.188.672.723 CLP", font=font_mono_lg, fill=(0, 229, 163))

    # Metric Cards Grid (2x2)
    card_y = 352
    metrics = [
        ("465", "VUELOS OFICIALES", "100% Órdenes de Compra"),
        ("240", "MESES CRONOLÓGICOS", "2007 a Octubre 2026"),
        ("2.5D", "MAPA CARTOGRÁFICO", "Arcos Balísticos a 60 FPS"),
        ("VOTO", "TRIBUNAL CIUDADANO", "¿Se justifica o es derroche?")
    ]

    for i, (val, label, sub) in enumerate(metrics):
        cx = 66 + (i % 2) * 276
        cy = card_y + (i // 2) * 88
        cw, ch = 260, 76
        
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8, fill=(16, 28, 44), outline=(32, 54, 82), width=1)
        draw.text((cx + 12, cy + 8), val, font=font_bold_md, fill=(240, 246, 252))
        draw.text((cx + 80, cy + 12), label, font=font_bold_sm, fill=(56, 189, 248))
        draw.text((cx + 12, cy + 48), sub, font=font_regular, fill=(139, 155, 176))

    # Footer inside card
    draw.line([(66, 542), (66 + box_w - 60, 542)], fill=(30, 50, 75), width=1)
    draw.text((66, 556), "vuelospublicos.evegat.cl", font=font_bold_sm, fill=(0, 212, 255))
    draw.text((360, 558), "Por Eduardo Vega Toledo • Datos de ChileCompra", font=font_regular, fill=(87, 101, 119))

    # Right floating label for SCL
    draw.text((ox - 45, oy + 16), "SANTIAGO (SCL)", font=font_mono_md, fill=(0, 212, 255))

    # Ensure output dir exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    print(f"[OK] OG image generated: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_og_image(os.path.join(base, "og-image.png"))
    create_og_image(os.path.join(base, "docs", "og-image.png"))
