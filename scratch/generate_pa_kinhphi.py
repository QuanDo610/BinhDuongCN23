import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_pa_document():
    doc = docx.Document()

    # 1. Page Margins & A4
    section = doc.sections[0]
    section.page_width = Inches(8.27)    # 210mm
    section.page_height = Inches(11.69)  # 297mm
    section.top_margin = Inches(0.79)    # 20mm
    section.bottom_margin = Inches(0.79) # 20mm
    section.left_margin = Inches(1.18)   # 30mm
    section.right_margin = Inches(0.59)  # 15mm

    # 2. Header Page numbering (center, skip first page)
    section.different_first_page_header_footer = True
    header = section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_p.paragraph_format.space_before = Pt(0)
    header_p.paragraph_format.space_after = Pt(0)
    
    # Add page number XML
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    header_p._p.append(fldSimple)
    for run in header_p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)

    # 3. Base styles
    normal_style = doc.styles['Normal']
    font = normal_style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)

    # Helper function to remove table borders
    def remove_table_borders(table):
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>' % nsdecls('w'))
                tcPr.append(tcBorders)

    # Helper function to set cell padding
    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(r'<w:tcMar %s><w:top w:w="%d" w:type="dxa"/><w:bottom w:w="%d" w:type="dxa"/><w:left w:w="%d" w:type="dxa"/><w:right w:w="%d" w:type="dxa"/></w:tcMar>' % (nsdecls('w'), top, bottom, left, right))
        tcPr.append(tcMar)

    # Helper function to set table cell borders (all solid thin gray/black)
    def set_cell_box_borders(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>' % nsdecls('w'))
        tcPr.append(tcBorders)

    # ==========================================
    # HEADER CƠ QUAN VÀ QUỐC HIỆU
    # ==========================================
    t_header = doc.add_table(rows=1, cols=2)
    t_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_header.autofit = False
    remove_table_borders(t_header)

    t_header.rows[0].cells[0].width = Inches(3.0)
    t_header.rows[0].cells[1].width = Inches(3.5)
    set_cell_margins(t_header.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_header.rows[0].cells[1], 0, 0, 0, 0)

    c0 = t_header.rows[0].cells[0]
    c1 = t_header.rows[0].cells[1]

    # Bên trái: Cơ quan
    p = c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("SỞ NÔNG NGHIỆP VÀ MÔI TRƯỜNG\nVĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r = p.add_run("CHI NHÁNH SỐ 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_line_cq = c0.add_paragraph()
    p_line_cq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_cq.paragraph_format.space_before = Pt(0)
    p_line_cq.paragraph_format.space_after = Pt(2)
    r = p_line_cq.add_run("————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(9)

    p_qhns = c0.add_paragraph()
    p_qhns.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qhns.paragraph_format.space_before = Pt(0)
    p_qhns.paragraph_format.space_after = Pt(0)
    r = p_qhns.add_run("Mã số QHNS: 1122149")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    # Bên phải: Quốc hiệu
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r = p.add_run("Độc lập - Tự do - Hạnh phúc")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p_line_qh = c1.add_paragraph()
    p_line_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_qh.paragraph_format.space_before = Pt(0)
    p_line_qh.paragraph_format.space_after = Pt(2)
    r = p_line_qh.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    p_ngay = c1.add_paragraph()
    p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ngay.paragraph_format.space_before = Pt(0)
    p_ngay.paragraph_format.space_after = Pt(0)
    r = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày 07 tháng 10 năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    # TIÊU ĐỀ PHƯƠNG ÁN
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("PHƯƠNG ÁN DỰ TOÁN KINH PHÍ")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.15
    r = p_sub.add_run("Về việc xin cấp kinh phí trang bị phương tiện PCCC (26 bình chữa cháy),\nthiết bị làm việc (01 máy in 2 mặt A4, 01 ghế ngồi Giám đốc) và cải tạo\nsửa chữa chống thấm dột kho lưu trữ hồ sơ địa chính của Chi nhánh số 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_line_ty = doc.add_paragraph()
    p_line_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_ty.paragraph_format.space_before = Pt(0)
    p_line_ty.paragraph_format.space_after = Pt(12)
    r = p_line_ty.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    # Helper function for Section Headings
    def add_section_heading(roman_num, title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"{roman_num}. {title_text}")
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    def add_subsection_heading(num_text, title_text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.45)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"{num_text}. {title_text}")
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    def add_clause(text, indent_level=1, bold_prefix="", italic_prefix=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.first_line_indent = Inches(0.45 * indent_level)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(13)
        if italic_prefix:
            r_pre2 = p.add_run(italic_prefix)
            r_pre2.italic = True
            r_pre2.font.name = "Times New Roman"
            r_pre2.font.size = Pt(13)
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13)

    # -------------------------------------------------------------
    # PHẦN I: CĂN CỨ PHÁP LÝ VÀ SỰ CẦN THIẾT
    # -------------------------------------------------------------
    add_section_heading("I", "CĂN CỨ PHÁP LÝ VÀ SỰ CẦN THIẾT XÂY DỰNG PHƯƠNG ÁN")
    
    add_subsection_heading("1", "Căn cứ pháp lý")
    cancu_list = [
        ("Căn cứ Luật Quản lý, sử dụng tài sản công ", "ngày 21 tháng 6 năm 2017; Luật sửa đổi, bổ sung một số điều của Luật Đấu thầu, Luật Đầu tư theo phương thức đối tác công tư, Luật Hải quan, Luật Thuế giá trị gia tăng, Luật Thuế xuất khẩu, thuế nhập khẩu, Luật Đầu tư, Luật Đầu tư công, Luật Quản lý sử dụng tài sản công số 90/2025/QH15 ngày 25 tháng 6 năm 2025;"),
        ("Căn cứ Luật Phòng cháy và chữa cháy ", "ngày 29 tháng 6 năm 2001 và Luật sửa đổi, bổ sung một số điều của Luật Phòng cháy và chữa cháy ngày 22 tháng 11 năm 2013;"),
        ("Căn cứ Luật Đấu thầu số 22/2023/QH15 ", "ngày 23 tháng 6 năm 2023; Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu;"),
        ("Căn cứ Nghị định số 136/2020/NĐ-CP ", "ngày 24 tháng 11 năm 2020 và Nghị định số 50/2024/NĐ-CP ngày 10 tháng 5 năm 2024 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 136/2020/NĐ-CP quy định chi tiết thi hành Luật Phòng cháy và chữa cháy;"),
        ("Căn cứ Tiêu chuẩn Quốc gia TCVN 3890:2023 ", "về Phòng cháy chữa cháy - Phương tiện phòng cháy và chữa cháy cho nhà và công trình - Trang bị, bố trí;"),
        ("Căn cứ Quyết định số 50/2017/QĐ-TTg ", "ngày 31 tháng 12 năm 2017 của Thủ tướng Chính phủ quy định tiêu chuẩn, định mức sử dụng máy móc, thiết bị;"),
        ("Căn cứ Nghị định số 155/2025/NĐ-CP ", "ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;"),
        ("Căn cứ Nghị định số 186/2025/NĐ-CP ", "ngày 01 tháng 7 năm 2025 và Nghị định số 286/2025/NĐ-CP ngày 03 tháng 11 năm 2025 của Chính phủ về quản lý, sử dụng tài sản công;"),
        ("Căn cứ Nghị định số 60/2021/NĐ-CP ", "ngày 21 tháng 6 năm 2021 và Nghị định số 111/2025/NĐ-CP ngày 22 tháng 5 năm 2025 của Chính phủ quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;"),
        ("Căn cứ Thông tư số 65/2021/TT-BTC ", "ngày 29 tháng 7 năm 2021 của Bộ Tài chính quy định về lập dự toán, quản lý, sử dụng và quyết toán kinh phí bảo dưỡng, sửa chữa tài sản công;"),
        ("Căn cứ Quyết định số 1886/QĐ-UBND ", "ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố Hồ Chí Minh về tổ chức lại Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh trên cơ sở hợp nhất Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Văn phòng Đăng ký đất đai tỉnh Bình Dương và Văn phòng Đăng ký đất đai tỉnh Bà Rịa – Vũng Tàu;"),
        ("Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ", "ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng đăng ký đất đai số 23;"),
        ("Căn cứ Quyết định số 841/QĐ-SNNMT-VP ", "ngày 30 tháng 9 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc điều động và bổ nhiệm ông Nguyễn Chiến Thắng giữ chức vụ Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 kể từ ngày 01 tháng 10 năm 2026;"),
        ("Căn cứ Quyết định số 01/QĐ-VPĐK-HC ", "ngày 02 tháng 10 năm 2025 của Giám đốc Văn phòng đăng ký đất đai Thành phố về ban hành Quy chế làm việc của Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh;"),
        ("Căn cứ Quyết định số 02/QĐ-VPĐK-HC ", "ngày 02 tháng 10 năm 2025 của Giám đốc Văn phòng đăng ký đất đai Thành phố về ban hành Nội quy cơ quan Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh;"),
        ("Căn cứ Phương án số PA23r/PA-CN23 ", "về sử dụng tài sản công phục vụ viên chức và người lao động tại Chi nhánh Văn phòng Đăng ký đất đai số 23 và Bảng đối chiếu định mức trụ sở theo Nghị định 155/2025/NĐ-CP;"),
        ("Căn cứ Báo cáo tình hình PCCC năm 2026 ", "ngày 05 tháng 10 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23.")
    ]
    for pre, txt in cancu_list:
        add_clause(txt, 1, pre)

    add_subsection_heading("2", "Hiện trạng trụ sở và diện tích cơ sở nhà đất Chi nhánh số 23 (theo Phương án PA23r)")
    add_clause("Chi nhánh Văn phòng Đăng ký đất đai số 23 đang trực tiếp quản lý, sử dụng cơ sở nhà, đất tại số 358 đường Huỳnh Văn Cù, khu phố Chánh Lộc 7, phường Thủ Dầu Một, Thành phố Hồ Chí Minh (tiếp nhận nguyên trạng từ UBND phường Chánh Mỹ cũ theo Biên bản bàn giao ngày 09/5/2019):", 1)
    add_clause("- Diện tích khuôn viên đất thực tế đang quản lý, sử dụng ổn định: 1.417,70 m².\n"
               "- Tổng diện tích sàn xây dựng thực tế của công trình khối nhà làm việc: 835,30 m² (kết cấu nhà Cấp III, khung cột, sàn bê tông cốt thép, mái tole kết hợp seno bê tông, tường gạch).\n"
               "- Diện tích nhà để xe (công trình ngoài nhà): 200,00 m² phục vụ phương tiện cho 85 cán bộ, viên chức, người lao động và người dân đến giao dịch hành chính tại Bộ phận Một cửa.\n"
               "- Tổng số lượng người làm việc thực tế được giao năm 2026: 85 người (03 lãnh đạo Chi nhánh, 79 viên chức chuyên môn, 03 nhân viên hỗ trợ phục vụ).", 1)
    add_clause("Theo Bảng đối chiếu định mức trụ sở tại Phương án PA23r, tổng diện tích sàn cần thiết theo tiêu chuẩn định mức nhà nước (Nghị định 155/2025/NĐ-CP và Thông tư 09/2007/TT-BNV) là 3.751,00 m², trong khi diện tích sàn hiện hữu tại số 358 Huỳnh Văn Cù chỉ có 835,30 m² (mới đáp ứng 28,69% định mức).", 1)

    add_subsection_heading("3", "Sự cần thiết xin cấp kinh phí trang bị và cải tạo chống dột")
    add_clause("a) Về trang bị 26 bình chữa cháy:\n"
               "Theo Báo cáo công tác PCCC năm 2026 của Chi nhánh số 23 và Phương án PA23r, Chi nhánh hiện đang lưu trữ khối lượng khổng lồ tài liệu địa chính, sổ bộ gốc với diện tích sàn kho 406 m² đã lấp đầy 100% công suất giá kệ; ngoài ra còn khoảng 30% lượng hồ sơ chưa chỉnh lý phải lưu tạm tại các lối đi và 02 phòng làm việc. Đây là các vật liệu giấy rất dễ bắt cháy. Hiện trạng 26 bình chữa cháy tại cơ quan (gồm bình bột ABC MFZL4 và khí CO2 MT3 bố trí tại Sảnh tiếp nhận hồ sơ Một cửa: 4 bình; cửa kho lưu trữ: 2 bình; hành lang: 4 bình; phòng làm việc Tổ Lưu trữ: 4 bình; cầu thang: 4 bình; phòng Đo đạc: 4 bình; phòng Đăng ký & Cấp GCN: 4 bình) đã qua nhiều năm sử dụng, hết hạn kiểm định áp lực khí đẩy và chất chữa cháy bị vón cục, suy giảm khả năng dập lửa. Theo quy định tại TCVN 3890:2023 và Nghị định 50/2024/NĐ-CP, việc thay thế, trang bị mới 26 bình chữa cháy đạt chuẩn kiểm định PCCC là yêu cầu cấp bách hàng đầu để bảo vệ an toàn tính mạng con người và tài liệu lưu trữ quốc gia.", 1)
    
    add_clause("b) Về trang bị 01 máy in 2 mặt A4:\n"
               "Theo Quyết định số 2637/QĐ-SNNMT-VP, Chi nhánh số 23 phụ trách địa bàn 05 phường đô thị trung tâm (Phú Lợi, Phú An, Bình Dương, Chánh Hiệp, Thủ Dầu Một) với khối lượng tiếp nhận và thụ lý hồ sơ biến động đất đai rất lớn. Theo báo cáo rà soát máy in và bảng đối chiếu thiết bị, các máy in A4 tại Bộ phận tiếp nhận và giải quyết hồ sơ thường xuyên bị kẹt giấy, hỏng sấy do cường độ in ấn cao (in trích lục địa chính, phiếu chuyển thông tin thuế, giấy tiếp nhận, dự thảo giấy chứng nhận). Việc trang bị 01 máy in laser tốc độ cao in 2 mặt tự động khổ A4 (kết nối mạng LAN) là hết sức cần thiết để đảm bảo tiến độ giải quyết TTHC không bị ách tắc.", 1)

    add_clause("c) Về trang bị 01 ghế ngồi làm việc cho Giám đốc Chi nhánh:\n"
               "Căn cứ Quyết định số 841/QĐ-SNNMT-VP ngày 30/9/2026 của Giám đốc Sở Nông nghiệp và Môi trường TP.HCM, ông Nguyễn Chiến Thắng (nguyên Phó Giám đốc VPĐKĐĐ TP) được điều động và bổ nhiệm giữ chức vụ Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 kể từ ngày 01/10/2026. Hiện tại phòng làm việc của Giám đốc Chi nhánh (diện tích 30 m² theo PA23r) chưa có ghế ngồi làm việc đạt tiêu chuẩn; chiếc ghế hiện trạng cũ từ giai đoạn tiếp nhận năm 2019 đã bị rách đệm, hỏng piston nâng hạ. Căn cứ tiêu chuẩn định mức trang thiết bị làm việc theo Quyết định số 50/2017/QĐ-TTg của Thủ tướng Chính phủ đối với chức danh Giám đốc đơn vị sự nghiệp trực thuộc cấp tỉnh, việc trang bị 01 ghế xoay da cao cấp cho tân Giám đốc Chi nhánh là hoàn toàn đúng chế độ, tiêu chuẩn định mức nhà nước.", 1)

    add_clause("d) Về cải tạo kho lưu trữ chống thấm dột:\n"
               "Kho lưu trữ hồ sơ địa chính hiện hữu của Chi nhánh số 23 có diện tích sàn 406 m² (gồm kho chính 391 m² và kho tiếp nhận sau sáp nhập 15 m²), cùng với khối nhà dự kiến tiếp nhận từ Điểm trạm y tế 3 liền kề (548 m² sàn theo PA23r) được xây dựng từ nhiều năm trước. Do ảnh hưởng của thời tiết mưa bão kéo dài tại khu vực Đông Nam Bộ, hệ thống sàn mái bê tông, sê nô thu nước và mương đón nước mái tole của kho lưu trữ đã bị lão hóa nghiêm trọng, xuất hiện nhiều vết nứt chân chim và nứt kết cấu, nước mưa thẩm thấu chảy dột trực tiếp xuống khu vực các giá kệ compactor chứa hồ sơ địa chính gốc và bản đồ địa chính. Nếu không kịp thời thi công xử lý chống thấm dột toàn diện, nguy cơ ẩm mốc, mục nát, phân hủy và hư hại vĩnh viễn các hồ sơ địa chính gốc, hồ sơ cấp GCN là cực kỳ nghiêm trọng, không thể khắc phục được.", 1)

    # -------------------------------------------------------------
    # PHẦN II: NỘI DUNG, QUY CÁCH VÀ KHỐI LƯỢNG THỰC HIỆN
    # -------------------------------------------------------------
    add_section_heading("II", "NỘI DUNG, DANH MỤC THIẾT BỊ VÀ GIẢI PHÁP KỸ THUẬT")

    add_subsection_heading("1", "Danh mục trang thiết bị đề nghị mua sắm mới")
    
    # Bảng 1: Thiết bị mua sắm
    t_tb = doc.add_table(rows=1, cols=6)
    t_tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tb.autofit = False
    
    headers_tb = ["STT", "Tên thiết bị / Hàng hóa", "Quy cách kỹ thuật / Xuất xứ", "ĐVT", "Số lượng", "Vị trí bố trí / Ghi chú"]
    widths_tb = [Inches(0.5), Inches(1.5), Inches(2.2), Inches(0.5), Inches(0.5), Inches(1.3)]
    
    for i, h in enumerate(headers_tb):
        c = t_tb.rows[0].cells[i]
        c.width = widths_tb[i]
        set_cell_margins(c, 80, 80, 100, 100)
        set_cell_box_borders(c)
        shading = parse_xml(r'<w:shd %s w:fill="F2F2F2"/>' % nsdecls('w'))
        c._tc.get_or_add_tcPr().append(shading)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    data_tb = [
        ("1", "Bình chữa cháy bột ABC (MFZL4)", "Loại bình xách tay 4kg bột ABC chữa cháy chất rắn, lỏng, khí; vỏ thép chịu áp lực cao; kèm tem kiểm định PCCC của Cục Cảnh sát PCCC&CNCH. Hàng mới 100%.", "Bình", "16", "Bố trí tại các sảnh tiếp dân Một cửa (4), hành lang (4), cầu thang (4), phòng bảo vệ và kho (4)"),
        ("2", "Bình chữa cháy khí CO2 (MT3)", "Loại bình xách tay 3kg khí CO2 chữa cháy điện tử, hồ sơ lưu trữ không để lại cặn bẩn; van đồng, vòi phun loa kèn; kèm tem kiểm định PCCC. Hàng mới 100%.", "Bình", "10", "Bố trí tại phòng máy chủ Server, phòng kỹ thuật lưu trữ và kho lưu trữ hồ sơ địa chính (dễ thấy, dễ lấy)"),
        ("3", "Máy in 2 mặt tự động A4", "Máy in laser đen trắng A4 khổ giấy A4/Letter; tốc độ in tối thiểu 38-40 trang/phút; tự động đảo mặt (Duplex); độ phân giải 1200x1200dpi; kết nối USB 2.0 & Network LAN Gigabit (tương đương dòng HP LaserJet Pro 4003dn/M404dn hoặc Brother). Hàng mới 100%.", "Cái", "1", "Bố trí tại Bộ phận Đăng ký cấp GCN / Một cửa phục vụ in trích lục, phiếu chuyển thông tin thuế và kết quả TTHC"),
        ("4", "Ghế ngồi làm việc Giám đốc", "Ghế xoay da lãnh đạo cao cấp; đệm tựa mút đúc bọc da thật/da PU cao cấp màu đen; tay vịn gỗ tự nhiên/hợp kim bọc da; chân xoay hợp kim mạ crom chịu lực; cần thủy lực nâng hạ và ngả hãm nhiều góc độ. Đúng định mức trang thiết bị lãnh đạo theo QĐ 50/2017/QĐ-TTg.", "Cái", "1", "Bố trí tại Phòng làm việc Giám đốc Chi nhánh số 23 (phục vụ đồng chí Nguyễn Chiến Thắng - tân Giám đốc Chi nhánh)")
    ]

    for row_data in data_tb:
        row = t_tb.add_row()
        for idx, val in enumerate(row_data):
            c = row.cells[idx]
            c.width = widths_tb[idx]
            set_cell_margins(c, 80, 80, 100, 100)
            set_cell_box_borders(c)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            if idx in [0, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    add_subsection_heading("2", "Giải pháp kỹ thuật và khối lượng cải tạo chống dột kho lưu trữ hồ sơ")
    add_clause("Căn cứ phương pháp thi công chống thấm dột chuẩn kỹ thuật tương đồng phương án đã duyệt tại Chi nhánh số 34, giải pháp kỹ thuật xử lý chống thấm dột kho lưu trữ Chi nhánh số 23 bao gồm 02 hạng mục chính:", 1)
    
    add_clause("a) Hạng mục 1: Chống thấm sàn mái bê tông, sê nô mái và mương đón nước bằng màng khò nhiệt Bitumode Delta - P 3mm (mặt trơn):\n"
               "- Chuẩn bị bề mặt: Dùng máy mài chuyên dụng mài phẳng tạp chất, đục tẩy sạch bê tông bong tróc; thổi sạch bụi bẩn, trám vá vết nứt bê tông bằng vữa chuyên dụng; bo góc chân tường 45 độ.\n"
               "- Quét lớp lót kết dính: Quét 01 lớp lót Primer gốc bitum (Nirol - W) với định mức tiêu chuẩn 0,2 kg/m² để tạo độ bám dính tối ưu.\n"
               "- Thi công dán màng: Khò nhiệt chảy màng chống thấm cao cấp Bitumode Delta - P 3mm dán đều lên sàn, mép giáp mí chồng mí tối thiểu 10 cm, vén cao chân tường 20 - 30 cm.\n"
               "- Khối lượng dự toán diện tích sàn mái và sê nô chống thấm: 350,00 m².", 1)

    add_clause("b) Hạng mục 2: Chống thấm tường sàn mái, tường sê nô và tường bao mương đón nước bằng hóa chất đàn hồi SikaCoat Plus:\n"
               "- Chuẩn bị bề mặt: Đánh cạo sạch rong rêu, nấm mốc, lớp vôi vữa cũ bằng bàn chải sắt; xử lý các vết nứt nẻ bằng keo mastic trám trét chuyên dụng.\n"
               "- Thi công lớp phủ chống thấm: Lăn quét 02 lớp chống thấm đàn hồi kháng tia UV SikaCoat Plus với định mức 0,6 kg/m² (lớp thứ nhất chờ khô 3 - 4 giờ trước khi lăn lớp thứ hai).\n"
               "- Khối lượng dự toán diện tích tường seno và thành vách chống thấm: 280,00 m².", 1)

    # -------------------------------------------------------------
    # PHẦN III: QUY TRÌNH THỰC HIỆN VÀ HÌNH THỨC LỰA CHỌN NHÀ THẦU
    # -------------------------------------------------------------
    add_section_heading("III", "QUY TRÌNH THỰC HIỆN VÀ HÌNH THỨC LỰA CHỌN NHÀ THẦU")

    add_subsection_heading("1", "Hình thức lựa chọn nhà thầu")
    add_clause("Căn cứ quy định tại Luật Đấu thầu số 22/2023/QH15, Luật số 90/2025/QH15 và khoản 4 Điều 78 Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu:\n"
               "- Gói thầu mua sắm hàng hóa (bình chữa cháy, máy in, ghế Giám đốc) có giá trị dự toán khoảng 34.000.000 đồng (dưới 100 triệu đồng).\n"
               "- Gói thầu dịch vụ phi tư vấn cải tạo sửa chữa chống thấm dột kho lưu trữ có giá trị dự toán khoảng 185.000.000 đồng (thuộc hạn mức gói thầu dịch vụ phi tư vấn không hình thành dự án dưới 500 triệu đồng / dịch vụ thuộc dự án dưới 02 tỷ đồng).\n"
               "- Hình thức lựa chọn nhà thầu: Áp dụng hình thức Chỉ định thầu rút gọn theo đúng quy định hiện hành.\n"
               "- Loại hợp đồng: Hợp đồng trọn gói.", 1)

    add_subsection_heading("2", "Quy trình thực hiện theo các bước chuẩn")
    add_clause("Quy trình tổ chức thực hiện phương án mua sắm và thi công sửa chữa tuân thủ 06 bước chặt chẽ:\n"
               "• Bước 1: Khảo sát hiện trạng, lập danh mục kỹ thuật và thu thập báo giá thị trường (Chi nhánh số 23 chủ trì, thu thập đủ 03 báo giá hợp lệ của 03 nhà cung cấp độc lập).\n"
               "• Bước 2: Lập phương án dự toán kinh phí trình Phòng Kế hoạch – Tài chính Văn phòng Đăng ký đất đai Thành phố thẩm định; trình Ban Giám đốc Văn phòng đăng ký đất đai Thành phố phê duyệt chủ trương và dự toán.\n"
               "• Bước 3: Lập, thẩm định và phê duyệt kế hoạch lựa chọn nhà thầu theo quy định pháp luật về đấu thầu.\n"
               "• Bước 4: Thương thảo hợp đồng, hoàn thiện hồ sơ chỉ định thầu rút gọn và ban hành Quyết định phê duyệt kết quả lựa chọn nhà thầu; đăng tải thông tin trên Hệ thống mạng đấu thầu quốc gia.\n"
               "• Bước 5: Ký kết hợp đồng trọn gói; tổ chức giao nhận hàng hóa thiết bị và triển khai thi công sửa chữa; giám sát thi công, an toàn lao động và nghiệm thu chặt chẽ.\n"
               "• Bước 6: Hoàn tất hồ sơ kiểm soát chi, thanh quyết toán kinh phí và bàn giao tài sản đưa vào sử dụng, hạch toán ghi tăng tài sản công của đơn vị theo quy định.", 1)

    add_subsection_heading("3", "Công tác kiểm tra, nghiệm thu và hồ sơ thanh toán")
    add_clause("Ban Lãnh đạo Chi nhánh số 23 cùng Tổ Hành chính – Tổng hợp chịu trách nhiệm trực tiếp kiểm tra, nghiệm thu về số lượng, chất lượng, chủng loại, quy cách kỹ thuật của 26 bình chữa cháy (kèm biên bản kiểm định PCCC), máy in, ghế Giám đốc và khối lượng thực tế thi công chống thấm dột kho lưu trữ.\n"
               "Bộ hồ sơ thanh quyết toán bao gồm: Quyết định phê duyệt dự toán và KHLCNT; Hợp đồng kinh tế trọn gói; Biên bản bàn giao, nghiệm thu đưa vào sử dụng; Hóa đơn điện tử hợp pháp; Chứng thư bảo hành, tem kiểm định thiết bị; Chứng từ thanh toán qua Kho bạc/Ngân hàng.", 1)

    # -------------------------------------------------------------
    # PHẦN IV: DỰ TOÁN KINH PHÍ THỰC HIỆN
    # -------------------------------------------------------------
    add_section_heading("IV", "DỰ TOÁN KINH PHÍ VÀ NGUỒN VỐN THỰC HIỆN")

    add_subsection_heading("1", "Bảng tổng hợp dự toán kinh phí")
    add_clause("Dự toán kinh phí được xây dựng trên cơ sở tham khảo khảo sát giá thị trường của 03 đơn vị cung ứng độc lập và suất vốn đầu tư sửa chữa chống thấm tương đương tại các Chi nhánh trực thuộc Văn phòng Đăng ký đất đai Thành phố (áp dụng thuế suất GTGT 8% theo chính sách giảm thuế tại Nghị quyết 204/2025/QH15 và Nghị định 174/2025/NĐ-CP):", 1)

    # Bảng 2: Dự toán chi tiết
    t_dt = doc.add_table(rows=1, cols=7)
    t_dt.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_dt.autofit = False

    headers_dt = ["STT", "Nội dung hạng mục", "ĐVT", "Khối lượng", "Đơn giá chưa thuế (VNĐ)", "Thuế GTGT (8%) (VNĐ)", "Tổng cộng sau thuế (VNĐ)"]
    widths_dt = [Inches(0.4), Inches(2.2), Inches(0.4), Inches(0.5), Inches(1.1), Inches(0.9), Inches(1.1)]

    for i, h in enumerate(headers_dt):
        c = t_dt.rows[0].cells[i]
        c.width = widths_dt[i]
        set_cell_margins(c, 80, 80, 80, 80)
        set_cell_box_borders(c)
        shading = parse_xml(r'<w:shd %s w:fill="F2F2F2"/>' % nsdecls('w'))
        c._tc.get_or_add_tcPr().append(shading)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    items_dt = [
        ("A", "MUA SẮM PHƯƠNG TIỆN PCCC VÀ THIẾT BỊ LÀM VIỆC", "", "", "", "", ""),
        ("1", "Bình chữa cháy bột ABC 4kg (MFZL4) có kiểm định PCCC", "Bình", "16", "290.000", "371.200", "5.011.200"),
        ("2", "Bình chữa cháy khí CO2 3kg (MT3) có kiểm định PCCC", "Bình", "10", "480.000", "384.000", "5.184.000"),
        ("3", "Máy in laser đen trắng tự động 2 mặt khổ A4 kết nối mạng (HP/Brother)", "Cái", "1", "15.500.000", "1.240.000", "16.740.000"),
        ("4", "Ghế xoay da làm việc cao cấp cho Giám đốc Chi nhánh", "Cái", "1", "6.500.000", "520.000", "7.020.000"),
        ("Cộng A", "Tổng kinh phí mua sắm thiết bị (A)", "", "", "31.440.000", "2.515.200", "33.955.200"),
        ("B", "CẢI TẠO, SỬA CHỮA CHỐNG THẤM DỘT KHO LƯU TRỮ HỒ SƠ", "", "", "", "", ""),
        ("1", "Chống thấm sàn mái, seno, mương đón nước bằng màng khò nóng Bitumode Delta-P 3mm", "m²", "350,00", "303.250", "8.491.000", "114.628.500"),
        ("2", "Chống thấm tường sàn mái, tường seno bằng hóa chất kháng UV SikaCoat Plus", "m²", "280,00", "233.000", "5.219.200", "70.459.200"),
        ("Cộng B", "Tổng kinh phí sửa chữa chống dột kho lưu trữ (B)", "", "", "171.377.500", "13.710.200", "185.087.700"),
        ("TỔNG", "TỔNG CỘNG KINH PHÍ XIN CẤP (A + B)", "", "", "202.817.500", "16.225.400", "219.042.900")
    ]

    for row_data in items_dt:
        row = t_dt.add_row()
        is_bold_row = row_data[0] in ["A", "B", "Cộng A", "Cộng B", "TỔNG"]
        is_section_header = row_data[0] in ["A", "B"]
        
        for idx, val in enumerate(row_data):
            c = row.cells[idx]
            c.width = widths_dt[idx]
            set_cell_margins(c, 60, 60, 80, 80)
            set_cell_box_borders(c)
            
            if is_section_header:
                shading = parse_xml(r'<w:shd %s w:fill="EBF1F5"/>' % nsdecls('w'))
                c._tc.get_or_add_tcPr().append(shading)
            elif row_data[0] == "TỔNG":
                shading = parse_xml(r'<w:shd %s w:fill="FDE9D9"/>' % nsdecls('w'))
                c._tc.get_or_add_tcPr().append(shading)

            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            
            if idx in [0, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif idx in [4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            r = p.add_run(val)
            r.bold = is_bold_row
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)

    # Thuyết minh tổng tiền bằng chữ
    p_money = doc.add_paragraph()
    p_money.paragraph_format.first_line_indent = Inches(0.45)
    p_money.paragraph_format.space_before = Pt(8)
    p_money.paragraph_format.space_after = Pt(4)
    r = p_money.add_run("Tổng dự toán kinh phí đề nghị cấp: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_money.add_run("219.042.900 đồng ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_money.add_run("(Bằng chữ: Hai trăm mười chín triệu, không trăm bốn mươi hai nghìn, chín trăm đồng).")
    r.italic = True
    r.font.name = "Times New Roman"

    add_clause("Trong đó chi tiết từng phần:\n"
               "- Kinh phí mua sắm 26 bình chữa cháy và thiết bị làm việc (A): 33.955.200 đồng (Bằng chữ: Ba mươi ba triệu, chín trăm năm mươi lăm nghìn, hai trăm đồng).\n"
               "- Kinh phí sửa chữa, chống thấm dột kho lưu trữ hồ sơ (B): 185.087.700 đồng (Bằng chữ: Một trăm tám mươi lăm triệu, không trăm tám mươi bảy nghìn, bảy trăm đồng).", 1)

    add_subsection_heading("2", "Nguồn kinh phí đề xuất")
    add_clause("Căn cứ Nghị định số 60/2021/NĐ-CP và Quyết định phân bổ dự toán thu chi của Văn phòng Đăng ký đất đai Thành phố, Chi nhánh số 23 kính đề nghị sử dụng nguồn kinh phí:\n"
               "- Quỹ Phát triển hoạt động sự nghiệp của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh; hoặc\n"
               "- Nguồn kinh phí không thường xuyên được giao năm 2026 của đơn vị.", 1)

    # -------------------------------------------------------------
    # PHẦN V: HIỆU QUẢ CỦA PHƯƠNG ÁN VÀ KIẾN NGHỊ
    # -------------------------------------------------------------
    add_section_heading("V", "HIỆU QUẢ CỦA PHƯƠNG ÁN VÀ KIẾN NGHỊ")

    add_subsection_heading("1", "Hiệu quả mang lại")
    add_clause("• Về công tác an toàn PCCC và bảo quản tài liệu: Việc thay mới 26 bình chữa cháy đạt chuẩn và chống dột dứt điểm sàn mái kho lưu trữ giúp triệt tiêu hoàn toàn nguy cơ cháy nổ, ẩm mốc, phân hủy đối với hơn 3.000 mét giá tài liệu địa chính gốc và hồ sơ biến động đất đai lưu trữ tại đơn vị; bảo đảm an toàn tính mạng cho 85 cán bộ nhân viên và hàng trăm lượt người dân đến giao dịch hàng ngày.\n"
               "• Về hiệu quả chuyên môn và cải cách TTHC: Trang bị kịp thời máy in 2 mặt tốc độ cao giúp các Tổ nghiệp vụ rút ngắn thời gian in ấn, luân chuyển hồ sơ, nâng cao tỷ lệ giải quyết hồ sơ đúng hạn và trước hạn cho công dân, doanh nghiệp trên địa bàn 05 phường phụ trách.\n"
               "• Về điều kiện làm việc: Đảm bảo điều kiện, trang thiết bị làm việc theo đúng chế độ, tiêu chuẩn định mức nhà nước đối với tân Giám đốc Chi nhánh vừa được điều động, bổ nhiệm theo Quyết định số 841/QĐ-SNNMT-VP ngày 30/9/2026 của Sở Nông nghiệp và Môi trường.\n"
               "• Về kinh tế và quản lý tài sản công: Phương án tận dụng triệt để cơ sở vật chất hiện có, xử lý cục bộ chống dột chất lượng cao với chi phí tiết kiệm tối đa, không để phát sinh hư hỏng lây lan gây lãng phí ngân sách nhà nước.", 1)

    add_subsection_heading("2", "Kiến nghị")
    add_clause("Để kịp thời khắc phục tình trạng thấm dột trước mùa mưa cao điểm, đảm bảo an toàn PCCC kho lưu trữ và phương tiện làm việc phục vụ công tác chuyên môn, Chi nhánh Văn phòng Đăng ký đất đai số 23 kính đề nghị:\n"
               "1. Kính trình Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, phê duyệt chủ trương và phê duyệt Phương án dự toán kinh phí nêu trên.\n"
               "2. Kính đề nghị Phòng Kế hoạch – Tài chính Văn phòng Đăng ký đất đai Thành phố hỗ trợ thẩm định dự toán, hướng dẫn các thủ tục chỉ định thầu rút gọn và bố trí nguồn kinh phí thanh toán để Chi nhánh số 23 sớm tổ chức triển khai thực hiện theo quy định./.", 1)

    # ==========================================
    # KHỐI KÝ DUYỆT BẢNG 2 CỘT THEO MẪU PA34
    # ==========================================
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(12)
    p_space.paragraph_format.space_after = Pt(0)

    # Dòng ngày tháng ký
    p_date_end = doc.add_paragraph()
    p_date_end.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date_end.paragraph_format.space_before = Pt(0)
    p_date_end.paragraph_format.space_after = Pt(8)
    r = p_date_end.add_run("Thành phố Hồ Chí Minh, ngày 07 tháng 10 năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    t_sign_box = doc.add_table(rows=1, cols=2)
    t_sign_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign_box.autofit = False
    remove_table_borders(t_sign_box)

    t_sign_box.rows[0].cells[0].width = Inches(3.2)
    t_sign_box.rows[0].cells[1].width = Inches(3.3)
    set_cell_margins(t_sign_box.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_sign_box.rows[0].cells[1], 0, 0, 0, 0)

    cell_l = t_sign_box.rows[0].cells[0]
    cell_r = t_sign_box.rows[0].cells[1]

    # Bên trái: Người lập & Tổ trưởng HC-TH
    p = cell_l.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("NGƯỜI LẬP PHƯƠNG ÁN")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_empty = cell_l.add_paragraph()
    p_empty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_empty.paragraph_format.space_before = Pt(0)
    p_empty.paragraph_format.space_after = Pt(40)
    r = p_empty.add_run("(Ký và ghi rõ họ tên)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_name_l = cell_l.add_paragraph()
    p_name_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name_l.paragraph_format.space_before = Pt(0)
    p_name_l.paragraph_format.space_after = Pt(0)
    r = p_name_l.add_run("Tổ Hành chính – Tổng hợp")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Bên phải: Giám đốc Chi nhánh 23
    p = cell_r.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("CHI NHÁNH SỐ 23 LẬP DỰ TOÁN\nGIÁM ĐỐC")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_empty_r = cell_r.add_paragraph()
    p_empty_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_empty_r.paragraph_format.space_before = Pt(0)
    p_empty_r.paragraph_format.space_after = Pt(40)
    r = p_empty_r.add_run("(Ký, đóng dấu và ghi rõ họ tên)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_name_r = cell_r.add_paragraph()
    p_name_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name_r.paragraph_format.space_before = Pt(0)
    p_name_r.paragraph_format.space_after = Pt(0)
    r = p_name_r.add_run("Nguyễn Chiến Thắng")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)

    # Khối phê duyệt cấp trên (Bảng phê duyệt của VPĐKĐĐ TP)
    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(16)
    p_space2.paragraph_format.space_after = Pt(0)

    t_app = doc.add_table(rows=1, cols=2)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_app.autofit = False
    remove_table_borders(t_app)

    t_app.rows[0].cells[0].width = Inches(3.2)
    t_app.rows[0].cells[1].width = Inches(3.3)
    set_cell_margins(t_app.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_app.rows[0].cells[1], 0, 0, 0, 0)

    app_l = t_app.rows[0].cells[0]
    app_r = t_app.rows[0].cells[1]

    # Thẩm định của Phòng KHTC
    p = app_l.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("ĐƠN VỊ THẨM ĐỊNH:\nPHÒNG KẾ HOẠCH – TÀI CHÍNH")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p_empty_app_l = app_l.add_paragraph()
    p_empty_app_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_empty_app_l.paragraph_format.space_after = Pt(45)
    r = p_empty_app_l.add_run("(Ký và ghi rõ họ tên)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_app_l_name = app_l.add_paragraph()
    p_app_l_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app_l_name.add_run("Đào Vân Anh")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Phê duyệt của Giám đốc VPĐKĐĐ TP
    p = app_r.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("PHÊ DUYỆT CỦA GIÁM ĐỐC\nVĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p_empty_app_r = app_r.add_paragraph()
    p_empty_app_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_empty_app_r.paragraph_format.space_after = Pt(45)
    r = p_empty_app_r.add_run("(Ký, đóng dấu và ghi rõ họ tên)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_app_r_name = app_r.add_paragraph()
    p_app_r_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app_r_name.add_run("Bùi Thị Bích Tuyền")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Lưu tài liệu vào OUTPUT
    out_path = "OUTPUT/Phuong_an_xin_kinh_phi_CN23.docx"
    doc.save(out_path)
    print(f"Generated successfully: {out_path}")

if __name__ == "__main__":
    create_pa_document()
