import math
import os
import base64
import zipfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def make_pikachu_head(size=1024):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = size / 1024.0

    # 1. Ear polygon definitions (smooth outer curves)
    left_ear = [
        (330 * scale, 480 * scale),
        (260 * scale, 370 * scale),
        (205 * scale, 250 * scale),
        (165 * scale, 150 * scale),
        (155 * scale, 90 * scale),   # Apex outer
        (185 * scale, 75 * scale),   # Top tip
        (230 * scale, 95 * scale),   # Apex inner
        (285 * scale, 185 * scale),
        (355 * scale, 285 * scale),
        (420 * scale, 395 * scale),
    ]

    right_ear = [
        ((1024 - 330) * scale, 480 * scale),
        ((1024 - 260) * scale, 370 * scale),
        ((1024 - 205) * scale, 250 * scale),
        ((1024 - 165) * scale, 150 * scale),
        ((1024 - 155) * scale, 90 * scale),   # Apex outer
        ((1024 - 185) * scale, 75 * scale),   # Top tip
        ((1024 - 230) * scale, 95 * scale),   # Apex inner
        ((1024 - 285) * scale, 185 * scale),
        ((1024 - 355) * scale, 285 * scale),
        ((1024 - 420) * scale, 395 * scale),
    ]

    # Head shape (Chubby round cheeks)
    cx, cy = 512 * scale, 650 * scale
    n = 240
    head_pts = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        # Puff cheeks out at bottom-left and bottom-right
        cheek_bulge = 85 * scale * (math.sin(angle) ** 2) * (math.cos(angle) ** 2) if sin_a > -0.1 else 0
        rx = 335 * scale + cheek_bulge
        ry = 285 * scale - 30 * scale * sin_a
        head_pts.append((cx + rx * cos_a, cy + ry * sin_a))

    # --- 1. UNIFIED SILHOUETTE MASK ---
    silhouette = Image.new("L", (size, size), 0)
    s_draw = ImageDraw.Draw(silhouette)
    s_draw.polygon(left_ear, fill=255)
    s_draw.polygon(right_ear, fill=255)
    s_draw.polygon(head_pts, fill=255)

    # --- 2. SMOOTH DROP SHADOW ---
    shadow_mask = Image.new("L", (size, size), 0)
    sm_draw = ImageDraw.Draw(shadow_mask)
    sy_off = int(22 * scale)
    sm_draw.polygon([(x, y + sy_off) for x, y in left_ear], fill=255)
    sm_draw.polygon([(x, y + sy_off) for x, y in right_ear], fill=255)
    sm_draw.polygon([(x, y + sy_off) for x, y in head_pts], fill=255)
    
    shadow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_fill = Image.new("RGBA", (size, size), (15, 23, 42, 130)) # Deep navy/black shadow
    shadow_layer.paste(s_fill, (0, 0), shadow_mask)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(16 * scale))
    canvas.paste(shadow_layer, (0, 0), shadow_layer)

    # --- 3. BASE YELLOW GRADIENT (SUNNY & VIBRANT) ---
    body = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(body)
    y_min, y_max = int(70 * scale), int(960 * scale)
    for y in range(y_min, y_max):
        t = (y - y_min) / float(y_max - y_min)
        # Gradient: Top sunny highlight (#FFF566) -> Pikachu yellow (#FFD700) -> Warm amber (#F59E0B)
        if t < 0.45:
            rt = t / 0.45
            r = int(255)
            g = int(245 - rt * (245 - 215))
            b = int(100 - rt * (100 - 0))
        else:
            rt = (t - 0.45) / 0.55
            r = int(255 - rt * (255 - 245))
            g = int(215 - rt * (215 - 158))
            b = int(0 + rt * (11 - 0))
        b_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    body.putalpha(silhouette)
    canvas.paste(body, (0, 0), body)

    # --- 4. BLACK EAR TIPS (WITH SMOOTH ANGLED CUT) ---
    # Left ear tip mask
    tip_mask_l = Image.new("L", (size, size), 0)
    tml_draw = ImageDraw.Draw(tip_mask_l)
    # Cut across ear at y ~ 160-220
    tml_draw.polygon([
        (120 * scale, 40 * scale),
        (260 * scale, 85 * scale),
        (230 * scale, 190 * scale),
        (135 * scale, 220 * scale),
    ], fill=255)
    # Mask by left ear and silhouette
    tip_mask_l = ImageChops.multiply(tip_mask_l, silhouette)
    
    tip_layer = Image.new("RGBA", (size, size), (26, 23, 23, 255))
    canvas.paste(tip_layer, (0, 0), tip_mask_l)

    # Right ear tip mask
    tip_mask_r = Image.new("L", (size, size), 0)
    tmr_draw = ImageDraw.Draw(tip_mask_r)
    tmr_draw.polygon([
        ((1024 - 120) * scale, 40 * scale),
        ((1024 - 260) * scale, 85 * scale),
        ((1024 - 230) * scale, 190 * scale),
        ((1024 - 135) * scale, 220 * scale),
    ], fill=255)
    tip_mask_r = ImageChops.multiply(tip_mask_r, silhouette)
    canvas.paste(tip_layer, (0, 0), tip_mask_r)

    # --- 5. PERIMETER OUTLINE ONLY (NO SEAMS ACROSS FOREHEAD!) ---
    # We dilate the unified silhouette mask by 4px and subtract the original mask
    filter_size = int(max(3, 7 * scale))
    if filter_size % 2 == 0:
        filter_size += 1
    dilated_mask = silhouette.filter(ImageFilter.MaxFilter(filter_size))
    perimeter_mask = ImageChops.subtract(dilated_mask, silhouette)
    
    outline_layer = Image.new("RGBA", (size, size), (217, 119, 6, 235)) # Crisp golden-amber
    canvas.paste(outline_layer, (0, 0), perimeter_mask)

    draw = ImageDraw.Draw(canvas)

    # --- 6. ROSY RED ELECTRIC CHEEKS (GLOW + HIGHLIGHT) ---
    chk_r = 76 * scale
    chk_y = 705 * scale
    lx_chk = 246 * scale
    rx_chk = (1024 - 246) * scale

    # Soft ambient glow behind cheeks
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_img)
    g_draw.ellipse([lx_chk - chk_r - 12*scale, chk_y - chk_r - 12*scale, lx_chk + chk_r + 12*scale, chk_y + chk_r + 12*scale], fill=(239, 68, 68, 80))
    g_draw.ellipse([rx_chk - chk_r - 12*scale, chk_y - chk_r - 12*scale, rx_chk + chk_r + 12*scale, chk_y + chk_r + 12*scale], fill=(239, 68, 68, 80))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(10 * scale))
    canvas.paste(glow_img, (0, 0), glow_img)

    # Main red cheek circles (Electric vibrant red #EE2727)
    draw.ellipse([lx_chk - chk_r, chk_y - chk_r, lx_chk + chk_r, chk_y + chk_r], fill=(238, 40, 40, 255), outline=(190, 25, 25, 240), width=int(3*scale))
    draw.ellipse([rx_chk - chk_r, chk_y - chk_r, rx_chk + chk_r, chk_y + chk_r], fill=(238, 40, 40, 255), outline=(190, 25, 25, 240), width=int(3*scale))

    # Cute glossy highlights on cheeks
    draw.ellipse([lx_chk - chk_r*0.58, chk_y - chk_r*0.62, lx_chk - chk_r*0.14, chk_y - chk_r*0.22], fill=(255, 255, 255, 160))
    draw.ellipse([rx_chk + chk_r*0.14, chk_y - chk_r*0.62, rx_chk + chk_r*0.58, chk_y - chk_r*0.22], fill=(255, 255, 255, 160))

    # --- 7. BIG EXPRESSIVE KAWAII EYES (OVAL ANIME STYLE) ---
    eye_rx = 48 * scale
    eye_ry = 58 * scale
    eye_y = 588 * scale
    lx_eye = 360 * scale
    rx_eye = (1024 - 360) * scale

    # Eye base (Deep shiny obsidian black)
    draw.ellipse([lx_eye - eye_rx, eye_y - eye_ry, lx_eye + eye_rx, eye_y + eye_ry], fill=(22, 18, 18, 255), outline=(8, 6, 6, 255), width=int(3*scale))
    draw.ellipse([rx_eye - eye_rx, eye_y - eye_ry, rx_eye + eye_rx, eye_y + eye_ry], fill=(22, 18, 18, 255), outline=(8, 6, 6, 255), width=int(3*scale))

    # Warm brown iris crescent at lower eye
    draw.ellipse([lx_eye - eye_rx*0.75, eye_y + eye_ry*0.18, lx_eye + eye_rx*0.75, eye_y + eye_ry*0.86], fill=(130, 60, 20, 160))
    draw.ellipse([rx_eye - eye_rx*0.75, eye_y + eye_ry*0.18, rx_eye + eye_rx*0.75, eye_y + eye_ry*0.86], fill=(130, 60, 20, 160))

    # Primary large white sparkle (Top-right of both eyes)
    sp1_r = 19 * scale
    draw.ellipse([lx_eye + 6*scale - sp1_r, eye_y - 12*scale - sp1_r, lx_eye + 6*scale + sp1_r, eye_y - 12*scale + sp1_r], fill=(255, 255, 255, 255))
    draw.ellipse([rx_eye + 18*scale - sp1_r, eye_y - 12*scale - sp1_r, rx_eye + 18*scale + sp1_r, eye_y - 12*scale + sp1_r], fill=(255, 255, 255, 255))

    # Secondary cute tiny sparkle (Bottom-left)
    sp2_r = 8 * scale
    draw.ellipse([lx_eye - 18*scale - sp2_r, eye_y + 18*scale - sp2_r, lx_eye - 18*scale + sp2_r, eye_y + 18*scale + sp2_r], fill=(255, 255, 255, 230))
    draw.ellipse([rx_eye - 6*scale - sp2_r, eye_y + 18*scale - sp2_r, rx_eye - 6*scale + sp2_r, eye_y + 18*scale + sp2_r], fill=(255, 255, 255, 230))

    # --- 8. TINY ADORABLE NOSE ---
    nx, ny = 512 * scale, 650 * scale
    nw, nh = 13 * scale, 8 * scale
    draw.polygon([
        (nx - nw, ny - nh),
        (nx + nw, ny - nh),
        (nx, ny + nh)
    ], fill=(28, 22, 22, 255))

    # --- 9. SWEET OPEN HAPPY SMILE (:D) ---
    mouth_mask = Image.new("L", (size, size), 0)
    mm_draw = ImageDraw.Draw(mouth_mask)

    m_left_x = 448 * scale
    m_right_x = 576 * scale
    m_top_y = 698 * scale
    m_bottom_y = 786 * scale
    m_center_x = 512 * scale

    mouth_pts = []
    # Smooth upper lip: gentle curved line from left to center to right
    steps = 30
    for i in range(steps + 1):
        t = i / float(steps)
        x = m_left_x + t * (m_right_x - m_left_x)
        # Gentle cat-curve: dipping slightly at center
        dist_from_center = abs(t - 0.5) * 2.0
        y = (m_top_y + (1.0 - dist_from_center) * 4 * scale)
        mouth_pts.append((x, y))

    # Deep rounded bowl for lower mouth
    for i in range(steps + 1):
        t = i / float(steps)
        angle = t * math.pi
        x = m_center_x + math.cos(angle) * (64 * scale)
        y = m_top_y + math.sin(angle) * ((m_bottom_y - m_top_y))
        mouth_pts.append((x, y))

    # Fill mouth cavity with rich ruby/dark cherry red
    mm_draw.polygon(mouth_pts, fill=255)
    mouth_fill = Image.new("RGBA", (size, size), (155, 18, 54, 255))
    canvas.paste(mouth_fill, (0, 0), mouth_mask)

    # Cute pink tongue
    tongue_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tongue_layer)
    t_draw.ellipse([
        (m_center_x - 52 * scale), (m_bottom_y - 48 * scale),
        (m_center_x + 52 * scale), (m_bottom_y + 30 * scale)
    ], fill=(251, 113, 133, 255), outline=(244, 63, 94, 255), width=int(2*scale))
    tongue_layer.putalpha(mouth_mask)
    canvas.paste(tongue_layer, (0, 0), tongue_layer)

    # Mouth dark outline
    draw.polygon(mouth_pts, outline=(45, 12, 18, 255), width=int(max(2, 5 * scale)))

    return canvas

