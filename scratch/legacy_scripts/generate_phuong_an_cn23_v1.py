import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=70, bottom=70, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
    tblPr.append(borders)

def set_table_borderless(table):
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
            tcPr.append(tcBorders)

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def add_divider_line(cell_or_doc, length_type="nation"):
    """
    Tạo đường kẻ ngang mảnh bằng chuỗi em-dash (—) nối liền không đứt đoạn,
    theo chuẩn QUY_CHUAN_DOCX_ND30.md:
    - length_type="agency": Dưới tên cơ quan ban hành -> 8 em-dashes cỡ 8.5pt.
    - length_type="nation": Dưới Tiêu ngữ -> 18 em-dashes cỡ 8.5pt.
    - length_type="subject": Dưới Trích yếu nội dung -> 8 em-dashes cỡ 8.5pt.
    """
    p = cell_or_doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    sp = parse_xml(r'<w:spacing %s w:before="0" w:after="80" w:line="120" w:lineRule="exact"/>' % nsdecls('w'))
    pPr.append(sp)
    
    dash_count = 18 if length_type == "nation" else 8
    r = p.add_run("—" * dash_count)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    r.bold = True
    return p

def add_page_number_to_section(section):
    section.different_first_page_header_footer = True
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w'))
    p._p.append(fld)

def add_para(doc, text="", bold_prefix="", indent=True, italic=False, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.49)
    else:
        p.paragraph_format.first_line_indent = Inches(0)
        
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(13)
        r_pre.bold = True
        
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.italic = italic
        r.bold = bold
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    return p

