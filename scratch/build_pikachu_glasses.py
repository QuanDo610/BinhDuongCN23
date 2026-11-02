import math
import os
import zipfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def make_pikachu_head_with_glasses(size=1024):
    scale = size / 1024.0

    # 1. Ear polygons (smoothed)
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
        cheek_bulge = 85 * scale * (math.sin(angle) ** 2) * (math.cos(angle) ** 2) if sin_a > -0.1 else 0
        rx = 335 * scale + cheek_bulge
        ry = 285 * scale - 30 * scale * sin_a
        head_pts.append((cx + rx * cos_a, cy + ry * sin_a))

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # --- Silhouette Mask ---
    silhouette = Image.new("L", (size, size), 0)
    s_draw = ImageDraw.Draw(silhouette)
    s_draw.polygon(left_ear, fill=255)
    s_draw.polygon(right_ear, fill=255)
    s_draw.polygon(head_pts, fill=255)

    # --- Drop Shadow ---
    shadow_mask = Image.new("L", (size, size), 0)
    sm_draw = ImageDraw.Draw(shadow_mask)
    sy_off = int(22 * scale)
    sm_draw.polygon([(x, y + sy_off) for x, y in left_ear], fill=255)
    sm_draw.polygon([(x, y + sy_off) for x, y in right_ear], fill=255)
    sm_draw.polygon([(x, y + sy_off) for x, y in head_pts], fill=255)
    
    shadow_layer = Image.new("RGBA", (size, size), (15, 23, 42, 130))
    shadow_layer.putalpha(shadow_mask)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(16 * scale))
    canvas.paste(shadow_layer, (0, 0), shadow_layer)

    # --- Yellow Gradient Body ---
    body = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(body)
    y_min, y_max = int(70 * scale), int(960 * scale)
    for y in range(y_min, y_max):
        t = (y - y_min) / float(y_max - y_min)
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

    # --- Black Ear Tips ---
    tip_mask_l = Image.new("L", (size, size), 0)
    tml_draw = ImageDraw.Draw(tip_mask_l)
    tml_draw.polygon([
        (120 * scale, 40 * scale),
        (260 * scale, 85 * scale),
        (230 * scale, 190 * scale),
        (135 * scale, 220 * scale),
    ], fill=255)
    tip_mask_l = ImageChops.multiply(tip_mask_l, silhouette)
    tip_layer = Image.new("RGBA", (size, size), (26, 23, 23, 255))
    canvas.paste(tip_layer, (0, 0), tip_mask_l)

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

    # --- Outer Perimeter Golden Outline ---
    filter_size = int(max(3, 7 * scale))
    if filter_size % 2 == 0:
        filter_size += 1
    dilated_mask = silhouette.filter(ImageFilter.MaxFilter(filter_size))
    perimeter_mask = ImageChops.subtract(dilated_mask, silhouette)
    outline_layer = Image.new("RGBA", (size, size), (217, 119, 6, 235))
    canvas.paste(outline_layer, (0, 0), perimeter_mask)

    draw = ImageDraw.Draw(canvas)

    # --- Red Cheeks ---
    chk_r = 76 * scale
    chk_y = 705 * scale
    lx_chk = 246 * scale
    rx_chk = (1024 - 246) * scale

    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_img)
    g_draw.ellipse([lx_chk - chk_r - 12*scale, chk_y - chk_r - 12*scale, lx_chk + chk_r + 12*scale, chk_y + chk_r + 12*scale], fill=(239, 68, 68, 80))
    g_draw.ellipse([rx_chk - chk_r - 12*scale, chk_y - chk_r - 12*scale, rx_chk + chk_r + 12*scale, chk_y + chk_r + 12*scale], fill=(239, 68, 68, 80))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(10 * scale))
    canvas.paste(glow_img, (0, 0), glow_img)

    draw.ellipse([lx_chk - chk_r, chk_y - chk_r, lx_chk + chk_r, chk_y + chk_r], fill=(238, 40, 40, 255), outline=(190, 25, 25, 240), width=int(3*scale))
    draw.ellipse([rx_chk - chk_r, chk_y - chk_r, rx_chk + chk_r, chk_y + chk_r], fill=(238, 40, 40, 255), outline=(190, 25, 25, 240), width=int(3*scale))

    draw.ellipse([lx_chk - chk_r*0.58, chk_y - chk_r*0.62, lx_chk - chk_r*0.14, chk_y - chk_r*0.22], fill=(255, 255, 255, 160))
    draw.ellipse([rx_chk + chk_r*0.14, chk_y - chk_r*0.62, rx_chk + chk_r*0.58, chk_y - chk_r*0.22], fill=(255, 255, 255, 160))

    # --- Kawaii Oval Eyes ---
    eye_rx = 48 * scale
    eye_ry = 58 * scale
    eye_y = 588 * scale
    lx_eye = 360 * scale
    rx_eye = (1024 - 360) * scale

    draw.ellipse([lx_eye - eye_rx, eye_y - eye_ry, lx_eye + eye_rx, eye_y + eye_ry], fill=(22, 18, 18, 255), outline=(8, 6, 6, 255), width=int(3*scale))
    draw.ellipse([rx_eye - eye_rx, eye_y - eye_ry, rx_eye + eye_rx, eye_y + eye_ry], fill=(22, 18, 18, 255), outline=(8, 6, 6, 255), width=int(3*scale))

    draw.ellipse([lx_eye - eye_rx*0.75, eye_y + eye_ry*0.18, lx_eye + eye_rx*0.75, eye_y + eye_ry*0.86], fill=(130, 60, 20, 160))
    draw.ellipse([rx_eye - eye_rx*0.75, eye_y + eye_ry*0.18, rx_eye + eye_rx*0.75, eye_y + eye_ry*0.86], fill=(130, 60, 20, 160))

    sp1_r = 19 * scale
    draw.ellipse([lx_eye + 6*scale - sp1_r, eye_y - 12*scale - sp1_r, lx_eye + 6*scale + sp1_r, eye_y - 12*scale + sp1_r], fill=(255, 255, 255, 255))
    draw.ellipse([rx_eye + 18*scale - sp1_r, eye_y - 12*scale - sp1_r, rx_eye + 18*scale + sp1_r, eye_y - 12*scale + sp1_r], fill=(255, 255, 255, 255))

    sp2_r = 8 * scale
    draw.ellipse([lx_eye - 18*scale - sp2_r, eye_y + 18*scale - sp2_r, lx_eye - 18*scale + sp2_r, eye_y + 18*scale + sp2_r], fill=(255, 255, 255, 230))
    draw.ellipse([rx_eye - 6*scale - sp2_r, eye_y + 18*scale - sp2_r, rx_eye - 6*scale + sp2_r, eye_y + 18*scale + sp2_r], fill=(255, 255, 255, 230))

    # --- Tiny Nose ---
    nx, ny = 512 * scale, 650 * scale
    nw, nh = 13 * scale, 8 * scale
    draw.polygon([
        (nx - nw, ny - nh),
        (nx + nw, ny - nh),
        (nx, ny + nh)
    ], fill=(28, 22, 22, 255))

    # --- Joyful Anime Smile ---
    mouth_mask = Image.new("L", (size, size), 0)
    mm_draw = ImageDraw.Draw(mouth_mask)
    m_left_x, m_right_x = 448 * scale, 576 * scale
    m_top_y, m_bottom_y = 698 * scale, 786 * scale
    m_center_x = 512 * scale

    mouth_pts = []
    steps = 30
    for i in range(steps + 1):
        t = i / float(steps)
        x = m_left_x + t * (m_right_x - m_left_x)
        dist_from_center = abs(t - 0.5) * 2.0
        y = (m_top_y + (1.0 - dist_from_center) * 4 * scale)
        mouth_pts.append((x, y))

    for i in range(steps + 1):
        t = i / float(steps)
        angle = t * math.pi
        x = m_center_x + math.cos(angle) * (64 * scale)
        y = m_top_y + math.sin(angle) * ((m_bottom_y - m_top_y))
        mouth_pts.append((x, y))

    mm_draw.polygon(mouth_pts, fill=255)
    mouth_fill = Image.new("RGBA", (size, size), (155, 18, 54, 255))
    canvas.paste(mouth_fill, (0, 0), mouth_mask)

    tongue_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tongue_layer)
    t_draw.ellipse([
        (m_center_x - 52 * scale), (m_bottom_y - 48 * scale),
        (m_center_x + 52 * scale), (m_bottom_y + 30 * scale)
    ], fill=(251, 113, 133, 255), outline=(244, 63, 94, 255), width=int(2*scale))
    tongue_layer.putalpha(mouth_mask)
    canvas.paste(tongue_layer, (0, 0), tongue_layer)
    draw.polygon(mouth_pts, outline=(45, 12, 18, 255), width=int(max(2, 5 * scale)))

    # =========================================================================
    # --- COOL SQUARE GLASSES (MẮT KÍNH VUÔNG THÔNG THÁI / IT EXPERT) ---
    # =========================================================================
    rim_w = 160 * scale
    rim_h = 130 * scale
    rim_r = 16 * scale  # Definitely square with comfortable rounded corners
    frame_th = int(12 * scale)

    lx_c = 360 * scale
    rx_c = 664 * scale
    cy_g = 588 * scale

    l_rect = [lx_c - rim_w/2, cy_g - rim_h/2, lx_c + rim_w/2, cy_g + rim_h/2]
    r_rect = [rx_c - rim_w/2, cy_g - rim_h/2, rx_c + rim_w/2, cy_g + rim_h/2]

    # 1. Subtle drop shadow under glasses
    glasses_shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gs_draw = ImageDraw.Draw(glasses_shadow)
    sy_off_g = 10 * scale
    gs_draw.rounded_rectangle([l_rect[0], l_rect[1]+sy_off_g, l_rect[2], l_rect[3]+sy_off_g], radius=rim_r, outline=(0, 0, 0, 110), width=frame_th)
    gs_draw.rounded_rectangle([r_rect[0], r_rect[1]+sy_off_g, r_rect[2], r_rect[3]+sy_off_g], radius=rim_r, outline=(0, 0, 0, 110), width=frame_th)
    # Bridge shadow
    gs_draw.arc([l_rect[2]-8*scale, cy_g - 28*scale + sy_off_g, r_rect[0]+8*scale, cy_g + 2*scale + sy_off_g], start=190, end=350, fill=(0, 0, 0, 110), width=int(10*scale))
    glasses_shadow = glasses_shadow.filter(ImageFilter.GaussianBlur(8 * scale))
    canvas.paste(glasses_shadow, (0, 0), glasses_shadow)

    # 2. Translucent glass lens fill with subtle cyan/white shine
    lens = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(lens)
    l_draw.rounded_rectangle(l_rect, radius=rim_r, fill=(230, 245, 255, 30))
    l_draw.rounded_rectangle(r_rect, radius=rim_r, fill=(230, 245, 255, 30))

    # Diagonal lens glare lines (Anime reflection)
    glare_mask = Image.new("L", (size, size), 0)
    gm_draw = ImageDraw.Draw(glare_mask)
    gm_draw.rounded_rectangle(l_rect, radius=rim_r, fill=255)
    gm_draw.rounded_rectangle(r_rect, radius=rim_r, fill=255)

    glare_lines = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(glare_lines)
    for offset in [-15, 25]:
        gl_draw.polygon([
            (lx_c + 25 + offset, cy_g - rim_h/2 - 10),
            (lx_c + 50 + offset, cy_g - rim_h/2 - 10),
            (lx_c - 10 + offset, cy_g + rim_h/2 + 10),
            (lx_c - 35 + offset, cy_g + rim_h/2 + 10),
        ], fill=(255, 255, 255, 65))
        gl_draw.polygon([
            (rx_c + 25 + offset, cy_g - rim_h/2 - 10),
            (rx_c + 50 + offset, cy_g - rim_h/2 - 10),
            (rx_c - 10 + offset, cy_g + rim_h/2 + 10),
            (rx_c - 35 + offset, cy_g + rim_h/2 + 10),
        ], fill=(255, 255, 255, 65))
    glare_lines.putalpha(ImageChops.multiply(glare_lines.split()[3], glare_mask))
    canvas.paste(lens, (0, 0), lens)
    canvas.paste(glare_lines, (0, 0), glare_lines)

    # 3. Square frames (Glossy Black/Charcoal #18181b)
    g_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(g_layer)
    draw_g.rounded_rectangle(l_rect, radius=rim_r, outline=(24, 24, 27, 255), width=frame_th)
    draw_g.rounded_rectangle(r_rect, radius=rim_r, outline=(24, 24, 27, 255), width=frame_th)

    # Top frame glossy highlight
    draw_g.line([(l_rect[0] + rim_r, l_rect[1] + 2), (l_rect[2] - rim_r, l_rect[1] + 2)], fill=(113, 113, 122, 230), width=int(3*scale))
    draw_g.line([(r_rect[0] + rim_r, r_rect[1] + 2), (r_rect[2] - rim_r, r_rect[1] + 2)], fill=(113, 113, 122, 230), width=int(3*scale))

    # Arched bridge connecting two frames over nose
    draw_g.arc([l_rect[2] - 8*scale, cy_g - 28*scale, r_rect[0] + 8*scale, cy_g + 2*scale], start=190, end=350, fill=(24, 24, 27, 255), width=int(11*scale))
    draw_g.arc([l_rect[2] - 8*scale, cy_g - 29*scale, r_rect[0] + 8*scale, cy_g + 1*scale], start=195, end=345, fill=(113, 113, 122, 220), width=int(2*scale))

    # Temples going out to sides
    temple_y = cy_g - rim_h/2 + 18*scale
    draw_g.line([(l_rect[0] + 4*scale, temple_y), (l_rect[0] - 60*scale, temple_y - 6*scale)], fill=(24, 24, 27, 255), width=int(10*scale))
    draw_g.line([(r_rect[2] - 4*scale, temple_y), (r_rect[2] + 60*scale, temple_y - 6*scale)], fill=(24, 24, 27, 255), width=int(10*scale))

    # Golden rivets on corners
    rivet_r = 3.5 * scale
    draw_g.ellipse([l_rect[0] + 10*scale - rivet_r, temple_y - rivet_r, l_rect[0] + 10*scale + rivet_r, temple_y + rivet_r], fill=(245, 158, 11, 255))
    draw_g.ellipse([r_rect[2] - 10*scale - rivet_r, temple_y - rivet_r, r_rect[2] - 10*scale + rivet_r, temple_y + rivet_r], fill=(245, 158, 11, 255))

    canvas.paste(g_layer, (0, 0), g_layer)
    return canvas

