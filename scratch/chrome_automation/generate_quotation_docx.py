import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_run(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, color_rgb=(15, 23, 42)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_header_block(doc):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    cell_left = tbl.cell(0, 0)
    cell_left.width = Inches(3.2)
    p_cq = cell_left.paragraphs[0]
    p_cq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_cq.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM\n")
    format_run(r1, size_pt=10, bold=True)
    r2 = p_cq.add_run("CHI NHÁNH SỐ 23\n")
    format_run(r2, size_pt=10.5, bold=True, color_rgb=(2, 132, 199))
    r3 = p_cq.add_run("Số: ...... /BG-CN23")
    format_run(r3, size_pt=9.5, italic=True)

    cell_right = tbl.cell(0, 1)
    cell_right.width = Inches(3.8)
    p_tn = cell_right.paragraphs[0]
    p_tn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p_tn.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    format_run(r4, size_pt=10, bold=True)
    r5 = p_tn.add_run("Độc lập - Tự do - Hạnh phúc\n")
    format_run(r5, size_pt=10.5, bold=True)
    r6 = p_tn.add_run("Thủ Dầu Một, ngày 28 tháng 09 năm 2026")
    format_run(r6, size_pt=9.5, italic=True)

    for cell in tbl.rows[0].cells:
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(4)

def add_signature_block(doc, author_name="Đỗ Trọng Minh Quân"):
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(14)
    
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    cell_left = tbl.cell(0, 0)
    cell_left.width = Inches(3.5)
    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_nl = p_left.add_run("Nơi nhận:\n")
    format_run(r_nl, size_pt=10, bold=True, italic=True)
    r_nl2 = p_left.add_run("- Như trên (báo cáo);\n- Chị Bùi Thị Minh Nguyệt (phối hợp);\n- Lưu: Hồ sơ kế hoạch CNTT.")
    format_run(r_nl2, size_pt=9.5, italic=True)

    cell_right = tbl.cell(0, 1)
    cell_right.width = Inches(3.5)
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_right.add_run("NGƯỜI LẬP BÁO GIÁ\n\n\n\n\n")
    format_run(r_title, size_pt=11, bold=True)
    r_name = p_right.add_run(author_name)
    format_run(r_name, size_pt=11.5, bold=True, color_rgb=(15, 23, 42))

    for cell in tbl.rows[0].cells:
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)

