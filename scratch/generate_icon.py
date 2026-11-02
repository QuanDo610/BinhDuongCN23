import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_portal_icon():
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Outer drop shadow
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    margin = 16
    # Rounded rectangle badge
    radius = 48
    sdraw.rounded_rectangle(
        [margin + 4, margin + 8, size - margin - 4, size - margin + 8],
        radius=radius,
        fill=(0, 0, 0, 110)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow, (0, 0), shadow)

    # 2. Main base: Glossy deep royal blue gradient
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(base)
    
    # We create a gradient mask
    for y in range(margin, size - margin):
        ratio = (y - margin) / (size - 2 * margin)
        # Gradient from rich royal blue (#1e3a8a -> #1d4ed8 -> #0284c7)
        r = int(24 + ratio * 10)
        g = int(58 + ratio * 60)
        b = int(140 + ratio * 90)
        bdraw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))
        
    # Mask to rounded rectangle
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=255
    )
    
    # Gold border
    gold_border = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gold_border)
    gdraw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        outline=(245, 158, 11, 230), # Rich gold
        width=4
    )
    # Inner subtle rim
    gdraw.rounded_rectangle(
        [margin + 3, margin + 3, size - margin - 3, size - margin - 3],
        radius=radius - 2,
        outline=(254, 240, 138, 140), # Light gold rim
        width=1
    )

    base.putalpha(mask)
    img.paste(base, (0, 0), base)
    img.paste(gold_border, (0, 0), gold_border)

    # 3. Central Shield Emblem (Golden / White Shield)
    shield_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shield_img)
    
    cx, cy = size // 2, size // 2 - 10
    sw = 62  # half width
    sh = 70  # shield height
    
    # Shield polygon points
    shield_pts = [
        (cx - sw, cy - 42),
        (cx + sw, cy - 42),
        (cx + sw, cy + 12),
        (cx, cy + sh),
        (cx - sw, cy + 12)
    ]
    
    # Shield shadow
    s_shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ss_draw = ImageDraw.Draw(s_shadow)
    ss_draw.polygon([(x, y + 4) for x, y in shield_pts], fill=(0, 0, 0, 120))
    s_shadow = s_shadow.filter(ImageFilter.GaussianBlur(5))
    img.paste(s_shadow, (0, 0), s_shadow)

    # Shield fill (Dark cyan / sapphire)
    s_draw.polygon(shield_pts, fill=(15, 23, 42, 240), outline=(245, 158, 11, 255), width=3)
    
    # Golden inner shield accent
    inner_pts = [
        (cx - sw + 6, cy - 36),
        (cx + sw - 6, cy - 36),
        (cx + sw - 6, cy + 9),
        (cx, cy + sh - 8),
        (cx - sw + 6, cy + 9)
    ]
    s_draw.polygon(inner_pts, outline=(253, 224, 71, 160), width=1)

    img.paste(shield_img, (0, 0), shield_img)

    # 4. Text or Emblem inside Shield: "23" in bold gold with star
    draw = ImageDraw.Draw(img)
    
    # Golden star on top inside shield
    def draw_star(draw_ctx, center, r_outer, r_inner, fill):
        pts = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            pts.append((center[0] + r * math.cos(angle), center[1] + r * math.sin(angle)))
        draw_ctx.polygon(pts, fill=fill)

    draw_star(draw, (cx, cy - 20), 12, 5, fill=(251, 191, 36, 255))

    # Number "23" large and bold
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw "23"
    t_23 = "23"
    bbox = draw.textbbox((0, 0), t_23, font=font_large)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = cy - 2
    # Shadow for text
    draw.text((tx + 1, ty + 2), t_23, font=font_large, fill=(0, 0, 0, 180))
    # Golden / white text
    draw.text((tx, ty), t_23, font=font_large, fill=(255, 255, 255, 255))

    # Bottom banner / pill: "VPĐK ĐẤT ĐAI"
    bw = 148
    bh = 26
    bx1 = cx - bw // 2
    by1 = size - margin - 38
    bx2 = cx + bw // 2
    by2 = by1 + bh
    
    # Banner shadow
    b_shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bs_draw = ImageDraw.Draw(b_shadow)
    bs_draw.rounded_rectangle([bx1, by1 + 2, bx2, by2 + 2], radius=13, fill=(0, 0, 0, 100))
    b_shadow = b_shadow.filter(ImageFilter.GaussianBlur(3))
    img.paste(b_shadow, (0, 0), b_shadow)

    # Banner body
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=13, fill=(245, 158, 11, 255), outline=(254, 240, 138, 255), width=1)
    
    banner_txt = "VPĐK CN 23"
    bbox_b = draw.textbbox((0, 0), banner_txt, font=font_small)
    btw, bth = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    btx = cx - btw // 2
    bty = by1 + (bh - bth) // 2 - 2
    draw.text((btx, bty), banner_txt, font=font_small, fill=(15, 23, 42, 255))

    # Save multi-size ICO
    ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save("A_THANG/vpdk23.ico", format="ICO", sizes=ico_sizes)
    img.save("A_THANG/vpdk23_preview.png", format="PNG")
    print("Created A_THANG/vpdk23.ico and preview png successfully!")

create_portal_icon()