def make_pikachu_app_badge(size=1024):
    """Modern squircle app icon tile with Pikachu's cute face inside"""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = size / 1024.0
    margin = 54 * scale
    radius = 210 * scale

    # 1. Tile drop shadow
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([margin + 4*scale, margin + 18*scale, size - margin - 4*scale, size - margin + 20*scale], radius=radius, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24 * scale))
    canvas.paste(shadow, (0, 0), shadow)

    # 2. Tile squircle base: Radiant Royal Electric Yellow & Gold Gradient
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tile)
    for y in range(int(margin), int(size - margin)):
        t = (y - margin) / float(size - 2 * margin)
        # Gradient: Fresh vivid sunny yellow (#FFE600) to deep rich warm marigold (#F59E0B)
        r = int(255 - t * (255 - 245))
        g = int(235 - t * (235 - 158))
        b = int(40 - t * (40 - 11))
        t_draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))
    
    tile_mask = Image.new("L", (size, size), 0)
    tm_draw = ImageDraw.Draw(tile_mask)
    tm_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=255)
    tile.putalpha(tile_mask)
    canvas.paste(tile, (0, 0), tile)

    # 3. Outer golden border and inner rim
    border = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border)
    b_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, outline=(245, 158, 11, 240), width=int(8*scale))
    b_draw.rounded_rectangle([margin + 6*scale, margin + 6*scale, size - margin - 6*scale, size - margin - 6*scale], radius=radius - 6*scale, outline=(254, 240, 138, 180), width=int(2*scale))
    canvas.paste(border, (0, 0), border)

    # 4. Draw Pikachu inside the badge (scaled down to fit comfortably)
    pika = make_pikachu_head(1024)
    target_pika_size = int(820 * scale)
    pika_resized = pika.resize((target_pika_size, target_pika_size), Image.Resampling.LANCZOS)
    
    # Position Pikachu in center
    px = int((size - target_pika_size) / 2)
    py = int((size - target_pika_size) / 2 + 15 * scale)
    canvas.paste(pika_resized, (px, py), pika_resized)

    # 5. Top glass highlight (Clean translucent overlay)
    glass_mask = Image.new("L", (size, size), 0)
    gm_draw = ImageDraw.Draw(glass_mask)
    # Glass curve at upper half
    gm_draw.polygon([
        (margin, margin),
        (size - margin, margin),
        (size - margin, margin + 260*scale),
        (margin, margin + 140*scale)
    ], fill=255)
    # Intersect with rounded squircle
    gm_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=255)
    
    glass_highlight = Image.new("RGBA", (size, size), (255, 255, 255, 45))
    glass_highlight.putalpha(ImageChops.multiply(glass_mask, tile_mask))
    canvas.paste(glass_highlight, (0, 0), glass_highlight)

    return canvas

def generate_icons():
    print("🎨 Generating Pikachu icons...")
    
    # 1. Pure Pikachu Head
    head_1024 = make_pikachu_head(1024)
    head_1024.resize((512, 512), Image.Resampling.LANCZOS).save("A_THANG/pikachu_preview.png", "PNG")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    head_1024.save("A_THANG/pikachu.ico", format="ICO", sizes=sizes)
    print("   [OK] A_THANG/pikachu.ico (Pure Character Icon)")

    # 2. Modern Squircle App Badge
    badge_1024 = make_pikachu_app_badge(1024)
    badge_1024.resize((512, 512), Image.Resampling.LANCZOS).save("A_THANG/pikachu_badge_preview.png", "PNG")
    badge_1024.save("A_THANG/pikachu_badge.ico", format="ICO", sizes=sizes)
    print("   [OK] A_THANG/pikachu_badge.ico (Squircle App Badge Icon)")

if __name__ == "__main__":
    generate_icons()