def make_pikachu_badge_with_glasses(size=1024):
    """Badge Squircle app tile with Pikachu wearing square glasses"""
    scale = size / 1024.0
    margin = 54 * scale
    radius = 210 * scale

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 1. Shadow
    s_mask = Image.new("L", (size, size), 0)
    sm_draw = ImageDraw.Draw(s_mask)
    sm_draw.rounded_rectangle([margin + 4*scale, margin + 18*scale, size - margin - 4*scale, size - margin + 20*scale], radius=radius, fill=255)
    shadow = Image.new("RGBA", (size, size), (15, 23, 42, 130))
    shadow.putalpha(s_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24 * scale))
    canvas.paste(shadow, (0, 0), shadow)

    # 2. Tile Squircle Background (Royal Sky-Blue Gradient)
    tile_mask = Image.new("L", (size, size), 0)
    tm_draw = ImageDraw.Draw(tile_mask)
    tm_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=255)

    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tile)
    for y in range(int(margin), int(size - margin)):
        t = (y - margin) / float(size - 2 * margin)
        # Vivid Sky Blue to Royal Sapphire
        r = int(56 - t * (56 - 30))
        g = int(189 - t * (189 - 58))
        b = int(248 - t * (248 - 138))
        t_draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))
    tile.putalpha(tile_mask)
    canvas.paste(tile, (0, 0), tile)

    # 3. Gold Beveled Border
    border = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border)
    b_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, outline=(245, 158, 11, 255), width=int(10*scale))
    b_draw.rounded_rectangle([margin + 7*scale, margin + 7*scale, size - margin - 7*scale, size - margin - 7*scale], radius=radius - 7*scale, outline=(254, 240, 138, 200), width=int(3*scale))
    canvas.paste(border, (0, 0), border)

    # 4. Pikachu with Square Glasses
    pika = make_pikachu_head_with_glasses(1024)
    target_pika_size = int(820 * scale)
    pika_resized = pika.resize((target_pika_size, target_pika_size), Image.Resampling.LANCZOS)
    px = int((size - target_pika_size) / 2)
    py = int((size - target_pika_size) / 2 + 15 * scale)
    canvas.paste(pika_resized, (px, py), pika_resized)

    return canvas