def add_legal_basis(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Inches(0.49)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.italic = True
    return p

def format_cell_text(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.first_line_indent = Inches(0)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)
    r.bold = bold
    r.italic = italic
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    return p

def main():
    doc = docx.Document()
    
    # Thiết lập Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)
    
    # 1. Thiết lập trang A4 Portrait căn lề chuẩn Nghị định 30/2020/NĐ-CP
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width = Inches(8.27)    # 210mm
    sec.page_height = Inches(11.69)  # 297mm
    sec.top_margin = Inches(0.79)    # 20mm
    sec.bottom_margin = Inches(0.79) # 20mm
    sec.left_margin = Inches(1.18)   # 30mm (chuẩn gáy tập)
    sec.right_margin = Inches(0.59)  # 15mm
    add_page_number_to_section(sec)
    
    # 2. Header Quốc hiệu & Đơn vị ban hành (Table 2 cột không viền)
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    set_table_borderless(tbl_hdr)
    
    cell_left = tbl_hdr.rows[0].cells[0]
    cell_right = tbl_hdr.rows[0].cells[1]
    cell_left.width = Inches(3.25)
    cell_right.width = Inches(3.25)
    
    # Cột trái: Tên cơ quan chủ quản và cơ quan ban hành
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.space_after = Pt(0)
    p_l.paragraph_format.line_spacing = 1.1
    r_cq_cq = p_l.add_run("SỞ NÔNG NGHIỆP VÀ MÔI TRƯỜNG\nVĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM\n")
    r_cq_cq.font.name = "Times New Roman"
    r_cq_cq.font.size = Pt(12)
    r_cq = p_l.add_run("CHI NHÁNH SỐ 23")
    r_cq.font.name = "Times New Roman"
    r_cq.font.size = Pt(13)
    r_cq.bold = True
    add_divider_line(cell_left, length_type="agency")
    
    p_code = cell_left.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.1
    r_c = p_code.add_run("Mã số QHNS: 1122149\nSố:       /PA-CN23")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(12)
    r_c.italic = True
    
    # Cột phải: Quốc hiệu, Tiêu ngữ, Địa danh & Thời gian
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.space_after = Pt(0)
    p_r.paragraph_format.line_spacing = 1.1
    r_qh = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_qh.font.name = "Times New Roman"
    r_qh.font.size = Pt(13)
    r_qh.bold = True
    r_tn = p_r.add_run("Độc lập - Tự do - Hạnh phúc")
    r_tn.font.name = "Times New Roman"
    r_tn.font.size = Pt(13)
    r_tn.bold = True
    add_divider_line(cell_right, length_type="nation")
    
    p_date = cell_right.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_after = Pt(0)
    p_date.paragraph_format.line_spacing = 1.1
    r_d = p_date.add_run("Thành phố Hồ Chí Minh, ngày 13 tháng 10 năm 2026")
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(13)
    r_d.italic = True
    
    # 3. Tiêu đề Phương án
    p_title_space = doc.add_paragraph()
    p_title_space.paragraph_format.space_after = Pt(6)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_t1 = p_title.add_run("PHƯƠNG ÁN DỰ TOÁN KINH PHÍ\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(15)
    r_t1.bold = True
    
    r_t2 = p_title.add_run("Về việc trang bị tài sản làm việc cho Giám đốc Chi nhánh mới nhậm chức theo Quyết định số 8541/QĐ-SNNMT-VP và Quy chế chi tiêu nội bộ số 355; sửa chữa chống thấm trụ sở và trang bị thiết bị phòng cháy, chữa cháy tại Chi nhánh Văn phòng Đăng ký đất đai số 23")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(13)
    r_t2.bold = True
    
    add_divider_line(doc, length_type="subject")
    
    # 4. DANH MỤC BIỂU VÀ PHỤ LỤC (theo mẫu CN34)
    p_bm = doc.add_paragraph()
    p_bm.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_bm.paragraph_format.space_before = Pt(8)
    p_bm.paragraph_format.space_after = Pt(4)
    r_bm = p_bm.add_run("DANH MỤC BIỂU VÀ PHỤ LỤC:")
    r_bm.font.name = "Times New Roman"
    r_bm.font.size = Pt(13)
    r_bm.bold = True
    
    add_para(doc, "Biểu 1: Bảng tổng hợp nội dung và khối lượng các hạng mục công việc.", indent=True)
    add_para(doc, "Biểu 2: Bảng tổng hợp dự toán kinh phí xin cấp chi tiết (3 nhóm hạng mục).", indent=True)
    add_para(doc, "Phụ lục 01: Bảng đối chiếu so sánh báo giá của 03 đơn vị cung cấp/thi công và đánh giá lựa chọn đơn vị có giá thấp nhất.", indent=True)
    
    # 5. PHẦN I: MỤC ĐÍCH VÀ CĂN CỨ XÂY DỰNG PHƯƠNG ÁN
    add_heading_1(doc, "I. MỤC ĐÍCH VÀ CĂN CỨ XÂY DỰNG PHƯƠNG ÁN")
    
    add_heading_2(doc, "A. Giới thiệu chung về hoạt động của Văn phòng Đăng ký đất đai Thành phố và Chi nhánh số 23:")
    
    add_para(doc, "1. Căn cứ pháp lý:", bold_prefix="", indent=False, bold=True)
    
    legal_bases = [
        "Căn cứ Luật Đất đai số 31/2024/QH15 ngày 18 tháng 01 năm 2024 được sửa đổi, bổ sung một số điều theo Luật số 43/2024/QH15 ngày 29 tháng 6 năm 2024;",
        "Căn cứ Luật Quản lý, sử dụng tài sản công số 15/2017/QH14 ngày 21 tháng 6 năm 2017; Luật sửa đổi, bổ sung một số điều của Luật Đấu thầu, Luật Đầu tư theo phương thức đối tác công tư, Luật Hải quan, Luật Thuế giá trị gia tăng, Luật Thuế xuất khẩu, thuế nhập khẩu, Luật Đầu tư, Luật Đầu tư công, Luật Quản lý sử dụng tài sản công số 90/2025/QH15 ngày 25 tháng 6 năm 2025;",
        "Căn cứ Luật Phòng cháy và chữa cháy số 27/2001/QH10 ngày 29 tháng 6 năm 2001 và Luật sửa đổi, bổ sung một số điều của Luật Phòng cháy và chữa cháy số 40/2013/QH13 ngày 22 tháng 11 năm 2013;",
        "Căn cứ Luật Đấu thầu số 22/2023/QH15 ngày 23 tháng 6 năm 2023; Luật số 57/2024/QH15 ngày 29 tháng 11 năm 2024 sửa đổi, bổ sung một số điều của Luật Quy hoạch, Luật Đầu tư, Luật Đầu tư theo phương thức đối tác công tư và Luật Đấu thầu;",
        "Căn cứ Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu;",
        "Căn cứ Nghị định số 17/2025/NĐ-CP ngày 06 tháng 02 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của các nghị định quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu;",
        "Căn cứ Nghị định số 155/2025/NĐ-CP ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;",
        "Căn cứ Nghị định số 136/2020/NĐ-CP ngày 24 tháng 11 năm 2020 và Nghị định số 50/2024/NĐ-CP ngày 10 tháng 5 năm 2024 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 136/2020/NĐ-CP quy định chi tiết thi hành một số điều và biện pháp thi hành Luật Phòng cháy và chữa cháy;",
        "Căn cứ Tiêu chuẩn Quốc gia TCVN 3890:2023 về Phòng cháy chữa cháy - Phương tiện phòng cháy và chữa cháy cho nhà và công trình - Trang bị, bố trí;",
        "Căn cứ Nghị định số 60/2021/NĐ-CP ngày 21 tháng 6 năm 2021 của Chính phủ quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập và Nghị định số 111/2025/NĐ-CP ngày 22 tháng 5 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 60/2021/NĐ-CP;",
        "Căn cứ Thông tư số 65/2021/TT-BTC ngày 29 tháng 7 năm 2021 của Bộ trưởng Bộ Tài chính quy định về lập dự toán, quản lý, sử dụng và quyết toán kinh phí bảo dưỡng, sửa chữa tài sản công;",
        "Căn cứ Nghị quyết số 204/2025/QH15 ngày 17 tháng 6 năm 2025 của Quốc hội và Nghị định số 174/2025/NĐ-CP ngày 30 tháng 6 năm 2025 của Chính phủ quy định chính sách giảm thuế giá trị gia tăng áp dụng thuế suất 8%;",
        "Căn cứ Quyết định số 1886/QĐ-UBND ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố Hồ Chí Minh về tổ chức lại Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh trên cơ sở hợp nhất Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Văn phòng Đăng ký đất đai tỉnh Bình Dương và Văn phòng Đăng ký đất đai tỉnh Bà Rịa – Vũng Tàu;",
        "Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23;",
        "Căn cứ Quyết định số 355/QĐ-VPĐK-KHTC ngày 31 tháng 12 năm 2025 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc ban hành Quy chế chi tiêu nội bộ năm 2025 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh;",
        "Căn cứ Quyết định số 8541/QĐ-SNNMT-VP ngày 30 tháng 9 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc điều động và bổ nhiệm ông Nguyễn Chiến Thắng, Phó Giám đốc Văn phòng Đăng ký đất đai Thành phố giữ chức vụ Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 thuộc Văn phòng Đăng ký đất đai Thành phố;",
        "Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc giao số lượng người làm việc cho Chi nhánh Văn phòng Đăng ký đất đai số 23;",
        "Căn cứ Công văn số 1656/CN23-HCTH ngày 21 tháng 7 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 về việc thuyết minh tiêu chuẩn, định mức sử dụng diện tích trụ sở làm việc tại số 358 Huỳnh Văn Cù, phường Thủ Dầu Một kèm Biên bản bàn giao, tiếp nhận tài sản công ngày 09 tháng 5 năm 2019;",
        "Căn cứ Báo cáo PCCC năm 2026 ngày 28 tháng 9 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 về tình hình triển khai các hoạt động hưởng ứng Ngày toàn dân phòng cháy, chữa cháy và an toàn kho tài liệu địa chính theo chỉ đạo tại Công văn số 24482/VPĐK-KT ngày 19 tháng 8 năm 2026 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh."
    ]
    for lb in legal_bases:
        add_legal_basis(doc, lb)
        
    add_para(doc, "2. Vị trí, chức năng, nhiệm vụ, quyền hạn:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Chi nhánh Văn phòng Đăng ký đất đai số 23 là đơn vị sự nghiệp công lập trực thuộc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, có tư cách pháp nhân, có con dấu riêng và được mở tài khoản tại Kho bạc Nhà nước và Ngân hàng theo quy định của pháp luật. Chi nhánh có chức năng thực hiện đăng ký đất đai, cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất; xây dựng, quản lý, cập nhật, chỉnh lý thống nhất hồ sơ địa chính và cơ sở dữ liệu đất đai; thống kê, kiểm kê đất đai; cung cấp thông tin, dữ liệu đất đai cho các tổ chức, cá nhân theo quy định của pháp luật trên địa bàn quản lý.")
    
    add_para(doc, "3. Cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Cơ cấu tổ chức bộ máy của Chi nhánh số 23 được quy định tại Quyết định số 2637/QĐ-SNNMT-VP của Sở Nông nghiệp và Môi trường và Quyết định số 8541/QĐ-SNNMT-VP về công tác cán bộ, gồm Ban Giám đốc và 03 tổ chuyên môn nghiệp vụ:")
    
    # Bảng cơ cấu tổ chức (Table 0)
    tbl_org = doc.add_table(rows=5, cols=3)
    tbl_org.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_org)
    make_row_header(tbl_org.rows[0])
    
    headers_org = ["STT", "Cơ cấu tổ chức", "Nhiệm vụ chủ yếu & Phụ trách"]
    widths_org = [Inches(0.6), Inches(2.2), Inches(3.7)]
    for i, h in enumerate(headers_org):
        format_cell_text(tbl_org.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
        set_cell_background(tbl_org.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_org.rows[0].cells[i], top=80, bottom=80, left=100, right=100)
        tbl_org.rows[0].cells[i].width = widths_org[i]
        
    org_data = [
        ("1", "Ban Giám đốc", "01 Giám đốc (ông Nguyễn Chiến Thắng - bổ nhiệm theo QĐ số 8541/QĐ-SNNMT-VP ngày 30/9/2026) và 01 Phó Giám đốc (ông Đặng Huy Cường). Lãnh đạo, chỉ đạo, điều hành toàn diện mọi mặt hoạt động của Chi nhánh."),
        ("2", "Tổ Hành chính - Tổng hợp", "Tổ trưởng: bà Nguyễn Thị Bích Tuyền. Thực hiện công tác văn thư lưu trữ, hành chính quản trị, tổ chức cán bộ, tài chính - kế toán, mua sắm tài sản, quản lý phương tiện PCCC và hậu cần."),
        ("3", "Tổ Kỹ thuật Địa chính và Lưu trữ", "Tổ trưởng: ông Trần Thanh Triết. Thực hiện công tác kỹ thuật đo đạc địa chính, kiểm tra nội nghiệp bản vẽ, thống kê kiểm kê đất đai; trực tiếp quản lý, bảo quản, khai thác kho lưu trữ hồ sơ, tài liệu địa chính gốc."),
        ("4", "Tổ Đăng ký và Cấp giấy chứng nhận", "Tổ trưởng: bà Nguyễn Thị Thùy Trang. Thực hiện thủ tục đăng ký đất đai, nhà ở và tài sản khác gắn liền với đất; cấp Giấy chứng nhận, đăng ký biến động và đăng ký biện pháp bảo đảm cho cá nhân, hộ gia đình.")
    ]
    for r_idx, r_val in enumerate(org_data, start=1):
        make_row_cant_split(tbl_org.rows[r_idx])
        for c_idx in range(3):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            bold = True if c_idx == 1 else False
            format_cell_text(tbl_org.rows[r_idx].cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=11)
            set_cell_margins(tbl_org.rows[r_idx].cells[c_idx], top=80, bottom=80, left=100, right=100)
            tbl_org.rows[r_idx].cells[c_idx].width = widths_org[c_idx]

    add_para(doc, "4. Chế độ làm việc và người đứng đầu:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Chi nhánh Văn phòng Đăng ký đất đai số 23 làm việc theo chế độ thủ trưởng kết hợp nguyên tắc tập trung dân chủ. Giám đốc Chi nhánh là người đứng đầu, chịu trách nhiệm trước Giám đốc Sở Nông nghiệp và Môi trường, Giám đốc Văn phòng Đăng ký đất đai Thành phố và trước pháp luật về toàn bộ hoạt động của Chi nhánh. Phó Giám đốc giúp việc Giám đốc và chịu trách nhiệm về lĩnh vực được phân công.")
    
    add_para(doc, "5. Số lượng viên chức, người lao động được giao:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Theo Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Chi nhánh số 23 được giao chỉ tiêu số lượng người làm việc năm 2026 là 85 người, gồm: 03 viên chức quản lý lãnh đạo Chi nhánh; 42 viên chức chuyên ngành; 37 chức danh chuyên môn dùng chung và 03 nhân viên hợp đồng lao động hỗ trợ, phục vụ (02 bảo vệ, 01 phục vụ).")
    
    add_para(doc, "6. Hiện trạng cơ sở nhà, đất và trụ sở hoạt động (theo Công văn số 1656/CN23-HCTH):", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Trụ sở hoạt động của Chi nhánh số 23 đặt tại số 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh (tiếp nhận nguyên trạng từ UBND phường Chánh Mỹ cũ theo Biên bản bàn giao, tiếp nhận tài sản công ngày 09 tháng 5 năm 2019):")
    add_para(doc, "- Khuôn viên đất quản lý, sử dụng ổn định: 1.417,70 m².")
    add_para(doc, "- Tổng diện tích sàn xây dựng thực tế của công trình khối nhà làm việc hiện hữu: 835,30 m², bao gồm:")
    add_para(doc, "  + Khối nhà trụ sở chính (kết cấu 02 tầng): Diện tích tầng 1 là 274,10 m²; diện tích tầng 2 là 274,10 m² (tổng diện tích sàn khối chính: 548,20 m²).")
    add_para(doc, "  + Khối nhà Bộ phận Tiếp nhận và Trả kết quả hồ sơ (Một cửa): 69,90 m².")
    add_para(doc, "  + Khối nhà Ban chỉ huy Quân sự cũ (bố trí phòng chuyên môn): 81,50 m².")
    add_para(doc, "  + Khối Hội trường họp chuyên môn kết hợp tiếp dân: 117,60 m².")
    add_para(doc, "  + Khu vệ sinh (Toilet): 18,10 m².")
    add_para(doc, "- Đánh giá hiện trạng công trình: Trụ sở UBND phường Chánh Mỹ cũ được đầu tư xây dựng đưa vào sử dụng đã lâu. Qua thời gian dài khai thác, nhiều hạng mục đã xuống cấp trầm trọng: kết cấu sàn mái bê tông, sê nô, máng xối và mương đón nước mái tôn bị rạn nứt, thấm dột nước mưa; trần nhà và tường bao ẩm mốc, sơn nước bong tróc từng mảng lớn, hệ thống điện và phụ kiện hư hỏng; đe dọa trực tiếp đến tính mạng cán bộ, người dân và an toàn của hàng nghìn mét giá tài liệu, hồ sơ địa chính gốc lưu trữ tại đơn vị.")
    
    add_para(doc, "7. Về cơ chế tài chính:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Chi nhánh Văn phòng Đăng ký đất đai số 23 thực hiện cơ chế tự chủ tài chính theo Nghị định số 60/2021/NĐ-CP và Nghị định số 111/2025/NĐ-CP của Chính phủ. Nguồn kinh phí hoạt động được bảo đảm từ nguồn thu phí, giá dịch vụ đăng ký đất đai theo quy định và nguồn kinh phí cấp cho hoạt động không thường xuyên, Quỹ Phát triển hoạt động sự nghiệp của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh.")

    add_heading_2(doc, "B. Mục đích của Phương án:")
    add_para(doc, "1. Sự cần thiết xây dựng phương án:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Xuất phát từ 03 yêu cầu thực tế cấp bách tại Chi nhánh Văn phòng Đăng ký đất đai số 23:")
    add_para(doc, "Thứ nhất, về việc trang bị tài sản làm việc cho tân Giám đốc Chi nhánh: Thực hiện Quyết định số 8541/QĐ-SNNMT-VP ngày 30 tháng 9 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh, ông Nguyễn Chiến Thắng (nguyên Phó Giám đốc Văn phòng Đăng ký đất đai Thành phố) được điều động và bổ nhiệm giữ chức vụ Giám đốc Chi nhánh số 23 kể từ ngày 01 tháng 10 năm 2026, được bảo lưu hệ số phụ cấp chức vụ lãnh đạo là 0,6 đến hết ngày 03 tháng 3 năm 2030. Hiện nay, phòng làm việc của Giám đốc Chi nhánh chưa được trang bị đầy đủ tài sản làm việc đạt chuẩn theo định mức. Do đó, việc trang bị bộ bàn ghế ngồi làm việc, tủ tài liệu, máy vi tính, máy in, điện thoại bàn và bàn ghế tiếp khách cho tân Giám đốc theo đúng tiêu chuẩn, định mức quy định tại Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC là điều kiện tiên quyết để đảm bảo hoạt động chỉ đạo, điều hành của người đứng đầu đơn vị.")
    add_para(doc, "Thứ hai, về việc sửa chữa chống thấm trụ sở cơ quan: Như đã thuyết minh tại Công văn số 1656/CN23-HCTH, trụ sở tại số 358 Huỳnh Văn Cù đang trong tình trạng xuống cấp nghiêm trọng, sàn mái và tường bị nứt, ngấm dột mỗi khi trời mưa lớn. Để kịp thời bảo vệ cơ sở vật chất, chống ẩm mốc phá hủy hồ sơ tài liệu địa chính, Chi nhánh số 23 cần áp dụng quy trình và giải pháp kỹ thuật sửa chữa chống thấm đã được kiểm chứng hiệu quả theo mẫu phương án của Chi nhánh số 34 (sử dụng màng chống thấm khò nhiệt Bitumode Delta-P 3mm và sơn phủ kháng UV SikaCoat Plus).")
    add_para(doc, "Thứ ba, về việc trang bị, bổ sung thiết bị phòng cháy chữa cháy (PCCC): Theo Báo cáo PCCC năm 2026 của đơn vị, Chi nhánh hiện có 26 bình chữa cháy tại chỗ nhưng chưa đồng bộ, thiếu bình khí CO2 chuyên dùng cho khu vực lưu trữ tài liệu giấy và phòng máy chủ, thiếu trang thiết bị cứu hộ, thoát nạn (đèn Exit, đèn sự cố, mặt nạ phòng độc cho lực lượng PCCC cơ sở, kệ bình, túi sơ cấp cứu). Nhằm thực hiện chỉ đạo của Văn phòng Đăng ký đất đai Thành phố tại Công văn số 24482/VPĐK-KT ngày 19/8/2026, việc bổ sung hoàn chỉnh phương tiện PCCC đạt chuẩn TCVN 3890:2023 là yêu cầu cấp thiết để bảo đảm an toàn tính mạng cho 85 nhân sự, hàng trăm lượt công dân đến giao dịch và tuyệt đối bảo vệ an toàn kho lưu trữ tài liệu đất đai.")
    
    add_para(doc, "2. Mục đích cụ thể của phương án:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "• Đảm bảo điều kiện, trang thiết bị làm việc của Giám đốc Chi nhánh mới nhậm chức theo đúng tiêu chuẩn, định mức quy định tại Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC và Quyết định bổ nhiệm số 8541/QĐ-SNNMT-VP.")
    add_para(doc, "• Khắc phục triệt để tình trạng thấm dột sàn mái, sê nô và tường nhà, tạo lập môi trường làm việc khô ráo, an toàn, bảo quản hồ sơ, sổ bộ địa chính không bị ẩm mốc, hư hại.")
    add_para(doc, "• Trang bị đầy đủ phương tiện PCCC tại chỗ, phương tiện cứu nạn cứu hộ theo quy chuẩn kỹ thuật, nâng cao năng lực ứng phó sự cố cháy nổ cho 4 tổ PCCC cơ sở.")
    add_para(doc, "• Làm căn cứ pháp lý để lập kế hoạch lựa chọn nhà thầu, áp dụng hình thức chỉ định thầu rút gọn theo Nghị định số 214/2025/NĐ-CP và quản lý, sử dụng nguồn kinh phí sự nghiệp đúng quy định, tiết kiệm, hiệu quả cao.")

    # 6. PHẦN II: YÊU CẦU VÀ NGUYÊN TẮC THỰC HIỆN
    add_heading_1(doc, "II. YÊU CẦU VÀ NGUYÊN TẮC THỰC HIỆN")
    
    add_heading_2(doc, "1. Phạm vi thực hiện:")
    add_para(doc, "Phương án bao gồm 03 nhóm nội dung công việc thực hiện tại trụ sở Chi nhánh Văn phòng Đăng ký đất đai số 23 (số 358 Huỳnh Văn Cù, phường Thủ Dầu Một):")
    add_para(doc, "- Nhóm 1: Mua sắm trang bị tài sản, máy móc thiết bị làm việc tại phòng Giám đốc Chi nhánh.")
    add_para(doc, "- Nhóm 2: Thi công sửa chữa, chống thấm sàn mái, sê nô, mương đón nước và tường sàn mái trụ sở làm việc.")
    add_para(doc, "- Nhóm 3: Mua sắm trang bị bổ sung thiết bị PCCC và cứu nạn, cứu hộ tại chỗ cơ sở.")

    add_heading_2(doc, "2. Yêu cầu kỹ thuật và quy cách từng nhóm hạng mục:")
    
    add_para(doc, "2.1. Yêu cầu kỹ thuật đối với tài sản trang bị cho Giám đốc Chi nhánh mới nhậm chức:", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Căn cứ Quyết định số 8541/QĐ-SNNMT-VP và Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC (Mục VII, Mục VIII và Mục B Phụ lục), tài sản trang bị mới 100%, bảo đảm thẩm mỹ, công năng và đúng định mức tối đa:")
    add_para(doc, "• Bộ bàn ghế ngồi làm việc Giám đốc: Bàn lãnh đạo gỗ công nghiệp cao cấp sơn phủ PU/Melamine chống trầy xước, có tủ phụ; kèm ghế xoay da lãnh đạo cao cấp, nệm mút đúc bọc da thật/PU màu đen, cần hơi thủy lực ngả hãm đa góc độ. Định mức tối đa theo Quy chế 355: 10.000.000 đồng/bộ (hoặc 7.000.000 đồng/bộ theo chức danh Chi nhánh).")
    add_para(doc, "• Tủ tài liệu Giám đốc: Tủ gỗ cao cấp 3 buồng, chia ngăn để tài liệu và khoang treo áo, kính cường lực, khóa an toàn. Định mức tối đa theo Quy chế 355: 7.000.000 đồng/chiếc.")
    add_para(doc, "• Máy vi tính để bàn làm việc: Máy tính đồng bộ thương hiệu uy tín (Dell/HP), bộ vi xử lý Intel Core i7 thế hệ mới, RAM 16GB DDR4/DDR5, ổ cứng thể rắn SSD NVMe 512GB, màn hình LED 23.8 - 27 inch FHD chống chói, bàn phím chuột đồng bộ. Định mức tối đa theo Quy chế 355: 20.000.000 đồng/bộ.")
    add_para(doc, "• Máy in laser đen trắng tự động 2 mặt: Máy in A4 tốc độ cao từ 38-40 trang/phút, tự động in hai mặt (Duplex), kết nối USB 2.0 và cổng mạng Network LAN Gigabit. Định mức tối đa theo Quy chế 355: 13.000.000 đồng/chiếc.")
    add_para(doc, "• Điện thoại cố định bàn: Điện thoại để bàn có màn hình hiển thị số gọi đến, âm thanh chuẩn rõ nét. Định mức tối đa theo Quy chế 355: 1.000.000 đồng/chiếc.")
    add_para(doc, "• Bộ bàn ghế họp, tiếp khách tại phòng Giám đốc: 01 bàn trà mặt đá/gỗ cao cấp kết hợp bộ sofa da sang trọng (hoặc bàn tròn 4 ghế bọc đệm da cao cấp). Định mức tối đa theo Mục B Quy chế 355: 13.000.000 đồng/bộ.")

    add_para(doc, "2.2. Yêu cầu kỹ thuật công tác thi công sửa chữa chống thấm (theo mẫu phương án CN34):", bold_prefix="", indent=False, bold=True)
    add_para(doc, "Áp dụng đầy đủ quy trình kỹ thuật chống thấm của Chi nhánh số 34, bao gồm 02 giải pháp:")
    add_para(doc, "a) Chống thấm sàn mái, sê nô mái, mương đón nước mái tôn bằng màng chống thấm Bitumode Delta – P 3mm (mặt trơn) dạng khò nhiệt:")
    add_para(doc, "- Chuẩn bị mặt bằng: Dùng máy mài chuyên dụng mài bỏ tạp chất, rêu mốc, lớp vữa yếu để tạo nhám tăng độ bám dính. Vệ sinh sạch bụi bẩn, tạp chất; xử lý vá phẳng các vết nứt, lỗ mọt; bo góc chân tường 45 độ.")
    add_para(doc, "- Phủ lớp lót kết nối: Quét 01 lớp lót hệ nước Nirol-W (hoặc Sikaproof Membrane pha nước) với định mức 0,2 kg/m², để khô hoàn toàn.")
    add_para(doc, "- Thi công dán màng: Sử dụng màng chống thấm bitum biến tính Polypropylene Bitumode Delta – P dày 3mm (mặt trơn) dạng khò nóng bằng đèn khò gas, dán chặt toàn bộ mặt sàn, mép nối chồng mí tối thiểu 10cm, dán vén lên chân tường tối thiểu 20-30cm.")
    add_para(doc, "b) Chống thấm tường sàn mái, tường sê nô mái, tường mương đón nước bằng hóa chất kháng UV SikaCoat Plus:")
    add_para(doc, "- Vệ sinh sạch bề mặt tường cũ bằng bàn chải sắt và máy phun nước áp lực; cạo bỏ dầu mỡ, lớp sơn vôi cũ bị rêu mốc, bong tróc.")
    add_para(doc, "- Xử lý vết nứt: Sử dụng Mastic dẻo chuyên dụng trám trét làm phẳng các khe nứt chân chim và khuyết tật bề mặt.")
    add_para(doc, "- Lăn phủ lớp chống thấm: Lăn phủ 02 lớp chống thấm đàn hồi kháng tia UV SikaCoat Plus với định mức chuẩn 0,6 kg/m² (lớp 1 chờ khô 3-4 giờ mới thi công lớp 2).")

    add_para(doc, "2.3. Yêu cầu kỹ thuật đối với thiết bị PCCC và cứu nạn cứu hộ (theo Báo cáo PCCC CN23):", bold_prefix="", indent=False, bold=True)
    add_para(doc, "• Bình chữa cháy bột ABC 4kg (MFZL4): Vỏ thép đúc chịu áp lực, nạp bột chữa cháy đa năng ABC dập tắt đám cháy chất rắn, lỏng, khí và thiết bị điện; có đồng hồ đo áp suất, có dán tem kiểm định của Cục Cảnh sát PCCC&CNCH. Hàng mới 100%.")
    add_para(doc, "• Bình chữa cháy khí CO2 3kg (MT3): Khí CO2 tinh khiết hóa lỏng chuyên dùng cho phòng máy chủ, kho lưu trữ hồ sơ tài liệu địa chính; khi dập lửa không để lại cặn bẩn, không làm ướt hay hư hỏng tài liệu giấy; có tem kiểm định PCCC. Hàng mới 100%.")
    add_para(doc, "• Kệ đặt bình chữa cháy đôi: Khung sắt sơn tĩnh điện màu đỏ chống rỉ sét, kích thước phù hợp đặt 02 bình chữa cháy, giữ bình cách sàn chống ẩm ướt.")
    add_para(doc, "• Bộ bảng tiêu lệnh và nội quy PCCC: Bằng chất liệu Mica cao cấp bền màu, chữ in sắc nét.")
    add_para(doc, "• Đèn chiếu sáng sự cố khẩn cấp (Emergency light): Tự động bật sáng khi mất nguồn điện lưới, thời gian duy trì sáng tối thiểu 2-3 giờ.")
    add_para(doc, "• Đèn chỉ dẫn thoát nạn (Exit LED): Đèn LED hiển thị lối thoát hiểm một mặt/hai mặt, tiết kiệm điện, có pin dự phòng.")
    add_para(doc, "• Mặt nạ phòng độc lọc khói độc: Mặt nạ trùm đầu tráng bạc chống bức xạ nhiệt kèm phin lọc độc chuyên dụng chống khí CO, HCN, khói độc; trang bị cho 4 tổ PCCC cơ sở.")
    add_para(doc, "• Túi y tế sơ cấp cứu loại B: Đầy đủ bông băng, gạc, nẹp, thuốc sát trùng theo đúng Thông tư số 19/2016/TT-BYT của Bộ Y tế.")
    add_para(doc, "• Dụng cụ phá dỡ cứu nạn: Rìu cứu nạn cán gỗ/thép chịu lực cách điện và búa thoát hiểm đa năng.")

    add_heading_2(doc, "3. Nguyên tắc thực hiện và lựa chọn nhà thầu:")
    add_para(doc, "• Căn cứ điểm c khoản 4 Điều 78 Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định về chỉ định thầu đối với gói thầu thuộc dự toán mua sắm không hình thành dự án có giá gói thầu không quá 500 triệu đồng; tổng dự toán của phương án này dưới 500 triệu đồng nên đủ điều kiện áp dụng hình thức chỉ định thầu rút gọn.")
    add_para(doc, "• Loại hợp đồng: Hợp đồng trọn gói.")
    add_para(doc, "• Thuế suất thuế GTGT: Áp dụng chính sách giảm thuế giá trị gia tăng xuống mức 8% theo quy định tại Nghị quyết số 204/2025/QH15 của Quốc hội và Nghị định số 174/2025/NĐ-CP của Chính phủ.")

    # 7. PHẦN III: NỘI DUNG - KHỐI LƯỢNG VÀ QUY TRÌNH THỰC HIỆN
    add_heading_1(doc, "III. NỘI DUNG, KHỐI LƯỢNG VÀ QUY TRÌNH THỰC HIỆN")
    
    add_para(doc, "Biểu 1: BẢNG TỔNG HỢP NỘI DUNG VÀ KHỐI LƯỢNG CÁC HẠNG MỤC", bold_prefix="", indent=False, bold=True)
    
    # Bảng Biểu 1 (Nội dung và khối lượng)
    tbl_b1 = doc.add_table(rows=1, cols=4)
    tbl_b1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b1)
    make_row_header(tbl_b1.rows[0])
    
    headers_b1 = ["STT", "NỘI DUNG HẠNG MỤC CÔNG VIỆC", "ĐVT", "KHỐI LƯỢNG"]
    widths_b1 = [Inches(0.6), Inches(4.3), Inches(0.7), Inches(0.9)]
    for i, h in enumerate(headers_b1):
        format_cell_text(tbl_b1.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
        set_cell_background(tbl_b1.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_b1.rows[0].cells[i], top=80, bottom=80, left=100, right=100)
        tbl_b1.rows[0].cells[i].width = widths_b1[i]
        
    b1_data = [
        ("I", "TRANG BỊ TÀI SẢN PHÒNG LÀM VIỆC GIÁM ĐỐC MỚI NHẬM CHỨC (THEO QĐ 8541 & QC 355)", "", ""),
        ("1", "Bộ bàn ghế ngồi làm việc Giám đốc (Bàn lãnh đạo cao cấp + Ghế xoay da thật/PU lãnh đạo ngả lưng)", "Bộ", "01"),
        ("2", "Tủ đựng tài liệu Giám đốc (Tủ gỗ 3 buồng chia ngăn tài liệu có khóa an toàn)", "Chiếc", "01"),
        ("3", "Máy vi tính để bàn làm việc (Core i7, RAM 16GB, SSD 512GB NVMe, Màn hình LED 24 inch FHD)", "Bộ", "01"),
        ("4", "Máy in laser đen trắng tự động 2 mặt khổ A4 kết nối cổng mạng LAN (HP/Brother)", "Chiếc", "01"),
        ("5", "Điện thoại bàn cố định hiển thị số gọi đến", "Chiếc", "01"),
        ("6", "Bộ bàn ghế họp, tiếp khách tại phòng Giám đốc (Bàn trà + Sofa da cao cấp)", "Bộ", "01"),
        ("II", "SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH SỐ 23 (THEO MẪU PHƯƠNG ÁN CN34)", "", ""),
        ("1", "Chống thấm sàn mái, sê nô mái, mương đón nước bằng màng khò nhiệt Bitumode Delta-P 3mm mặt trơn:\n- Dùng máy mài chuyên dụng tạo nhám, vệ sinh sạch bề mặt;\n- Quét 01 lớp lót hệ nước Nirol-W (định mức 0,2 kg/m²);\n- Chống thấm mái sử dụng Màng khò nóng Bitumode Delta-P 3mm mặt trơn.", "m²", "357,43"),
        ("2", "Chống thấm tường sàn mái, tường sê nô mái, tường mương đón nước bằng SikaCoat Plus:\n- Vệ sinh sạch bề mặt bằng bàn chải sắt;\n- Sử dụng MASTIC chuyên dụng sửa chữa, trám trét các vết nứt;\n- Lăn phủ 02 lớp chống thấm kháng tia UV SikaCoat Plus (định mức 0,6 kg/m²).", "m²", "285,38"),
        ("III", "TRANG BỊ THIẾT BỊ PHÒNG CHÁY CHỮA CHÁY (THEO BÁO CÁO PCCC CN23 & TCVN 3890:2023)", "", ""),
        ("1", "Bình chữa cháy bột ABC 4kg (MFZL4) có tem kiểm định của Cục Cảnh sát PCCC&CNCH", "Bình", "16"),
        ("2", "Bình chữa cháy khí CO2 3kg (MT3) có tem kiểm định PCCC (bảo vệ kho lưu trữ và máy chủ)", "Bình", "10"),
        ("3", "Kệ sắt để bình chữa cháy đôi sơn tĩnh điện màu đỏ", "Kệ", "13"),
        ("4", "Bộ bảng nội quy và tiêu lệnh chữa cháy bằng chất liệu Mica cao cấp", "Bộ", "06"),
        ("5", "Đèn chiếu sáng sự cố khẩn cấp tự động bật khi mất điện (Emergency Light)", "Bộ", "06"),
        ("6", "Đèn chỉ dẫn thoát nạn LED Exit 2 mặt (Exit Light)", "Bộ", "06"),
        ("7", "Mặt nạ phòng độc lọc khói khí độc chuyên dụng trang bị cho lực lượng PCCC cơ sở", "Cái", "12"),
        ("8", "Túi y tế sơ cấp cứu cứu hộ chuyên dụng loại B (theo Thông tư 19/2016/TT-BYT)", "Túi", "02"),
        ("9", "Dụng cụ phá dỡ cứu nạn: Rìu cứu hộ chuyên dụng cách điện + búa thoát hiểm đa năng", "Bộ", "02")
    ]
    
    for r_val in b1_data:
        row = tbl_b1.add_row()
        make_row_cant_split(row)
        is_group_header = r_val[0] in ["I", "II", "III"]
        for c_idx in range(4):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            bold = True if is_group_header else (c_idx == 0)
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=10.5)
            if is_group_header:
                set_cell_background(row.cells[c_idx], "F7F8FA")
            set_cell_margins(row.cells[c_idx], top=60, bottom=60, left=100, right=100)
            row.cells[c_idx].width = widths_b1[c_idx]

    add_heading_2(doc, "Quy trình thực hiện chuẩn 6 bước (theo mẫu CN34):")
    steps = [
        ("Bước 1: Khảo sát hiện trạng và thu thập báo giá: ", "Chi nhánh Văn phòng Đăng ký đất đai số 23 phối hợp với Tổ Hành chính – Tổng hợp tiến hành khảo sát chi tiết hiện trạng cơ sở vật chất, đo đạc khối lượng thấm dột thực tế và thu thập đủ 03 báo giá cạnh tranh từ các đơn vị cung cấp, thi công chuyên nghiệp."),
        ("Bước 2: Lập, thẩm định và trình duyệt phương án dự toán: ", "Chi nhánh số 23 lập Phương án dự toán chi tiết trình Phòng Kế hoạch – Tài chính Văn phòng Đăng ký đất đai Thành phố thẩm định, trình Giám đốc Văn phòng Đăng ký đất đai Thành phố phê duyệt."),
        ("Bước 3: Lập, thẩm định và trình duyệt Kế hoạch lựa chọn nhà thầu: ", "Chi nhánh số 23 lập Tờ trình kèm Kế hoạch lựa chọn nhà thầu (áp dụng hình thức chỉ định thầu rút gọn, hợp đồng trọn gói) chuyển Phòng Kế hoạch – Tài chính thẩm định trình Thủ trưởng đơn vị phê duyệt."),
        ("Bước 4: Thương thảo hợp đồng và ban hành Quyết định phê duyệt kết quả chỉ định thầu: ", "Chi nhánh số 23 tiến hành thương thảo hợp đồng với nhà thầu được chỉ định; Phòng Hành chính – Tổng hợp và Phòng Kế hoạch – Tài chính thực hiện thủ tục đăng tải thông tin trên Mạng đấu thầu quốc gia theo quy định."),
        ("Bước 5: Ký kết hợp đồng và tổ chức triển khai thực hiện: ", "Giám đốc Chi nhánh số 23 ký hợp đồng trọn gói với đơn vị được lựa chọn; phối hợp các Tổ chuyên môn giám sát chặt chẽ quá trình cung cấp tài sản, thi công chống thấm và bàn giao thiết bị PCCC."),
        ("Bước 6: Kiểm tra nghiệm thu, bàn giao đưa vào sử dụng và thanh quyết toán: ", "Ban Giám đốc Chi nhánh cùng Tổ Hành chính - Tổng hợp nghiệm thu thực tế, lập biên bản bàn giao tài sản đưa vào sử dụng; hoàn tất chứng từ chuyển Phòng Kế hoạch – Tài chính kiểm soát chi và giải ngân thanh toán dứt điểm.")
    ]
    for s_title, s_desc in steps:
        add_para(doc, s_desc, bold_prefix=s_title, indent=True)
        
    add_heading_2(doc, "Trách nhiệm kiểm tra nghiệm thu và hồ sơ thanh quyết toán:")
    add_para(doc, "• Chi nhánh Văn phòng Đăng ký đất đai số 23 và Tổ Hành chính – Tổng hợp chịu trách nhiệm toàn diện về tính chính xác của các chỉ tiêu số lượng, chủng loại, quy cách kỹ thuật, tem kiểm định PCCC và chất lượng thi công chống thấm trên biên bản nghiệm thu.")
    add_para(doc, "• Hồ sơ kiểm tra nghiệm thu làm căn cứ thanh toán gồm:")
    add_para(doc, "  1. Hợp đồng kinh tế trọn gói ký giữa Chi nhánh số 23 và đơn vị cung cấp/thi công;")
    add_para(doc, "  2. Biên bản kiểm tra nghiệm thu bàn giao đưa vào sử dụng có đầy đủ chữ ký của Giám đốc Chi nhánh và các thành phần liên quan;")
    add_para(doc, "  3. Hóa đơn điện tử hợp pháp theo đúng quy định pháp luật về thuế;")
    add_para(doc, "  4. Giấy chứng nhận chất lượng hàng hóa, phiếu bảo hành, tem kiểm định phương tiện PCCC của cơ quan chức năng;")
    add_para(doc, "  5. Các tài liệu chứng từ hợp pháp khác theo quy định kế toán tài chính.")

    # 8. PHẦN IV: DỰ TOÁN KINH PHÍ VÀ NGUỒN VỐN THỰC HIỆN
    add_heading_1(doc, "IV. DỰ TOÁN KINH PHÍ VÀ NGUỒN VỐN THỰC HIỆN")
    
    add_heading_2(doc, "1. Dự toán kinh phí chi tiết:")
    add_para(doc, "Dự toán kinh phí được xây dựng trên cơ sở đối chiếu định mức quy định tại Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC, suất vốn đầu tư sửa chữa chống thấm chuẩn của Chi nhánh số 34 và khảo sát 03 bảng báo giá cạnh tranh trên thị trường (áp dụng thuế suất thuế GTGT 8% theo Nghị định số 174/2025/NĐ-CP):")
    
    add_para(doc, "Biểu 2: BẢNG TỔNG HỢP DỰ TOÁN KINH PHÍ CHI TIẾT", bold_prefix="", indent=False, bold=True)
    
    # Bảng Biểu 2 với cấu trúc 8 CỘT CHUẨN XÁC TOÁN HỌC 100%
    tbl_b2 = doc.add_table(rows=1, cols=8)
    tbl_b2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b2)
    make_row_header(tbl_b2.rows[0])
    
    headers_b2 = ["STT", "NỘI DUNG HẠNG MỤC", "ĐVT", "KHỐI LƯỢNG", "ĐƠN GIÁ CHƯA VAT (ĐỒNG)", "THÀNH TIỀN CHƯA VAT (ĐỒNG)", "THUẾ VAT 8% (ĐỒNG)", "THÀNH TIỀN SAU VAT (ĐỒNG)"]
    widths_b2 = [Inches(0.4), Inches(2.0), Inches(0.4), Inches(0.45), Inches(0.85), Inches(1.15), Inches(0.8), Inches(1.15)]
    for i, h in enumerate(headers_b2):
        format_cell_text(tbl_b2.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
        set_cell_background(tbl_b2.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_b2.rows[0].cells[i], top=50, bottom=50, left=40, right=40)
        tbl_b2.rows[0].cells[i].width = widths_b2[i]
        
    b2_data = [
        ("A", "TRANG BỊ TÀI SẢN PHÒNG LÀM VIỆC GIÁM ĐỐC MỚI NHẬM CHỨC", "", "", "", "", "", ""),
        ("1", "Bộ bàn ghế ngồi làm việc Giám đốc (Bàn lãnh đạo + Ghế xoay da lãnh đạo)", "Bộ", "01", "9.259.259", "9.259.259", "740.741", "10.000.000"),
        ("2", "Tủ đựng tài liệu Giám đốc (Tủ 3 buồng chia ngăn có khóa an toàn)", "Chiếc", "01", "6.481.481", "6.481.481", "518.519", "7.000.000"),
        ("3", "Máy vi tính để bàn làm việc (Core i7, RAM 16GB, SSD 512GB, LCD 24 inch)", "Bộ", "01", "18.518.519", "18.518.519", "1.481.481", "20.000.000"),
        ("4", "Máy in laser đen trắng tự động 2 mặt khổ A4 kết nối mạng LAN", "Chiếc", "01", "12.037.037", "12.037.037", "962.963", "13.000.000"),
        ("5", "Điện thoại bàn cố định hiển thị số", "Chiếc", "01", "925.926", "925.926", "74.074", "1.000.000"),
        ("6", "Bộ bàn ghế tiếp khách phòng Giám đốc (Bàn trà + Sofa da cao cấp)", "Bộ", "01", "12.037.037", "12.037.037", "962.963", "13.000.000"),
        ("Cộng A", "Tổng kinh phí trang bị tài sản phòng Giám đốc (A)", "", "", "", "59.259.259", "4.740.741", "64.000.000"),
        ("B", "SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH SỐ 23 (THEO MẪU CN34)", "", "", "", "", "", ""),
        ("1", "Chống thấm sàn mái, sê nô, mương đón nước bằng màng khò nhiệt Bitumode Delta-P 3mm", "m²", "357,43", "303.250", "108.390.648", "8.671.252", "117.061.900"),
        ("2", "Chống thấm tường sàn mái, tường sê nô bằng SikaCoat Plus kháng UV", "m²", "285,38", "233.000", "66.493.540", "5.319.483", "71.773.023"),
        ("Cộng B", "Tổng kinh phí sửa chữa chống thấm trụ sở (B)", "", "", "", "174.844.188", "13.990.735", "188.834.923"),
        ("C", "TRANG BỊ THIẾT BỊ PHÒNG CHÁY CHỮA CHÁY (PCCC)", "", "", "", "", "", ""),
        ("1", "Bình chữa cháy bột ABC 4kg (MFZL4) có kiểm định PCCC", "Bình", "16", "290.000", "4.640.000", "371.200", "5.011.200"),
        ("2", "Bình chữa cháy khí CO2 3kg (MT3) có kiểm định PCCC", "Bình", "10", "480.000", "4.800.000", "384.000", "5.184.000"),
        ("3", "Kệ sắt để bình chữa cháy đôi sơn tĩnh điện", "Kệ", "13", "150.000", "1.950.000", "156.000", "2.106.000"),
        ("4", "Bộ bảng nội quy và tiêu lệnh chữa cháy Mica cao cấp", "Bộ", "06", "120.000", "720.000", "57.600", "777.600"),
        ("5", "Đèn chiếu sáng sự cố khẩn cấp (Emergency light)", "Bộ", "06", "350.000", "2.100.000", "168.000", "2.268.000"),
        ("6", "Đèn chỉ dẫn thoát nạn LED Exit 2 mặt", "Bộ", "06", "280.000", "1.680.000", "134.400", "1.814.400"),
        ("7", "Mặt nạ phòng độc lọc khói khí độc cho lực lượng PCCC cơ sở", "Cái", "12", "250.000", "3.000.000", "240.000", "3.240.000"),
        ("8", "Túi y tế sơ cấp cứu cứu hộ chuyên dụng loại B (TT 19/2016/TT-BYT)", "Túi", "02", "750.000", "1.500.000", "120.000", "1.620.000"),
        ("9", "Dụng cụ phá dỡ cứu nạn: Rìu cứu nạn cách điện + búa thoát hiểm", "Bộ", "02", "450.000", "900.000", "72.000", "972.000"),
        ("Cộng C", "Tổng kinh phí trang bị thiết bị PCCC (C)", "", "", "", "21.290.000", "1.703.200", "22.993.200"),
        ("TỔNG", "TỔNG CỘNG TOÀN BỘ PHƯƠNG ÁN (A + B + C)", "", "", "", "255.393.447", "20.434.676", "275.828.123")
    ]
    
    for r_val in b2_data:
        row = tbl_b2.add_row()
        make_row_cant_split(row)
        is_subtotal = r_val[0] in ["Cộng A", "Cộng B", "Cộng C", "TỔNG"]
        is_group_header = r_val[0] in ["A", "B", "C"]
        for c_idx in range(8):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 3] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [4, 5, 6, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            bold = True if (is_subtotal or is_group_header) else (c_idx == 0)
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=9)
            if is_group_header:
                set_cell_background(row.cells[c_idx], "F7F8FA")
            elif is_subtotal:
                set_cell_background(row.cells[c_idx], "EFF3F8")
            set_cell_margins(row.cells[c_idx], top=50, bottom=50, left=40, right=40)
            row.cells[c_idx].width = widths_b2[c_idx]

    add_para(doc, "Tổng dự toán kinh phí xin cấp toàn bộ Phương án: 275.828.123 đồng (Bằng chữ: Hai trăm bảy mươi lăm triệu, tám trăm hai mươi tám nghìn, một trăm hai mươi ba đồng).", bold_prefix="Kết luận dự toán: ", indent=True, bold=True)
    add_para(doc, "Trong đó:")
    add_para(doc, "+ Giá dịch vụ, hàng hóa chưa thuế: 255.393.447 đồng;")
    add_para(doc, "+ Thuế giá trị gia tăng (GTGT 8%): 20.434.676 đồng;")
    add_para(doc, "+ Dự toán phân bổ chi tiết:")
    add_para(doc, "  - Nhóm A (Tài sản làm việc Giám đốc mới): 64.000.000 đồng (Sau VAT);")
    add_para(doc, "  - Nhóm B (Sửa chữa chống thấm trụ sở): 188.834.923 đồng (Sau VAT - theo báo giá thấp nhất của Công ty TNHH Đầu tư Phát triển Toàn Đạt như mẫu CN34);")
    add_para(doc, "  - Nhóm C (Trang bị thiết bị PCCC): 22.993.200 đồng (Sau VAT).")

    add_heading_2(doc, "2. Nguồn kinh phí đề xuất thực hiện:")
    add_para(doc, "Căn cứ cơ chế tự chủ tài chính theo Nghị định số 60/2021/NĐ-CP và Quyết định số 355/QĐ-VPĐK-KHTC, Chi nhánh Văn phòng Đăng ký đất đai số 23 kính đề xuất cấp kinh phí từ các nguồn sau:")
    add_para(doc, "- Quỹ Phát triển hoạt động sự nghiệp của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh; hoặc")
    add_para(doc, "- Nguồn kinh phí không thường xuyên được giao dự toán năm 2026 của cơ quan, đơn vị.")

    # 9. PHẦN V: HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ
    add_heading_1(doc, "V. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ")
    
    add_heading_2(doc, "1. Hồ sơ đính kèm:")
    add_para(doc, "• Quyết định số 8541/QĐ-SNNMT-VP ngày 30/9/2026 của Sở Nông nghiệp và Môi trường TP.HCM về việc bổ nhiệm Giám đốc Chi nhánh số 23 (Bản sao y);")
    add_para(doc, "• Công văn số 1656/CN23-HCTH ngày 21/7/2026 về thuyết minh diện tích trụ sở và Biên bản bàn giao, tiếp nhận tài sản công ngày 09/5/2019 (Bản chụp);")
    add_para(doc, "• Báo cáo PCCC năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 (Bản chính);")
    add_para(doc, "• Bảng đối chiếu định mức trang thiết bị theo Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC (Bản trích sao);")
    add_para(doc, "• 03 bảng báo giá của 03 đơn vị cung ứng thiết bị và thi công chống thấm độc lập (Bản chính).")

    add_heading_2(doc, "2. Số lượng bản phương án và phân công lưu trữ:")
    add_para(doc, "Phương án được lập thành 04 bản chính có giá trị pháp lý như nhau, phân công quản lý lưu trữ như sau:")
    add_para(doc, "- 01 bản chính + Bản chính hồ sơ đính kèm: Lưu tại Phòng Kế hoạch – Tài chính Văn phòng Đăng ký đất đai Thành phố kèm Quyết định phê duyệt phương án;")
    add_para(doc, "- 02 bản chính + Bản chụp hồ sơ đính kèm: Trả về Chi nhánh Văn phòng Đăng ký đất đai số 23 để tổ chức thực hiện và phục vụ công tác thanh quyết toán đợt đầu;")
    add_para(doc, "- 01 bản chính: Lưu tại Văn thư Chi nhánh Văn phòng Đăng ký đất đai số 23 theo quy chế lưu trữ.")

    add_heading_2(doc, "3. Công tác số hóa hồ sơ:")
    add_para(doc, "Chi nhánh Văn phòng Đăng ký đất đai số 23 chịu trách nhiệm số hóa 100% hồ sơ, chứng từ liên quan từ khâu lập phương án dự toán, quy trình chỉ định thầu, ký kết hợp đồng đến kiểm tra nghiệm thu; chuyển dữ liệu số hóa về Phòng Kế hoạch – Tài chính khi thực hiện thanh quyết toán cuối cùng./.")

    # 10. CHỮ KÝ 4 CẤP PHÊ DUYỆT (theo mẫu CN34)
    p_sig_space = doc.add_paragraph()
    p_sig_space.paragraph_format.space_before = Pt(12)
    p_sig_space.paragraph_format.space_after = Pt(4)
    
    tbl_sig1 = doc.add_table(rows=1, cols=2)
    tbl_sig1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borderless(tbl_sig1)
    c1_l = tbl_sig1.rows[0].cells[0]
    c1_r = tbl_sig1.rows[0].cells[1]
    c1_l.width = Inches(3.25)
    c1_r.width = Inches(3.25)
    
    p_s1_l = c1_l.paragraphs[0]
    p_s1_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s1_l.paragraph_format.space_after = Pt(0)
    p_s1_l.paragraph_format.line_spacing = 1.15
    r_nl = p_s1_l.add_run("NGƯỜI LẬP PHƯƠNG ÁN\n\n\n\n\n")
    r_nl.font.name = "Times New Roman"
    r_nl.font.size = Pt(13)
    r_nl.bold = True
    r_nl_name = p_s1_l.add_run("Tổ Hành chính – Tổng hợp\n(bà Nguyễn Thị Bích Tuyền)")
    r_nl_name.font.name = "Times New Roman"
    r_nl_name.font.size = Pt(13)
    r_nl_name.bold = True
    
    p_s1_r = c1_r.paragraphs[0]
    p_s1_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s1_r.paragraph_format.space_after = Pt(0)
    p_s1_r.paragraph_format.line_spacing = 1.15
    r_gd23 = p_s1_r.add_run("CHI NHÁNH SỐ 23 LẬP DỰ TOÁN\nGIÁM ĐỐC\n\n\n\n")
    r_gd23.font.name = "Times New Roman"
    r_gd23.font.size = Pt(13)
    r_gd23.bold = True
    r_gd23_name = p_s1_r.add_run("Nguyễn Chiến Thắng")
    r_gd23_name.font.name = "Times New Roman"
    r_gd23_name.font.size = Pt(13)
    r_gd23_name.bold = True
    
    p_sig_space2 = doc.add_paragraph()
    p_sig_space2.paragraph_format.space_before = Pt(16)
    p_sig_space2.paragraph_format.space_after = Pt(4)
    
    tbl_sig2 = doc.add_table(rows=1, cols=2)
    tbl_sig2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borderless(tbl_sig2)
    c2_l = tbl_sig2.rows[0].cells[0]
    c2_r = tbl_sig2.rows[0].cells[1]
    c2_l.width = Inches(3.25)
    c2_r.width = Inches(3.25)
    
    p_s2_l = c2_l.paragraphs[0]
    p_s2_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s2_l.paragraph_format.space_after = Pt(0)
    p_s2_l.paragraph_format.line_spacing = 1.15
    r_td = p_s2_l.add_run("ĐƠN VỊ THẨM ĐỊNH:\nPHÒNG KẾ HOẠCH – TÀI CHÍNH\nTRƯỞNG PHÒNG\n\n\n\n")
    r_td.font.name = "Times New Roman"
    r_td.font.size = Pt(13)
    r_td.bold = True
    r_td_name = p_s2_l.add_run("Đào Vân Anh")
    r_td_name.font.name = "Times New Roman"
    r_td_name.font.size = Pt(13)
    r_td_name.bold = True
    
    p_s2_r = c2_r.paragraphs[0]
    p_s2_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s2_r.paragraph_format.space_after = Pt(0)
    p_s2_r.paragraph_format.line_spacing = 1.15
    r_pd = p_s2_r.add_run("PHÊ DUYỆT CỦA GIÁM ĐỐC\nVĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM\n\n\n\n")
    r_pd.font.name = "Times New Roman"
    r_pd.font.size = Pt(13)
    r_pd.bold = True
    r_pd_name = p_s2_r.add_run("Bùi Thị Bích Tuyền")
    r_pd_name.font.name = "Times New Roman"
    r_pd_name.font.size = Pt(13)
    r_pd_name.bold = True

    # 11. PHỤ LỤC 01: BẢNG SO SÁNH ĐỐI CHIẾU 03 BÁO GIÁ CẠNH TRANH (theo mẫu CN34)
    doc.add_page_break()
    
    p_pl_title = doc.add_paragraph()
    p_pl_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pl_title.paragraph_format.space_before = Pt(8)
    p_pl_title.paragraph_format.space_after = Pt(4)
    r_plt1 = p_pl_title.add_run("Phụ lục 01\n")
    r_plt1.font.name = "Times New Roman"
    r_plt1.font.size = Pt(14)
    r_plt1.bold = True
    r_plt2 = p_pl_title.add_run("BẢNG TỔNG HỢP SO SÁNH BÁO GIÁ CỦA 03 ĐƠN VỊ CUNG CẤP DỊCH VỤ, HÀNG HÓA\nVÀ ĐÁNH GIÁ LỰA CHỌN ĐƠN VỊ CÓ GIÁ THẤP NHẤT")
    r_plt2.font.name = "Times New Roman"
    r_plt2.font.size = Pt(13)
    r_plt2.bold = True
    
    add_divider_line(doc, length_type="subject")
    
    add_para(doc, "Căn cứ 03 bảng báo giá cạnh tranh trên thị trường của 03 đơn vị cung cấp dịch vụ, thi công và thiết bị PCCC (đính kèm hồ sơ phương án):", indent=False)
    add_para(doc, "1. Công ty TNHH Đầu tư Phát triển Toàn Đạt;")
    add_para(doc, "2. Công ty TNHH Xây dựng Vạn Đạt;")
    add_para(doc, "3. Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát.")
    
    # Bảng Phụ lục so sánh 3 đơn vị
    tbl_pl = doc.add_table(rows=1, cols=8)
    tbl_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pl)
    make_row_header(tbl_pl.rows[0])
    
    pl_headers_r0 = ["STT", "Tên đơn vị báo giá", "Đơn giá sàn mái (đồng)", "Thành tiền sàn mái (357,43m²)", "Đơn giá tường (đồng)", "Thành tiền tường (285,38m²)", "Tổng cộng chưa VAT (đồng)", "Tổng cộng sau VAT 8% (đồng)"]
    widths_pl = [Inches(0.4), Inches(1.8), Inches(0.7), Inches(0.9), Inches(0.7), Inches(0.9), Inches(1.0), Inches(1.1)]
    
    for i in range(8):
        format_cell_text(tbl_pl.rows[0].cells[i], pl_headers_r0[i], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
        set_cell_background(tbl_pl.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_pl.rows[0].cells[i], top=50, bottom=50, left=40, right=40)
        tbl_pl.rows[0].cells[i].width = widths_pl[i]
        
    pl_rows_data = [
        ("1", "Công ty TNHH Đầu tư Phát triển Toàn Đạt", "303.250", "108.390.648", "233.000", "66.493.540", "174.844.188", "188.834.923"),
        ("2", "Công ty TNHH Xây dựng Vạn Đạt", "336.640", "120.325.235", "250.960", "71.618.965", "191.944.200", "207.299.736"),
        ("3", "Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát", "357.835", "127.900.964", "274.940", "78.462.377", "206.363.341", "222.872.408")
    ]
    
    for r_val in pl_rows_data:
        row = tbl_pl.add_row()
        make_row_cant_split(row)
        for c_idx in range(8):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 4] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [3, 5, 6, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            bold = True if c_idx in [0, 7] else False
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=9)
            set_cell_margins(row.cells[c_idx], top=50, bottom=50, left=40, right=40)
            row.cells[c_idx].width = widths_pl[c_idx]

    add_heading_2(doc, "Nhận xét và kết quả đánh giá lựa chọn đơn vị:")
    add_para(doc, "Qua khảo sát giá thị trường thông qua 03 báo giá độc lập của các đơn vị cung cấp dịch vụ và thi công:")
    add_para(doc, "• Báo giá của Công ty TNHH Đầu tư Phát triển Toàn Đạt có giá sau thuế là 188.834.923 đồng;")
    add_para(doc, "• Báo giá của Công ty TNHH Xây dựng Vạn Đạt có giá sau thuế là 207.299.736 đồng (cao hơn 18.464.813 đồng);")
    add_para(doc, "• Báo giá của Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát có giá sau thuế là 222.872.408 đồng (cao hơn 34.037.485 đồng).")
    add_para(doc, "Như vậy, mức giá đề xuất lựa chọn là của Công ty TNHH Đầu tư Phát triển Toàn Đạt với tổng giá trị sau thuế 188.834.923 đồng. Đây là mức giá thấp nhất, đáp ứng đầy đủ yêu cầu kỹ thuật và biện pháp thi công, tiết kiệm ngân sách nhà nước và bảo đảm tính khả thi cao nhất theo đúng tinh thần mẫu phương án của Chi nhánh số 34./.")

    # Lưu file kết quả
    output_docx_path = "/Users/admin/Desktop/BINHDUONG/OUTPUT/Phuong_an_xin_kinh_phi_CN23_v1.docx"
    doc.save(output_docx_path)
    print(f"File created successfully at: {output_docx_path}")

if __name__ == "__main__":
    main()
