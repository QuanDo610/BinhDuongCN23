import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
    # Add page number field
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w'))
    p._p.append(fld)

def main():
    doc = docx.Document()

    # Configure Normal Style: Times New Roman, 13pt, Black, 1.2 line spacing
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)

    # ==========================================
    # SECTION 1: THÂN PHƯƠNG ÁN (PORTRAIT A4)
    # ==========================================
    sec1 = doc.sections[0]
    sec1.orientation = WD_ORIENT.PORTRAIT
    sec1.page_width = Inches(8.27)    # 210mm
    sec1.page_height = Inches(11.69)  # 297mm
    # Can le chuan ND 30: Top 20mm, Bot 20mm, Left 30mm, Right 15mm
    sec1.top_margin = Inches(0.79)    # 20mm
    sec1.bottom_margin = Inches(0.79) # 20mm
    sec1.left_margin = Inches(1.18)   # 30mm
    sec1.right_margin = Inches(0.59)  # 15mm
    add_page_number_to_section(sec1)

    # 1. BẢNG TIÊU ĐỀ ĐẦU TRANG (QUỐC HIỆU / CƠ QUAN BAN HÀNH - BORDERLESS)
    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    tbl_top.rows[0].cells[0].width = Inches(3.25)
    tbl_top.rows[0].cells[1].width = Inches(3.25)

    # Ô TRÁI: Cơ quan ban hành & Số ký hiệu
    c_left = tbl_top.rows[0].cells[0]
    p_unit = c_left.paragraphs[0]
    p_unit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_unit.paragraph_format.line_spacing = 1.15
    p_unit.paragraph_format.space_after = Pt(0)
    
    r1 = p_unit.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    
    r2 = p_unit.add_run("CHI NHÁNH SỐ 23\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    r2.font.bold = True
    
    r_line_unit = p_unit.add_run("────────────\n")
    r_line_unit.font.name = "Times New Roman"
    r_line_unit.font.size = Pt(9)
    r_line_unit.font.bold = True
    
    r_so = p_unit.add_run("Số:       /PA-CN23")
    r_so.font.name = "Times New Roman"
    r_so.font.size = Pt(13)

    # Ô PHẢI: Quốc hiệu, Tiêu ngữ & Ngày tháng
    c_right = tbl_top.rows[0].cells[1]
    p_qh = c_right.paragraphs[0]
    p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qh.paragraph_format.line_spacing = 1.15
    p_qh.paragraph_format.space_after = Pt(0)

    r_qh = p_qh.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_qh.font.name = "Times New Roman"
    r_qh.font.size = Pt(12)
    r_qh.font.bold = True

    r_tn = p_qh.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r_tn.font.name = "Times New Roman"
    r_tn.font.size = Pt(13)
    r_tn.font.bold = True

    r_line_tn = p_qh.add_run("─────────────────────────\n")
    r_line_tn.font.name = "Times New Roman"
    r_line_tn.font.size = Pt(9)
    r_line_tn.font.bold = True

    r_date = p_qh.add_run("Thủ Dầu Một, ngày      tháng      năm 2026")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(13)
    r_date.font.italic = True

    set_table_borderless(tbl_top)

    # 2. TÊN LOẠI & TRÍCH YẾU (MẪU 1.4 NGHỊ ĐỊNH 30)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("PHƯƠNG ÁN")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(14)
    r_t.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.2
    r_s = p_sub.add_run("Sử dụng tài sản phục vụ viên chức và người lao động\ntại Chi nhánh Văn phòng Đăng ký đất đai số 23")
    r_s.font.name = "Times New Roman"
    r_s.font.size = Pt(14)
    r_s.font.bold = True

    p_line_trichyeu = doc.add_paragraph()
    p_line_trichyeu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_trichyeu.paragraph_format.space_before = Pt(0)
    p_line_trichyeu.paragraph_format.space_after = Pt(14)
    r_ly = p_line_trichyeu.add_run("────────────")
    r_ly.font.name = "Times New Roman"
    r_ly.font.size = Pt(9)
    r_ly.font.bold = True

    # Helper functions for formatted paragraphs
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        return p

    def add_body_p(text, indent=True, bold_prefix=None, is_italic=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(6)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5) # 1.27cm
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = "Times New Roman"
            r_b.font.size = Pt(13)
            r_b.font.bold = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        if is_italic:
            r.font.italic = True
        return p

    # 3. I. CĂN CỨ PHÁP LÝ (In thường, nghiêng, cỡ 13, cuối mỗi dòng chấm phẩy, dòng cuối chấm)
    add_heading_1("I. Căn cứ pháp lý")

    can_cu_list = [
        "Căn cứ Luật Quản lý, sử dụng tài sản công ngày 21 tháng 6 năm 2017;",
        "Căn cứ Nghị định số 155/2025/NĐ-CP ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;",
        "Căn cứ Nghị định số 186/2025/NĐ-CP ngày 01 tháng 7 năm 2025 của Chính phủ quy định chi tiết một số điều của Luật Quản lý, sử dụng tài sản công; Nghị định số 286/2025/NĐ-CP ngày 03 tháng 11 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của các Nghị định trong lĩnh vực quản lý, sử dụng tài sản công;",
        "Căn cứ Công văn số 223/BTC-QLCS ngày 08 tháng 01 năm 2026 của Bộ Tài chính về việc rà soát, bố trí tài sản công theo đúng định mức quy định;",
        "Căn cứ Kế hoạch số 74/KH-UBND ngày 23 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố Hồ Chí Minh về việc triển khai sắp xếp, xử lý tài sản công sau sáp nhập các cơ quan hành chính;",
        "Căn cứ Công văn số 545/UBND-KT ngày 23 tháng 01 năm 2026 của Ủy ban nhân dân Thành phố Hồ Chí Minh về việc tăng cường quản lý, sử dụng tài sản công hiệu quả, tiết kiệm;",
        "Căn cứ Quyết định số 02/2026/QĐ-CTUBND ngày 16 tháng 01 năm 2026 của Chủ tịch Ủy ban nhân dân Thành phố Hồ Chí Minh về ban hành Quy chế quản lý, sử dụng tài sản công thuộc phạm vi quản lý của Thành phố Hồ Chí Minh;",
        "Căn cứ Công văn số 5440/STC-QLCS ngày 09 tháng 3 năm 2026 của Sở Tài chính Thành phố Hồ Chí Minh về việc hướng dẫn lập phương án sắp xếp lại, xử lý nhà, đất công;",
        "Căn cứ Công văn số 6949/SNNMT-KHTC ngày 20 tháng 3 năm 2026 của Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc rà soát hiện trạng và nhu cầu sử dụng trụ sở làm việc của các đơn vị trực thuộc;",
        "Căn cứ Quyết định số 1886/QĐ-UBND ngày 01 tháng 10 năm 2025 của Ủy ban nhân dân Thành phố Hồ Chí Minh về tổ chức lại Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh trên cơ sở hợp nhất Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Văn phòng Đăng ký đất đai tỉnh Bình Dương và Văn phòng Đăng ký đất đai tỉnh Bà Rịa - Vũng Tàu;",
        "Căn cứ Quyết định số 1551/QĐ-SNNMT-VP ngày 02 tháng 10 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh trực thuộc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh;",
        "Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ngày 15 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23 trực thuộc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh;",
        "Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc giao số lượng người làm việc cho Chi nhánh Văn phòng Đăng ký đất đai số 23;",
        "Căn cứ Thông tư số 09/2007/TT-BNV ngày 26 tháng 11 năm 2007 của Bộ Nội vụ hướng dẫn kho lưu trữ chuyên dùng;",
        "Căn cứ Tiêu chuẩn quốc gia TCVN 4319:2012 về Nhà và công trình công cộng - Nguyên tắc cơ bản để thiết kế;",
        "Căn cứ Biên bản bàn giao, tiếp nhận tài sản công ngày 09 tháng 5 năm 2019 giữa Ủy ban nhân dân phường Chánh Mỹ và Chi nhánh Văn phòng Đăng ký quyền sử dụng đất thành phố Thủ Dầu Một (nay là Chi nhánh Văn phòng Đăng ký đất đai số 23);",
        "Căn cứ Công văn số 17475/VPĐK-KHTC ngày 08 tháng 6 năm 2026 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc rà soát, cập nhật bổ sung số liệu thông tin về cơ sở nhà, đất đang quản lý, sử dụng;",
        "Căn cứ Tờ trình số 195/TTr-TYT ngày 04 tháng 3 năm 2026 của Trạm Y tế phường Thủ Dầu Một về việc đề nghị điều chuyển tài sản dôi dư cơ sở Điểm trạm y tế 3;",
        "Căn cứ Công văn số 602/CN23-HCTH ngày 14 tháng 4 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 về việc xin hỗ trợ mượn tạm mặt bằng Trạm y tế cơ sở 3 (cũ) để làm kho lưu trữ hồ sơ;",
        "Căn cứ Tờ trình số 427/TTr-TYT ngày 17 tháng 4 năm 2026 của Trạm Y tế phường Thủ Dầu Một về việc đề nghị cho Chi nhánh Văn phòng Đăng ký đất đai số 23 mượn tạm cơ sở Điểm trạm y tế 3 để sử dụng làm kho lưu trữ;",
        "Căn cứ Công văn số 413/KTHT&ĐT-NS ngày 05 tháng 5 năm 2026 của Phòng Kinh tế hạ tầng và Đô thị phường Thủ Dầu Một về việc phúc đáp ý kiến liên quan đến cơ sở Điểm trạm y tế 3 dôi dư;",
        "Căn cứ Công văn số 1136/UBND-VP ngày 08 tháng 5 năm 2026 của Ủy ban nhân dân phường Thủ Dầu Một về việc hướng dẫn rà soát, bổ sung thuyết minh tiêu chuẩn định mức phục vụ công tác điều chuyển trụ sở làm việc;",
        "Căn cứ Công văn số 1509/CN23-HCTH ngày 03 tháng 7 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 về việc báo cáo, đề xuất phương án xử lý cơ sở nhà, đất tại số 358 Huỳnh Văn Cù và Điểm trạm y tế 3;",
        "Căn cứ Công văn số 2122/UBND-VP ngày 20 tháng 7 năm 2026 của Ủy ban nhân dân phường Thủ Dầu Một về việc phối hợp giải quyết kiến nghị điều chuyển tài sản công cơ sở Điểm trạm y tế 3;",
        "Căn cứ Công văn số 1656/CN23-HCTH ngày 21 tháng 7 năm 2026 của Chi nhánh Văn phòng Đăng ký đất đai số 23 về việc giải trình, bổ sung phương án sử dụng tài sản công phục vụ viên chức và người lao động."
    ]

    for cc in can_cu_list:
        add_body_p(cc, indent=True, is_italic=True)

    # 4. II. MỤC ĐÍCH CỦA PHƯƠNG ÁN
    add_heading_1("II. Mục đích của phương án")
    add_heading_2("1. Căn cứ xây dựng phương án")
    add_body_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 (sau đây gọi tắt là Chi nhánh số 23) hiện đang quản lý, sử dụng tạm thời cơ sở nhà, đất tại địa chỉ số 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh (trước đây là trụ sở Ủy ban nhân dân phường Chánh Mỹ cũ do Ủy ban nhân dân thành phố Thủ Dầu Một giao tạm tiếp nhận quản lý từ năm 2018 và chính thức bàn giao theo Biên bản ngày 09/5/2019). Cơ sở nhà, đất hiện đang được Chi nhánh sử dụng thực tế để thực hiện nhiệm vụ chuyên môn, bố trí Bộ phận tiếp nhận và trả kết quả thủ tục hành chính, giải quyết hồ sơ đất đai và phục vụ người dân, tổ chức.")
    add_body_p("Do đặc thù ngành quản lý đất đai, khối lượng hồ sơ, tài liệu địa chính gốc và tài liệu biến động phát sinh hàng ngày tại địa bàn phụ trách là rất lớn. Hiện nay, kho lưu trữ chuyên dùng tại trụ sở số 358 Huỳnh Văn Cù bố trí diện tích gồm 391,00 m² sàn (kho lưu trữ hồ sơ địa chính hiện hữu năm 2019) và 15,00 m² sàn (kho lưu trữ hồ sơ tiếp nhận sau sáp nhập năm 2025 tận dụng góc hành lang phòng làm việc), tổng diện tích là 406,00 m² sàn đã lấp đầy 100% công suất tải; khoảng 30% hồ sơ chưa chỉnh lý đang phải để tạm tại các phòng làm việc. Trong khi đó, toàn bộ công trình hiện hữu chỉ có 835,30 m² sàn xây dựng, không gian tòa nhà phải ưu tiên tối đa bố trí vị trí ngồi làm việc cho 85 cán bộ nhân viên và sảnh Một cửa tiếp công dân, đơn vị hoàn toàn không còn diện tích sàn trống để mở rộng kho lưu trữ.")
    add_body_p("Qua rà soát quỹ nhà đất công dôi dư trên địa bàn, cơ sở nhà đất tại Điểm trạm y tế 3 (Trạm Y tế phường Chánh Mỹ cũ) tọa lạc trên đường Huỳnh Văn Cù, khu phố Chánh Lộc 7, phường Thủ Dầu Một (diện tích khuôn viên đất 1.276,20 m²) hiện đang bỏ trống và ngành y tế không còn nhu cầu sử dụng. Trạm Y tế phường Thủ Dầu Một đã có Tờ trình số 195/TTr-TYT ngày 04/3/2026 xin điều chuyển tài sản dôi dư và Tờ trình số 427/TTr-TYT ngày 17/4/2026 kiến nghị Ủy ban nhân dân phường Thủ Dầu Một chấp thuận cho Chi nhánh số 23 mượn tạm mặt bằng này để làm kho lưu trữ trong khi chờ cơ quan có thẩm quyền quyết định điều chuyển. Tại Công văn số 1136/UBND-VP ngày 08/5/2026, Ủy ban nhân dân phường Thủ Dầu Một đã hướng dẫn Chi nhánh báo cáo cấp có thẩm quyền để lập thủ tục điều chuyển tài sản công theo đúng quy định.")

    add_heading_2("2. Mục đích xây dựng phương án")
    add_body_p("Cụ thể hóa việc quản lý, sử dụng tài sản công theo đúng quy định của Luật Quản lý, sử dụng tài sản công, Nghị định số 155/2025/NĐ-CP, Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP của Chính phủ; bảo đảm việc quản lý, khai thác tài sản đúng mục đích, đúng công năng, đúng tiêu chuẩn định mức và tiết kiệm, hiệu quả.")
    add_body_p("Làm căn cứ pháp lý để bố trí, sắp xếp, quản lý và sử dụng trụ sở làm việc, đất đai, kho lưu trữ chuyên ngành, nhà để xe và các tài sản công khác phục vụ hoạt động chuyên môn, đáp ứng yêu cầu thực hiện chức năng, nhiệm vụ của Chi nhánh Văn phòng Đăng ký đất đai.")
    add_body_p("Nâng cao hiệu quả khai thác, sử dụng tài sản công; chấm dứt tình trạng tài sản công dôi dư bị bỏ trống gây xuống cấp, lãng phí quỹ đất công; đồng thời làm cơ sở rà soát, đề xuất cấp có thẩm quyền ban hành quyết định điều chuyển, hạch toán, bảo trì và quản lý tài sản theo đúng quy định.")
    add_body_p("Đáp ứng yêu cầu cải cách hành chính, chuyển đổi số ngành tài nguyên và môi trường, nâng cao chất lượng cung cấp dịch vụ công trong lĩnh vực đăng ký đất đai, cấp Giấy chứng nhận và giao dịch bảo đảm cho người dân và doanh nghiệp.")
    add_body_p("Bảo đảm điều kiện và môi trường làm việc đạt chuẩn, an toàn lao động, phòng cháy chữa cháy cho 85 cán bộ, viên chức và người lao động của Chi nhánh theo đúng tiêu chuẩn Nhà nước quy định.")

    add_heading_2("3. Đánh giá sự cần thiết của việc tiếp nhận, quản lý và sử dụng tài sản")
    add_body_p("Căn cứ chức năng, nhiệm vụ được giao và chỉ tiêu biên chế được phê duyệt tại Quyết định số 480/QĐ-VPĐK-HC ngày 30/3/2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, Chi nhánh số 23 được giao 85 người làm việc. Đối chiếu định mức sử dụng trụ sở làm việc theo quy định tại Nghị định số 155/2025/NĐ-CP:")
    add_body_p("- Tổng diện tích làm việc định mức của các chức danh (85 người) là: 1.260,00 m² (gồm 82 chức danh chuyên môn lãnh đạo x 15 m²/người = 1.230 m² và 03 hợp đồng lao động phục vụ x 10 m²/người = 30 m²).")
    add_body_p("- Diện tích sử dụng chung tối đa được phép bố trí theo quy định (Khoản 2 Điều 6 Nghị định 155/2025/NĐ-CP tối đa không quá 85% diện tích chức danh) là: 1.260,00 m² x 85% = 1.071,00 m².")
    add_body_p("- Tổng quy mô diện tích sàn xây dựng theo tiêu chuẩn định mức tối đa được phép bố trí: 1.260,00 m² + 1.071,00 m² = 2.331,00 m².")
    add_body_p("Trong khi đó, tổng diện tích sàn xây dựng thực tế của công trình hiện hữu tại số 358 Huỳnh Văn Cù chỉ có 835,30 m². So với diện tích thuần phòng làm việc của các chức danh (1.260 m²), cơ sở hiện hữu đang thiếu hụt trầm trọng 424,70 m² sàn; so với tổng quy mô định mức toàn bộ trụ sở (2.331 m²), cơ sở hiện hữu thiếu hụt 1.495,70 m² sàn và mới chỉ đáp ứng 35,83% nhu cầu định mức tối thiểu. Kết quả tính toán cơ học chứng minh ngay cả khi đơn vị sử dụng toàn bộ 100% diện tích sàn công trình hiện hữu chỉ để kê bàn ghế làm việc và triệt tiêu toàn bộ không gian dùng chung, trụ sở vẫn chưa đáp ứng đủ diện tích định mức.")
    add_body_p("Mặt khác, kho lưu trữ hồ sơ địa chính hiện hữu bố trí tổng cộng 406,00 m² sàn đã quá tải tuyệt đối 100%. Do đó, việc giữ lại nguyên vẹn trụ sở hiện hữu tại 358 Huỳnh Văn Cù kết hợp tiếp nhận điều chuyển cơ sở nhà đất công dôi dư độc lập liền kề tại Điểm trạm y tế 3 (khuôn viên đất 1.276,20 m²) để cải tạo thành kho lưu trữ hồ sơ địa chính chuyên ngành là giải pháp bắt buộc, tối ưu và cấp bách nhằm bảo vệ an toàn tài liệu quốc gia, phù hợp thẩm quyền và trình tự điều chuyển tài sản công quy định tại Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP.")

    # 5. III. THỰC TRẠNG QUẢN LÝ, SỬ DỤNG TÀI SẢN
    add_heading_1("III. Thực trạng quản lý, sử dụng tài sản tại Chi nhánh số 23")
    add_heading_2("1. Tổ chức bộ máy và nhân sự")
    add_body_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 là đơn vị trực thuộc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh. Số lượng người làm việc của đơn vị được giao theo Quyết định số 480/QĐ-VPĐK-HC ngày 30/3/2026 là 85 người, cơ cấu tổ chức bộ máy gồm:")
    add_body_p("+ Ban Giám đốc Chi nhánh: 03 người (Giám đốc và 02 Phó Giám đốc).")
    add_body_p("+ Nhân viên chuyên môn với 03 Tổ nghiệp vụ là 82 người, cụ thể:")
    add_body_p("• Tổ Hành chính - Tổng hợp: 16 người (trong đó gồm 03 hợp đồng lao động hỗ trợ, phục vụ: 01 tạp vụ, 02 bảo vệ; cùng các vị trí kế toán, văn thư, tổng hợp);", indent=False)
    add_body_p("• Tổ Đăng ký và Cấp giấy chứng nhận: 42 người (thực hiện nghiệp vụ đăng ký đất đai, cấp Giấy chứng nhận, đăng ký giao dịch bảo đảm);", indent=False)
    add_body_p("• Tổ Kỹ thuật địa chính: 24 người (thực hiện nghiệp vụ đo đạc, kiểm tra bản trích đo địa chính, trích lục hồ sơ kỹ thuật).", indent=False)

    add_heading_2("2. Phòng làm việc và phòng chuyên dụng")
    add_body_p("a) Hiện trạng công trình xây dựng tại số 358 Huỳnh Văn Cù:")
    add_body_p("Căn cứ Biên bản bàn giao, tiếp nhận tài sản công ngày 09 tháng 5 năm 2019, toàn bộ khối công trình xây dựng hiện hữu tại số 358 Huỳnh Văn Cù gồm 05 khối nhà với tổng diện tích sàn xây dựng thực tế là 835,30 m², cụ thể như sau:")

    # Table of Building Blocks
    tbl_blocks = doc.add_table(rows=1, cols=5)
    tbl_blocks.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_blocks.autofit = False
    set_table_borders(tbl_blocks, color="000000", sz="4")

    col_w_b = [Inches(0.6), Inches(2.5), Inches(1.0), Inches(1.1), Inches(1.3)]
    for i, w in enumerate(col_w_b):
        tbl_blocks.rows[0].cells[i].width = w

    hdr_b = ["STT", "Danh mục khối công trình", "Số tầng", "Diện tích sàn (m²)", "Hiện trạng bố trí sử dụng"]
    for i, h in enumerate(hdr_b):
        c = tbl_blocks.rows[0].cells[i]
        c.text = h
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            run.font.bold = True
    make_row_header(tbl_blocks.rows[0])

    blocks_data = [
        ("1", "Khối nhà trụ sở chính", "02 tầng", "548,20", "Tầng 1: 274,10 m²; Tầng 2: 274,10 m² (Bố trí phòng BGĐ, các tổ chuyên môn)"),
        ("2", "Khối nhà Bộ phận Một cửa", "01 tầng", "69,90", "Bộ phận Một cửa tiếp nhận hồ sơ (26 m²) và bộ phận xử lý hồ sơ"),
        ("3", "Khối nhà Ban chỉ huy Quân sự cũ", "01 tầng", "81,50", "Bố trí bộ phận đo đạc, kỹ thuật địa chính"),
        ("4", "Hội trường", "01 tầng", "117,60", "Bố trí phòng họp chuyên môn kết hợp tiếp công dân (26 m²) và hội trường chung"),
        ("5", "Nhà vệ sinh (Toilet)", "01 tầng", "18,10", "Khu vệ sinh dùng chung toàn cơ quan"),
        ("", "TỔNG CỘNG DIỆN TÍCH SÀN", "", "835,30", "Khối công trình hiện hữu đang sử dụng ổn định")
    ]

    for row_item in blocks_data:
        row = tbl_blocks.add_row()
        make_row_cant_split(row)
        for i, w in enumerate(col_w_b):
            row.cells[i].width = w
        for c_i, val in enumerate(row_item):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if c_i in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_i == 3:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if val and val[0].isdigit() else WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
                if row_item[0] == "":
                    run.font.bold = True

    add_body_p("b) Thống kê diện tích bố trí các phòng, tổ chuyên môn và diện tích dùng chung:")
    add_body_p("Theo thuyết minh tại Công văn số 1656/CN23-HCTH ngày 21/7/2026, cơ cấu bố trí diện tích sàn thực tế như sau:")
    add_body_p("- Tổng diện tích làm việc bố trí cho 85 chức danh: 535,30 m² (gồm diện tích ngồi làm việc của Ban Giám đốc 03 người, viên chức các tổ chuyên môn 79 người và hợp đồng phục vụ 03 người).")
    add_body_p("- Diện tích các hạng mục sử dụng chung cố định được tách bạch gồm: Bộ phận Một cửa tiếp nhận và trả kết quả: 26,00 m²; Phòng họp chuyên môn kết hợp tiếp công dân: 26,00 m²; Phòng máy chủ và thiết bị CNTT: 15,00 m²; Khu vực sảnh, hành lang, cầu thang, nhà vệ sinh và diện tích PCCC: 123,30 m² (Tổng diện tích dùng chung thực tế: 190,30 m²).")
    add_body_p("Ghi chú đối với bảng thống kê chi tiết từng phòng: Do cơ sở nhà đất tiếp nhận nguyên trạng từ trụ sở UBND xã/phường cũ năm 2019, hồ sơ bàn giao không có bản vẽ hoàn công chi tiết diện tích từng phòng riêng lẻ của các chức danh (diện tích riêng phòng Giám đốc, các Phó Giám đốc, các Tổ nghiệp vụ chưa có số liệu đo đạc bóc tách chính thức, chỉ có tổng diện tích sàn các khối công trình 835,30 m² và tổng diện tích bố trí chức danh 535,30 m²). Đơn vị để trống số liệu phân tách này và sẽ cập nhật chính xác sau khi hoàn thành công tác đo đạc hiện trạng chi tiết.")

    add_body_p("c) Khu vực kho lưu trữ hồ sơ địa chính:")
    add_body_p("- Kho lưu trữ tại trụ sở 358 Huỳnh Văn Cù: Chi nhánh bố trí diện tích kho lưu trữ gồm 391,00 m² sàn (kho lưu trữ hồ sơ địa chính hiện hữu năm 2019) và 15,00 m² sàn (kho lưu trữ hồ sơ tiếp nhận sau sáp nhập năm 2025 tận dụng góc hành lang phòng làm việc), tổng diện tích là 406,00 m² sàn. Hiện tại kho đã chứa đầy 100% công suất tải, hồ sơ phát sinh chưa chỉnh lý khoảng 30% đang phải để tạm tại các phòng làm việc.")
    add_body_p("- Nhu cầu diện tích kho bảo quản hồ sơ chuyên dùng theo quy định tại Thông tư số 09/2007/TT-BNV là từ 500 m² đến 600 m² và diện tích xử lý nghiệp vụ lưu trữ khoảng 250 m² đến 300 m².")

    add_body_p("d) Diện tích nhà để xe và cơ cấu sử dụng mặt bằng khuôn viên đất:")
    add_body_p("- Diện tích nhà để xe: Nhà để xe hiện hữu có mái che trong khuôn viên trụ sở số 358 Huỳnh Văn Cù là 200,00 m², phục vụ nhu cầu để xe của 85 cán bộ nhân viên và người dân đến giải quyết thủ tục hành chính. Đây là hạng mục phụ trợ ngoài nhà, không tính vào diện tích sàn thông thủy của các khối nhà làm việc theo quy định tại Khoản 3 Điều 3 Nghị định số 155/2025/NĐ-CP.")
    add_body_p("- Bóc tách cơ cấu sử dụng tổng thể khuôn viên đất 1.417,70 m²: Toàn bộ khuôn viên đất tại số 358 Huỳnh Văn Cù có diện tích 1.417,70 m² được phân bổ rành mạch gồm: (1) Diện tích sàn xây dựng các khối nhà làm việc là 835,30 m²; (2) Diện tích nhà để xe có mái che là 200,00 m² (tổng diện tích xây dựng có mái che trên đất là 1.035,30 m²); (3) Phần chênh lệch 382,40 m² còn lại (1.417,70 m² - 1.035,30 m²) là diện tích đất sân bãi bê tông, đường giao thông nội bộ, bồn hoa cây xanh và khoảng lùi thông gió, hành lang an toàn phòng cháy chữa cháy ngoài trời. Phần diện tích 382,40 m² này hoàn toàn là sân bãi ngoài trời, không phải diện tích phòng làm việc và không phải diện tích sử dụng chung trong nhà.")

    # 6. IV. DANH MỤC TÀI SẢN
    add_heading_1("IV. Danh mục tài sản")
    add_heading_2("1. Về đất đai (Tổng diện tích: 2.693,90 m²)")
    add_body_p("• Cơ sở nhà, đất số 1 (Hiện hữu đang quản lý, sử dụng): Địa chỉ tại số 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh. Diện tích đất thực tế đang quản lý, sử dụng ổn định là 1.417,70 m² (theo Biên bản bàn giao ngày 09/5/2019 ghi nhận tạm tính là 1.404,10 m²; diện tích sử dụng ổn định theo rà soát thực tế là 1.417,70 m²).")
    add_body_p("• Cơ sở nhà, đất số 2 (Đề nghị tiếp nhận điều chuyển): Địa chỉ tại Điểm trạm y tế 3 (Trạm Y tế phường Chánh Mỹ cũ), tọa lạc trên đường Huỳnh Văn Cù, khu phố Chánh Lộc 7, phường Thủ Dầu Một, Thành phố Hồ Chí Minh (liền kề cơ sở số 358 Huỳnh Văn Cù). Diện tích khuôn viên đất là 1.276,20 m² hiện đang bỏ trống, không có nhu cầu sử dụng.")

    add_heading_2("2. Về nhà và công trình xây dựng")
    add_body_p("• Tại cơ sở số 358 Huỳnh Văn Cù: Tổng diện tích sàn xây dựng thực tế là 835,30 m². Công trình cấp III, kết cấu khung, sàn, mái bê tông cốt thép, tường xây gạch; gồm 05 khối nhà như đã thống kê tại Mục III. Hiện trạng công trình đã qua sử dụng nhiều năm, một số hạng mục xuống cấp cần được duy tu, bảo dưỡng định kỳ.")
    add_body_p("• Tại cơ sở Điểm trạm y tế 3 (cũ): Gồm khối nhà làm việc trạm y tế trước đây. Hiện trạng: Đang bỏ trống. Diện tích sàn xây dựng: ... m² (Hồ sơ pháp lý kèm theo Tờ trình 195/TTr-TYT và 427/TTr-TYT chưa có biên bản đo đạc chi tiết diện tích sàn xây dựng khối nhà, chỉ ghi nhận diện tích khuôn viên đất 1.276,20 m²; đơn vị để trống và kiến nghị đo đạc xác định chính xác khi tiến hành bàn giao). Cấp nhà: Cấp ...; Hiện trạng kỹ thuật: Cần cải tạo sửa chữa để chuyển đổi công năng làm kho lưu trữ chuyên ngành.")

    add_heading_2("3. Đánh giá hiện trạng tài sản")
    add_body_p("Qua rà soát hồ sơ quản lý tài sản và kiểm tra thực tế, toàn bộ cơ sở nhà, đất tại số 358 Huỳnh Văn Cù đang được Chi nhánh quản lý, sử dụng đúng mục đích làm trụ sở cơ quan hành chính nhà nước; tuyệt đối không có hiện tượng sử dụng sai mục đích, cho thuê, cho mượn hoặc liên doanh, liên kết trái quy định pháp luật.")
    add_body_p("Cơ sở Điểm trạm y tế 3 do Ủy ban nhân dân phường Thủ Dầu Một quản lý (Trạm Y tế phường trực tiếp theo dõi) hiện không còn nhu cầu sử dụng, đang để trống. Việc tiếp nhận điều chuyển cơ sở này sang Chi nhánh số 23 để làm kho lưu trữ chuyên ngành đảm bảo tính liên kết vị trí (liền kề trụ sở chính), tối ưu hóa hiệu quả sử dụng tài sản nhà nước, tránh lãng phí đất công theo đúng tinh thần chỉ đạo tại Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP.")

    # 7. V. PHƯƠNG ÁN SỬ DỤNG VÀ QUẢN LÝ
    add_heading_1("V. Phương án sử dụng tài sản và quản lý sau khi tiếp nhận")
    add_heading_2("1. Phương án sử dụng tài sản")
    add_body_p("Sau khi có Quyết định điều chuyển tài sản công của Ủy ban nhân dân Thành phố Hồ Chí Minh và hoàn thành công tác bàn giao tiếp nhận, phương án phân bổ sử dụng cụ thể như sau:")
    add_body_p("- Cơ sở số 358 Huỳnh Văn Cù (đất 1.417,70 m²; sàn 835,30 m²): Tiếp tục duy trì làm Văn phòng làm việc hành chính tập trung của Chi nhánh số 23; bố trí phòng làm việc cho Ban Giám đốc và các tổ chuyên môn nghiệp vụ; bố trí Bộ phận tiếp nhận và trả kết quả thủ tục hành chính hiện đại; phòng tiếp dân; phòng máy chủ CNTT và khu vực nhà để xe phục vụ cán bộ nhân viên và nhân dân.")
    add_body_p("- Cơ sở Điểm trạm y tế 3 (khuôn viên đất 1.276,20 m² liền kề): Sử dụng để cải tạo, nâng cấp thành Hệ thống Kho lưu trữ hồ sơ địa chính chuyên ngành tập trung của Chi nhánh số 23; lắp đặt hệ thống giá kệ lưu trữ đạt chuẩn, trang thiết bị phòng cháy chữa cháy, kiểm soát nhiệt độ, độ ẩm và bố trí khu vực kỹ thuật xử lý nghiệp vụ lưu trữ (phân loại, bóc tách, chỉnh lý, số hóa hồ sơ địa chính).")

    add_heading_2("2. Phương án quản lý, sử dụng tài sản sau tiếp nhận")
    add_body_p("Sau khi hoàn thành tiếp nhận, Chi nhánh số 23 có trách nhiệm:")
    add_body_p("• Quản lý, sử dụng tài sản đúng mục đích, đúng công năng và đúng tiêu chuẩn định mức quy định tại Luật Quản lý, sử dụng tài sản công, Nghị định số 155/2025/NĐ-CP, Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP.")
    add_body_p("• Thực hiện đầy đủ quy trình hạch toán kế toán, đăng ký quyền quản lý sử dụng và cập nhật thông tin tài sản vào Cơ sở dữ liệu quốc gia về tài sản công theo quy định.")
    add_body_p("• Tổ chức kiểm kê định kỳ hàng năm; lập kế hoạch bảo trì, bảo dưỡng, sửa chữa cơ sở vật chất thường xuyên; bảo đảm an toàn tuyệt đối về phòng cháy chữa cháy và an ninh trật tự.")
    add_body_p("• Tuyệt đối không sử dụng tài sản vào mục đích kinh doanh, cho thuê, cho mượn, liên doanh, liên kết khi chưa được cấp có thẩm quyền phê duyệt.")

    # 8. VI. ĐÁNH GIÁ HIỆU QUẢ
    add_heading_1("VI. Đánh giá hiệu quả của phương án")
    add_body_p("• Về chuyên môn, nghiệp vụ: Giải quyết triệt để bài toán thiếu hụt diện tích kho lưu trữ chuyên dụng; bảo vệ an toàn tuyệt đối cho khối tài liệu địa chính gốc quốc gia; đưa toàn bộ hồ sơ lưu tạm ra khỏi các phòng làm việc, trả lại môi trường làm việc thông thoáng, đúng quy chuẩn cho cán bộ nhân viên.")
    add_body_p("• Về kinh tế - xã hội và quản lý tài sản công: Khai thác tối ưu và xử lý dứt điểm cơ sở nhà đất công dôi dư đang bỏ trống; chấm dứt nguy cơ lãng phí tài sản nhà nước; tiết kiệm ngân sách nhà nước do không phải bố trí kinh phí thuê mặt bằng kho ngoài hoặc đầu tư xây dựng mới trụ sở; thực hiện đúng tinh thần tháo gỡ vướng mắc, sắp xếp tài sản công theo Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP.")
    add_body_p("• Về phục vụ nhân dân và cải cách TTHC: Việc đặt kho lưu trữ ngay liền kề khối nhà hành chính tạo liên kết hữu cơ thuận lợi, giúp cán bộ rút ngắn thời gian tra cứu, trích lục hồ sơ địa chính phục vụ công tác cấp Giấy chứng nhận và đăng ký giao dịch bảo đảm, nâng cao tỷ lệ giải quyết hồ sơ đúng hạn và trước hạn cho người dân và doanh nghiệp.")

    # 9. VII. KIẾN NGHỊ
    add_heading_1("VII. Kiến nghị")
    add_body_p("Từ các căn cứ pháp lý, thực trạng hạ tầng và kết quả đối chiếu tiêu chuẩn định mức nêu trên, Chi nhánh Văn phòng Đăng ký đất đai số 23 kính đề nghị:")
    add_body_p("1. Kính trình Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, tổng hợp báo cáo Sở Nông nghiệp và Môi trường tham mưu Ủy ban nhân dân Thành phố Hồ Chí Minh ban hành Quyết định điều chuyển tài sản công đối với cơ sở Điểm trạm y tế 3 (Trạm Y tế phường Chánh Mỹ cũ), diện tích đất 1.276,20 m² tọa lạc tại đường Huỳnh Văn Cù, khu phố Chánh Lộc 7, phường Thủ Dầu Một từ Ủy ban nhân dân phường Thủ Dầu Một sang Sở Nông nghiệp và Môi trường để giao cho Chi nhánh Văn phòng Đăng ký đất đai số 23 trực tiếp quản lý, sử dụng làm kho lưu trữ hồ sơ địa chính chuyên ngành.")
    add_body_p("2. Đề nghị Ủy ban nhân dân phường Thủ Dầu Một tiếp tục phối hợp, hoàn tất các hồ sơ thủ tục điều chuyển tài sản công theo đúng quy định tại Nghị định số 186/2025/NĐ-CP và Nghị định số 286/2025/NĐ-CP.")
    add_body_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 cam kết sau khi được bàn giao tiếp nhận sẽ quản lý, khai thác sử dụng cơ sở nhà, đất đúng mục đích, đúng quy chuẩn định mức của Nhà nước, bảo đảm an toàn, tiết kiệm và hiệu quả cao nhất.")

    # 10. CHỮ KÝ & NƠI NHẬN (MẪU 1.4 NGHỊ ĐỊNH 30 - BORDERLESS TABLE)
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    tbl_sig.rows[0].cells[0].width = Inches(3.25)
    tbl_sig.rows[0].cells[1].width = Inches(3.25)

    # Cột trái: Nơi nhận (Ô 9b)
    c_noi_nhan = tbl_sig.rows[0].cells[0]
    p_nn = c_noi_nhan.paragraphs[0]
    p_nn.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_nn.paragraph_format.line_spacing = 1.15
    p_nn.paragraph_format.space_after = Pt(2)
    
    r_nn_t = p_nn.add_run("Nơi nhận:\n")
    r_nn_t.font.name = "Times New Roman"
    r_nn_t.font.size = Pt(12)
    r_nn_t.font.bold = True
    r_nn_t.font.italic = True

    nn_items = [
        "- Văn phòng Đăng ký đất đai TP.HCM (để b/c);",
        "- UBND phường Thủ Dầu Một;",
        "- Ban Giám đốc Chi nhánh;",
        "- Các Tổ chuyên môn, bộ phận;",
        "- Lưu: VT, HCTH."
    ]
    for item in nn_items:
        r_item = p_nn.add_run(item + "\n")
        r_item.font.name = "Times New Roman"
        r_item.font.size = Pt(11)

    # Cột phải: Thẩm quyền & Người ký (Ô 7a, 7b, 7c)
    c_ky = tbl_sig.rows[0].cells[1]
    p_ky = c_ky.paragraphs[0]
    p_ky.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ky.paragraph_format.line_spacing = 1.15
    p_ky.paragraph_format.space_after = Pt(2)

    r_tm = p_ky.add_run("KT. GIÁM ĐỐC\nPHÓ GIÁM ĐỐC\n\n\n\n\n")
    r_tm.font.name = "Times New Roman"
    r_tm.font.size = Pt(13)
    r_tm.font.bold = True

    r_ten = p_ky.add_run("Đặng Huy Cường")
    r_ten.font.name = "Times New Roman"
    r_ten.font.size = Pt(13)
    r_ten.font.bold = True

    set_table_borderless(tbl_sig)

    # ==========================================
    # SECTION 2: PHỤ LỤC BẢNG ĐỐI CHIẾU (LANDSCAPE A4)
    # ==========================================
    sec2 = doc.add_section()
    sec2.orientation = WD_ORIENT.LANDSCAPE
    sec2.page_width = Inches(11.69)  # 297mm
    sec2.page_height = Inches(8.27)  # 210mm
    # Can le Landscape can doi
    sec2.top_margin = Inches(0.60)   # 15mm
    sec2.bottom_margin = Inches(0.60)# 15mm
    sec2.left_margin = Inches(0.79)  # 20mm
    sec2.right_margin = Inches(0.59) # 15mm
    add_page_number_to_section(sec2)

    # Header Phụ lục theo Mẫu 2.1 Nghị định 30
    p_pl_title = doc.add_paragraph()
    p_pl_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pl_title.paragraph_format.space_before = Pt(0)
    p_pl_title.paragraph_format.space_after = Pt(2)
    r_pl1 = p_pl_title.add_run("Phụ lục\n")
    r_pl1.font.name = "Times New Roman"
    r_pl1.font.size = Pt(14)
    r_pl1.font.bold = True

    r_pl2 = p_pl_title.add_run("BẢNG ĐỐI CHIẾU NHU CẦU DIỆN TÍCH VĂN PHÒNG LÀM VIỆC VÀ KHO LƯU TRỮ\nCẦN THIẾT THEO TIÊU CHUẨN ĐỊNH MỨC NHÀ NƯỚC\n")
    r_pl2.font.name = "Times New Roman"
    r_pl2.font.size = Pt(13)
    r_pl2.font.bold = True

    r_pl3 = p_pl_title.add_run("(Kèm theo Phương án số        /PA-CN23 ngày      tháng      năm 2026\ncủa Chi nhánh Văn phòng Đăng ký đất đai số 23)")
    r_pl3.font.name = "Times New Roman"
    r_pl3.font.size = Pt(13)
    r_pl3.font.italic = True

    p_tbl_bases = doc.add_paragraph()
    p_tbl_bases.paragraph_format.space_before = Pt(4)
    p_tbl_bases.paragraph_format.space_after = Pt(6)
    p_tbl_bases.paragraph_format.line_spacing = 1.15
    r_b_text = p_tbl_bases.add_run(
        "- Căn cứ định mức tại Nghị định số 155/2025/NĐ-CP ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;\n"
        "- Căn cứ Nghị định số 186/2025/NĐ-CP ngày 01 tháng 7 năm 2025 và Nghị định số 286/2025/NĐ-CP ngày 03 tháng 11 năm 2025 của Chính phủ sửa đổi, bổ sung một số điều của các Nghị định trong lĩnh vực quản lý, sử dụng tài sản công;\n"
        "- Căn cứ Thông tư số 09/2007/TT-BNV ngày 26 tháng 11 năm 2007 của Bộ Nội vụ hướng dẫn kho lưu trữ chuyên dùng;\n"
        "- Căn cứ Tiêu chuẩn quốc gia TCVN 4319:2012 về Nhà và công trình công cộng - Nguyên tắc cơ bản để thiết kế;\n"
        "- Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh."
    )
    r_b_text.font.name = "Times New Roman"
    r_b_text.font.size = Pt(9.5)
    r_b_text.font.italic = True

    # Main Appendix Table
    tbl_app = doc.add_table(rows=2, cols=7)
    tbl_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_app.autofit = False
    set_table_borders(tbl_app, color="000000", sz="4")

    col_widths_app = [
        Inches(0.55), # STT
        Inches(3.35), # Chỉ tiêu
        Inches(1.10), # Hiện trạng
        Inches(1.05), # Số người / mét TL
        Inches(1.15), # Định mức NN
        Inches(1.05), # So sánh
        Inches(2.05)  # Ghi chú
    ]

    for r in tbl_app.rows:
        for i, w in enumerate(col_widths_app):
            r.cells[i].width = w

    r0 = tbl_app.rows[0]
    r1 = tbl_app.rows[1]

    # Header Row 0 & 1 with merges
    c_stt = r0.cells[0].merge(r1.cells[0])
    c_stt.text = "STT"

    c_ct = r0.cells[1].merge(r1.cells[1])
    c_ct.text = "Chỉ tiêu"

    c_ht = r0.cells[2].merge(r1.cells[2])
    c_ht.text = "Hiện trạng\ndiện tích (m²)"

    c_nc = r0.cells[3].merge(r0.cells[4])
    c_nc.text = "Nhu cầu diện tích sàn"

    r1.cells[3].text = "Số người\nhoặc số mét\ntài liệu"
    r1.cells[4].text = "Diện tích cần\nthiết theo định\nmức Nhà nước (m²)"

    c_ss = r0.cells[5].merge(r1.cells[5])
    c_ss.text = "So sánh:\nHiện trạng -\nNhu cầu (m²)"

    c_gc = r0.cells[6].merge(r1.cells[6])
    c_gc.text = "Ghi chú: định mức\nNhà nước quy định"

    for r in [r0, r1]:
        make_row_header(r)
        for c in r.cells:
            set_cell_margins(c, top=80, bottom=80, left=60, right=60)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(9.5)
                    run.font.bold = True

    data_appendix = [
        # A. HIỆN TRẠNG NHÀ, ĐẤT ĐANG SỬ DỤNG VÀ ĐỀ NGHỊ TIẾP NHẬN
        {
            "stt": "A",
            "chỉ_tiêu": "HIỆN TRẠNG NHÀ, ĐẤT ĐANG SỬ DỤNG VÀ ĐỀ NGHỊ TIẾP NHẬN",
            "ht": "", "sl": "", "dm": "", "ss": "", "gc": "",
            "bold": True, "align_left": True, "bg": "F2F2F2"
        },
        {
            "stt": "1",
            "chỉ_tiêu": "Cơ sở hiện hữu: Số 358 Huỳnh Văn Cù, P. Thủ Dầu Một\n- Diện tích đất: 1.417,70 m²\n- Diện tích sàn xây dựng: 835,30 m²\n- Cấp nhà: Cấp III, kết cấu khung, sàn BTCT, tường gạch",
            "ht": "835,30",
            "sl": "85",
            "dm": "2.331,00",
            "ss": "-1.495,70",
            "gc": "Biên bản bàn giao ngày 09/5/2019; thực tế mới đáp ứng 35,83% định mức.",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "2",
            "chỉ_tiêu": "Cơ sở đề nghị điều chuyển: Điểm trạm y tế 3 (P. Chánh Mỹ cũ)\n- Vị trí: Đường Huỳnh Văn Cù (liền kề số 358)\n- Diện tích khuôn viên đất: 1.276,20 m²\n- Diện tích sàn xây dựng: ... m² (chưa đo bóc tách)",
            "ht": "1.276,20 (đất)",
            "sl": "-",
            "dm": "1.276,20",
            "ss": "0,00",
            "gc": "Tờ trình 195, 427 của Trạm Y tế và CV 1136 của UBND phường. Đang bỏ trống.",
            "bold": False, "align_left": True, "bg": None
        },

        # B. DIỆN TÍCH SÀN LÀM VIỆC
        {
            "stt": "B",
            "chỉ_tiêu": "DIỆN TÍCH SÀN LÀM VIỆC THEO TIÊU CHUẨN ĐỊNH MỨC NGHỊ ĐỊNH 155/2025/NĐ-CP",
            "ht": "835,30",
            "sl": "85",
            "dm": "2.331,00",
            "ss": "-1.495,70",
            "gc": "Tổng nhu cầu định mức theo Nghị định số 155/2025/NĐ-CP",
            "bold": True, "align_left": True, "bg": "F2F2F2"
        },
        {
            "stt": "1",
            "chỉ_tiêu": "Diện tích làm việc của các chức danh (85 người):",
            "ht": "535,30",
            "sl": "85",
            "dm": "1.260,00",
            "ss": "-724,70",
            "gc": "Phụ lục II Nghị định số 155/2025/NĐ-CP ngày 16/6/2025 của Chính phủ",
            "bold": True, "align_left": True, "bg": None
        },
        {
            "stt": "1.1",
            "chỉ_tiêu": "Ban Giám đốc Chi nhánh: 03 người",
            "ht": "60,00",
            "sl": "03",
            "dm": "60,00",
            "ss": "0,00",
            "gc": "Định mức tối đa 20 m²/người",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "1.2",
            "chỉ_tiêu": "Chuyên viên và các chức danh tương đương: 79 người\n(Gồm 42 viên chức chuyên ngành + 37 chuyên viên dùng chung)",
            "ht": "445,30",
            "sl": "79",
            "dm": "1.185,00",
            "ss": "-739,70",
            "gc": "Định mức tối đa 15 m²/người (Số thứ tự 9, Phụ lục II)",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "1.3",
            "chỉ_tiêu": "Cá nhân ký hợp đồng lao động phục vụ: 03 người\n(01 nhân viên phục vụ, 02 nhân viên bảo vệ)",
            "ht": "30,00",
            "sl": "03",
            "dm": "30,00",
            "ss": "0,00",
            "gc": "Định mức tối đa 10 m²/người (Số thứ tự 10, Phụ lục II)",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "",
            "chỉ_tiêu": "Cộng diện tích làm việc của chức danh:",
            "ht": "535,30",
            "sl": "85",
            "dm": "1.260,00",
            "ss": "-724,70",
            "gc": "1.230 m² + 30 m² = 1.260,00 m²",
            "bold": True, "align_left": True, "bg": None
        },
        {
            "stt": "2",
            "chỉ_tiêu": "Diện tích sử dụng chung toàn trụ sở gồm:\n- Bộ phận Một cửa tiếp nhận và trả kết quả: 26,00 m²\n- Phòng họp chuyên môn kết hợp tiếp dân: 26,00 m²\n- Phòng máy chủ, CNTT: 15,00 m²\n- Sảnh, hành lang, cầu thang, khu vệ sinh, PCCC: 123,30 m²",
            "ht": "190,30",
            "sl": "-",
            "dm": "1.071,00",
            "ss": "-880,70",
            "gc": "Khoản 2 Điều 6 Nghị định 155: Tối đa không quá 85% diện tích chức danh (1.260 × 85% = 1.071 m²)",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "3",
            "chỉ_tiêu": "Diện tích nhà để xe (Công trình ngoài nhà):\n(Đáp ứng nhu cầu cho 85 CBCNV và khách liên hệ giải quyết TTHC)",
            "ht": "200,00",
            "sl": "85 người\n+ khách",
            "dm": "350,00",
            "ss": "-150,00",
            "gc": "Khoản 3 Điều 3 NĐ 155 và TCVN 4319:2012 (Mô tô 3 m²/xe; ô tô 25 m²/xe). Không tính vào diện tích sàn thông thủy.",
            "bold": False, "align_left": True, "bg": None
        },

        # C. DIỆN TÍCH LƯU TRỮ VÀ XỬ LÝ NGHIỆP VỤ LƯU TRỮ
        {
            "stt": "C",
            "chỉ_tiêu": "DIỆN TÍCH KHO LƯU TRỮ VÀ XỬ LÝ NGHIỆP VỤ HỒ SƠ ĐỊA CHÍNH",
            "ht": "406,00",
            "sl": ">3.000m TL",
            "dm": "1.000,00",
            "ss": "-594,00",
            "gc": "Căn cứ Thông tư số 09/2007/TT-BNV hướng dẫn kho lưu trữ chuyên dùng",
            "bold": True, "align_left": True, "bg": "F2F2F2"
        },
        {
            "stt": "1",
            "chỉ_tiêu": "Diện tích sàn kho bảo quản hồ sơ địa chính gốc:\n- Hiện trạng kho tại 358 Huỳnh Văn Cù: 406,00 m² (kho 2019: 391 m² + kho 2025: 15 m² lấp kín 100%)\n- Nhu cầu kho bảo quản hồ sơ biến động tích lũy và phát sinh",
            "ht": "406,00",
            "sl": ">3.000m\ngiá tài liệu",
            "dm": "600,00",
            "ss": "-194,00",
            "gc": "Thông tư 09/2007/TT-BNV: Kho lưu trữ loại 3 và loại 4 diện tích 500 - 936 m².",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "2",
            "chỉ_tiêu": "Khu vực xử lý nghiệp vụ lưu trữ:\n(Tiếp nhận, phân loại, bóc tách, chỉnh lý, khử trùng, số hóa hồ sơ)",
            "ht": "0,00",
            "sl": "-",
            "dm": "300,00",
            "ss": "-300,00",
            "gc": "Thông tư 09/2007/TT-BNV: Bố trí bằng 50% diện tích sàn kho bảo quản tài liệu.",
            "bold": False, "align_left": True, "bg": None
        },
        {
            "stt": "3",
            "chỉ_tiêu": "Cơ sở đề xuất giải quyết kho lưu trữ:\nTiếp nhận điều chuyển Điểm trạm y tế 3 dôi dư liền kề (1.276,20 m² đất)",
            "ht": "1.276,20 (đất)",
            "sl": "-",
            "dm": "1.276,20",
            "ss": "Đạt",
            "gc": "Tối ưu hóa tài sản công dôi dư theo NĐ 186/2025/NĐ-CP và NĐ 286/2025/NĐ-CP.",
            "bold": False, "align_left": True, "bg": None
        },

        # TỔNG CỘNG ĐỐI CHIẾU TOÀN TRỤ SỞ
        {
            "stt": "",
            "chỉ_tiêu": "TỔNG CỘNG ĐỐI CHIẾU TOÀN TRỤ SỞ (B + C)",
            "ht": "835,30",
            "sl": "85 người",
            "dm": "2.331,00",
            "ss": "-1.495,70",
            "gc": "Hiện trạng mới chỉ đáp ứng 35,83% nhu cầu định mức. Căn cứ bắt buộc phải bổ sung kho Điểm trạm y tế 3.",
            "bold": True, "align_left": True, "bg": "E8EEF5"
        }
    ]

    for row_info in data_appendix:
        new_row = tbl_app.add_row()
        make_row_cant_split(new_row)
        
        for i, w in enumerate(col_widths_app):
            new_row.cells[i].width = w
            
        vals = [
            row_info["stt"],
            row_info["chỉ_tiêu"],
            row_info["ht"],
            row_info["sl"],
            row_info["dm"],
            row_info["ss"],
            row_info["gc"]
        ]
        
        for c_idx, text in enumerate(vals):
            cell = new_row.cells[c_idx]
            cell.text = text
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            if row_info.get("bg"):
                set_cell_background(cell, row_info["bg"])
                
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif c_idx in [2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if (text and any(ch.isdigit() for ch in text)) else WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for r_item in p.runs:
                r_item.font.name = "Times New Roman"
                r_item.font.size = Pt(9.5)
                if row_info["bold"]:
                    r_item.font.bold = True

    # Chữ ký cuối Phụ lục
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(12)
    p_sp.paragraph_format.space_after = Pt(0)

    tbl_pl_sig = doc.add_table(rows=1, cols=2)
    tbl_pl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pl_sig.autofit = False
    tbl_pl_sig.rows[0].cells[0].width = Inches(5.0)
    tbl_pl_sig.rows[0].cells[1].width = Inches(5.0)

    c_pl1 = tbl_pl_sig.rows[0].cells[0]
    p_k1 = c_pl1.paragraphs[0]
    p_k1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_k1 = p_k1.add_run("NGƯỜI LẬP BẢNG\n\n\n\n\nNguyễn Thị Bích Tuyền")
    r_k1.font.name = "Times New Roman"
    r_k1.font.size = Pt(11)
    r_k1.font.bold = True

    c_pl2 = tbl_pl_sig.rows[0].cells[1]
    p_k2 = c_pl2.paragraphs[0]
    p_k2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_k2 = p_k2.add_run("KT. GIÁM ĐỐC\nPHÓ GIÁM ĐỐC\n\n\n\n\nĐặng Huy Cường")
    r_k2.font.name = "Times New Roman"
    r_k2.font.size = Pt(11)
    r_k2.font.bold = True

    set_table_borderless(tbl_pl_sig)

    # LƯU FILE KẾT QUẢ VÀO OUTPUT THEO QUY ĐỊNH
    out_file1 = "OUTPUT/phuong_an_cn23_new.docx"
    doc.save(out_file1)
    print(f"SUCCESS: Đã tạo file kết quả chuẩn NĐ 30 tại: {out_file1}")

    # Đồng thời lưu một bản tên rõ ràng
    out_file2 = "OUTPUT/Phuong_an_CN23_new_ND30.docx"
    doc.save(out_file2)
    print(f"SUCCESS: Đã lưu bản đối chiếu tại: {out_file2}")

if __name__ == "__main__":
    main()