def build_all_assets():
    print("🎨 Generating Pikachu Square Glasses Icons...")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

    # 1. Badge with Square Glasses (USER'S FAVORITE!)
    badge_1024 = make_pikachu_badge_with_glasses(1024)
    badge_1024.resize((512, 512), Image.Resampling.LANCZOS).save("A_THANG/pikachu_badge_preview.png", "PNG")
    badge_1024.save("A_THANG/pikachu_badge.ico", format="ICO", sizes=sizes)
    print("   [OK] A_THANG/pikachu_badge_preview.png & pikachu_badge.ico")

    # 2. Standalone Pikachu with Square Glasses (Transparent Background)
    pure_1024 = make_pikachu_head_with_glasses(1024)
    pure_1024.resize((512, 512), Image.Resampling.LANCZOS).save("A_THANG/pikachu_preview.png", "PNG")
    pure_1024.save("A_THANG/pikachu.ico", format="ICO", sizes=sizes)
    print("   [OK] A_THANG/pikachu_preview.png & pikachu.ico")

    # 3. Update BAT script to name shortcut "Family CN23" and use pikachu_badge.ico
    bat_content = """@echo off
:: ===============================================================================
:: CỔNG DỊCH VỤ NỘI BỘ - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
:: - Mở trực tiếp bằng Google Chrome hoặc Microsoft Edge
:: - Biểu tượng Pikachu Đeo Kính Vuông Nổi Bật (Chống bấm nhầm 100%)
:: - Tên Shortcut Desktop: "Family CN23"
:: ===============================================================================
chcp 65001 >nul
title Cài đặt Phím tắt "Family CN23" Pikachu Kính Vuông
color 0E

echo.
echo ===============================================================================
echo            FAMILY CN23 - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
echo                 (Hệ thống Lịch Tuần & Tiếp nhận IT Helpdesk)
echo ===============================================================================
echo.
echo [*] BƯỚC 1: Đang thiết lập Biểu tượng Pikachu Kính Vuông nổi bật...

:: Tạo thư mục lưu Icon ứng dụng trong LocalAppData của cán bộ
set "APP_DIR=%LOCALAPPDATA%\\VPDK23"
if not exist "%APP_DIR%" mkdir "%APP_DIR%" 2>nul

:: Ưu tiên 1: Icon Badge Pikachu Kính Vuông nền xanh viền vàng (Mẫu chính thức)
set "ICON_FILE=%APP_DIR%\\pikachu_badge.ico"

if exist "%~dp0pikachu_badge.ico" (
    copy /y "%~dp0pikachu_badge.ico" "%ICON_FILE%" >nul 2>&1
)

:: Ưu tiên 2: Tải trực tiếp từ máy chủ GitHub chính thức
if not exist "%ICON_FILE%" (
    curl -s -L "https://raw.githubusercontent.com/QuanDo610/vpdk-cn23/main/pikachu_badge.ico" -o "%ICON_FILE%" 2>nul
)

:: Ưu tiên 3: Icon pikachu.ico có sẵn
if not exist "%ICON_FILE%" (
    if exist "%~dp0pikachu.ico" (
        copy /y "%~dp0pikachu.ico" "%ICON_FILE%" >nul 2>&1
    )
)

:: Ưu tiên 4: Icon huy hiệu cũ dự phòng
if not exist "%ICON_FILE%" (
    if exist "%~dp0vpdk23.ico" (
        copy /y "%~dp0vpdk23.ico" "%ICON_FILE%" >nul 2>&1
    )
)

:: Ưu tiên 5: Icon hệ thống Windows
if not exist "%ICON_FILE%" (
    set "ICON_FILE=%SystemRoot%\\System32\\shell32.dll,220"
    echo   [!] Tạm thời dùng biểu tượng hệ thống Windows.
) else (
    echo   [OK] Đã thiết lập thành công Biểu tượng Pikachu Đeo Kính Vuông sắc nét.
)

echo.
echo [*] BƯỚC 2: Đang tự động dò tìm trình duyệt Google Chrome hoặc Microsoft Edge...

set "BROWSER_EXE="
set "BROWSER_NAME="

:: Dò tìm Google Chrome
if exist "%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
)

:: Nếu không có Chrome, tự động chuyển sang Microsoft Edge (mặc định 100% trên Win 10/11)
if not defined BROWSER_EXE (
    if exist "%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    ) else if exist "%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

:: Dò tìm bằng lệnh where nếu cài ở ổ đĩa khác
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where chrome.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Google Chrome"
    )
)
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where msedge.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

if not defined BROWSER_EXE (
    set "BROWSER_EXE=%SystemRoot%\\explorer.exe"
    set "BROWSER_NAME=Trình duyệt mặc định"
)

echo   [OK] Trình duyệt chuyên dụng: %BROWSER_NAME%

echo.
echo [*] BƯỚC 3: Đang khởi tạo Lối tắt "Family CN23" ngoài Desktop...

set "TARGET_URL=https://quando610.github.io/vpdk-cn23/index.html"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $desktop = [Environment]::GetFolderPath('Desktop'); ^
   $name = 'Family CN23.lnk'; ^
   $p1 = Join-Path $desktop $name; ^
   function MakeLnk($dest) { ^
       $s = $ws.CreateShortcut($dest); ^
       $s.TargetPath = '%BROWSER_EXE%'; ^
       $s.Arguments = '%TARGET_URL%'; ^
       $s.IconLocation = '%ICON_FILE%'; ^
       $s.Description = 'Family CN23 - Cổng Dịch Vụ Nội Bộ Chi Nhánh 23'; ^
       $s.WorkingDirectory = [System.IO.Path]::GetDirectoryName('%BROWSER_EXE%'); ^
       $s.Save(); ^
   }; ^
   MakeLnk($p1); ^
   Write-Host '   -> Da tao Shortcut [Family CN23] thanh cong tai:' $p1 -ForegroundColor Yellow; ^
   if (Test-Path \"$env:USERPROFILE\\Desktop\") { ^
       $p2 = Join-Path \"$env:USERPROFILE\\Desktop\" $name; ^
       if ($p2 -ne $p1) { MakeLnk($p2); } ^
   }; ^
   if (Test-Path \"$env:USERPROFILE\\OneDrive\\Desktop\") { ^
       $p3 = Join-Path \"$env:USERPROFILE\\OneDrive\\Desktop\" $name; ^
       if ($p3 -ne $p1) { MakeLnk($p3); } ^
   }; ^
   Remove-Item \"$desktop\\Cổng Dịch Vụ - Chi Nhánh 23.lnk\" -ErrorAction SilentlyContinue; ^
   Remove-Item \"$desktop\\Cổng Dịch Vụ - Chi Nhánh 23.url\" -ErrorAction SilentlyContinue; ^
   Remove-Item \"$desktop\\Cong Dich Vu - Chi Nhanh 23.url\" -ErrorAction SilentlyContinue; ^
   Remove-Item \"$desktop\\Family CN23.url\" -ErrorAction SilentlyContinue;"

echo.
echo ===============================================================================
echo  [V] HOÀN TẤT THÀNH CÔNG!
echo      - Lối tắt [Family CN23] với icon Pikachu Kính Vuông đã được cài ngoài Desktop.
echo      - Cố định mở chuyên dụng qua: %BROWSER_NAME%.
echo ===============================================================================
echo.
echo [*] Đang tự động mở Family CN23 lần đầu bằng %BROWSER_NAME%...
start "" "%BROWSER_EXE%" "%TARGET_URL%"

echo.
echo -------------------------------------------------------------------------------
echo  HƯỚNG DẪN DÀNH CHO CÁN BỘ:
echo  1. Hằng ngày, cán bộ chỉ cần bấm đúp vào biểu tượng Pikachu "Family CN23"
echo     ngay trên màn hình Desktop.
echo  2. Đăng nhập bằng Số CCCD (12 số) và Mật khẩu được cấp.
echo -------------------------------------------------------------------------------
echo.
echo Nhấn phím bất kỳ để đóng cửa sổ này...
pause >nul
exit /b
"""

    bat_path = "A_THANG/Tao_Icon_Desktop_VPDK23.bat"
    with open(bat_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(bat_content)
    print("   [OK] A_THANG/Tao_Icon_Desktop_VPDK23.bat")

    # Also create Cai_Dat_Family_CN23.bat as alias
    bat_alias = "A_THANG/Cai_Dat_Family_CN23.bat"
    with open(bat_alias, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(bat_content)
    print("   [OK] A_THANG/Cai_Dat_Family_CN23.bat")

    # 4. Package ZIP file (Both Tao_Icon_Desktop_VPDK23.zip and Family_CN23_Desktop.zip)
    for zname in ["Tao_Icon_Desktop_VPDK23.zip", "Family_CN23_Desktop.zip"]:
        zip_path = os.path.join("A_THANG", zname)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(bat_path, arcname="Tao_Icon_Desktop_VPDK23.bat")
            z.write(bat_alias, arcname="Cai_Dat_Family_CN23.bat")
            z.write("A_THANG/pikachu_badge.ico", arcname="pikachu_badge.ico")
            z.write("A_THANG/pikachu.ico", arcname="pikachu.ico")
            z.write("A_THANG/vpdk23.ico", arcname="vpdk23.ico")
            z.write("A_THANG/pikachu_badge_preview.png", arcname="pikachu_badge_preview.png")
            z.write("A_THANG/pikachu_preview.png", arcname="pikachu_preview.png")
        print(f"   [OK] Packaged {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    build_all_assets()