def create_quotation_docx(output_path):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.8)

    add_header_block(doc)

    # Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("BẢNG DỰ TOÁN & BÁO GIÁ DỊCH VỤ PHẦN MỀM\nXÂY DỰNG MỚI HỆ THỐNG OERP ĐIỀU HÀNH TÁC NGHIỆP ĐẤT ĐAI")
    format_run(r_t, size_pt=13.5, bold=True, color_rgb=(3, 105, 161))

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("(Áp dụng đơn giá ưu đãi nội bộ: 20 USD / giờ làm việc - Tỷ giá: 25.400 VNĐ/USD)")
    format_run(r_sub, size_pt=10.5, italic=True)

    # Kính gửi
    p_kg = doc.add_paragraph()
    p_kg.paragraph_format.space_after = Pt(10)
    p_kg.paragraph_format.left_indent = Inches(0.5)
    r_kg = p_kg.add_run("Kính gửi: ")
    format_run(r_kg, size_pt=11.5, bold=True)
    r_kg2 = p_kg.add_run("Chị Nguyễn Thị Bích Tuyền\n")
    format_run(r_kg2, size_pt=11.5, bold=True, color_rgb=(2, 132, 199))
    r_dg = p_kg.add_run("Đồng gửi: ")
    format_run(r_dg, size_pt=11, bold=True)
    r_dg2 = p_kg.add_run("Chị Bùi Thị Minh Nguyệt (Bộ phận chuyên môn)")
    format_run(r_dg2, size_pt=11, italic=True)

    # Lời mở đầu
    p_in = doc.add_paragraph()
    p_in.paragraph_format.line_spacing = 1.2
    p_in.paragraph_format.space_after = Pt(8)
    r_intro = p_in.add_run(
        "Căn cứ theo yêu cầu rà soát, đánh giá phương án thay thế phần mềm OERP thuê ngoài hiện tại bằng phương án xây dựng mới độc lập, "
        "nhằm mục tiêu làm chủ hoàn toàn mã nguồn (Source Code), dữ liệu và có thể chủ động sửa chữa, bảo trì lâu dài cho Chi nhánh; "
        "tôi xin gửi bảng dự toán khối lượng công việc, thời gian và chi phí lập trình theo đơn giá hỗ trợ ưu đãi nội bộ là "
    )
    format_run(r_intro, size_pt=11)
    r_rate = p_in.add_run("20 USD / giờ (~ 508.000 VNĐ/giờ)")
    format_run(r_rate, size_pt=11, bold=True, color_rgb=(180, 83, 9))
    r_intro2 = p_in.add_run(" chi tiết như sau:")
    format_run(r_intro2, size_pt=11)

    # Bảng chi tiết
    tbl = doc.add_table(rows=1, cols=5)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    headers = ["STT", "Giai đoạn & Nội dung công việc chi tiết", "Thời lượng\n(Giờ)", "Đơn giá\n(USD)", "Thành tiền\n(VNĐ)"]
    col_w = [Inches(0.5), Inches(3.3), Inches(0.9), Inches(0.9), Inches(1.5)]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.width = col_w[i]
        set_cell_background(cell, "0284C7")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        format_run(r, size_pt=10, bold=True, color_rgb=(255, 255, 255))

    RATE_USD = 20
    EXCHANGE_RATE = 25400

    items = [
        # Giai đoạn 1
        ("I", "KHẢO SÁT & THU THẬP YÊU CẦU (REQUIREMENTS)", 140, "header"),
        ("1.1", "Phỏng vấn các bộ phận: Một Cửa, Đo đạc, Thẩm tra, Thuế, Lãnh đạo", 40, "item"),
        ("1.2", "Rà soát quy trình TTHC đất đai, mẫu phiếu hẹn, biên nhận, sổ theo dõi", 30, "item"),
        ("1.3", "Xây dựng tài liệu đặc tả yêu cầu chức năng phần mềm (SRS)", 40, "item"),
        ("1.4", "Thiết kế Wireframe & Prototype giao diện mẫu Figma cho 9 phân hệ", 30, "item"),

        # Giai đoạn 2
        ("II", "THIẾT KẾ KIẾN TRÚC HỆ THỐNG & CƠ SỞ DỮ LIỆU", 90, "header"),
        ("2.1", "Thiết kế mô hình CSDL quan hệ (ERD Schema) tối ưu, chuẩn hóa", 40, "item"),
        ("2.2", "Thiết kế kiến trúc Backend API, Security RBAC (phân quyền đa cấp phòng ban)", 30, "item"),
        ("2.3", "Thiết kế giải pháp lưu trữ File số hóa (tích hợp NAS Synology nội bộ)", 20, "item"),

        # Giai đoạn 3
        ("III", "LẬP TRÌNH BACKEND & CƠ SỞ DỮ LIỆU (CORE API)", 460, "header"),
        ("3.1", "Module Phân quyền, Xác thực bảo mật cán bộ & Ghi nhật ký (Audit Log)", 40, "item"),
        ("3.2", "Module Một Cửa: Tiếp nhận hồ sơ, sinh mã biên nhận, tra cứu ngăn chặn", 80, "item"),
        ("3.3", "Module Quy trình: Phân công đo đạc, luân chuyển nội bộ, tính thuế", 90, "item"),
        ("3.4", "Module Quản lý file scan: Upload, nén ảnh, bảo mật trích lục, tài liệu", 60, "item"),
        ("3.5", "Module Trả kết quả: Bàn giao sổ đỏ, ký nhận, xuất / nhập dữ liệu Excel", 40, "item"),
        ("3.6", "Module Tra cứu hồ sơ Một Cửa & Dashboard giám sát luồng trích đo", 50, "item"),
        ("3.7", "Module Báo cáo thống kê CCHC, lọc tham số & xuất báo cáo lãnh đạo", 60, "item"),
        ("3.8", "Tích hợp cổng SMS Brandname tự động & Engine xuất văn bản Word/PDF", 40, "item"),

        # Giai đoạn 4
        ("IV", "LẬP TRÌNH GIAO DIỆN CLIENT (FRONTEND DEVELOPMENT)", 420, "header"),
        ("4.1", "Xây dựng khung ứng dụng (Layout, Navigation, Component Design System)", 60, "item"),
        ("4.2", "Lập trình 9 phân hệ giao diện người dùng tương thích API Backend", 260, "item"),
        ("4.3", "Lập trình Dashboard biểu đồ trực quan, tối ưu tốc độ tải và responsive", 60, "item"),
        ("4.4", "Tối ưu thao tác phím tắt, in biên nhận nhanh tại quầy Một Cửa", 40, "item"),

        # Giai đoạn 5
        ("V", "CHUYỂN ĐỔI & LÀM SẠCH DỮ LIỆU CŨ (DATA MIGRATION)", 90, "header"),
        ("5.1", "Viết script trích xuất, làm sạch và chuyển đổi CSDL cũ sang hệ thống mới", 60, "item"),
        ("5.2", "Đối soát tính toàn vẹn dữ liệu (Data Integrity check) hồ sơ lịch sử", 30, "item"),

        # Giai đoạn 6
        ("VI", "KIỂM THỬ CHẤT LƯỢNG & BẢO MẬT (QA/QC & TESTING)", 180, "header"),
        ("6.1", "Kiểm thử chức năng chi tiết theo từng luồng nghiệp vụ đất đai", 70, "item"),
        ("6.2", "Kiểm thử chịu tải cao điểm Một Cửa (Load & Stress Testing)", 30, "item"),
        ("6.3", "Kiểm thử an toàn thông tin & bảo mật (Security Pentest chống lộ CSDL)", 40, "item"),
        ("6.4", "Tổ chức kiểm thử người dùng thực tế (UAT) với cán bộ Chi nhánh", 40, "item"),

        # Giai đoạn 7
        ("VII", "TRIỂN KHAI, BÀN GIAO & ĐÀO TẠO (DELIVERY)", 80, "header"),
        ("7.1", "Cài đặt hệ thống trên cụm máy chủ HP cơ quan & cấu hình mạng an toàn", 30, "item"),
        ("7.2", "Soạn thảo bộ tài liệu Hướng dẫn sử dụng và Tài liệu kỹ thuật quản trị", 25, "item"),
        ("7.3", "Đào tạo, chuyển giao và trực tiếp hướng dẫn cán bộ sử dụng", 25, "item"),

        # Giai đoạn 8
        ("VIII", "BẢO TRÌ & HỖ TRỢ VẬN HÀNH (MAINTENANCE - 3 THÁNG ĐẦU)", 140, "header"),
        ("8.1", "Trực kỹ thuật xử lý sự cố trong giờ hành chính tiếp dân (SLA khẩn cấp)", 80, "item"),
        ("8.2", "Cân chỉnh, tối ưu hiệu năng CSDL định kỳ, tự động sao lưu an toàn vào NAS", 60, "item")
    ]

    total_hours = 0
    total_cost_usd = 0
    total_cost_vnd = 0

    for stt, name, hours, row_type in items:
        row = tbl.add_row()
        cost_usd = hours * RATE_USD
        cost_vnd = cost_usd * EXCHANGE_RATE

        if row_type == "header":
            # Dòng tiêu đề giai đoạn
            for col_idx in range(5):
                cell = row.cells[col_idx]
                cell.width = col_w[col_idx]
                set_cell_background(cell, "F1F5F9")
                set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                p = cell.paragraphs[0]
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(stt)
                    format_run(r, size_pt=10, bold=True, color_rgb=(3, 105, 161))
                elif col_idx == 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    r = p.add_run(name)
                    format_run(r, size_pt=10, bold=True, color_rgb=(15, 23, 42))
                elif col_idx == 2:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(f"{hours} h")
                    format_run(r, size_pt=10, bold=True)
                elif col_idx == 3:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    r = p.add_run(f"${cost_usd:,}")
                    format_run(r, size_pt=10, bold=True)
                elif col_idx == 4:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    r = p.add_run(f"{cost_vnd:,.0f} đ")
                    format_run(r, size_pt=10, bold=True, color_rgb=(3, 105, 161))
            total_hours += hours
            total_cost_usd += cost_usd
            total_cost_vnd += cost_vnd
        else:
            # Dòng con
            for col_idx in range(5):
                cell = row.cells[col_idx]
                cell.width = col_w[col_idx]
                set_cell_background(cell, "FFFFFF")
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(stt)
                    format_run(r, size_pt=9.5, italic=True)
                elif col_idx == 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    r = p.add_run(name)
                    format_run(r, size_pt=9.5)
                elif col_idx == 2:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(f"{hours}")
                    format_run(r, size_pt=9.5)
                elif col_idx == 3:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    r = p.add_run(f"${cost_usd:,}")
                    format_run(r, size_pt=9.5)
                elif col_idx == 4:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    r = p.add_run(f"{cost_vnd:,.0f} đ")
                    format_run(r, size_pt=9.5)

    # DÒNG TỔNG CỘNG
    row_total = tbl.add_row()
    for col_idx in range(5):
        cell = row_total.cells[col_idx]
        cell.width = col_w[col_idx]
        set_cell_background(cell, "FEF3C7")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        if col_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run("★")
            format_run(r, size_pt=11, bold=True, color_rgb=(180, 83, 9))
        elif col_idx == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run("TỔNG CỘNG TOÀN BỘ CHU TRÌNH DỰ ÁN")
            format_run(r, size_pt=10.5, bold=True, color_rgb=(180, 83, 9))
        elif col_idx == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f"{total_hours:,} h")
            format_run(r, size_pt=10.5, bold=True, color_rgb=(180, 83, 9))
        elif col_idx == 3:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(f"${total_cost_usd:,}")
            format_run(r, size_pt=10.5, bold=True, color_rgb=(180, 83, 9))
        elif col_idx == 4:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(f"{total_cost_vnd:,.0f} đ")
            format_run(r, size_pt=11, bold=True, color_rgb=(185, 28, 28))

    # Viền bảng
    for row in tbl.rows:
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
            tcPr.append(tcBorders)

    # Ghi chú tổng tiền bằng chữ
    p_text_sum = doc.add_paragraph()
    p_text_sum.paragraph_format.space_before = Pt(8)
    p_text_sum.paragraph_format.space_after = Pt(8)
    r_ts = p_text_sum.add_run("Tổng chi phí dự toán bằng chữ: ")
    format_run(r_ts, size_pt=11, bold=True)
    r_ts2 = p_text_sum.add_run("Tám trăm mười hai triệu tám trăm nghìn đồng chẵn (tương đương 32.000 USD).")
    format_run(r_ts2, size_pt=11, bold=True, italic=True, color_rgb=(185, 28, 28))

    # Đánh giá tiến độ & Đề xuất so sánh
    h_eval = doc.add_paragraph()
    h_eval.paragraph_format.space_before = Pt(10)
    h_eval.paragraph_format.space_after = Pt(4)
    r_he = h_eval.add_run("GHI CHÚ VỀ TIẾN ĐỘ THỰC HIỆN & KHUYẾN NGHỊ THỰC TẾ:")
    format_run(r_he, size_pt=11.5, bold=True, color_rgb=(3, 105, 161))

    bullets = [
        ("Thời gian thực hiện:", " Với khối lượng 1.600 giờ, nếu 01 nhân sự làm việc liên tục toàn thời gian (160 giờ/tháng) sẽ mất khoảng 10 tháng; nếu triển khai theo nhóm dự án 3-4 người sẽ mất khoảng 4-5 tháng."),
        ("Bàn giao sản phẩm:", " Bàn giao 100% Mã nguồn gốc (Full Source Code C# & Angular), CSDL mới độc lập, tài liệu thiết kế hệ thống và cam kết bảo hành, hỗ trợ kỹ thuật trực tiếp trong 3 tháng đầu."),
        ("Khuyến nghị so sánh phương án:", " Mức dự toán 812.800.000 đ là chi phí xây mới hoàn toàn phần mềm đạt chuẩn. Tuy nhiên, căn cứ theo tiêu chí tiết kiệm ngân sách 'Tăng xin giảm mua', nếu cơ quan lựa chọn PHƯƠNG ÁN DI DỜI BẢN CHẠY VÀ CSDL CŨ VỀ MÁY CHỦ HP CÓ SẴN TẠI CHI NHÁNH thì CHI PHÍ ĐẦU TƯ LÀ 0 ĐỒNG và cắt giảm được ngay 9.600.000 đ/năm tiền thuê ngoài. Tôi trân trọng báo cáo đầy đủ cả 2 phương án để Lãnh đạo xem xét, quyết định.")
    ]

    for b_title, b_desc in bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(3)
        r_bt = p_b.add_run(b_title + " ")
        format_run(r_bt, size_pt=10.5, bold=True)
        r_bd = p_b.add_run(b_desc)
        format_run(r_bd, size_pt=10.5)

    add_signature_block(doc)
    doc.save(output_path)
    print(f"✅ Đã tạo thành công Báo giá Word: {output_path}")

if __name__ == "__main__":
    out_path = "/Users/admin/Desktop/BINHDUONG/Bang_bao_gia_du_an_OERP_software.docx"
    create_quotation_docx(out_path)
