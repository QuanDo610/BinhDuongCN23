import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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

def add_page_number_to_section(section):
    section.different_first_page_header_footer = True
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w'))
    p._p.append(fld)

def format_cell_text(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.first_line_indent = Inches(0)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)
    r.bold = bold
    r.italic = italic
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    return p

def add_p(doc, text="", bold_prefix="", indent=False, italic=False, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, font_size=13, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.49)
    else:
        p.paragraph_format.first_line_indent = Inches(0)
        
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(font_size)
        r_pre.bold = True
        
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.italic = italic
        r.bold = bold
    return p

def build_cn23_proposal():
    doc = docx.Document()
    
    # 1. Cấu hình Normal Style theo chuẩn Nghị định 30 (Times New Roman, 13pt)
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)
    
    # Căn lề khổ A4 chuẩn NĐ 30: Top 20mm, Bottom 20mm, Left 30mm, Right 15mm
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.79)
    sec.left_margin = Inches(1.18)
    sec.right_margin = Inches(0.59)
    add_page_number_to_section(sec)
    
    # ==========================================
    # PHẦN ĐẦU: MỤC LỤC & DANH MỤC BIỂU VÀ PHỤ LỤC (Y CHANG MẪU CN34)
    # KHÔNG CÓ TIÊU ĐỀ TIÊU NGỮ ĐẦU TRANG THEO ĐÚNG MẪU CN34
    # ==========================================
    add_p(doc, "MỤC LỤC", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=15, space_before=12, space_after=10)
    
    toc_items = [
        ("MỤC ĐÍCH", "1", 0),
        ("A. Giới thiệu chung về hoạt động của hệ thống Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh", "1", 1),
        ("1. Căn cứ pháp lý", "1", 2),
        ("2. Vị trí, chức năng, nhiệm vụ, quyền hạn", "3", 2),
        ("3. Cơ cấu tổ chức", "4", 2),
        ("4. Chế độ làm việc", "5", 2),
        ("5. Các tổ chức chính trị, chính trị - xã hội", "5", 2),
        ("6. Số lượng viên chức, lao động hợp đồng", "5", 2),
        ("7. Trụ sở hoạt động", "6", 2),
        ("8. Về cơ chế tài chính", "6", 2),
        ("B. Mục đích của phương án", "7", 1),
        ("1. Căn cứ xây dựng phương án", "7", 2),
        ("2. Việc xây dựng phương án nhằm các mục đích sau", "8", 2),
        ("II. YÊU CẦU", "9", 0),
        ("1. Phạm vi thực hiện", "9", 2),
        ("2. Về công tác thi công và mua sắm trang thiết bị", "9", 2),
        ("3. Yêu cầu kỹ thuật đối với đơn vị cung cấp/thi công", "11", 2),
        ("4. Về nội dung chi phí thực hiện", "12", 2),
        ("III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN", "12", 0),
        ("1. Cơ sở pháp lý", "12", 2),
        ("1.1 Văn bản quy định về công tác đấu thầu, chỉ định thầu", "12", 3),
        ("1.2 Văn bản quy định về Luật quản lý, sử dụng tài sản công", "13", 3),
        ("1.3 Văn bản quy định về thuế suất", "13", 3),
        ("1.4 Các mẫu biểu sử dụng", "13", 3),
        ("2. Nội dung và khối lượng", "13", 2),
        ("3. Quy trình thực hiện (sắp xếp theo thứ tự thực hiện)", "14", 2),
        ("3.1 Quy trình thực hiện (6 bước)", "14", 3),
        ("3.2 Trách nhiệm trong công tác kiểm tra nghiệm thu", "15", 3),
        ("IV. DỰ TOÁN KINH PHÍ", "15", 0),
        ("1. Dự toán kinh phí", "15", 2),
        ("2. Nguồn kinh phí", "17", 2),
        ("IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ", "17", 0),
        ("1. Hồ sơ đính kèm", "17", 2),
        ("2. Số lượng bản phương án dự toán ký chính", "18", 2),
        ("3. Lưu trữ hồ sơ", "18", 2),
        ("4. Số hóa hồ sơ", "18", 2),
        ("Phụ lục 01: Bảng báo giá của 03 đơn vị cung cấp / thi công", "19", 0),
    ]
    
    for t_title, t_page, t_lvl in toc_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.50), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        
        indent_in = 0.0 if t_lvl == 0 else (0.25 if t_lvl == 1 else (0.45 if t_lvl == 2 else 0.65))
        p.paragraph_format.left_indent = Inches(indent_in)
        p.paragraph_format.first_line_indent = Inches(0)
        
        is_bold = (t_lvl == 0 or t_lvl == 1)
        r1 = p.add_run(t_title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.bold = is_bold
        
        r2 = p.add_run("\t" + t_page)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.bold = is_bold
        
    add_p(doc, "DANH MỤC BIỂU VÀ PHỤ LỤC", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_before=14, space_after=6)
    
    list_bieu = [
        ("Biểu 1: Nội dung và khối lượng", "13"),
        ("Biểu 2: Dự toán kinh phí sửa chữa chống thấm và trang bị tài sản", "15"),
        ("Phụ lục 01: Bảng báo giá của 03 đơn vị cung cấp / thi công", "19")
    ]
    for b_title, b_page in list_bieu:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.50), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Inches(0)
        
        r1 = p.add_run(b_title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11.5)
        r1.bold = False
        
        r2 = p.add_run("\t" + b_page)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11.5)
        r2.bold = False
    
    # Ngắt trang sang phần nội dung chính y chang CN34
    doc.add_page_break()
    
    # ==========================================
    # PHẦN NỘI DUNG CHÍNH (THEO KHUNG CN34)
    # ==========================================
    add_p(doc, "Chủ quản: Sở Nông nghiệp và Môi trường", bold=True, font_size=13, space_before=6, space_after=2)
    add_p(doc, "Đơn vị: Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh", bold=True, font_size=13, space_after=2)
    add_p(doc, "Mã số QHNS: 1122149", bold=True, font_size=13, space_after=12)
    
    add_p(doc, "PHƯƠNG ÁN DỰ TOÁN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=15, space_before=6, space_after=4)
    add_p(doc, "Công tác: “Trang bị tài sản làm việc cho Giám đốc Chi nhánh mới nhậm chức theo Quyết định số 8541/QĐ-SNNMT-VP và Quy chế chi tiêu nội bộ số 355; sửa chữa chống thấm trụ sở và trang bị thiết bị phòng cháy, chữa cháy tại Chi nhánh Văn phòng Đăng ký đất đai số 23”", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=12)
    
    add_p(doc, "MỤC ĐÍCH", bold=True, font_size=13, space_before=8, space_after=4)
    add_p(doc, "A. Giới thiệu chung về hoạt động của hệ thống Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh:", bold=True, font_size=13, space_after=4)
    add_p(doc, "1. Căn cứ pháp lý", bold=True, font_size=13, space_after=4)
    add_p(doc, "Luật Đất đai và các Nghị định, Thông tư hướng dẫn", italic=True, font_size=13, space_after=3)
    
    land_laws = [
        "- Luật Đất đai số 31/2024/QH15 được sửa đổi bổ sung một số điều theo Luật số 43/2024/QH15;",
        "- Nghị định số 101/2024/NĐ-CP ngày 29 tháng 7 năm 2024 của Chính phủ quy định về điều tra cơ bản đất đai; đăng ký, cấp giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất và hệ thống thông tin đất đai;",
        "- Nghị định số 102/2024/NĐ-CP ngày 30 tháng 7 năm 2024 của Chính phủ quy định chi tiết thi hành một số điều của Luật Đất đai;",
        "- Nghị định số 151/2025/NĐ-CP ngày 12 tháng 6 năm 2025 của Chính phủ quy định về phân định thẩm quyền của chính quyền địa phương 02 cấp, phân quyền, phân cấp trong lĩnh vực đất đai;",
        "- Nghị định số 226/2025/NĐ-CP ngày 15 tháng 8 năm 2025 sửa đổi, bổ sung một số điều của các Nghị định quy định chi tiết thi hành Luật Đất đai;",
        "- Thông tư số 08/2024/TT-BTNMT ngày 31 tháng 7 năm 2024 của Bộ Tài nguyên và Môi trường quy định về thống kê, kiểm kê đất đai và lập bản đồ hiện trạng sử dụng đất;",
        "- Thông tư số 10/2024/TT-BTNMT ngày 31 tháng 7 năm 2024 của Bộ Tài nguyên và Môi trường quy định về hồ sơ địa chính, giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất;",
        "- Thông tư số 23/2025/TT-BTNMT ngày 20 tháng 6 năm 2025 của Bộ trưởng Bộ Nông nghiệp và Môi trường quy định phân cấp, phân định thẩm quyền quản lý nhà nước trong lĩnh vực đất đai."
    ]
    for ll in land_laws:
        add_p(doc, ll, indent=True, space_after=3)
        
    add_p(doc, "a/ Văn bản về cơ chế của đơn vị sự nghiệp công lập", bold=True, font_size=13, space_before=4, space_after=3)
    career_laws = [
        "- Nghị định số 60/2021/NĐ-CP ngày 21 tháng 6 năm 2021 của Chính phủ về quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;",
        "- Nghị định số 106/2020/NĐ-CP ngày 10 tháng 9 năm 2020 của Chính phủ về vị trí việc làm và số lượng người làm việc trong đơn vị sự nghiệp công lập;",
        "- Nghị định số 120/2020/NĐ-CP ngày 07 tháng 10 năm 2020 của Chính phủ quy định về thành lập, tổ chức lại, giải thể đơn vị sự nghiệp công lập;",
        "- Nghị định số 111/2022/NĐ-CP ngày 30 tháng 12 năm 2022 của Chính phủ về hợp đồng đối với một số loại công việc trong cơ quan hành chính và đơn vị sự nghiệp công lập;",
        "- Nghị định số 111/2025/NĐ-CP ngày 22 tháng 5 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 60/2021/NĐ-CP ngày 21 tháng 6 năm 2021 của chính phủ quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;",
        "- Thông tư số 56/2022/TT-BTC ngày 16 tháng 9 năm 2022 của Bộ Tài chính hướng dẫn một số nội dung về cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập; xử lý tài sản, tài chính khi tổ chức lại, giải thể đơn vị sự nghiệp công lập."
    ]
    for cl in career_laws:
        add_p(doc, cl, indent=True, space_after=3)

    add_p(doc, "b/ Văn bản về thành lập, ban hành Quy chế tổ chức và hoạt động", bold=True, font_size=13, space_before=4, space_after=3)
    org_laws = [
        "- Quyết định số 1886/QĐ-UBND ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố về tổ chức lại Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh trên cơ sở hợp nhất Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Văn phòng Đăng ký đất đai tỉnh Bình Dương và Văn phòng Đăng ký đất đai tỉnh Bà Rịa – Vũng Tàu;",
        "- Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh;",
        "- Quyết định số 8541/QĐ-SNNMT-VP ngày 30 tháng 9 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc điều động và bổ nhiệm ông Nguyễn Chiến Thắng, Phó Giám đốc Văn phòng Đăng ký đất đai Thành phố giữ chức vụ Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 thuộc Văn phòng Đăng ký đất đai Thành phố."
    ]
    for ol in org_laws:
        add_p(doc, ol, indent=True, space_after=3)

    add_p(doc, "c/ Văn bản về quy chế tài chính và chi tiêu nội bộ", bold=True, font_size=13, space_before=4, space_after=3)
    fin_laws = [
        "- Quyết định số 2882/QĐ-SNNMT-KHTC ngày 29 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường về việc giao chỉ tiêu dự toán thu, chi ngân sách năm 2026 cho các cơ quan, đơn vị thuộc Sở Nông nghiệp và Môi trường;",
        "- Quyết định số 355/QĐ-VPĐK-KHTC ngày 31 tháng 12 năm 2025 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc ban hành Quy chế chi tiêu nội bộ năm 2025 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh;",
        "- Quyết định số 792/QĐ-SNNMT-KHTC ngày 10 tháng 02 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường về việc điều chỉnh dự toán ngân sách nhà nước năm 2026 cho các cơ quan, đơn vị thuộc Sở Nông nghiệp và Môi trường (lần 3);",
        "- Quyết định số 805/QĐ-SNNMT-KHTC ngày 10 tháng 02 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường về việc điều chỉnh dự toán ngân sách nhà nước năm 2026 cho các cơ quan, đơn vị thuộc Sở Nông nghiệp và Môi trường (lần 4);",
        "- Quyết định số 907/QĐ-SNNMT-KHTC ngày 13 tháng 02 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường về việc điều chỉnh dự toán ngân sách nhà nước năm 2026 cho các cơ quan, đơn vị thuộc Sở Nông nghiệp và Môi trường (lần 5);",
        "- Quyết định số 1020/QĐ-SNNMT-KHTC ngày 04 tháng 3 năm 2026 của Giám đốc Sở Nông nghiệp và Môi trường về việc điều chỉnh dự toán ngân sách nhà nước năm 2026 cho các cơ quan, đơn vị thuộc Sở Nông nghiệp và Môi trường (lần 6); trong đó đơn vị sử dụng ngân sách: Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh - Mã quan hệ ngân sách 1122149 - Mã KBNN nơi giao dịch: 0111 - Mã chương 412 - Mã ngành kinh tế 338."
    ]
    for fl in fin_laws:
        add_p(doc, fl, indent=True, space_after=3)

    add_p(doc, "d/ Văn bản về định mức kinh tế kỹ thuật của các hoạt động nghiệp vụ và PCCC", bold=True, font_size=13, space_before=4, space_after=3)
    tech_laws = [
        "- Thông tư số 03/2022/TT-BTNMT ngày 28 tháng 02 năm 2022 của Bộ trưởng Bộ Tài nguyên và Môi trường ban hành Quy định kỹ thuật và định mức kinh tế - kỹ thuật về công tác thu nhận, lưu trữ, bảo quản và cung cấp thông tin, dữ liệu tài nguyên và môi trường;",
        "- Thông tư số 136/2017/TT-BTC ngày 22 tháng 12 năm 2017 của Bộ trưởng Bộ Tài chính quy định lập, quản lý, sử dụng kinh phí chi hoạt động kinh tế đối với các nhiệm vụ chi về tài nguyên và môi trường;",
        "- Luật Phòng cháy và chữa cháy số 27/2001/QH10 và Luật số 40/2013/QH13 sửa đổi, bổ sung một số điều của Luật Phòng cháy và chữa cháy;",
        "- Tiêu chuẩn Quốc gia TCVN 3890:2023 về Phòng cháy chữa cháy - Phương tiện phòng cháy và chữa cháy cho nhà và công trình - Trang bị, bố trí;",
        "- Công văn số 24482/VPĐK-KT ngày 19 tháng 8 năm 2026 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc tăng cường công tác phòng cháy chữa cháy và an toàn bảo quản hồ sơ tài liệu địa chính."
    ]
    for tl in tech_laws:
        add_p(doc, tl, indent=True, space_after=3)

    add_p(doc, "2. Vị trí, chức năng, nhiệm vụ, quyền hạn", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Chi nhánh Văn phòng đăng ký đất đai số 23 là đơn vị sự nghiệp công lập trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh, có tư cách pháp nhân, có con dấu riêng và được mở tài khoản tại Kho bạc Nhà nước, Ngân hàng để hoạt động theo quy định của pháp luật; có chức năng thực hiện đăng ký đất đai, nhà ở và tài sản khác gắn liền với đất; xây dựng, quản lý, cập nhật, chỉnh lý thống nhất hồ sơ địa chính và cơ sở dữ liệu đất đai; thống kê, kiểm kê đất đai; cung cấp thông tin về đất đai cho các tổ chức, cá nhân theo quy định của pháp luật;", indent=True)
    add_p(doc, "Chi nhánh Văn phòng đăng ký đất đai số 23 quyết định về quy chế làm việc và trình tự giải quyết công việc trong nội bộ Chi nhánh Văn phòng đăng ký đất đai số 23 và mối quan hệ công tác với các tổ chức, cá nhân bên ngoài có liên quan đến việc thực hiện chức năng, nhiệm vụ, quyền hạn của Chi nhánh Văn phòng đăng ký đất đai số 23.", indent=True)
    add_p(doc, "Trụ sở chính của Chi nhánh Văn phòng đăng ký đất đai số 23 đặt tại số 358 Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh.", indent=True)

    add_p(doc, "3. Cơ cấu tổ chức", bold=True, font_size=13, space_before=6, space_after=3)
    
    # Table 0: Cơ cấu tổ chức CN23 theo đúng mẫu Table 0 của CN34
    tbl_org = doc.add_table(rows=6, cols=3)
    tbl_org.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_org)
    make_row_header(tbl_org.rows[0])
    
    headers_org = ["Stt", "Cơ cấu tổ chức", "Nhiệm vụ chủ yếu"]
    widths_org = [Inches(0.6), Inches(2.2), Inches(3.7)]
    for i, h in enumerate(headers_org):
        format_cell_text(tbl_org.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
        set_cell_background(tbl_org.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_org.rows[0].cells[i], top=70, bottom=70, left=90, right=90)
        tbl_org.rows[0].cells[i].width = widths_org[i]
        
    format_cell_text(tbl_org.rows[1].cells[0], "", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
    format_cell_text(tbl_org.rows[1].cells[1], "CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23:", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11)
    format_cell_text(tbl_org.rows[1].cells[2], "CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23:", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11)
    set_cell_background(tbl_org.rows[1].cells[0], "F8F9FA")
    set_cell_background(tbl_org.rows[1].cells[1], "F8F9FA")
    set_cell_background(tbl_org.rows[1].cells[2], "F8F9FA")
    
    org_rows = [
        ("1", "Ban Giám đốc", "01 Giám đốc (ông Nguyễn Chiến Thắng - bổ nhiệm theo QĐ số 8541/QĐ-SNNMT-VP ngày 30/9/2026). 01 Phó Giám đốc (ông Đặng Huy Cường). Chỉ đạo, điều hành toàn bộ hoạt động của Chi nhánh."),
        ("2", "Tổ Hành chính - Tổng hợp", "Tổ trưởng: bà Nguyễn Thị Bích Tuyền. Hành chính, tổ chức nhân sự, văn thư lưu trữ; tài chính - kế toán; báo cáo, tổng hợp, mua sắm tài sản và quản lý PCCC."),
        ("3", "Tổ Kỹ thuật Địa chính và Lưu trữ", "Tổ trưởng: ông Trần Thanh Triết. Công tác kỹ thuật địa chính, kiểm tra nội nghiệp bản vẽ, thống kê kiểm kê đất đai. Trực tiếp quản lý, bảo quản, khai thác kho lưu trữ hồ sơ tài liệu địa chính."),
        ("4", "Tổ Đăng ký và Cấp giấy chứng nhận", "Tổ trưởng: bà Nguyễn Thị Thùy Trang. Thực hiện công tác đăng ký đất đai, cấp Giấy chứng nhận và đăng ký biện pháp bảo đảm cho cá nhân, hộ gia đình.")
    ]
    for r_idx, (s, o, d) in enumerate(org_rows, start=2):
        make_row_cant_split(tbl_org.rows[r_idx])
        format_cell_text(tbl_org.rows[r_idx].cells[0], s, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
        format_cell_text(tbl_org.rows[r_idx].cells[1], o, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11)
        format_cell_text(tbl_org.rows[r_idx].cells[2], d, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=11)
        set_cell_margins(tbl_org.rows[r_idx].cells[0], top=70, bottom=70, left=90, right=90)
        set_cell_margins(tbl_org.rows[r_idx].cells[1], top=70, bottom=70, left=90, right=90)
        set_cell_margins(tbl_org.rows[r_idx].cells[2], top=70, bottom=70, left=90, right=90)
        tbl_org.rows[r_idx].cells[0].width = widths_org[0]
        tbl_org.rows[r_idx].cells[1].width = widths_org[1]
        tbl_org.rows[r_idx].cells[2].width = widths_org[2]

    add_p(doc, "4. Chế độ làm việc:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Chi nhánh Văn phòng đăng ký đất đai số 23 làm việc theo nguyên tắc tập trung dân chủ, thực hiện chế độ thủ trưởng; bảo đảm sự lãnh đạo của Đảng, sự chỉ đạo, điều hành của Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh, tuân thủ quy định của pháp luật và Quy chế làm việc này. Viên chức và người lao động phải thực hiện, giải quyết công việc đúng chức năng, nhiệm vụ, quyền hạn được giao và theo quy định của pháp luật.", indent=True)
    add_p(doc, "Giám đốc là thủ trưởng, người đứng đầu, chịu trách nhiệm chỉ đạo, điều hành toàn bộ hoạt động của Chi nhánh theo chức năng, nhiệm vụ, quyền hạn được quy định; chịu trách nhiệm trước Giám đốc Sở Nông nghiệp và Môi trường, Giám đốc Văn phòng đăng ký đất đai Thành phố và trước pháp luật về kết quả hoạt động của Chi nhánh.", indent=True)

    add_p(doc, "5. Các tổ chức chính trị, chính trị - xã hội:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "- Chi bộ Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Đảng bộ Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh / Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh.", indent=True)
    add_p(doc, "- Chi nhánh Văn phòng đăng ký đất đai số 23 tổ chức và sinh hoạt theo chỉ đạo của Đảng bộ cấp trên và Công đoàn cơ sở.", indent=True)

    add_p(doc, "6. Số lượng viên chức, lao động hợp đồng:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc giao số lượng người làm việc năm 2026 cho Chi nhánh số 23 là 85 người và được phân bổ như sau:", indent=True)
    add_p(doc, "- Ban Giám đốc: 02 người (01 Giám đốc, 01 Phó Giám đốc);", indent=True)
    add_p(doc, "- Hành chính – Tổng hợp: 14 người (viên chức và người lao động);", indent=True)
    add_p(doc, "- Đăng ký và cấp GCN: 32 người (viên chức và người lao động);", indent=True)
    add_p(doc, "- Kỹ thuật Địa chính và Lưu trữ: 34 người (viên chức và người lao động);", indent=True)
    add_p(doc, "- Bảo vệ và phục vụ: 03 người (02 bảo vệ, 01 phục vụ).", indent=True)

    add_p(doc, "7. Trụ sở hoạt động:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Trụ sở chính của Chi nhánh Văn phòng đăng ký đất đai số 23 đặt tại số 358 Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh. Khuôn viên đất quản lý, sử dụng ổn định là 1.417,70 m²; tổng diện tích sàn xây dựng thực tế của công trình khối nhà làm việc hiện hữu là 835,30 m².", indent=True)

    add_p(doc, "8. Về cơ chế tài chính:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "8.1. Chi nhánh Văn phòng đăng ký đất đai số 23 thực hiện cơ chế tự chủ tài chính theo Nghị định 60/2021/NĐ-CP và Nghị định 111/2025/NĐ-CP đối với đơn vị sự nghiệp công lập theo loại hình tự bảo đảm chi phí hoạt động.", indent=True)
    add_p(doc, "8.2. Nguồn tài chính sử dụng:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "a) Kinh phí cấp cho hoạt động không thường xuyên thực hiện chức năng, nhiệm vụ của Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh theo quy định hiện hành để phù hợp với cơ chế tự chủ của đơn vị sự nghiệp công lập.", indent=True)
    add_p(doc, "b) Nguồn thu từ hoạt động sự nghiệp, gồm:", indent=True)
    add_p(doc, "- Phí trong lĩnh vực đăng ký đất đai, đăng ký giao dịch bảo đảm, khai thác đất đai, cung cấp thông tin đất đai theo quy định của pháp luật hiện hành.", indent=True)
    add_p(doc, "- Các khoản thu từ thực hiện hoạt động dịch vụ theo hợp đồng ký kết và theo quy định của pháp luật gồm: kiểm tra nội nghiệp bản vẽ.", indent=True)
    add_p(doc, "- Các khoản thu từ hoạt động sự nghiệp khác theo quy định của pháp luật.", indent=True)

    add_p(doc, "B.  Mục đích của phương án:", bold=True, font_size=13, space_before=8, space_after=3)
    add_p(doc, "1. Căn cứ xây dựng phương án", bold=True, font_size=13, space_after=3)
    add_p(doc, "Ngày 09 tháng 05 năm 2019, tại UBND phường Chánh Mỹ, Chi nhánh Văn phòng Đăng ký quyền sử dụng đất thành phố Thủ Dầu Một (nay là Chi nhánh Văn phòng Đăng ký đất đai số 23) đã tiếp nhận bàn giao cơ sở nhà, đất tại số 358 Huỳnh Văn Cù theo Biên bản bàn giao, tiếp nhận tài sản công (đính kèm Công văn số 1656/CN23-HCTH ngày 21/07/2026 của Chi nhánh số 23). Tổng diện tích sàn xây dựng công trình hiện hữu là 835,30 m², bao gồm: Khối nhà trụ sở chính 2 tầng có diện tích tầng 1 là 274,10 m², tầng 2 là 274,10 m² (tổng khối chính 548,20 m²); Khối nhà bộ phận một cửa diện tích 69,90 m²; Khối nhà Ban chỉ huy Quân sự cũ diện tích 81,50 m²; Hội trường diện tích 117,60 m²; Khu vệ sinh 18,10 m².", indent=True)
    add_p(doc, "Đến nay, hiện trạng sàn mái, tường sàn mái, trần nhà của Chi nhánh số 23 bị thấm dột nghiêm trọng qua nhiều năm sử dụng chưa được sửa chữa, chống thấm dột triệt để. Như vậy, mục đích của phương án sửa chữa chống thấm trụ sở Chi nhánh số 23 là nhu cầu cấp thiết nhằm tạo điều kiện bảo đảm môi trường làm việc khô thoáng sạch đẹp, bảo đảm điều kiện bảo quản lưu trữ hồ sơ, tài liệu địa chính chuyên môn của đơn vị không bị ẩm mốc, rách nát, hư hỏng theo đúng quy định hiện hành.", indent=True)
    add_p(doc, "Đồng thời, ngày 30 tháng 9 năm 2026, Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh đã ban hành Quyết định số 8541/QĐ-SNNMT-VP về việc điều động và bổ nhiệm ông Nguyễn Chiến Thắng, Phó Giám đốc Văn phòng Đăng ký đất đai Thành phố giữ chức vụ Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 kể từ ngày 01 tháng 10 năm 2026, bảo lưu hệ số phụ cấp chức vụ là 0,6 đến ngày 03/3/2030. Hiện nay phòng làm việc của Giám đốc Chi nhánh chưa được trang bị đầy đủ tài sản làm việc; do đó, phương án đề xuất trang bị bổ sung bàn ghế làm việc, tủ tài liệu, máy vi tính, máy in, điện thoại và bàn ghế tiếp khách theo đúng tiêu chuẩn, định mức tại Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC để phục vụ công tác lãnh đạo, điều hành cơ quan.", indent=True)
    add_p(doc, "Mặt khác, theo Báo cáo công tác PCCC năm 2026 của đơn vị và chỉ đạo của Văn phòng Đăng ký đất đai Thành phố tại Công văn số 24482/VPĐK-KT ngày 19/8/2026, Chi nhánh hiện có 26 bình chữa cháy tại chỗ nhưng chưa đồng bộ, cần trang bị bổ sung bình khí CO2 chuyên dùng cho kho lưu trữ hồ sơ địa chính và phòng máy chủ, bình bột ABC, kệ để bình, đèn sự cố, đèn Exit, mặt nạ phòng độc cho 4 tổ PCCC cơ sở để bảo đảm an toàn tính mạng con người và hồ sơ tài liệu theo chuẩn TCVN 3890:2023.", indent=True)

    add_p(doc, "2. Việc xây dựng phương án sửa chữa chống thấm, trang bị tài sản Giám đốc và thiết bị PCCC nhằm các mục đích sau:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "- Đảm bảo cơ sở vật chất, môi trường làm việc thoáng mát sạch sẽ không bị dột và ẩm ướt, trơn trượt.", indent=True)
    add_p(doc, "- Đảm bảo điều kiện bảo quản tài liệu, dữ liệu chuyên môn của đơn vị không bị ẩm mốc, hư hỏng, khô thoáng.", indent=True)
    add_p(doc, "- Đảm bảo trang bị tài sản, phương tiện làm việc cho Giám đốc mới nhậm chức đúng tiêu chuẩn, định mức quy định tại Quy chế chi tiêu nội bộ số 355 và Quyết định số 8541/QĐ-SNNMT-VP.", indent=True)
    add_p(doc, "- Trang bị đầy đủ phương tiện PCCC tại chỗ, bảo đảm an toàn tính mạng cho 85 nhân sự và bảo vệ tuyệt đối kho tài liệu địa chính.", indent=True)
    add_p(doc, "- Sử dụng nguồn kinh phí của đơn vị đúng quy định, tiết kiệm và hiệu quả cao.", indent=True)
    add_p(doc, "- Là cơ sở để lập kế hoạch lựa chọn nhà thầu và tổ chức đấu thầu theo quy định của pháp luật.", indent=True)

    # II. YÊU CẦU
    add_p(doc, "II. YÊU CẦU", bold=True, font_size=13, space_before=8, space_after=3)
    add_p(doc, "1. Phạm vi sửa chữa chống thấm và trang bị tài sản", bold=True, font_size=13, space_after=3)
    add_p(doc, "Việc sửa chữa chống thấm trụ sở, trang bị tài sản Giám đốc mới và thiết bị PCCC của Chi nhánh số 23 phải đảm bảo đáp ứng nhu cầu cơ sở vật chất, bảo quản lưu trữ tài liệu công tác chuyên môn của Chi nhánh Văn phòng Đăng ký đất đai số 23.", indent=True)

    add_p(doc, "2. Về công tác thi công sửa chữa chống thấm và mua sắm trang thiết bị", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Phương án dự toán của đơn vị trong năm 2026 được thực hiện cụ thể như sau:", indent=True)
    add_p(doc, "2.1. Chống thấm sàn mái, sê nô mái, mương đón nước mái tôn bằng màng chống thấm Bitumode Delta – P 3mm :", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "a/ Chuẩn bị mặt bằng:", bold=True, font_size=13, space_after=2)
    add_p(doc, "- Bề mặt cần chống thấm phải đặc chắc, không nứt nẻ, các tạp chất, mảnh vỡ, bụi bẩn phải được vệ sinh đúng yêu cầu. Các lớp vật liệu bề mặt có lực bám dính không tốt hoặc có khả năng bong tróc phải được đục bỏ hoàn toàn, các lổ ty phải được cắt lún sâu 0,01mm.", indent=True)
    add_p(doc, "- Dùng máy mài chuyên dụng mài bỏ tạp chất… tạo nhám để tạo bám dính tốt.", indent=True)
    add_p(doc, "- Các vết nứt (nếu có) phải được xử lý, vá lại vết nứt, lỗ mọt lớn trước khi thi công chống thấm.", indent=True)
    add_p(doc, "- Chân tường phải được bo góc 45 độ (tùy theo mạch ngừng).", indent=True)
    add_p(doc, "b/ Phủ lớp lót:", bold=True, font_size=13, space_after=2)
    add_p(doc, "- Thêm 20-50% nước vào Sikaproof Membrane (hoặc Nirol-W) và trộn đều.", indent=True)
    add_p(doc, "- Dùng chổi hoặc rulo quét lên 1 lớp lót.", indent=True)
    add_p(doc, "- Định mức 0.2kg/m2.", indent=True)

    add_p(doc, "2.2. Chống thấm tường sàn mái, tường sê nô mái, tường mương đón nước mái tôn bằng SikaCoat Plus:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "a/ Chuẩn bị mặt bằng:", bold=True, font_size=13, space_after=2)
    add_p(doc, "Tường cũ: Phải cạo bỏ dầu mỡ, rêu mốc, các lớp sơn, vôi cũ sau đó rửa kỹ bằng nước sạch và để khô.", indent=True)
    add_p(doc, "Bước 1: Chuẩn bị hỗn hợp theo tỷ lệ như sau:", indent=True)
    add_p(doc, "+ Thùng 25 kg Mastic dẻo: 4-7 kg Xi măng", indent=True)
    add_p(doc, "+ Lượng nước sạch (vừa đủ).", indent=True)
    add_p(doc, "Bước 2: + Dùng bay trét 1 lớp, mỗi lớp cách nhau từ 3 – 4 giờ.", indent=True)
    add_p(doc, "+ Để khô sau 6 – 8 giờ dùng giấy nhám xả phẳng, thổi sạch bụi, có thể lăn sơn lót.", indent=True)
    add_p(doc, "b/ Lăn phủ lớp chống thấm:", bold=True, font_size=13, space_after=2)
    add_p(doc, "+ Thi công 2 lớp SikaCoat Plus với định mức ~0.3kg/ m2/ lớp bằng cọ, ru-lô.", indent=True)
    add_p(doc, "+ Thi công lớp thứ 1 chờ khô trong khoảng 3-4 tiếng", indent=True)
    add_p(doc, "+ Thi công lớp thứ 2", indent=True)

    add_p(doc, "2.3. Về trang bị tài sản làm việc cho Giám đốc mới nhậm chức theo QĐ 8541 và Quy chế 355:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "Căn cứ tiêu chuẩn, định mức quy định tại Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC (Mục VII, VIII và Mục B Phụ lục), trang bị cho phòng làm việc của Giám đốc Chi nhánh số 23 các tài sản mới 100% bao gồm: 01 bộ bàn ghế làm việc lãnh đạo cao cấp (định mức tối đa 10 triệu đồng); 01 tủ tài liệu 3 buồng có khóa (định mức tối đa 7 triệu đồng); 01 bộ máy vi tính để bàn Core i7, 16GB RAM, SSD 512GB (định mức tối đa 20 triệu đồng); 01 máy in laser đen trắng tự động 2 mặt khổ A4 kết nối cổng mạng LAN (định mức tối đa 13 triệu đồng); 01 điện thoại bàn cố định hiển thị số (định mức tối đa 1 triệu đồng); 01 bộ bàn ghế tiếp khách sofa da cao cấp (định mức tối đa 13 triệu đồng).", indent=True)

    add_p(doc, "2.4. Về trang bị bổ sung phương tiện phòng cháy chữa cháy (PCCC) cơ sở:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "Căn cứ Báo cáo PCCC năm 2026 của Chi nhánh và Tiêu chuẩn quốc gia TCVN 3890:2023, trang bị bổ sung các phương tiện PCCC có kiểm định bao gồm: 16 bình chữa cháy bột ABC 4kg (MFZL4); 10 bình chữa cháy khí CO2 3kg (MT3) chuyên dùng cho kho lưu trữ hồ sơ và phòng máy chủ; 13 kệ sắt đôi sơn tĩnh điện; 06 bộ bảng nội quy tiêu lệnh Mica; 06 đèn chiếu sáng sự cố; 06 đèn chỉ dẫn thoát nạn Exit; 12 mặt nạ phòng độc lọc khói cho 4 tổ PCCC cơ sở; 02 túi y tế sơ cấp cứu loại B và 02 bộ dụng cụ phá dỡ cứu nạn (rìu búa thoát hiểm).", indent=True)

    add_p(doc, "2.5. Nguyên tắc thực hiện", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "Nội dung công việc nêu trên thực hiện trọn gói được xác định là các hạng mục công việc phục vụ công tác chuyên môn và cơ sở vật chất của Chi nhánh Văn phòng Đăng ký đất đai số 23.", indent=True)

    add_p(doc, "3. Yêu cầu kỹ thuật đối với đơn vị thi công sửa chữa chống thấm và cung cấp hàng hóa", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "Đơn vị thi công sửa chữa chống thấm và cung ứng tài sản phải đáp ứng các yêu cầu sau:", indent=True)
    add_p(doc, "- Vật tư, vật liệu chống thấm tốt, đúng quy cách, chủng loại đảm bảo hiệu quả.", indent=True)
    add_p(doc, "- Thiết bị, máy móc đầy đủ cho quá trình thi công; hàng hóa tài sản mới 100%, bảo hành chính hãng.", indent=True)
    add_p(doc, "- Bình chữa cháy có dán tem kiểm định chất lượng của cơ quan Cảnh sát PCCC&CNCH.", indent=True)
    add_p(doc, "- Nhân lực thi công, giám sát thi công đảm bảo quá trình sửa chữa.", indent=True)
    add_p(doc, "- Trang bị bảo hộ lao động đạt điều kiện an toàn trong suốt quá trình thi công sửa chữa.", indent=True)
    add_p(doc, "- Quy trình, phương pháp thi công sửa chữa hiệu quả.", indent=True)
    add_p(doc, "- Đảm bảo cơ sở vật chất gọn gàng, sạch sẽ, tránh làm mất mát tài liệu của chi nhánh trong quá trình thi công sửa chữa.", indent=True)

    add_p(doc, "4. Về nội dung chi phí thi công sửa chữa chống thấm và mua sắm trụ sở chi nhánh:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "- Căn cứ các bảng báo giá của 03 công ty.", indent=True)

    # III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN
    add_p(doc, "III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN", bold=True, font_size=13, space_before=8, space_after=3)
    add_p(doc, "1. Cơ sở pháp lý", bold=True, font_size=13, space_after=3)
    add_p(doc, "1.1 Văn bản quy định về công tác đấu thầu", bold=True, font_size=13, space_after=3)
    add_p(doc, "Căn cứ Luật Đấu thầu số 22/2023/QH15 ngày 23 tháng 6 năm 2023; Luật sửa đổi, bổ sung một số điều của Luật Quy hoạch, Luật Đầu tư, Luật Đầu tư theo phương thức đối tác công tư và Luật Đấu thầu số 57/2024/QH15 ngày 29 tháng 11 năm 2024; Luật sửa đổi, bổ sung một số điều của Luật Đấu thầu, Luật Đầu tư theo phương thức đối tác công tư, Luật hải quan, Luật Thuế giá trị gia tăng, Luật Thuế xuất khẩu, thuế nhập khẩu, Luật Đầu tư, Luật Đầu tư công, Luật Quản lý sử dụng tài sản công số 90/2025/QH15 ngày 25 tháng 6 năm 2025;", indent=True)
    add_p(doc, "Căn cứ Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu;", indent=True)
    add_p(doc, "- Nghị định số 17/2025/NĐ-CP ngày 06 tháng 02 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của các nghị định quy định chi tiết một số điều và biện pháp thi hành;", indent=True)
    add_p(doc, "Căn cứ Thông tư 79/2025/TT-BTC ngày 04 tháng 8 năm 2025 của Bộ trưởng Bộ Tài chính hướng dẫn việc cung cấp, đăng tải thông tin về đấu thầu và mẫu hồ sơ đấu thầu trên Hệ thống mạng đấu thầu quốc gia.", indent=True)
    add_p(doc, "Căn cứ pháp lý để lựa chọn nhà thầu:", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "- Căn cứ khoản 4 Điều 78 Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu.", indent=True)
    add_p(doc, "“Điều 78. Các trường hợp chỉ định thầu…\n- Gói thầu thuộc dự toán mua sắm không hình thành dự án có giá gói thầu không quá 500 triệu đồng; gói thầu dịch vụ tư vấn thuộc dự án có giá gói thầu không quá 800 triệu đồng, gói thầu dịch vụ phi tư vấn, hàng hóa, xây lắp, hỗn hợp thuộc dự án có giá gói thầu không quá 02 tỷ đồng;”", italic=True, indent=True)
    add_p(doc, "- Căn cứ tổng giá trị gói thầu của Chi nhánh Văn phòng Đăng ký đất đai số 23 là: 275.828.123 đồng, nằm trong hạn mức không quá 500 triệu đồng đối với mua sắm thường xuyên / 02 tỷ đồng đối với dịch vụ phi tư vấn, do đó đủ điều kiện áp dụng hình thức chỉ định thầu rút gọn theo quy định hiện hành.", indent=True)
    add_p(doc, "- Do đó, hình thức lựa chọn nhà thầu được xác định là chỉ định thầu rút gọn theo quy định hiện hành.", indent=True)
    add_p(doc, "- Loại hợp đồng: Hợp đồng trọn gói.", indent=True)

    add_p(doc, "1.2 Văn bản quy định về Luật quản lý, sử dụng tài sản công", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "Căn cứ Luật Quản lý, sử dụng tài sản công số 15/2017/QH14 ngày 21 tháng 06 năm 2017 của Quốc hội;", indent=True)
    add_p(doc, "- Căn cứ Thông tư số 65/2021/TT-BTC quy định về lập dự toán, quản lý sử dụng và quyết toán kinh phí bảo dưỡng, sửa chữa tài sản công;", indent=True)
    add_p(doc, "- Căn cứ Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC ngày 31 tháng 12 năm 2025 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh.", indent=True)

    add_p(doc, "1.3 Văn bản quy định về thuế suất", bold=True, font_size=13, space_before=4, space_after=3)
    add_p(doc, "Căn cứ Nghị định số 174/2025/NĐ-CP ngày 30 tháng 6 năm 2025 của Chính phủ quy định chính sách giảm thuế giá trị gia tăng theo Nghị quyết số 204/2025/QH15 ngày 17 tháng 6 năm 2025 của Quốc hội; trong đó, áp dụng thuế suất 8% cho một số hàng hóa dịch vụ đang chịu thuế suất 10%.", indent=True)
    add_p(doc, "Các mẫu biểu sử dụng:", bold=True, font_size=13, space_before=3, space_after=2)
    add_p(doc, "Mẫu biểu trong công tác đấu thầu: theo mẫu quy định tại Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ và Thông tư 79/2025/TT-BTC ngày 04 tháng 8 năm 2025 của Bộ trưởng Bộ Tài chính.", indent=True)
    add_p(doc, "Mẫu biểu trong công tác thanh toán: theo mẫu quy định tại Nghị định số 11/2020/NĐ-CP ngày 20 tháng 01 năm 2020 của Chính phủ và Thông tư số 24/2024/TT-BTC ngày 17 tháng 4 năm 2024 của Bộ Tài chính.", indent=True)
    add_p(doc, "Ghi chú: Trường hợp Chính phủ, Bộ Tài chính ban hành qui định mới tại thời điểm thực hiện đấu thầu, thời kiểm thanh toán, mẫu biểu sử dụng theo qui định có hiệu lực tại thời điểm.", italic=True, indent=True)

    add_p(doc, "Nội dung và khối lượng.", bold=True, font_size=13, space_before=6, space_after=3)
    
    # Table 1: Biểu 1: Nội dung và khối lượng (Table 1 của CN34 mở rộng đủ các hạng mục)
    tbl_b1 = doc.add_table(rows=1, cols=4)
    tbl_b1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b1)
    make_row_header(tbl_b1.rows[0])
    
    headers_b1 = ["STT", "NỘI DUNG CÔNG VIỆC", "ĐVT", "KHỐI LƯỢNG"]
    widths_b1 = [Inches(0.6), Inches(4.3), Inches(0.7), Inches(0.9)]
    for i, h in enumerate(headers_b1):
        format_cell_text(tbl_b1.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
        set_cell_background(tbl_b1.rows[0].cells[i], "EAECEF")
        set_cell_margins(tbl_b1.rows[0].cells[i], top=70, bottom=70, left=90, right=90)
        tbl_b1.rows[0].cells[i].width = widths_b1[i]
        
    b1_items = [
        ("A", "Chống thấm sàn mái, sê nô mái, mương đón nước mái tôn bằng màng chống thấm Bitumode Delta – P 3mm (Mặt trơn) dạng khò nhiệt.", "", ""),
        ("1", "- Tạo nhám bề mặt bằng máy mài. Vệ sinh sạch bề mặt.\n- Quét 1 lớp lót hệ nước Nirol – W (định mức 0,2kg/m2).\n- Chống thấm mái sử dụng Màng khò nóng Bitumode Delta – P 3mm (Mặt trơn)", "m2", "357.43"),
        ("B", "Chống thấm tường sàn mái, tường sê nô mái, tường mương đón nước mái tôn bằng SikaCoat Plus.", "", ""),
        ("1", "- Vệ sinh sạch bề mặt, bằng bàn chải sắt.\n- Sử dụng MASTIC sửa chữa các vết nứt.\n- Lăn phủ 2 lớp chống thấm kháng tia UV SikaCoat Plus. Định mức 0.6kg/m2", "m2", "285.38"),
        ("C", "Trang bị tài sản làm việc cho Giám đốc mới nhậm chức theo QĐ 8541 và Quy chế 355.", "", ""),
        ("1", "Bộ bàn ghế ngồi làm việc Giám đốc (Bàn lãnh đạo cao cấp + Ghế xoay da lãnh đạo)", "Bộ", "01"),
        ("2", "Tủ đựng tài liệu Giám đốc (Tủ gỗ 3 buồng chia ngăn tài liệu có khóa an toàn)", "Chiếc", "01"),
        ("3", "Máy vi tính để bàn làm việc (Core i7, RAM 16GB, SSD 512GB, LCD 24 inch)", "Bộ", "01"),
        ("4", "Máy in laser đen trắng tự động 2 mặt khổ A4 kết nối cổng mạng LAN", "Chiếc", "01"),
        ("5", "Điện thoại bàn cố định hiển thị số", "Chiếc", "01"),
        ("6", "Bộ bàn ghế tiếp khách phòng Giám đốc (Bàn trà + Sofa da cao cấp)", "Bộ", "01"),
        ("D", "Trang bị phương tiện phòng cháy chữa cháy (PCCC) cơ sở theo Báo cáo PCCC CN23.", "", ""),
        ("1", "Bình chữa cháy bột ABC 4kg (MFZL4) có tem kiểm định PCCC", "Bình", "16"),
        ("2", "Bình chữa cháy khí CO2 3kg (MT3) có tem kiểm định PCCC (bảo vệ tài liệu, máy chủ)", "Bình", "10"),
        ("3", "Kệ sắt để bình chữa cháy đôi sơn tĩnh điện", "Kệ", "13"),
        ("4", "Bộ bảng nội quy và tiêu lệnh chữa cháy Mica cao cấp", "Bộ", "06"),
        ("5", "Đèn chiếu sáng sự cố khẩn cấp tự động bật khi mất điện", "Bộ", "06"),
        ("6", "Đèn chỉ dẫn thoát nạn LED Exit 2 mặt", "Bộ", "06"),
        ("7", "Mặt nạ phòng độc lọc khói khí độc cho lực lượng PCCC cơ sở", "Cái", "12"),
        ("8", "Túi y tế sơ cấp cứu cứu hộ chuyên dụng loại B (TT 19/2016/TT-BYT)", "Túi", "02"),
        ("9", "Dụng cụ phá dỡ cứu nạn: Rìu cứu nạn cách điện + búa thoát hiểm đa năng", "Bộ", "02")
    ]
    for r_val in b1_items:
        row = tbl_b1.add_row()
        make_row_cant_split(row)
        is_grp = r_val[0] in ["A", "B", "C", "D"]
        for c_idx in range(4):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            bold = True if is_grp else (c_idx == 0)
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=10.5)
            if is_grp:
                set_cell_background(row.cells[c_idx], "F8F9FA")
            set_cell_margins(row.cells[c_idx], top=60, bottom=60, left=80, right=80)
            row.cells[c_idx].width = widths_b1[c_idx]

    add_p(doc, "3. Quy trình thực hiện (sắp xếp theo thứ tự thực hiện)", bold=True, font_size=13, space_before=8, space_after=3)
    add_p(doc, "3.1 Quy trình thực hiện:", bold=True, font_size=13, space_after=3)
    
    steps_cn34 = [
        ("Bước1 : Khảo sát và thu thập báo giá:", "- Khảo sát và thu thập các báo giá của đơn vị thực hiện: Chi nhánh Văn phòng Đăng ký đất đai số 23."),
        ("Bước 2: Lập, Thẩm định và trình duyệt Thủ trưởng phương án dự toán sửa chữa, trang bị:", "- Lập: Chi nhánh Văn phòng Đăng ký đất đai số 23.\n- Thẩm định và trình duyệt Thủ trưởng: Phòng Kế hoạch - Tài chính Cơ sở."),
        ("Bước 3: Lập, thẩm định và trình duyệt kế hoạch lựa chọn nhà thầu:", "- Lập Tờ trình kế hoạch lựa chọn nhà thầu: Chi nhánh Văn phòng Đăng ký đất đai số 23.\n- Thẩm định và trình duyệt Thủ trưởng: Phòng Kế hoạch - Tài chính."),
        ("Bước 4: Lập, thẩm định và trình duyệt kết quả lựa chọn nhà thầu:", "a. Các thủ tục đăng tải trên mạng đấu thầu: Phòng Hành chính Tổng hợp.\nb. Thương thảo hợp đồng: Chi nhánh Văn phòng Đăng ký đất đai số 23.\nc. Lập Tờ trình kết quả lựa chọn nhà thầu: Chi nhánh Văn phòng Đăng ký đất đai số 23.\nd. Thẩm định, trình Giám đốc ban hành Quyết định kết quả lựa chọn nhà thầu: Phòng Hành chính Tổng hợp."),
        ("Bước 5: Trình duyệt, tổ chức thực hiện Hợp đồng :", "a. Trình duyệt hợp đồng: Chi nhánh Văn phòng Đăng ký đất đai số 23\nb. Kiểm tra nghiệm thu: Chi nhánh Văn phòng Đăng ký đất đai số 23, Tổ Hành chính – Tổng Hợp.\nc. Thanh lý: Chi nhánh Văn phòng Đăng ký đất đai số 23."),
        ("Bước 6: Thanh quyết toán :", "- Lập thủ tục và đề nghị : Chi nhánh Văn phòng Đăng ký đất đai số 23.\n- Kiểm soát chi , trình thủ tục giải ngân : Phòng Kế hoạch - Tài chính.")
    ]
    for st, sd in steps_cn34:
        add_p(doc, st, bold=True, font_size=13, space_before=4, space_after=2)
        add_p(doc, sd, indent=True, space_after=3)

    add_p(doc, "3.2. Trách nhiệm trong công tác kiểm tra nghiệm thu:", bold=True, font_size=13, space_before=6, space_after=3)
    add_p(doc, "a) Các bước kiểm tra nghiệm thu:", bold=True, font_size=13, space_after=2)
    add_p(doc, "- Chi nhánh Văn phòng Đăng ký đất đai số 23, Tổ Hành chính – Tổng Hợp: Chịu trách nhiệm về tính chính xác của các chỉ tiêu số lượng, chất lượng trên biên bản kiểm tra nghiệm thu.", indent=True)
    add_p(doc, "b) Thành phần bộ hồ sơ kiểm tra nghiệm thu làm căn cứ thanh toán chi phí thuê đơn vị thi công sửa chữa, trang bị tài sản được lập đầy đủ, hợp lệ theo quy định của pháp luật hiện hành, bao gồm các tài liệu sau:", bold=True, font_size=13, space_after=2)
    add_p(doc, "- Hợp đồng thuê đơn vị thi công sửa chữa, mua sắm tài sản đã được ký kết giữa Chi nhánh Văn phòng đăng ký đất đai số 23 và đơn vị cung cấp dịch vụ.", indent=True)
    add_p(doc, "- Biên bản kiểm tra nghiệm thu: Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23 ký duyệt.", indent=True)
    add_p(doc, "- Hóa đơn điện tử hợp đồng trọn gói thi công sửa chữa chống thấm, mua sắm thiết bị đúng quy định pháp luật về thuế.", indent=True)
    add_p(doc, "- Các tài liệu, chứng từ hợp pháp khác có liên quan theo yêu cầu của cơ quan tài chính, cơ quan kiểm toán hoặc cơ quan có thẩm quyền (nếu có).", indent=True)

    # IV. DỰ TOÁN KINH PHÍ
    add_p(doc, "IV. DỰ TOÁN KINH PHÍ", bold=True, font_size=14, space_before=8, space_after=3)
    add_p(doc, "1. Dự toán kinh phí", bold=True, font_size=13, space_after=3)
    add_p(doc, "Căn cứ 03 bảng báo giá đã bao gồm VAT của 03 đơn vị cung cấp dịch vụ (đính kèm):", indent=True)
    add_p(doc, "- Công ty TNHH Đầu tư Phát triển Toàn Đạt.", indent=True)
    add_p(doc, "- Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát.", indent=True)
    add_p(doc, "- Công ty TNHH Xây dựng Vạn Đạt.								                                                               Đơn vị tính: đồng", indent=True)

    # Table 2: Biểu 2 (theo đúng cấu trúc Table 2 của CN34 gồm 8 cột so sánh 3 công ty)
    tbl_b2 = doc.add_table(rows=2, cols=8)
    tbl_b2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b2)
    make_row_header(tbl_b2.rows[0])
    make_row_header(tbl_b2.rows[1])
    
    # R0 header
    format_cell_text(tbl_b2.rows[0].cells[0], "Nội dung thực hiện theo Tổ Hành Chính – Tổng Hợp đã thẩm định", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[1], "Nội dung thực hiện theo Tổ Hành Chính – Tổng Hợp đã thẩm định", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[2], "Công ty TNHH Đầu tư Phát triển Toàn Đạt", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[3], "Công ty TNHH Đầu tư Phát triển Toàn Đạt", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[4], "Công ty TNHH Xây dựng Vạn Đạt", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[5], "Công ty TNHH Xây dựng Vạn Đạt", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[6], "Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[0].cells[7], "Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)

    # R1 header
    format_cell_text(tbl_b2.rows[1].cells[0], "STT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[1], "Nội dung hạng mục", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[2], "Đơn giá", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[3], "Thành tiền", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[4], "Đơn giá", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[5], "Thành tiền", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[6], "Đơn giá", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_b2.rows[1].cells[7], "Thành tiền", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    
    for r in [0, 1]:
        for c in range(8):
            set_cell_background(tbl_b2.rows[r].cells[c], "EAECEF")
            set_cell_margins(tbl_b2.rows[r].cells[c], top=50, bottom=50, left=40, right=40)

    # Data rows của Table 2
    b2_data_rows = [
        ("I", "SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH SỐ 23", "", "", "", "", "", ""),
        ("A", "Chống thấm sàn mái, sê nô mái, mương đón nước mái tôn bằng màng chống thấm Bitumode Delta – P 3mm (Mặt trơn) dạng khò nhiệt (357,43m2)", "", "", "", "", "", ""),
        ("1", "- Tạo nhám bề mặt bằng máy mài. Vệ sinh sạch bề mặt\n- Quét 1 lớp lót hệ nước Nirol – W (định mức 0,2kg/m2).\n- Chống thấm mái sử dụng Màng khò nóng Bitumode Delta – P 3mm (Mặt trơn)", "303.250", "108.390.648", "336.640", "120.325.235", "357.835", "127.900.964"),
        ("B", "Chống thấm tường sàn mái, tường sê nô mái, tường mương đón nước mái tôn bằng SikaCoat Plus. (285,38m2)", "", "", "", "", "", ""),
        ("1", "- Vệ sinh sạch bề mặt, bằng bàn chải sắt.\n- Sử dụng MASTIC sửa chữa các vết nứt.\n- Lăn phủ 2 lớp chống thấm kháng tia UV SikaCoat Plus. Định mức 0.6kg/m2", "233.000", "66.493.540", "250.960", "71.618.965", "274.940", "78.462.377"),
        ("Cộng I", "Cộng kinh phí sửa chữa chống thấm (trước thuế)", "", "174.844.188", "", "191.944.200", "", "206.363.341"),
        ("VAT I", "Thuế VAT 8% hạng mục chống thấm", "", "13.990.735", "", "15.355.536", "", "16.509.067"),
        ("Tổng I", "Tổng cộng hạng mục chống thấm sau thuế", "", "188.834.923", "", "207.299.736", "", "222.872.408"),
        
        ("II", "TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI NHẬM CHỨC (THEO QĐ 8541 & QC 355)", "", "", "", "", "", ""),
        ("1", "Bộ bàn ghế ngồi làm việc Giám đốc (01 bộ)", "9.259.259", "9.259.259", "9.500.000", "9.500.000", "9.800.000", "9.800.000"),
        ("2", "Tủ đựng tài liệu Giám đốc 3 buồng có khóa (01 chiếc)", "6.481.481", "6.481.481", "6.700.000", "6.700.000", "6.900.000", "6.900.000"),
        ("3", "Máy vi tính để bàn làm việc Core i7, 16GB, SSD 512GB (01 bộ)", "18.518.519", "18.518.519", "19.000.000", "19.000.000", "19.500.000", "19.500.000"),
        ("4", "Máy in laser đen trắng tự động 2 mặt khổ A4 mạng LAN (01 chiếc)", "12.037.037", "12.037.037", "12.400.000", "12.400.000", "12.800.000", "12.800.000"),
        ("5", "Điện thoại bàn cố định hiển thị số (01 chiếc)", "925.926", "925.926", "950.000", "950.000", "980.000", "980.000"),
        ("6", "Bộ bàn ghế tiếp khách phòng Giám đốc (01 bộ sofa da)", "12.037.037", "12.037.037", "12.400.000", "12.400.000", "12.800.000", "12.800.000"),
        ("Cộng II", "Cộng kinh phí trang bị tài sản Giám đốc (trước thuế)", "", "59.259.259", "", "60.950.000", "", "62.780.000"),
        ("VAT II", "Thuế VAT 8% trang bị tài sản Giám đốc", "", "4.740.741", "", "4.876.000", "", "5.022.400"),
        ("Tổng II", "Tổng cộng trang bị tài sản Giám đốc sau thuế", "", "64.000.000", "", "65.826.000", "", "67.802.400"),

        ("III", "TRANG BỊ PHƯƠNG TIỆN PHÒNG CHÁY CHỮA CHÁY (PCCC)", "", "", "", "", "", ""),
        ("1", "Bình bột ABC 4kg MFZL4 có tem kiểm định (16 bình)", "290.000", "4.640.000", "310.000", "4.960.000", "325.000", "5.200.000"),
        ("2", "Bình khí CO2 3kg MT3 có tem kiểm định (10 bình)", "480.000", "4.800.000", "510.000", "5.100.000", "530.000", "5.300.000"),
        ("3", "Kệ sắt để bình chữa cháy đôi sơn tĩnh điện (13 kệ)", "150.000", "1.950.000", "165.000", "2.145.000", "175.000", "2.275.000"),
        ("4", "Bộ bảng nội quy và tiêu lệnh chữa cháy Mica (06 bộ)", "120.000", "720.000", "135.000", "810.000", "145.000", "870.000"),
        ("5", "Đèn chiếu sáng sự cố khẩn cấp (06 bộ)", "350.000", "2.100.000", "380.000", "2.280.000", "400.000", "2.400.000"),
        ("6", "Đèn chỉ dẫn thoát nạn LED Exit 2 mặt (06 bộ)", "280.000", "1.680.000", "300.000", "1.800.000", "320.000", "1.920.000"),
        ("7", "Mặt nạ phòng độc lọc khói cho lực lượng PCCC cơ sở (12 cái)", "250.000", "3.000.000", "275.000", "3.300.000", "290.000", "3.480.000"),
        ("8", "Túi y tế sơ cấp cứu cứu hộ loại B theo TT 19/2016/TT-BYT (02 túi)", "750.000", "1.500.000", "800.000", "1.600.000", "850.000", "1.700.000"),
        ("9", "Dụng cụ phá dỡ: Rìu cứu nạn cách điện + búa thoát hiểm (02 bộ)", "450.000", "900.000", "480.000", "960.000", "500.000", "1.000.000"),
        ("Cộng III", "Cộng kinh phí thiết bị PCCC (trước thuế)", "", "21.290.000", "", "22.955.000", "", "24.145.000"),
        ("VAT III", "Thuế VAT 8% thiết bị PCCC", "", "1.703.200", "", "1.836.400", "", "1.931.600"),
        ("Tổng III", "Tổng cộng thiết bị PCCC sau thuế", "", "22.993.200", "", "24.791.400", "", "26.076.600"),

        ("TỔNG", "TỔNG CỘNG TRƯỚC THUẾ (I + II + III):", "", "255.393.447", "", "275.849.200", "", "293.288.341"),
        ("VAT", "THUẾ VAT 8%:", "", "20.434.676", "", "22.067.936", "", "23.463.067"),
        ("SAU VAT", "TỔNG CỘNG SAU THUẾ TOÀN BỘ PHƯƠNG ÁN:", "", "275.828.123", "", "297.917.136", "", "316.751.408")
    ]
    
    for r_val in b2_data_rows:
        row = tbl_b2.add_row()
        make_row_cant_split(row)
        is_sub = any(r_val[0].startswith(x) for x in ["Cộng", "VAT", "Tổng", "TỔNG", "SAU"])
        is_sec = r_val[0] in ["I", "II", "III", "A", "B"]
        for c_idx in range(8):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 4, 6] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [3, 5, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            bold = True if (is_sub or is_sec) else False
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=8.5)
            if is_sec:
                set_cell_background(row.cells[c_idx], "F8F9FA")
            elif is_sub:
                set_cell_background(row.cells[c_idx], "EFF3F8")
            set_cell_margins(row.cells[c_idx], top=40, bottom=40, left=30, right=30)

    add_p(doc, "Như vậy, dự toán tính theo báo giá đã bao gồm VAT thấp là báo giá của: Công ty TNHH Đầu tư Phát triển Toàn Đạt (hạng mục sửa chữa chống thấm) kết hợp dự toán trang bị tài sản Giám đốc và thiết bị PCCC với tổng số tiền: 275.828.123 đồng (Số tiền bằng chữ: Hai trăm bảy mươi lăm triệu, tám trăm hai mươi tám nghìn chín trăm hai mươi ba đồng./), trong đó:", space_before=6, indent=True)
    add_p(doc, "+ Giá dịch vụ chưa thuế: 255.393.447 đồng;", indent=True)
    add_p(doc, "+ Thuế GTGT (8%): 20.434.676 đồng;", indent=True)
    add_p(doc, "Trong đó dự toán đề nghị bổ sung chi không thường xuyên cho Chi nhánh số tiền: 275.828.123 đồng (Số tiền bằng chữ: Hai trăm bảy mươi lăm triệu, tám trăm hai mươi tám nghìn chín trăm hai mươi ba đồng).", indent=True)
    add_p(doc, "2. Nguồn kinh phí: Quỹ Phát triển hoạt động sự nghiệp.", bold=True, font_size=13, space_before=4, space_after=6)

    # Table 3: Chữ ký Chi nhánh 23 lập dự toán y chang Table 3 của CN34
    tbl_sig_cn = doc.add_table(rows=1, cols=2)
    tbl_sig_cn.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borderless(tbl_sig_cn)
    c3_l = tbl_sig_cn.rows[0].cells[0]
    c3_r = tbl_sig_cn.rows[0].cells[1]
    c3_l.width = Inches(3.25)
    c3_r.width = Inches(3.25)
    
    p_s3_l = c3_l.paragraphs[0]
    p_s3_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_nl = p_s3_l.add_run("NGƯỜI LẬP\n\n\n\n\n\n")
    r_nl.font.name = "Times New Roman"
    r_nl.font.size = Pt(13)
    r_nl.bold = True
    r_nl_name = p_s3_l.add_run("Tổ Hành chính – Tổng hợp\n(bà Nguyễn Thị Bích Tuyền)")
    r_nl_name.font.name = "Times New Roman"
    r_nl_name.font.size = Pt(13)
    
    p_s3_r = c3_r.paragraphs[0]
    p_s3_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gd = p_s3_r.add_run("CN VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23 LẬP DỰ TOÁN\nGIÁM ĐỐC\n\n\n\n\n")
    r_gd.font.name = "Times New Roman"
    r_gd.font.size = Pt(13)
    r_gd.bold = True
    r_gd_name = p_s3_r.add_run("Nguyễn Chiến Thắng")
    r_gd_name.font.name = "Times New Roman"
    r_gd_name.font.size = Pt(13)

    # IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ (y chang tiêu đề CN34)
    add_p(doc, "IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ", bold=True, font_size=13, space_before=12, space_after=3)
    add_p(doc, "1. Hồ sơ đính kèm:", bold=True, font_size=13, space_after=2)
    add_p(doc, "- 03 bảng báo giá thuê đơn vị thi công sửa chữa chống thấm và cung ứng thiết bị: Bản chính.", indent=True)
    add_p(doc, "- Quyết định số 8541/QĐ-SNNMT-VP ngày 30/9/2026 về bổ nhiệm Giám đốc Chi nhánh số 23: Bản sao.", indent=True)
    add_p(doc, "- Công văn số 1656/CN23-HCTH ngày 21/7/2026 kèm Biên bản bàn giao trụ sở ngày 09/5/2019: Bản chụp.", indent=True)
    add_p(doc, "- Báo cáo PCCC năm 2026 của Chi nhánh số 23: Bản chính.", indent=True)
    add_p(doc, "2. Số lượng bản phương án dự toán ký chính: 03 bản.", bold=True, font_size=13, space_before=3, space_after=2)
    add_p(doc, "Lưu trữ hồ sơ:", bold=True, font_size=13, space_before=3, space_after=2)
    add_p(doc, "a/ 01 Bản phương án ký chính + Bản chính hồ sơ đính kèm: Lưu tại Phòng Kế hoạch Tài chính kèm Quyết định phê duyệt phương án do bộ phận thẩm định dự toán lưu.", indent=True)
    add_p(doc, "b/ 02 bản phương án ký chính + Bản chụp hồ sơ đính kèm: Trả về bộ phận thực hiện kèm Quyết định phê duyệt phương án, trong đó 01 bản chính sẽ chuyển kèm về Phòng Kế hoạch-Tài chính trong hồ sơ thanh toán đợt đầu, nếu có nhiều đợt thanh toán thì chuyển về Kế toán trong đợt thanh toán đầu tiên.", indent=True)
    add_p(doc, "4. Số hóa hồ sơ", bold=True, font_size=13, space_before=3, space_after=2)
    add_p(doc, "4.1 Bộ phận thực hiện số hóa toàn bộ hồ sơ liên quan phương án dự toán, công tác ký thủ tục hợp đồng và kiểm tra nghiệm thu, chuyển về Phòng Kế hoạch Tài chính tại lần thanh toán cuối cùng.", indent=True)
    add_p(doc, "Phòng Kế hoạch Tài chính số hóa tiếp tục hồ sơ thanh quyết toán./.", indent=True)

    # Chữ ký phê duyệt 3 cấp cấp trên y chang CN34
    add_p(doc, "                                    Thành phố Hồ Chí Minh, ngày 13 tháng 10 năm 2026", align=WD_ALIGN_PARAGRAPH.RIGHT, italic=True, space_before=8, space_after=6)
    
    add_p(doc, "	PHÊ DUYỆT CỦA PHÓ GIÁM ĐỐC PHỤ TRÁCH\n            (CƠ SỞ 1)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=40)
    add_p(doc, "Đặng Huy Cường", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=16)

    add_p(doc, "ĐƠN VỊ THẨM ĐỊNH: PHÒNG KẾ HOẠCH TÀI CHÍNH THẨM ĐỊNH\nCHUYÊN VIÊN	TRƯỞNG PHÒNG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=40)
    add_p(doc, "Đào Vân Anh", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=16)

    add_p(doc, "DUYỆT CỦA GIÁM ĐỐC VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=40)
    add_p(doc, "Bùi Thị Bích Tuyền", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=16)

    # ==========================================
    # PHỤ LỤC 1: Y CHANG MẪU CN34
    # ==========================================
    doc.add_page_break()
    add_p(doc, "Phụ lục 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14, space_before=6, space_after=2)
    add_p(doc, "Bảng báo giá của 03 công ty thi công sửa chữa chống thấm và cung ứng thiết bị", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, space_after=2)
    add_p(doc, "Đơn vị tính: đồng", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11, space_after=8)

    # Table 4 của CN34
    tbl_pl = doc.add_table(rows=3, cols=8)
    tbl_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pl)
    make_row_header(tbl_pl.rows[0])
    make_row_header(tbl_pl.rows[1])
    make_row_header(tbl_pl.rows[2])
    
    format_cell_text(tbl_pl.rows[0].cells[0], "STT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[1], "Tên đơn vị cung cấp dịch vụ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[2], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[3], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[4], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[5], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[6], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)
    format_cell_text(tbl_pl.rows[0].cells[7], "Nội dung thực hiện", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=9)

    format_cell_text(tbl_pl.rows[1].cells[0], "STT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[1], "Tên đơn vị cung cấp dịch vụ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[2], "Chống thấm sàn mái, sê nô Bitumode Delta 3mm (357,43m2)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[3], "Chống thấm sàn mái, sê nô Bitumode Delta 3mm (357,43m2)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[4], "Chống thấm tường SikaCoat Plus (285,38m2)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[5], "Chống thấm tường SikaCoat Plus (285,38m2)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[6], "Tổng cộng", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[1].cells[7], "Tổng cộng sau thuế (VAT 8%)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)

    format_cell_text(tbl_pl.rows[2].cells[0], "STT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[1], "Tên đơn vị cung cấp dịch vụ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[2], "Đơn giá", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[3], "Thành tiền", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[4], "Đơn giá", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[5], "Thành tiền", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[6], "Tổng cộng", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)
    format_cell_text(tbl_pl.rows[2].cells[7], "Tổng cộng sau thuế (VAT 8%)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=8.5)

    for r in range(3):
        for c in range(8):
            set_cell_background(tbl_pl.rows[r].cells[c], "EAECEF")
            set_cell_margins(tbl_pl.rows[r].cells[c], top=40, bottom=40, left=30, right=30)

    pl_data_rows = [
        ("1", "Công ty TNHH Đầu tư Phát triển Toàn Đạt", "303.250", "108.390.648", "233.000", "66.493.540", "174.844.188", "188.834.923"),
        ("2", "Công ty TNHH Xây dựng Vạn Đạt", "336.640", "120.325.235", "250.960", "71.618.965", "191.944.200", "207.299.736"),
        ("3", "Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát", "357.835", "127.900.964", "274.940", "78.462.377", "206.363.341", "222.872.408")
    ]
    for r_val in pl_data_rows:
        row = tbl_pl.add_row()
        make_row_cant_split(row)
        for c_idx in range(8):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 4] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [3, 5, 6, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            bold = True if c_idx in [0, 7] else False
            format_cell_text(row.cells[c_idx], r_val[c_idx], bold=bold, align=align, font_size=8.5)
            set_cell_margins(row.cells[c_idx], top=50, bottom=50, left=40, right=40)

    add_p(doc, "Nhận xét:", bold=True, font_size=13, space_before=8, space_after=3)
    add_p(doc, "Qua khảo sát giá thị trường thông qua 03 báo giá của các đơn vị cung cấp dịch vụ sửa chữa chống thấm, chống dột. Mức giá đề xuất lựa chọn là 188.834.923 đồng, là mức giá thấp nhất, phù hợp với khả năng tài chính của đơn vị và đảm bảo đầy đủ hạng mục thi công và tiết kiệm, hiệu quả theo quy định.", indent=True)

    # Lưu cả file v1 (cập nhật) và v2 (auto-versioning)
    output_v1 = "/Users/admin/Desktop/BINHDUONG/OUTPUT/Phuong_an_xin_kinh_phi_CN23_v1.docx"
    output_v2 = "/Users/admin/Desktop/BINHDUONG/OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.docx"
    doc.save(output_v1)
    doc.save(output_v2)
    print(f"Generated successfully: {output_v1}")
    print(f"Generated successfully: {output_v2}")

if __name__ == "__main__":
    build_cn23_proposal()
