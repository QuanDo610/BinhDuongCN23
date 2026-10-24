import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
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
    
    # Add page number to header
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
    def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(r'<w:tcMar %s><w:top w:w="%d" w:type="dxa"/><w:bottom w:w="%d" w:type="dxa"/><w:left w:w="%d" w:type="dxa"/><w:right w:w="%d" w:type="dxa"/></w:tcMar>' % (nsdecls('w'), top, bottom, left, right))
        tcPr.append(tcMar)

    # ==========================================
    # PHẦN 1: QUYẾT ĐỊNH BAN HÀNH
    # ==========================================

    # Header Table
    t_header = doc.add_table(rows=1, cols=2)
    t_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_header.autofit = False
    remove_table_borders(t_header)

    col_widths = [Inches(2.7), Inches(3.8)]
    for row in t_header.rows:
        row.cells[0].width = col_widths[0]
        row.cells[1].width = col_widths[1]
        set_cell_margins(row.cells[0], 0, 0, 0, 0)
        set_cell_margins(row.cells[1], 0, 0, 0, 0)

    c0 = t_header.rows[0].cells[0]
    c1 = t_header.rows[0].cells[1]

    # Cơ quan ban hành (Trái)
    p = c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r = p.add_run("CHI NHÁNH SỐ 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p_line_cq = c0.add_paragraph()
    p_line_cq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_cq.paragraph_format.space_before = Pt(0)
    p_line_cq.paragraph_format.space_after = Pt(4)
    r = p_line_cq.add_run("————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(9)

    p_so = c0.add_paragraph()
    p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_so.paragraph_format.space_before = Pt(0)
    p_so.paragraph_format.space_after = Pt(0)
    r = p_so.add_run("Số:       /QĐ-CN23")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Quốc hiệu - Tiêu ngữ (Phải)
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r = p.add_run("Độc lập - Tự do - Hạnh phúc")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_line_qh = c1.add_paragraph()
    p_line_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_qh.paragraph_format.space_before = Pt(0)
    p_line_qh.paragraph_format.space_after = Pt(4)
    r = p_line_qh.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    p_ngay = c1.add_paragraph()
    p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ngay.paragraph_format.space_before = Pt(0)
    p_ngay.paragraph_format.space_after = Pt(0)
    r = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày     tháng     năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Tên loại văn bản: QUYẾT ĐỊNH
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(3)
    r = p_title.add_run("QUYẾT ĐỊNH")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    # Trích yếu
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.15
    r = p_sub.add_run("Ban hành Quy chế làm việc của Chi nhánh Văn phòng đăng ký đất đai số 23\ntrực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_line_ty = doc.add_paragraph()
    p_line_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_ty.paragraph_format.space_before = Pt(0)
    p_line_ty.paragraph_format.space_after = Pt(10)
    r = p_line_ty.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    # Thẩm quyền ký ban hành
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(4)
    p_auth.paragraph_format.space_after = Pt(8)
    r = p_auth.add_run("GIÁM ĐỐC CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23\nTHÀNH PHỐ HỒ CHÍ MINH")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    # Căn cứ pháp lý
    cancu_list = [
        "Căn cứ Luật Đất đai ngày 18 tháng 01 năm 2024; Luật sửa đổi, bổ sung một số điều của Luật Đất đai số 31/2024/QH15, Luật Nhà ở số 17/2023/QH15, Luật Kinh doanh bất động sản số 19/2023/QH15 và Luật Các tổ chức tín dụng số 32/2024/QH15 ngày 29 tháng 6 năm 2024;",
        "Căn cứ Nghị định số 101/2024/NĐ-CP ngày 29 tháng 7 năm 2024 của Chính phủ quy định về điều tra cơ bản đất đai; đăng ký, cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất và hệ thống thông tin đất đai;",
        "Căn cứ Nghị định số 102/2024/NĐ-CP ngày 30 tháng 7 năm 2024 của Chính phủ quy định chi tiết thi hành một số điều của Luật Đất đai;",
        "Căn cứ Nghị định số 151/2025/NĐ-CP ngày 12 tháng 6 năm 2025 của Chính phủ quy định về phân định thẩm quyền của chính quyền địa phương 02 cấp, phân quyền phân cấp trong lĩnh vực đất đai;",
        "Căn cứ Nghị quyết số 190/2025/QH15 ngày 19 tháng 02 năm 2025 của Quốc hội quy định về xử lý một số vấn đề liên quan đến sắp xếp tổ chức bộ máy nhà nước;",
        "Căn cứ Quyết định số 1886/QĐ-UBND ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố Hồ Chí Minh về tổ chức lại Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh trên cơ sở hợp nhất Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh, Văn phòng Đăng ký đất đai tỉnh Bình Dương và Văn phòng Đăng ký đất đai tỉnh Bà Rịa – Vũng Tàu;",
        "Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh;",
        "Căn cứ Quyết định số 01/QĐ-VPĐK-HC ngày 02 tháng 10 năm 2025 của Giám đốc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh về ban hành Quy chế làm việc của Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh;",
        "Căn cứ Quyết định số 02/QĐ-VPĐK-HC ngày 02 tháng 10 năm 2025 của Giám đốc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh về ban hành Nội quy cơ quan Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh;",
        "Theo đề nghị của Tổ trưởng Tổ Hành chính – Tổng hợp."
    ]

    for cc in cancu_list:
        p_cc = doc.add_paragraph()
        p_cc.paragraph_format.first_line_indent = Inches(0.45)
        p_cc.paragraph_format.space_after = Pt(3)
        p_cc.paragraph_format.line_spacing = 1.15
        p_cc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_cc.add_run(cc)
        r.italic = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    # QUYẾT ĐỊNH:
    p_qd = doc.add_paragraph()
    p_qd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qd.paragraph_format.space_before = Pt(6)
    p_qd.paragraph_format.space_after = Pt(6)
    r = p_qd.add_run("QUYẾT ĐỊNH:")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.5)

    # Điều 1, 2, 3
    dieu_qd = [
        ("Điều 1. ", "Ban hành kèm theo Quyết định này Quy chế làm việc của Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh."),
        ("Điều 2. ", "Quyết định này có hiệu lực thi hành kể từ ngày ký."),
        ("Điều 3. ", "Ban Lãnh đạo Chi nhánh, Tổ trưởng các Tổ nghiệp vụ (Tổ Hành chính – Tổng hợp, Tổ Đăng ký và Cấp giấy chứng nhận, Tổ Kỹ thuật Địa chính và Lưu trữ), cùng toàn thể viên chức, người lao động thuộc Chi nhánh Văn phòng đăng ký đất đai số 23 chịu trách nhiệm thi hành Quyết định này./.")
    ]

    for d_num, d_content in dieu_qd:
        p_d = doc.add_paragraph()
        p_d.paragraph_format.first_line_indent = Inches(0.45)
        p_d.paragraph_format.space_after = Pt(4)
        p_d.paragraph_format.line_spacing = 1.15
        p_d.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_num = p_d.add_run(d_num)
        r_num.bold = True
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(13)
        r_txt = p_d.add_run(d_content)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13)

    # Chữ ký Quyết định & Nơi nhận (Bảng 2 cột)
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = False
    remove_table_borders(t_sig)

    for row in t_sig.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.3)
        set_cell_margins(row.cells[0], 0, 0, 0, 0)
        set_cell_margins(row.cells[1], 0, 0, 0, 0)

    cell_nn = t_sig.rows[0].cells[0]
    cell_ky = t_sig.rows[0].cells[1]

    # Nơi nhận
    p_nn_head = cell_nn.paragraphs[0]
    p_nn_head.paragraph_format.space_after = Pt(2)
    r = p_nn_head.add_run("Nơi nhận:")
    r.bold = True
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    nn_items = [
        "- Sở Nông nghiệp và Môi trường (để b/c);",
        "- Ban Giám đốc VPĐKĐĐ TP (để b/c);",
        "- Các Phòng chuyên môn thuộc VPĐKĐĐ TP;",
        "- UBND TP. Thủ Dầu Một (để phối hợp);",
        "- UBND 05 phường phụ trách (để phối hợp);",
        "- Như Điều 3 (để thực hiện);",
        "- Lưu: VT, HC-TH."
    ]
    for item in nn_items:
        p_it = cell_nn.add_paragraph()
        p_it.paragraph_format.space_before = Pt(0)
        p_it.paragraph_format.space_after = Pt(1)
        p_it.paragraph_format.line_spacing = 1.05
        r = p_it.add_run(item)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # Chức danh ký
    p_ky_head = cell_ky.paragraphs[0]
    p_ky_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ky_head.paragraph_format.space_after = Pt(45) # Chừa khoảng trống ký tên
    r = p_ky_head.add_run("GIÁM ĐỐC")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_ky_ten = cell_ky.add_paragraph()
    p_ky_ten.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ky_ten.paragraph_format.space_before = Pt(0)
    p_ky_ten.paragraph_format.space_after = Pt(0)
    # Không để tên cứng nếu chưa có chỉ định cụ thể, để họ tên trống hoặc chức danh chuẩn
    r = p_ky_ten.add_run("(Ký, ghi rõ họ tên và đóng dấu)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    # Ngắt trang sang Quy chế
    doc.add_page_break()

    # ==========================================
    # PHẦN 2: TOÀN VĂN QUY CHẾ LÀM VIỆC
    # ==========================================

    # Header Quy chế (Bảng 2 cột)
    t_qc_head = doc.add_table(rows=1, cols=2)
    t_qc_head.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_qc_head.autofit = False
    remove_table_borders(t_qc_head)

    for row in t_qc_head.rows:
        row.cells[0].width = Inches(2.7)
        row.cells[1].width = Inches(3.8)
        set_cell_margins(row.cells[0], 0, 0, 0, 0)
        set_cell_margins(row.cells[1], 0, 0, 0, 0)

    qc_c0 = t_qc_head.rows[0].cells[0]
    qc_c1 = t_qc_head.rows[0].cells[1]

    p = qc_c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r = p.add_run("CHI NHÁNH SỐ 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p_line_cq2 = qc_c0.add_paragraph()
    p_line_cq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_cq2.paragraph_format.space_before = Pt(0)
    p_line_cq2.paragraph_format.space_after = Pt(0)
    r = p_line_cq2.add_run("————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(9)

    p = qc_c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r = p.add_run("Độc lập - Tự do - Hạnh phúc")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_line_qh2 = qc_c1.add_paragraph()
    p_line_qh2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_qh2.paragraph_format.space_before = Pt(0)
    p_line_qh2.paragraph_format.space_after = Pt(0)
    r = p_line_qh2.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    # Tiêu đề QUY CHẾ LÀM VIỆC
    p_qc_t = doc.add_paragraph()
    p_qc_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qc_t.paragraph_format.space_before = Pt(14)
    p_qc_t.paragraph_format.space_after = Pt(3)
    r = p_qc_t.add_run("QUY CHẾ LÀM VIỆC")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    p_qc_sub = doc.add_paragraph()
    p_qc_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qc_sub.paragraph_format.space_before = Pt(0)
    p_qc_sub.paragraph_format.space_after = Pt(2)
    p_qc_sub.paragraph_format.line_spacing = 1.15
    r = p_qc_sub.add_run("CỦA CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23\nTRỰC THUỘC VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI THÀNH PHỐ HỒ CHÍ MINH")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_qc_note = doc.add_paragraph()
    p_qc_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qc_note.paragraph_format.space_before = Pt(0)
    p_qc_note.paragraph_format.space_after = Pt(12)
    r = p_qc_note.add_run("(Ban hành kèm theo Quyết định số       /QĐ-CN23 ngày     tháng     năm 2026\ncủa Giám đốc Chi nhánh Văn phòng đăng ký đất đai số 23)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Helper function to add Chapter
    def add_chapter(chap_num, chap_title):
        p_c = doc.add_paragraph()
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.space_before = Pt(14)
        p_c.paragraph_format.space_after = Pt(2)
        r = p_c.add_run(chap_num)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(8)
        r = p_t.add_run(chap_title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    # Helper function to add Article Title
    def add_article_title(art_num_title):
        p_a = doc.add_paragraph()
        p_a.paragraph_format.first_line_indent = Inches(0.45)
        p_a.paragraph_format.space_before = Pt(8)
        p_a.paragraph_format.space_after = Pt(4)
        p_a.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_a.add_run(art_num_title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    # Helper function to add paragraph/clause
    def add_clause(text, indent_level=1, bold_prefix=""):
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
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13)

    # -------------------------------------------------------------
    # CHƯƠNG I: QUY ĐỊNH CHUNG
    # -------------------------------------------------------------
    add_chapter("Chương I", "QUY ĐỊNH CHUNG")

    add_article_title("Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng")
    add_clause("Quy chế này quy định về nguyên tắc làm việc; trách nhiệm, phạm vi, quyền hạn và cách thức giải quyết công việc; chương trình, kế hoạch công tác; chế độ hội họp, thông tin, báo cáo; trình tự giải quyết công việc thường xuyên và mối quan hệ công tác của Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh (sau đây gọi tắt là Chi nhánh số 23).", 1, "1. Phạm vi điều chỉnh: ")
    add_clause("Quy chế này áp dụng đối với Ban Lãnh đạo Chi nhánh số 23 (Giám đốc và các Phó Giám đốc Chi nhánh); Tổ trưởng, Tổ phó các Tổ nghiệp vụ (Tổ Hành chính – Tổng hợp, Tổ Đăng ký và Cấp giấy chứng nhận, Tổ Kỹ thuật Địa chính và Lưu trữ); toàn thể viên chức, người lao động làm việc tại Chi nhánh số 23; các cơ quan, tổ chức, cá nhân có quan hệ công tác liên quan thuộc phạm vi điều chỉnh của Quy chế này.", 1, "2. Đối tượng áp dụng: ")

    add_article_title("Điều 2. Vị trí pháp lý, chức năng và địa bàn phụ trách")
    add_clause("Chi nhánh số 23 là đơn vị sự nghiệp công lập trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh; chịu sự quản lý, chỉ đạo trực tiếp, toàn diện của Giám đốc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh; đồng thời chịu sự kiểm tra, hướng dẫn về chuyên môn nghiệp vụ của Sở Nông nghiệp và Môi trường và các cơ quan quản lý chuyên ngành cấp trên có liên quan.", 1, "1. Vị trí pháp lý: ")
    add_clause("Chi nhánh số 23 có tư cách pháp nhân, có con dấu riêng và được mở tài khoản tại Kho bạc Nhà nước, Ngân hàng thương mại theo quy định; thực hiện cơ chế tự chủ tài chính và hạch toán phụ thuộc theo quy định pháp luật đối với đơn vị sự nghiệp công lập.", 1, "2. Tư cách pháp nhân và tài chính: ")
    add_clause("Chi nhánh số 23 đặt tại số 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh.", 1, "3. Trụ sở làm việc: ")
    add_clause("Chi nhánh số 23 thực hiện chức năng, nhiệm vụ và quyền hạn giải quyết các thủ tục hành chính, cung cấp dịch vụ công về lĩnh vực đất đai trong phạm vi địa bàn quản lý gồm 05 đơn vị hành chính phường thuộc thành phố Thủ Dầu Một cũ: phường Phú Lợi, phường Phú An, phường Bình Dương, phường Chánh Hiệp và phường Thủ Dầu Một theo đúng Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Sở Nông nghiệp và Môi trường và Quyết định số 1886/QĐ-UBND ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố.", 1, "4. Chức năng và địa bàn phụ trách: ")

    add_article_title("Điều 3. Nguyên tắc làm việc")
    add_clause("Chi nhánh số 23 làm việc theo chế độ thủ trưởng kết hợp với chế độ tập thể lãnh đạo; bảo đảm nguyên tắc tập trung dân chủ; tuân thủ sự lãnh đạo của Đảng, sự chỉ đạo, điều hành trực tiếp của Giám đốc Văn phòng đăng ký đất đai Thành phố, Giám đốc Sở Nông nghiệp và Môi trường và tuân thủ các quy định của pháp luật, Nội quy cơ quan tại Quyết định số 02/QĐ-VPĐK-HC và Quy chế này.", 1, "1. ")
    add_clause("Đề cao trách nhiệm cá nhân, tính tiền phong gương mẫu của người đứng đầu. Mỗi nhiệm vụ, vụ việc chỉ giao cho một tổ chức (Tổ nghiệp vụ) hoặc một cá nhân chủ trì chịu trách nhiệm chính xuyên suốt. Người đứng đầu Tổ nghiệp vụ, cá nhân được giao chủ trì chịu trách nhiệm toàn diện về tiến độ, quy trình nghiệp vụ, tính chuẩn xác pháp lý và chất lượng kết quả công việc trước Lãnh đạo Chi nhánh và trước pháp luật.", 1, "2. ")
    add_clause("Phân công, phân cấp, ủy quyền rõ ràng, minh bạch giữa Giám đốc, các Phó Giám đốc, các Tổ trưởng nghiệp vụ và từng viên chức, người lao động. Cấp dưới phục tùng và chấp hành nghiêm túc sự lãnh đạo, chỉ đạo, điều hành của cấp trên. Tuyệt đối không đùn đẩy trách nhiệm, không chuyển công việc thuộc chức năng, thẩm quyền của Chi nhánh lên Ban Giám đốc Văn phòng đăng ký đất đai hoặc chuyển sang các cơ quan, đơn vị khác.", 1, "3. ")
    add_clause("Giải quyết công việc tuân thủ tuyệt đối quy trình nghiệp vụ, thời hạn giải quyết thủ tục hành chính, cơ chế một cửa, một cửa liên thông, quy chuẩn thể thức văn bản hành chính theo Nghị định số 30/2020/NĐ-CP và các quy định pháp luật chuyên ngành đất đai hiện hành.", 1, "4. ")
    add_clause("Thực hiện công khai, minh bạch, liêm chính, kỷ luật kỷ cương hành chính; triệt để thực hành tiết kiệm, chống lãng phí, phòng chống tiêu cực tham nhũng. Nghiêm cấm mọi hành vi gây phiền hà, nhũng nhiễu, chậm trễ hồ sơ, vòi vĩnh tổ chức, cá nhân và người dân. Ưu tiên hỗ trợ, tạo thuận lợi tối đa đối với người khuyết tật, phụ nữ mang thai, người cao tuổi, gia đình chính sách.", 1, "5. ")
    add_clause("Đẩy mạnh chuyển đổi số, hiện đại hóa hành chính, ứng dụng hệ thống thông tin đất đai, cơ sở dữ liệu địa chính số, tiếp nhận và luân chuyển xử lý hồ sơ trên môi trường điện tử gắn với chữ ký số chuyên dùng, bảo đảm an toàn, an ninh thông tin và bảo mật dữ liệu theo quy định.", 1, "6. ")

    # -------------------------------------------------------------
    # CHƯƠNG II: NHIỆM VỤ, QUYỀN HẠN VÀ CƠ CẤU TỔ CHỨC
    # -------------------------------------------------------------
    add_chapter("Chương II", "NHIỆM VỤ, QUYỀN HẠN VÀ CƠ CẤU TỔ CHỨC CỦA CHI NHÁNH")

    add_article_title("Điều 4. Nhiệm vụ và quyền hạn chuyên môn của Chi nhánh số 23")
    add_clause("Chi nhánh số 23 thực hiện đầy đủ 17 nhóm nhiệm vụ, quyền hạn theo quy định tại Điều 2 Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Sở Nông nghiệp và Môi trường trên địa bàn 05 phường được giao phụ trách, bao gồm:", 1)
    
    nhiemvu_list = [
        "Thực hiện đăng ký biến động quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất cho người sử dụng đất, chủ sở hữu tài sản gắn liền với đất là cá nhân, cộng đồng dân cư, người gốc Việt Nam định cư ở nước ngoài theo quy định.",
        "Thực hiện đo đạc, chỉnh lý, lập bản đồ địa chính, trích lục bản đồ địa chính; thực hiện thủ tục cấp đổi, cấp lại, đính chính, thu hồi, hủy Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất (sau đây gọi tắt là Giấy chứng nhận); hủy kết quả đăng ký biến động trên Giấy chứng nhận theo thẩm quyền và phân cấp.",
        "Kiểm tra, thẩm định và ký duyệt mảnh trích đo bản đồ địa chính thửa đất theo quy định; kiểm tra, xác nhận phiếu chỉnh lý đo đạc bản đồ, sơ đồ tài sản gắn liền với đất do tổ chức, cá nhân cung cấp phục vụ công tác đăng ký, cấp Giấy chứng nhận.",
        "Lập, chỉnh lý, cập nhật, lưu trữ và quản lý hồ sơ địa chính; tiếp nhận, bảo quản, quản lý và sử dụng phôi Giấy chứng nhận theo đúng quy định pháp luật và quy chế quản lý phôi của Văn phòng đăng ký đất đai Thành phố.",
        "Cập nhật, chỉnh lý thường xuyên cơ sở dữ liệu địa chính số; tích hợp, đồng bộ hóa và khai thác dữ liệu đất đai; xây dựng, quản lý, vận hành hệ thống thông tin đất đai trên địa bàn được phân công phụ trách.",
        "Cập nhật bản đồ địa chính số vào cơ sở dữ liệu quốc gia về đất đai theo phân công và quy chuẩn kỹ thuật.",
        "Thực hiện công tác thống kê, kiểm kê đất đai định kỳ và đột xuất; lập bản đồ hiện trạng sử dụng đất theo kế hoạch và hướng dẫn của cấp có thẩm quyền.",
        "Thực hiện đăng ký biện pháp bảo đảm bằng quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất; đăng ký thay đổi, sửa chữa sai sót, xóa đăng ký biện pháp bảo đảm theo đúng quy định của pháp luật.",
        "Cung cấp hồ sơ, bản đồ, thông tin, số liệu đất đai, tài sản gắn liền với đất cho các cơ quan nhà nước, tổ chức, cá nhân theo quy định của pháp luật và phân cấp quản lý.",
        "Thực hiện đối chiếu, kiểm tra và cung cấp thông tin lịch sử thửa đất theo hồ sơ địa chính qua các thời kỳ phục vụ công tác bồi thường, giải phóng mặt bằng, quản lý quy hoạch và giải quyết thủ tục cho tổ chức, cá nhân.",
        "Kiểm tra, đối chiếu, thực hiện chỉnh lý biến động bản đồ địa chính và sổ mục kê đất đai; thông báo kết quả cập nhật, chỉnh lý biến động cho Ủy ban nhân dân cấp phường theo định kỳ.",
        "Tiếp nhận, xử lý, giải quyết đơn thư phản ánh, kiến nghị, khiếu nại, tố cáo liên quan đến hoạt động của Chi nhánh theo thẩm quyền và trình tự pháp luật quy định.",
        "Tổ chức tiếp nhận hồ sơ và trả kết quả giải quyết thủ tục đăng ký đất đai, tài sản gắn liền với đất tại Bộ phận Một cửa; thực hiện dịch vụ công trực tuyến, tiếp nhận và trả kết quả qua dịch vụ bưu chính công ích.",
        "Thực hiện thu phí, lệ phí theo đúng biểu mức quy định của Hội đồng nhân dân, Ủy ban nhân dân Thành phố và pháp luật về phí, lệ phí; thực hiện các khoản thu từ dịch vụ công về đất đai quy định tại Điều 154 Luật Đất đai năm 2024.",
        "Thực hiện các dịch vụ tư vấn đo đạc, lập bản đồ, đăng ký đất đai, tài sản trên cơ sở chức năng, nhiệm vụ phù hợp với năng lực kỹ thuật của đơn vị và quy định của pháp luật.",
        "Quản lý tổ chức bộ máy, viên chức, người lao động, tài chính, tài sản công được giao; thực hiện nghiêm túc chế độ thông tin, báo cáo định kỳ, đột xuất về mọi mặt công tác của Chi nhánh.",
        "Thực hiện các nhiệm vụ chuyên môn khác do Giám đốc Sở Nông nghiệp và Môi trường, Giám đốc Văn phòng đăng ký đất đai Thành phố giao theo quy định pháp luật."
    ]
    for idx, nv in enumerate(nhiemvu_list, 1):
        add_clause(f"{idx}. {nv}", 1)

    add_article_title("Điều 5. Cơ cấu tổ chức bộ máy của Chi nhánh số 23")
    add_clause("Ban Lãnh đạo Chi nhánh gồm có Giám đốc Chi nhánh và các Phó Giám đốc Chi nhánh. Số lượng Phó Giám đốc Chi nhánh thực hiện theo đúng đề án vị trí việc làm và quy định pháp luật. Việc bổ nhiệm, bổ nhiệm lại, kéo dài thời gian công tác, miễn nhiệm, điều động, khen thưởng, kỷ luật đối với Giám đốc và Phó Giám đốc Chi nhánh do Giám đốc Sở Nông nghiệp và Môi trường quyết định theo phân cấp quản lý cán bộ.", 1, "1. Lãnh đạo Chi nhánh: ")
    add_clause("Chi nhánh số 23 được cơ cấu gồm 03 Tổ nghiệp vụ trực thuộc:\n"
               "a) Tổ Hành chính – Tổng hợp;\n"
               "b) Tổ Đăng ký và Cấp giấy chứng nhận;\n"
               "c) Tổ Kỹ thuật Địa chính và Lưu trữ.\n"
               "Việc thành lập, chia tách, sáp nhập, tổ chức lại các Tổ nghiệp vụ thuộc Chi nhánh do Giám đốc Chi nhánh quyết định sau khi có ý kiến thống nhất bằng văn bản của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố phụ trách đơn vị.", 1, "2. Các Tổ nghiệp vụ: ")
    add_clause("Mỗi Tổ nghiệp vụ có 01 Tổ trưởng và các Tổ phó (không quá 03 Tổ phó theo quy định tại Điều 4 Quyết định 2637/QĐ-SNNMT-VP) cùng các viên chức, người lao động chuyên môn. Việc bổ nhiệm, miễn nhiệm Tổ trưởng, Tổ phó do Giám đốc Chi nhánh quyết định sau khi có ý kiến thống nhất của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố.", 1, "3. Lãnh đạo Tổ nghiệp vụ: ")

    add_article_title("Điều 6. Chức năng, nhiệm vụ cụ thể của các Tổ nghiệp vụ")
    add_clause("Tổ Hành chính – Tổng hợp là tổ nghiệp vụ chuyên môn giúp việc cho Ban Lãnh đạo Chi nhánh về công tác tổng hợp, hành chính quản trị, tổ chức cán bộ, thi đua khen thưởng, tài chính kế toán và tiếp nhận - trả kết quả hồ sơ, cụ thể:\n"
               "- Công tác tổng hợp, điều phối: Xây dựng chương trình, kế hoạch công tác tháng, quý, năm, lịch tuần của Chi nhánh; theo dõi, đôn đốc tiến độ thực hiện; tổng hợp báo cáo định kỳ, đột xuất; chuẩn bị nội dung, tài liệu các cuộc họp giao ban, hội nghị của Chi nhánh.\n"
               "- Công tác văn thư, lưu trữ hành chính: Tiếp nhận, phân loại, đăng ký, chuyển giao, theo dõi văn bản đi, đến; quản lý con dấu pháp nhân của Chi nhánh, chứng thư số; thực hiện công tác bảo mật tài liệu hành chính theo quy định.\n"
               "- Công tác tổ chức cán bộ, lao động tiền lương: Quản lý hồ sơ viên chức, người lao động; theo dõi chấm công, ngày phép, đào tạo, bồi dưỡng, nâng lương, bảo hiểm xã hội, bảo hộ lao động, quy chế dân chủ cơ sở và nội quy kỷ luật cơ quan.\n"
               "- Công tác tài chính, kế toán: Lập dự toán thu, chi hàng năm; theo dõi, quản lý, kiểm soát các khoản thu phí, lệ phí, giá dịch vụ công về đất đai; thực hiện hạch toán phụ thuộc theo hướng dẫn của Văn phòng đăng ký đất đai Thành phố; quản lý tài sản công, cơ sở vật chất, mua sắm văn phòng phẩm, trang thiết bị; thực hiện công tác phòng cháy chữa cháy, an ninh trật tự, vệ sinh môi trường.\n"
               "- Công tác Bộ phận Một cửa: Bố trí viên chức tiếp nhận hồ sơ, kiểm tra tính đầy đủ của thành phần hồ sơ, xuất phiếu tiếp nhận và hẹn trả kết quả; số hóa hồ sơ đầu vào; luân chuyển hồ sơ sang các Tổ chuyên môn giải quyết; thu phí, lệ phí và bàn giao kết quả giải quyết cho tổ chức, công dân; hướng dẫn, giải đáp thủ tục hành chính, giải quyết phản ánh kiến nghị tại bộ phận tiếp dân.", 1, "1. Tổ Hành chính – Tổng hợp: ")

    add_clause("Tổ Đăng ký và Cấp giấy chứng nhận là tổ nghiệp vụ thực hiện các nhiệm vụ chuyên môn về đăng ký đất đai, cấp giấy chứng nhận, biến động đất đai và giao dịch bảo đảm trên địa bàn phụ trách, cụ thể:\n"
               "- Tiếp nhận hồ sơ từ Bộ phận Một cửa, thực hiện kiểm tra pháp lý, nguồn gốc sử dụng đất, điều kiện đăng ký, cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất theo quy định của Luật Đất đai năm 2024 và các nghị định hướng dẫn thi hành.\n"
               "- Thẩm tra, xác minh thực địa đối với các trường hợp cần thiết; dự thảo văn bản xin ý kiến hoặc xác minh nguồn gốc đất tại UBND 05 phường phụ trách.\n"
               "- Lập Phiếu chuyển thông tin để xác định nghĩa vụ tài chính về đất đai sang Chi cục Thuế; theo dõi, đôn đốc và nhận thông báo nghĩa vụ tài chính từ cơ quan Thuế để chuyển cho người sử dụng đất thực hiện.\n"
               "- Thực hiện đăng ký biến động (chuyển nhượng, tặng cho, thừa kế, chuyển mục đích sử dụng đất, tách thửa, hợp thửa, thay đổi thông tin nhân thân, biến động tài sản trên đất...); in Giấy chứng nhận mới hoặc in nội dung xác nhận thay đổi vào trang bổ sung, trang 3, 4 của Giấy chứng nhận hiện hành theo phân cấp.\n"
               "- Thực hiện đăng ký biện pháp bảo đảm bằng quyền sử dụng đất, tài sản gắn liền với đất; đăng ký thay đổi, đăng ký văn bản thông báo xử lý tài sản bảo đảm, xóa đăng ký biện pháp bảo đảm đúng thời hạn quy định (trong ngày làm việc hoặc không quá 03 ngày làm việc đối với trường hợp phức tạp).\n"
               "- Thực hiện thủ tục cấp đổi, cấp lại, đính chính thông tin Giấy chứng nhận bị sai sót; phối hợp giải quyết các thủ tục thu hồi, hủy Giấy chứng nhận theo quy định pháp luật.", 1, "2. Tổ Đăng ký và Cấp giấy chứng nhận: ")

    add_clause("Tổ Kỹ thuật Địa chính và Lưu trữ là tổ nghiệp vụ chuyên môn về kỹ thuật đo đạc, bản đồ địa chính, xây dựng cơ sở dữ liệu đất đai và quản lý kho lưu trữ hồ sơ địa chính, cụ thể:\n"
               "- Công tác đo đạc, bản đồ: Thực hiện trích lục bản đồ địa chính, trích đo địa chính thửa đất; kiểm tra, thẩm tra và trình Lãnh đạo Chi nhánh ký duyệt mảnh trích đo địa chính do các tổ chức tư vấn đo đạc thực hiện; kiểm tra xác nhận sơ đồ nhà ở và tài sản gắn liền với đất phục vụ đăng ký, cấp Giấy chứng nhận.\n"
               "- Công tác cập nhật, chỉnh lý hồ sơ địa chính: Cập nhật biến động thường xuyên lên bản đồ địa chính số, sổ địa chính, sổ mục kê đất đai; lập phiếu chỉnh lý biến động và sao gửi cho UBND các phường để đồng bộ hồ sơ; thực hiện công tác kiểm kê đất đai, lập bản đồ hiện trạng sử dụng đất định kỳ.\n"
               "- Quản lý, vận hành cơ sở dữ liệu số: Vận hành hệ thống thông tin đất đai tại Chi nhánh; số hóa dữ liệu hồ sơ địa chính; đồng bộ dữ liệu vào Cơ sở dữ liệu quốc gia về đất đai và cơ sở dữ liệu dùng chung của Văn phòng đăng ký đất đai Thành phố; bảo đảm an toàn dữ liệu, an ninh mạng và dự phòng hệ thống.\n"
               "- Công tác quản lý kho lưu trữ hồ sơ địa chính: Tiếp nhận, phân loại, chỉnh lý, bảo quản, đóng tập toàn bộ hồ sơ đăng ký đất đai, hồ sơ cấp Giấy chứng nhận đã hoàn thành từ Tổ Đăng ký và Cấp giấy chứng nhận; bảo quản nghiêm ngặt phôi Giấy chứng nhận; phục vụ tra cứu, cung cấp thông tin, trích sao dữ liệu đất đai theo yêu cầu của cơ quan có thẩm quyền và người dân; chấp hành nghiêm ngặt chế độ bảo mật, phòng chống cháy nổ, mối mọt tại kho lưu trữ hồ sơ.", 1, "3. Tổ Kỹ thuật Địa chính và Lưu trữ: ")

    # -------------------------------------------------------------
    # CHƯƠNG III: TRÁCH NHIỆM, QUYỀN HẠN VÀ CÁCH THỨC GIẢI QUYẾT CÔNG VIỆC
    # -------------------------------------------------------------
    add_chapter("Chương III", "TRÁCH NHIỆM, PHẠM VI, QUYỀN HẠN VÀ CÁCH THỨC GIẢI QUYẾT CÔNG VIỆC")

    add_article_title("Điều 7. Những nội dung đưa ra tập thể Ban Lãnh đạo Chi nhánh thảo luận trước khi Giám đốc quyết định")
    add_clause("Tập thể Ban Lãnh đạo Chi nhánh (Giám đốc và các Phó Giám đốc Chi nhánh, trường hợp cần thiết mở rộng đến Tổ trưởng các Tổ nghiệp vụ) thảo luận tập thể trước khi Giám đốc quyết định đối với các nội dung trọng tâm sau:\n"
               "1. Kế hoạch, chương trình công tác tháng, quý, 6 tháng và năm của Chi nhánh; đề án, giải pháp nâng cao hiệu quả giải quyết thủ tục hành chính, cải cách thủ tục hành chính và chuyển đổi số.\n"
               "2. Phương án sắp xếp tổ chức bộ máy, đề xuất biên chế, số lượng người làm việc, quy hoạch, đề bạt, bổ nhiệm, bổ nhiệm lại, điều động, luân chuyển nhân sự giữa các Tổ nghiệp vụ.\n"
               "3. Dự toán thu, chi tài chính hàng năm; phương án phân bổ kinh phí, mua sắm tài sản lớn, sửa chữa trụ sở làm việc; quy chế chi tiêu nội bộ (nếu được phân cấp).\n"
               "4. Báo cáo tổng kết công tác năm, kiểm điểm công tác lãnh đạo điều hành; bình xét danh hiệu thi đua, khen thưởng và kỷ luật viên chức, người lao động.\n"
               "5. Các hồ sơ vụ việc giải quyết thủ tục đất đai phức tạp, tồn đọng, khiếu nại gay gắt, có tranh chấp hoặc có ý kiến khác nhau giữa các Tổ nghiệp vụ; các vụ việc theo yêu cầu chỉ đạo trực tiếp của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố hoặc Sở Nông nghiệp và Môi trường.\n"
               "6. Hình thức thảo luận: Tổ chức họp Ban Lãnh đạo định kỳ hoặc đột xuất. Trường hợp khẩn cấp không thể tổ chức họp, Giám đốc gửi phiếu lấy ý kiến bằng văn bản cho các Phó Giám đốc. Các Phó Giám đốc có trách nhiệm trả lời đúng thời hạn; hết thời hạn không trả lời được xem là đồng ý. Sau khi thảo luận hoặc lấy ý kiến, Giám đốc là người đưa ra quyết định cuối cùng và chịu trách nhiệm toàn diện trước cấp trên và pháp luật.", 1)

    add_article_title("Điều 8. Trách nhiệm và quyền hạn giải quyết công việc của Giám đốc Chi nhánh")
    add_clause("Giám đốc Chi nhánh là người đứng đầu đơn vị sự nghiệp, chịu trách nhiệm trực tiếp, toàn diện trước Giám đốc Văn phòng đăng ký đất đai Thành phố, Giám đốc Sở Nông nghiệp và Môi trường và trước pháp luật về toàn bộ hoạt động của Chi nhánh số 23 theo chức năng, nhiệm vụ, quyền hạn được giao.", 1, "1. Vị trí, trách nhiệm chung: ")
    add_clause("Giám đốc Chi nhánh có các trách nhiệm cụ thể sau:\n"
               "a) Chỉ đạo, điều hành toàn diện mọi hoạt động của Chi nhánh theo đường lối, chủ trương của Đảng, chính sách, pháp luật của Nhà nước, Quy chế làm việc của Văn phòng đăng ký đất đai Thành phố và Quy chế này.\n"
               "b) Phân công nhiệm vụ cụ thể bằng văn bản cho các Phó Giám đốc, các Tổ trưởng nghiệp vụ và viên chức; thường xuyên kiểm tra, đôn đốc, giám sát việc thực hiện nhiệm vụ được giao.\n"
               "c) Quản lý, sử dụng viên chức, người lao động; tổ chức thực hiện các biện pháp phòng ngừa, đấu tranh chống tham nhũng, lãng phí, quan liêu, hách dịch, nhũng nhiễu trong đơn vị; chịu trách nhiệm liên đới nếu để xảy ra tiêu cực, vi phạm pháp luật thuộc phạm vi quản lý.\n"
               "d) Quản lý, sử dụng có hiệu quả tài chính, tài sản công, đất đai trụ sở, trang thiết bị kỹ thuật được giao theo đúng quy định pháp luật.", 1, "2. Trách nhiệm cụ thể: ")
    add_clause("Giám đốc Chi nhánh có các quyền hạn sau:\n"
               "a) Ban hành Quy chế làm việc của Chi nhánh, phân công nhiệm vụ Lãnh đạo Chi nhánh, quy định cụ thể chức năng, nhiệm vụ của các Tổ nghiệp vụ sau khi có ý kiến thống nhất của Văn phòng đăng ký đất đai Thành phố.\n"
               "b) Ký các quyết định điều hành nội bộ; ký các văn bản, báo cáo quan trọng gửi Ban Giám đốc Văn phòng đăng ký đất đai Thành phố, Sở Nông nghiệp và Môi trường, UBND thành phố Thủ Dầu Một và các sở, ngành liên quan.\n"
               "c) Ký cấp đổi, cấp lại, đính chính, ký duyệt đăng ký biến động trên Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất theo đúng thẩm quyền và phân cấp ủy quyền của Giám đốc Văn phòng đăng ký đất đai Thành phố.\n"
               "d) Phê duyệt dự toán, kế hoạch mua sắm, thanh quyết toán các khoản chi thường xuyên trong phạm vi nguồn tài chính được giao tự chủ; đề xuất ký kết hợp đồng lao động, hợp đồng vụ việc theo quy định.\n"
               "đ) Đề xuất việc khen thưởng, kỷ luật, bổ nhiệm, bổ nhiệm lại cán bộ, viên chức lên cấp trên có thẩm quyền; quyết định biểu dương, phê bình trong nội bộ cơ quan.\n"
               "e) Ủy quyền cho một Phó Giám đốc điều hành toàn bộ công việc của Chi nhánh khi Giám đốc vắng mặt.", 1, "3. Quyền hạn giải quyết công việc: ")
    add_clause("Khi Giám đốc Chi nhánh vắng mặt tại nhiệm sở từ 1/2 ngày làm việc trở lên phải báo cáo và được sự chấp thuận của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố phụ trách đơn vị (theo đúng Khoản 3 Điều 8 Quyết định 2637/QĐ-SNNMT-VP); đồng thời ủy quyền bằng văn bản cho một Phó Giám đốc điều hành Chi nhánh.", 1, "4. Chế độ vắng mặt: ")

    add_article_title("Điều 9. Trách nhiệm và quyền hạn giải quyết công việc của Phó Giám đốc Chi nhánh")
    add_clause("Phó Giám đốc Chi nhánh là cấp phó của người đứng đầu, giúp Giám đốc Chi nhánh phụ trách, theo dõi, chỉ đạo một số lĩnh vực công tác, một số Tổ nghiệp vụ theo phân công bằng văn bản của Giám đốc; chịu trách nhiệm trước Giám đốc Chi nhánh và trước pháp luật về toàn bộ quá trình và kết quả thực hiện nhiệm vụ được giao.", 1, "1. Vị trí, trách nhiệm: ")
    add_clause("Phó Giám đốc Chi nhánh có các quyền hạn và nghĩa vụ sau:\n"
               "a) Trong phạm vi lĩnh vực và nhiệm vụ được phân công, Phó Giám đốc được sử dụng quyền hạn của Giám đốc để chỉ đạo, đôn đốc, xử lý công việc và ký thừa lệnh, ký thay các văn bản, hồ sơ giải quyết thủ tục đất đai, đăng ký biến động, đăng ký biện pháp bảo đảm theo đúng thẩm quyền phân công, ủy quyền.\n"
               "b) Chủ động chỉ đạo, xử lý các công việc thường xuyên thuộc lĩnh vực phụ trách; kịp thời phát hiện, xử lý các vướng mắc, khó khăn trong thực hiện quy trình nghiệp vụ; chịu trách nhiệm cá nhân về đề xuất chuyên môn và tính pháp lý của hồ sơ do mình ký duyệt.\n"
               "c) Khi giải quyết công việc liên quan đến lĩnh vực do Phó Giám đốc khác phụ trách thì Phó Giám đốc chủ trì chủ động trao đổi, phối hợp thống nhất trước khi quyết định. Trường hợp còn ý kiến khác nhau hoặc vấn đề vượt thẩm quyền, phải báo cáo kịp thời xin ý kiến Giám đốc Chi nhánh.\n"
               "d) Trường hợp Ban Giám đốc Văn phòng đăng ký đất đai Thành phố làm việc và phân công công việc trực tiếp cho Phó Giám đốc Chi nhánh, Phó Giám đốc có trách nhiệm thi hành nghiêm túc, đồng thời báo cáo ngay cho Giám đốc Chi nhánh biết về nội dung chỉ đạo (theo đúng Khoản 6 Điều 7 Quyết định 2637/QĐ-SNNMT-VP).\n"
               "đ) Khi vắng mặt (do nghỉ phép, đi công tác), Phó Giám đốc phải báo cáo Giám đốc Chi nhánh bằng văn bản để bố trí người thay thế điều hành, bảo đảm hoạt động của đơn vị thông suốt, liên tục.", 1, "2. Quyền hạn và nghĩa vụ cụ thể: ")

    add_article_title("Điều 10. Trách nhiệm và quyền hạn của Tổ trưởng, Tổ phó các Tổ nghiệp vụ")
    add_clause("Tổ trưởng Tổ nghiệp vụ là người đứng đầu Tổ chuyên môn, chịu trách nhiệm trước Giám đốc Chi nhánh, Phó Giám đốc phụ trách và trước pháp luật về toàn bộ chất lượng, tiến độ công việc của Tổ; quản lý, điều hành, phân công nhiệm vụ cụ thể cho từng Tổ phó và viên chức, người lao động trong Tổ; kiểm tra, rà soát tính chuẩn xác, tính pháp lý của hồ sơ trước khi trình Lãnh đạo Chi nhánh ký duyệt.", 1, "1. Trách nhiệm, quyền hạn của Tổ trưởng: ")
    add_clause("Tổ phó là người giúp việc cho Tổ trưởng, phụ trách một số mảng công việc cụ thể theo phân công của Tổ trưởng và chỉ đạo của Lãnh đạo Chi nhánh; chịu trách nhiệm trước Tổ trưởng, trước Lãnh đạo Chi nhánh và pháp luật về kết quả công việc được giao. Khi Tổ trưởng vắng mặt, 01 Tổ phó được Tổ trưởng ủy nhiệm bằng văn bản điều hành hoạt động của Tổ.", 1, "2. Trách nhiệm, quyền hạn của Tổ phó: ")
    add_clause("Chấp hành tuyệt đối sự chỉ đạo của Lãnh đạo Chi nhánh; không chuyển công việc thuộc trách nhiệm của Tổ mình sang Tổ khác hoặc trình vượt cấp; thực hiện nghiêm túc chế độ báo cáo tuần, tháng, quý về tiến độ giải quyết hồ sơ và các khó khăn, vướng mắc phát sinh.", 1, "3. Kỷ luật điều hành: ")

    add_article_title("Điều 11. Trách nhiệm, nghĩa vụ và quyền hạn của viên chức, người lao động")
    add_clause("Viên chức, người lao động chịu trách nhiệm chấp hành nghiêm túc sự phân công nhiệm vụ của Lãnh đạo Chi nhánh và Tổ trưởng; chủ động nghiên cứu, nắm vững chuyên môn, chính sách, pháp luật về đất đai; trực tiếp xử lý hồ sơ, công việc được phân công bảo đảm chất lượng, đúng quy trình nghiệp vụ và đúng thời hạn quy định.", 1, "1. Trách nhiệm thực hiện nhiệm vụ: ")
    add_clause("Tuân thủ Nội quy cơ quan (Quyết định số 02/QĐ-VPĐK-HC) và văn hóa công sở:\n"
               "- Có mặt làm việc đúng giờ; trang phục chỉnh tề, lịch sự; đeo thẻ viên chức, thẻ nhân viên trong suốt thời gian làm việc.\n"
               "- Giữ gìn thái độ chuẩn mực, hòa nhã, lịch sự, tôn trọng, tận tình hướng dẫn người dân và tổ chức; ngôn ngữ giao tiếp chuẩn mực, tuyệt đối không hách dịch, quát tháo, tranh cãi với người dân.\n"
               "- Thực hiện bảo mật thông tin nội bộ, số liệu hồ sơ địa chính; nghiêm cấm sao chép, cung cấp dữ liệu ra ngoài khi chưa được phép của Lãnh đạo Chi nhánh; bảo quản cẩn thận hồ sơ, tài liệu, tài sản công được giao.", 1, "2. Nghĩa vụ và kỷ luật đạo đức công vụ: ")
    add_clause("Nghiêm cấm các hành vi tiêu cực theo Điều 9 Quyết định 02/QĐ-VPĐK-HC:\n"
               "- Nhận tiền, quà biếu, hiện vật hoặc lợi ích vật chất, phi vật chất dưới bất kỳ hình thức nào để ưu tiên, can thiệp xử lý nhanh hồ sơ hoặc bỏ qua sai phạm.\n"
               "- Cố ý làm sai lệch hồ sơ, giả mạo tài liệu, tẩy xóa, phá hoại dữ liệu địa chính số; tự ý kéo dài thời gian thụ lý hồ sơ không có lý do chính đáng.\n"
               "- Sử dụng phương tiện, trang thiết bị công vào mục đích cá nhân; làm việc riêng, uống rượu bia trong giờ làm việc, gây mất trật tự cơ quan.", 1, "3. Những việc bị nghiêm cấm: ")
    add_clause("Được bảo đảm các điều kiện làm việc cần thiết, trang thiết bị bảo hộ, máy móc chuyên dùng; được tham gia các khóa đào tạo, bồi dưỡng nâng cao trình độ; được hưởng đầy đủ tiền lương, phụ cấp, bảo hiểm và chế độ khen thưởng theo quy định pháp luật.", 1, "4. Quyền lợi: ")

    # -------------------------------------------------------------
    # CHƯƠNG IV: CHƯƠNG TRÌNH CÔNG TÁC, CHẾ ĐỘ THÔNG TIN, BÁO CÁO VÀ HỘI HỌP
    # -------------------------------------------------------------
    add_chapter("Chương IV", "CHƯƠNG TRÌNH CÔNG TÁC, CHẾ ĐỘ HỘI HỌP VÀ THÔNG TIN BÁO CÁO")

    add_article_title("Điều 12. Các loại chương trình và kế hoạch công tác")
    add_clause("Chi nhánh số 23 thực hiện công tác theo hệ thống kế hoạch, chương trình công tác đồng bộ, gồm:\n"
               "1. Chương trình công tác năm: Xác định các chỉ tiêu lớn, nhiệm vụ trọng tâm về tiếp nhận hồ sơ, cấp Giấy chứng nhận, đo đạc lập bản đồ, xây dựng CSDL địa chính, thu phí lệ phí; các giải pháp thực hiện và phân kỳ tiến độ từng quý, tháng.\n"
               "2. Chương trình công tác quý: Cụ thể hóa chương trình công tác năm thành danh mục nhiệm vụ chi tiết của từng Tổ nghiệp vụ; đánh giá kết quả quý trước và điều chỉnh mục tiêu quý tiếp theo.\n"
               "3. Chương trình công tác tháng: Triển khai các công việc cụ thể trong tháng đến từng Tổ nghiệp vụ và từng vị trí việc làm; kiểm điểm tiến độ định kỳ hàng tuần.\n"
               "4. Lịch công tác tuần: Bố trí lịch làm việc, tiếp dân, đi kiểm tra hiện trường, dự họp của Lãnh đạo Chi nhánh từ thứ Hai đến thứ Sáu (và sáng thứ Bảy theo quy định). Tổ Hành chính – Tổng hợp tổng hợp, ban hành lịch tuần vào chiều thứ Sáu hàng tuần.", 1)

    add_article_title("Điều 13. Chế độ hội họp và giao ban")
    add_clause("Chế độ hội họp của Chi nhánh được tổ chức khoa học, tiết kiệm, hiệu quả, gồm:\n"
               "1. Giao ban Lãnh đạo Chi nhánh: Tổ chức vào sáng thứ Hai hàng tuần để đánh giá kết quả chỉ đạo trong tuần qua và thống nhất kế hoạch công tác tuần mới.\n"
               "2. Giao ban toàn đơn vị: Tổ chức định kỳ hàng tháng giữa Ban Lãnh đạo Chi nhánh với Tổ trưởng, Tổ phó và toàn thể viên chức để đánh giá kết quả thực hiện nhiệm vụ chuyên môn, giải quyết các khó khăn vướng mắc và bình xét công tác.\n"
               "3. Hội nghị sơ kết 6 tháng và tổng kết năm: Đánh giá toàn diện các mặt công tác, kiểm điểm trách nhiệm của người đứng đầu, bình xét danh hiệu thi đua, khen thưởng theo quy định.\n"
               "4. Họp chuyên đề, đột xuất: Triển khai khi có chỉ đạo khẩn của Văn phòng đăng ký đất đai Thành phố hoặc giải quyết các hồ sơ, vụ việc đất đai phức tạp, cấp bách.", 1)

    add_article_title("Điều 14. Thời gian làm việc và tiếp nhận hồ sơ")
    add_clause("Thời gian làm việc hành chính của Chi nhánh thực hiện theo đúng Khoản 1 Điều 8 Quyết định số 02/QĐ-VPĐK-HC:\n"
               "- Buổi sáng: Từ 07 giờ 30 phút đến 11 giờ 30 phút.\n"
               "- Buổi chiều: Từ 13 giờ 00 phút đến 17 giờ 00 phút.\n"
               "- Các ngày làm việc từ thứ Hai đến thứ Sáu và sáng thứ Bảy (đối với Bộ phận Một cửa tiếp nhận và trả kết quả hồ sơ theo quy định giải quyết TTHC).", 1)

    add_article_title("Điều 15. Chế độ thông tin và báo cáo")
    add_clause("Chi nhánh số 23 thực hiện nghiêm túc chế độ báo cáo theo phân cấp:\n"
               "1. Báo cáo định kỳ gửi Ban Giám đốc Văn phòng đăng ký đất đai Thành phố: Báo cáo tuần (gửi trước 15 giờ thứ Năm), Báo cáo tháng (gửi trước ngày 22 hàng tháng), Báo cáo quý, 6 tháng, 9 tháng và Báo cáo năm (theo lịch của Văn phòng đăng ký đất đai Thành phố).\n"
               "2. Báo cáo đột xuất: Báo cáo ngay cho Giám đốc Văn phòng đăng ký đất đai Thành phố khi xảy ra các sự cố kỹ thuật lớn, tranh chấp đất đai khiếu kiện đông người, vi phạm kỷ luật của nhân viên hoặc có yêu cầu phối hợp khẩn cấp của cơ quan tố tụng, thanh tra, công an.\n"
               "3. Thông tin nội bộ: Thực hiện công khai, minh bạch các chủ trương, chính sách, kế hoạch công tác, phân bổ ngân sách, công tác cán bộ, khen thưởng kỷ luật cho toàn thể viên chức, người lao động qua bảng tin cơ quan và phần mềm điều hành nội bộ.", 1)

    add_article_title("Điều 16. Chế độ đào tạo, bồi dưỡng và nghỉ phép")
    add_clause("Chi nhánh thực hiện nghiêm túc Điều 8 Quyết định số 2637/QĐ-SNNMT-VP về chế độ đào tạo và nghỉ phép:\n"
               "1. Chế độ đào tạo, bồi dưỡng: Viên chức phải tham gia đầy đủ các chương trình đào tạo, bồi dưỡng chuyên môn do Văn phòng đăng ký đất đai Thành phố và Sở Nông nghiệp và Môi trường tổ chức; chủ động sắp xếp bàn giao công việc trước khi tham gia học tập.\n"
               "2. Chế độ nghỉ phép của viên chức, người lao động:\n"
               "- Khi có nhu cầu nghỉ phép năm, nghỉ việc riêng dưới 03 ngày làm việc: Phải có đơn bằng văn bản, có ý kiến của Tổ trưởng nghiệp vụ và được sự đồng ý của Lãnh đạo Chi nhánh.\n"
               "- Trường hợp nghỉ từ 03 ngày làm việc trở lên: Phải có ý kiến đề xuất của Giám đốc Chi nhánh và được sự chấp thuận của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố phụ trách Chi nhánh.\n"
               "- Nghỉ việc không hưởng lương: Phải có lý do chính đáng, được sự đồng ý của Giám đốc Chi nhánh và có văn bản chấp thuận của Giám đốc Văn phòng đăng ký đất đai Thành phố.\n"
               "- Nghỉ đi nước ngoài về việc riêng: Thực hiện theo đúng quy định quản lý cán bộ, viên chức đi nước ngoài của cấp có thẩm quyền.\n"
               "3. Chế độ vắng mặt của Lãnh đạo Chi nhánh: Giám đốc Chi nhánh khi vắng mặt từ 1/2 ngày làm việc trở lên phải báo cáo và được sự chấp thuận của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố phụ trách đơn vị.", 1)

    # -------------------------------------------------------------
    # CHƯƠNG V: QUY TRÌNH TIẾP NHẬN, XỬ LÝ VÀ TRÌNH KÝ CÔNG VIỆC
    # -------------------------------------------------------------
    add_chapter("Chương V", "QUY TRÌNH TIẾP NHẬN, XỬ LÝ VÀ TRÌNH KÝ HỒ SƠ, CÔNG VIỆC")

    add_article_title("Điều 17. Quy trình xử lý hồ sơ thủ tục hành chính tại Bộ phận Một cửa")
    add_clause("Toàn bộ hồ sơ yêu cầu giải quyết TTHC của người dân, tổ chức phải được tiếp nhận tập trung tại Bộ phận Một cửa của Chi nhánh:\n"
               "1. Tiếp nhận và số hóa: Viên chức Một cửa kiểm tra tính đầy đủ, hợp lệ của hồ sơ; quét (scan) số hóa toàn bộ tài liệu đầu vào; cấp Giấy tiếp nhận hồ sơ và hẹn trả kết quả có mã vạch định danh.\n"
               "2. Luân chuyển hồ sơ: Trong thời hạn tối đa 0,5 ngày làm việc kể từ khi tiếp nhận, bàn giao hồ sơ giấy kèm hồ sơ điện tử sang Tổ chuyên môn xử lý (Tổ Đăng ký và Cấp giấy chứng nhận hoặc Tổ Kỹ thuật Địa chính và Lưu trữ).\n"
               "3. Trả kết quả: Nhận kết quả đã ký duyệt và Giấy chứng nhận đã đóng dấu từ Tổ chuyên môn; thu phí, lệ phí theo biên lai điện tử; trả kết quả cho người dân và lưu phiếu kiểm soát quá trình giải quyết.", 1)

    add_article_title("Điều 18. Trình tự thẩm định, xác minh và luân chuyển xử lý nội bộ")
    add_clause("Quy trình xử lý nội bộ giữa các Tổ nghiệp vụ được thực hiện theo nguyên tắc khép kín, đúng thời hạn:\n"
               "1. Phân công xử lý: Tổ trưởng nghiệp vụ phân công chuyên viên thụ lý trong vòng 04 giờ làm việc kể từ khi nhận hồ sơ từ Bộ phận Một cửa.\n"
               "2. Thẩm định hồ sơ: Chuyên viên thụ lý kiểm tra pháp lý, đối chiếu hồ sơ địa chính, trích lục bản đồ. Trường hợp cần trích đo hoặc kiểm tra thực địa, Tổ Đăng ký và Cấp GCN phối hợp ngay với Tổ Kỹ thuật Địa chính để thực hiện.\n"
               "3. Luân chuyển thuế: Trường hợp phát sinh nghĩa vụ tài chính, lập Phiếu chuyển thông tin gửi cơ quan Thuế trong thời hạn không quá 02 ngày làm việc kể từ khi nhận đủ hồ sơ hợp lệ.\n"
               "4. Xử lý hồ sơ không đủ điều kiện: Chuyên viên lập văn bản thông báo hướng dẫn bổ sung hoặc trả lời lý do không giải quyết, trình Lãnh đạo Chi nhánh ký duyệt trong thời hạn quy định, gửi trả Bộ phận Một cửa để trả cho người nộp.", 1)

    add_article_title("Điều 19. Quy định về hồ sơ trình ký và trách nhiệm soát xét")
    add_clause("Hồ sơ trình Lãnh đạo Chi nhánh ký duyệt phải tuân thủ nghiêm ngặt theo Điều 13 Quyết định số 01/QĐ-VPĐK-HC:\n"
               "1. Thành phần hồ sơ trình: Bao gồm Phiếu trình giải quyết công việc (ghi rõ quá trình thụ lý, căn cứ pháp lý, ý kiến đề xuất); Dự thảo văn bản hoặc dự thảo Giấy chứng nhận; Hồ sơ gốc của người sử dụng đất; Phiếu chuyển thông tin địa chính, thông báo thuế (nếu có); Chữ ký nháy soát xét của chuyên viên thụ lý và Tổ trưởng nghiệp vụ.\n"
               "2. Trách nhiệm soát xét:\n"
               "- Chuyên viên thụ lý chịu trách nhiệm toàn diện trước pháp luật về tính chính xác của dữ liệu, nội dung ghi trên Giấy chứng nhận và tính pháp lý của hồ sơ đề xuất.\n"
               "- Tổ trưởng nghiệp vụ chịu trách nhiệm kiểm tra, thẩm định về quy trình, thủ tục, thời hạn giải quyết và tính chuẩn xác của hồ sơ trước khi ký nháy trình Lãnh đạo Chi nhánh.\n"
               "- Lãnh đạo Chi nhánh xem xét, ký duyệt trên cơ sở hồ sơ trình đầy đủ, hợp lệ.", 1)

    add_article_title("Điều 20. Phân định thẩm quyền ký duyệt văn bản và hồ sơ")
    add_clause("Thẩm quyền ký các loại văn bản và hồ sơ chuyên môn tại Chi nhánh số 23 được phân định rõ ràng:\n"
               "1. Giám đốc Chi nhánh ký duyệt:\n"
               "a) Các văn bản chỉ đạo điều hành nội bộ, quy chế, nội quy của Chi nhánh; kế hoạch công tác tháng, quý, năm.\n"
               "b) Báo cáo, tờ trình quan trọng gửi Ban Giám đốc Văn phòng đăng ký đất đai Thành phố, Sở Nông nghiệp và Môi trường và UBND thành phố Thủ Dầu Một.\n"
               "c) Quyết định, văn bản giải quyết khiếu nại, tố cáo, kết luận thanh tra, kiểm tra nội bộ.\n"
               "d) Ký cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất theo phân cấp, ủy quyền của Giám đốc Văn phòng đăng ký đất đai Thành phố; ký các hồ sơ đăng ký biến động phức tạp, hồ sơ chuyển quyền giá trị lớn.\n"
               "đ) Hợp đồng lao động, phê duyệt chi tiêu tài chính, mua sắm tài sản công theo thẩm quyền.\n"
               "2. Phó Giám đốc Chi nhánh ký duyệt (theo phân công của Giám đốc):\n"
               "a) Ký thay Giám đốc các hồ sơ đăng ký biến động quyền sử dụng đất, tài sản gắn liền với đất thường xuyên cho cá nhân, hộ gia đình trong phạm vi lĩnh vực được phân công.\n"
               "b) Ký xác nhận đăng ký biện pháp bảo đảm, xóa đăng ký thế chấp bằng quyền sử dụng đất, tài sản trên đất.\n"
               "c) Ký duyệt mảnh trích đo địa chính thửa đất, phiếu chỉnh lý bản đồ địa chính, trích lục bản đồ địa chính.\n"
               "d) Ký các phiếu chuyển thông tin nghĩa vụ tài chính sang cơ quan Thuế; thông báo thuế, thông báo trả kết quả, văn bản yêu cầu bổ sung hồ sơ.\n"
               "đ) Các văn bản triển khai nghiệp vụ, đôn đốc, báo cáo chuyên môn trong lĩnh vực được giao phụ trách.", 1)

    add_article_title("Điều 21. Thể thức và kỹ thuật trình bày văn bản hành chính")
    add_clause("Mọi văn bản hành chính do Chi nhánh số 23 ban hành bắt buộc 100% tuân thủ chặt chẽ thể thức, kỹ thuật trình bày văn bản theo đúng quy định tại Nghị định số 30/2020/NĐ-CP ngày 05 tháng 3 năm 2020 của Chính phủ và Quy chuẩn kỹ thuật DOCX ND30 của đơn vị, bảo đảm chuẩn xác về phông chữ Times New Roman, cỡ chữ, canh lề trang A4, số ký hiệu, trích yếu, chữ ký, con dấu và nơi nhận văn bản.", 1)

    # -------------------------------------------------------------
    # CHƯƠNG VI: QUAN HỆ CÔNG TÁC
    # -------------------------------------------------------------
    add_chapter("Chương VI", "MỐI QUAN HỆ CÔNG TÁC")

    add_article_title("Điều 22. Quan hệ với Sở Nông nghiệp và Môi trường và Văn phòng đăng ký đất đai Thành phố")
    add_clause("Chi nhánh số 23 tuân thủ nghiêm túc sự chỉ đạo của Giám đốc Sở Nông nghiệp và Môi trường; tham gia đầy đủ các cuộc họp do Lãnh đạo Sở triệu tập đối với các nội dung liên quan đến địa bàn và nhiệm vụ của Chi nhánh.", 1, "1. Đối với Sở Nông nghiệp và Môi trường: ")
    add_clause("Chi nhánh số 23 chịu sự quản lý, chỉ đạo trực tiếp, toàn diện của Giám đốc Văn phòng đăng ký đất đai Thành phố về tổ chức bộ máy, nhân sự, tài chính, cơ sở vật chất và chuyên môn nghiệp vụ; chấp hành tuyệt đối các chỉ đạo, kết luận của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố; kịp thời báo cáo, xin ý kiến chỉ đạo đối với các vụ việc phát sinh vượt thẩm quyền.", 1, "2. Đối với Văn phòng đăng ký đất đai Thành phố: ")

    add_article_title("Điều 23. Quan hệ với các Phòng chuyên môn và Chi nhánh trực thuộc Văn phòng đăng ký đất đai")
    add_clause("1. Đối với các Phòng chuyên môn thuộc Văn phòng đăng ký đất đai Thành phố (Phòng Hành chính – Tổng hợp, Phòng Đăng ký và Cấp giấy chứng nhận, Phòng Kỹ thuật Địa chính, Phòng Công nghệ Thông tin – Lưu trữ...): Chi nhánh số 23 chịu sự hướng dẫn, kiểm tra về chuyên môn nghiệp vụ; phối hợp chặt chẽ trong việc giải quyết hồ sơ nghiệp vụ liên thông; cung cấp số liệu, tài liệu báo cáo đúng thời hạn khi có yêu cầu.\n"
               "2. Đối với 37 Chi nhánh Văn phòng đăng ký đất đai trực thuộc khác: Quan hệ phối hợp công tác, chia sẻ kinh nghiệm nghiệp vụ, hỗ trợ tra cứu xác minh thông tin thửa đất, dữ liệu địa chính số liên quận, huyện, thành phố bảo đảm tính thống nhất, đồng bộ trên toàn địa bàn Thành phố Hồ Chí Minh mở rộng.", 1)

    add_article_title("Điều 24. Quan hệ với cấp ủy Đảng, Công đoàn và Đoàn Thanh niên")
    add_clause("1. Đối với Chi bộ Đảng: Lãnh đạo Chi nhánh phối hợp chặt chẽ với Chi ủy, Chi bộ trong công tác giáo dục chính trị tư tưởng, xây dựng đội ngũ viên chức, công tác tổ chức cán bộ, quy hoạch, bổ nhiệm, kiểm tra, giám sát đảng viên; tổ chức thực hiện các nghị quyết, chỉ thị của Đảng ủy cấp trên.\n"
               "2. Đối với Công đoàn và Chi đoàn Thanh niên: Lãnh đạo Chi nhánh phối hợp, tạo điều kiện thuận lợi cho tổ chức Công đoàn, Đoàn Thanh niên hoạt động hiệu quả; định kỳ làm việc để lắng nghe tâm tư, nguyện vọng, chăm lo bảo vệ quyền và lợi ích hợp pháp, chính đáng của đoàn viên; phát động các phong trào thi đua lao động giỏi, lao động sáng tạo, xây dựng cơ quan văn hóa, văn minh, hiện đại.", 1)

    add_article_title("Điều 25. Quan hệ phối hợp với UBND cấp huyện, UBND 05 phường và Chi cục Thuế")
    add_clause("1. Đối với UBND cấp huyện (thành phố Thủ Dầu Một): Thực hiện mối quan hệ phối hợp chặt chẽ theo Quy chế phối hợp do UBND Thành phố ban hành; tham gia các cuộc họp chuyên đề về quản lý đất đai; phối hợp cung cấp số liệu, dữ liệu phục vụ công tác quy hoạch, kế hoạch sử dụng đất, thu hồi đất, giải phóng mặt bằng trên địa bàn.\n"
               "2. Đối với UBND 05 phường phụ trách (Phú Lợi, Phú An, Bình Dương, Chánh Hiệp, Thủ Dầu Một): Thường xuyên trao đổi thông tin, phối hợp chặt chẽ trong việc xác minh nguồn gốc đất, tình trạng tranh chấp, lấn chiếm; phối hợp kiểm tra hiện trạng sử dụng đất; sao gửi thông báo cập nhật, chỉnh lý biến động địa chính để UBND cấp phường quản lý; tổ chức tiếp nhận hồ sơ lưu động hoặc giải quyết các vụ việc khiếu nại tại cơ sở.\n"
               "3. Đối với cơ quan Thuế: Phối hợp chặt chẽ trong công tác luân chuyển hồ sơ xác định nghĩa vụ tài chính qua đường truyền điện tử liên thông (hoặc trực tiếp); đôn đốc thông báo thuế bảo đảm thời hạn giải quyết TTHC cho người dân.", 1)

    add_article_title("Điều 26. Quan hệ với tổ chức, cá nhân, người dân đến làm việc")
    add_clause("Trong quan hệ giao dịch và làm việc với các tổ chức, doanh nghiệp và người dân, toàn thể Lãnh đạo, viên chức, người lao động Chi nhánh số 23 phải quán triệt phương châm 'Kỷ cương - Trách nhiệm - Tận tụy - Chuyên nghiệp':\n"
               "1. Luôn giữ thái độ tôn trọng, lắng nghe, hòa nhã, lịch sự; giải thích, hướng dẫn cặn kẽ, rõ ràng một lần bằng văn bản (Phiếu hướng dẫn hoàn thiện hồ sơ) nếu hồ sơ chưa hợp lệ, tuyệt đối không để người dân phải đi lại nhiều lần.\n"
               "2. Thực hiện nghiêm túc quy định không tiếp xúc, giải quyết công việc riêng với cá nhân, người nộp hồ sơ ngoài trụ sở cơ quan hoặc ngoài giờ làm việc trái quy định.\n"
               "3. Nghiêm cấm mọi hành vi quan liêu, hách dịch, cửa quyền, gây khó khăn, phiền hà, nhũng nhiễu, kéo dài thời gian giải quyết hồ sơ để vòi vĩnh, vụ lợi.\n"
               "4. Trường hợp người dân có hành vi gây rối, kích động, mất an ninh trật tự: Viên chức bình tĩnh ghi nhận, giữ vững nguyên tắc, kịp thời báo cáo Lãnh đạo Chi nhánh và phối hợp với lực lượng Công an địa phương xử lý theo quy định pháp luật.", 1)

    # -------------------------------------------------------------
    # CHƯƠNG VII: TỔ CHỨC THỰC HIỆN
    # -------------------------------------------------------------
    add_chapter("Chương VII", "ĐIỀU KHOẢN THI HÀNH")

    add_article_title("Điều 27. Theo dõi, kiểm tra và đánh giá thực hiện")
    add_clause("1. Việc chấp hành Quy chế làm việc là tiêu chí bắt buộc, quan trọng hàng đầu để đánh giá, xếp loại chất lượng viên chức, người lao động hàng tháng, quý và năm; là căn cứ bình xét các danh hiệu thi đua, khen thưởng hoặc xem xét xử lý kỷ luật đối với tập thể và cá nhân vi phạm.\n"
               "2. Tổ Hành chính – Tổng hợp có trách nhiệm làm đầu mối theo dõi, kiểm tra, đôn đốc việc thực hiện Quy chế làm việc trong toàn Chi nhánh; định kỳ báo cáo Giám đốc Chi nhánh tại các cuộc họp giao ban hàng tháng.", 1)

    add_article_title("Điều 28. Hiệu lực thi hành")
    add_clause("1. Quy chế này có hiệu lực thi hành kể từ ngày ký Quyết định ban hành. Toàn thể Ban Lãnh đạo Chi nhánh, Tổ trưởng, Tổ phó các Tổ nghiệp vụ cùng toàn thể viên chức, người lao động thuộc Chi nhánh số 23 có trách nhiệm thi hành nghiêm chỉnh Quy chế này.\n"
               "2. Trong quá trình tổ chức thực hiện, nếu có khó khăn, vướng mắc phát sinh hoặc có những nội dung chưa phù hợp với tình hình thực tế và quy định mới của cấp trên, các Tổ nghiệp vụ, viên chức kịp thời phản ánh về Tổ Hành chính – Tổng hợp để tổng hợp, báo cáo Giám đốc Chi nhánh xem xét sửa đổi, bổ sung cho phù hợp sau khi có ý kiến chấp thuận của Ban Giám đốc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh./.", 1)

    # Ký duyệt cuối Quy chế (Chi nhánh Văn phòng đăng ký đất đai số 23)
    p_end_space = doc.add_paragraph()
    p_end_space.paragraph_format.space_before = Pt(12)
    p_end_space.paragraph_format.space_after = Pt(0)

    t_qc_sig = doc.add_table(rows=1, cols=2)
    t_qc_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_qc_sig.autofit = False
    remove_table_borders(t_qc_sig)

    for row in t_qc_sig.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.3)
        set_cell_margins(row.cells[0], 0, 0, 0, 0)
        set_cell_margins(row.cells[1], 0, 0, 0, 0)

    c_sig_left = t_qc_sig.rows[0].cells[0]
    c_sig_right = t_qc_sig.rows[0].cells[1]

    # Bên phải là Giám đốc ký
    p_qc_ky = c_sig_right.paragraphs[0]
    p_qc_ky.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qc_ky.paragraph_format.space_after = Pt(45)
    r = p_qc_ky.add_run("GIÁM ĐỐC")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_qc_ky_ten = c_sig_right.add_paragraph()
    p_qc_ky_ten.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qc_ky_ten.paragraph_format.space_before = Pt(0)
    p_qc_ky_ten.paragraph_format.space_after = Pt(0)
    r = p_qc_ky_ten.add_run("(Ký, ghi rõ họ tên và đóng dấu)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    # Lưu tài liệu vào OUTPUT
    out_path = "OUTPUT/Quy_che_lam_viec_Chi_nhanh_23.docx"
    doc.save(out_path)
    print(f"Generated successfully: {out_path}")

if __name__ == "__main__":
    create_document()
