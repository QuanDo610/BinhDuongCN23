import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_formatted_totrinh():
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

    # 3. Base style
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

    # Helper function to set cell box borders
    def set_cell_box_borders(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>' % nsdecls('w'))
        tcPr.append(tcBorders)

    # ==========================================
    # HEADER CƠ QUAN VÀ QUỐC HIỆU (BẢNG 2 CỘT KHÔNG VIỀN)
    # ==========================================
    t_header = doc.add_table(rows=1, cols=2)
    t_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_header.autofit = False
    remove_table_borders(t_header)

    t_header.rows[0].cells[0].width = Inches(2.8)
    t_header.rows[0].cells[1].width = Inches(3.7)
    set_cell_margins(t_header.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_header.rows[0].cells[1], 0, 0, 0, 0)

    c0 = t_header.rows[0].cells[0]
    c1 = t_header.rows[0].cells[1]

    # Bên trái: Cơ quan
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
    r = p_so.add_run("Số:        /TTr-CN23")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

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
    r = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày 07 tháng 10 năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # TIÊU ĐỀ TỜ TRÌNH
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("TỜ TRÌNH")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.15
    r = p_sub.add_run("Về việc đề xuất đăng ký sử dụng thông tin dữ liệu đo đạc và bản đồ\nnhằm cung cấp thông tin dữ liệu thu nhận từ mạng lưới trạm định vị vệ tinh\nquốc gia về dữ liệu đo đạc thời gian thực (RTK) để phục vụ công tác đo đạc, lập bản đồ")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)

    p_line_ty = doc.add_paragraph()
    p_line_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_ty.paragraph_format.space_before = Pt(0)
    p_line_ty.paragraph_format.space_after = Pt(12)
    r = p_line_ty.add_run("————————————")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    # Kính gửi
    p_kg = doc.add_paragraph()
    p_kg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kg.paragraph_format.space_before = Pt(4)
    p_kg.paragraph_format.space_after = Pt(10)
    r_kg_label = p_kg.add_run("Kính gửi: ")
    r_kg_label.bold = True
    r_kg_label.font.name = "Times New Roman"
    r_kg_label.font.size = Pt(13)
    r_kg_to = p_kg.add_run("Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh.")
    r_kg_to.bold = True
    r_kg_to.font.name = "Times New Roman"
    r_kg_to.font.size = Pt(13)

    # Helper function for text
    def add_p(text, indent=True, italic=False, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.45)
        r = p.add_run(text)
        r.italic = italic
        r.bold = bold
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        return p

    def add_heading_section(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.45)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    # 1. Căn cứ pháp lý
    add_heading_section("1. Căn cứ pháp lý thực hiện:")
    add_p("Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23 trực thuộc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh;", italic=True)
    add_p("Căn cứ Thông tư số 47/2024/TT-BTC ngày 10 tháng 7 năm 2024 của Bộ Tài chính quy định mức thu, chế độ thu, nộp, miễn, quản lý và sử dụng phí khai thác, sử dụng thông tin dữ liệu đo đạc và bản đồ.", italic=True)

    # 2. Nội dung đề xuất
    add_heading_section("2. Nội dung đề xuất:")
    add_p("Hiện nay, Chi nhánh Văn phòng Đăng ký đất đai số 23 sử dụng các thiết bị định vị GNSS/GPS RTK trong quá trình hoạt động đo đạc bản đồ, trích đo địa chính, chỉnh lý biến động đất đai trên địa bàn quản lý. Theo đó, phương pháp đo RTK sử dụng trạm CORS quốc gia như một trạm Base cố định để thu nhận tín hiệu GNSS/GPS, từ đó đưa ra vị trí tọa độ thửa đất một cách nhanh chóng, đồng bộ và chuẩn xác cao.")
    add_p("Theo quy định tại Điều 2 và Biểu mức thu phí ban hành kèm theo Thông tư số 47/2024/TT-BTC ngày 10 tháng 7 năm 2024 của Bộ Tài chính, việc sử dụng dữ liệu đo động thời gian thực (dữ liệu tiếp nhận từ trạm CORS quốc gia) để thực hiện hoạt động đo đạc phải nộp phí với mức thu là 6.750.000 đồng/12 tháng/máy thu.")
    add_p("Căn cứ nhu cầu sử dụng thiết bị định vị GNSS/GPS RTK phục vụ công tác chuyên môn tại đơn vị, Chi nhánh Văn phòng Đăng ký đất đai số 23 xác định có 04 thiết bị sử dụng trạm CORS gần đến thời hạn gia hạn tài khoản dữ liệu với tổng kinh phí đăng ký sử dụng là 27.000.000 đồng (bằng chữ: Hai mươi bảy triệu đồng chẵn).")
    add_p("Danh mục chi tiết 04 thiết bị đăng ký sử dụng dữ liệu cụ thể như sau:")

    # ==========================================
    # BẢNG DANH MỤC THIẾT BỊ (TABLE 2)
    # ==========================================
    t_tb = doc.add_table(rows=1, cols=4)
    t_tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tb.autofit = False

    headers_tb = ["STT", "Loại máy", "Số máy (Serial number)", "Đơn giá (đồng/12 tháng)"]
    widths_tb = [Inches(0.8), Inches(2.2), Inches(2.0), Inches(1.5)]

    for i, h in enumerate(headers_tb):
        c = t_tb.rows[0].cells[i]
        c.width = widths_tb[i]
        set_cell_margins(c, 80, 80, 100, 100)
        set_cell_box_borders(c)
        shading = parse_xml(r'<w:shd %s w:fill="F2F2F2"/>' % nsdecls('w'))
        c._tc.get_or_add_tcPr().append(shading)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    rows_data = [
        ("1", "Trimble DA2", "6430100158", "6.750.000"),
        ("2", "Trimble DA2", "6416100243", "6.750.000"),
        ("3", "Trimble DA2", "6340100189", "6.750.000"),
        ("4", "Trimble DA2", "6416100009", "6.750.000")
    ]

    for r_data in rows_data:
        row = t_tb.add_row()
        for idx, val in enumerate(r_data):
            c = row.cells[idx]
            c.width = widths_tb[idx]
            set_cell_margins(c, 70, 70, 100, 100)
            set_cell_box_borders(c)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            if idx in [0, 1, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

    # Hàng Tổng cộng
    row_tot = t_tb.add_row()
    # Gộp ô 1, 2, 3 thành 1 ô "Tổng cộng"
    # Trong python-docx: cell_a.merge(cell_b)
    c_start = row_tot.cells[0]
    c_mid = row_tot.cells[1]
    c_end = row_tot.cells[2]
    c_merged = c_start.merge(c_end)
    c_merged.width = Inches(5.0)
    set_cell_margins(c_merged, 70, 70, 100, 100)
    set_cell_box_borders(c_merged)
    shading = parse_xml(r'<w:shd %s w:fill="F9F9F9"/>' % nsdecls('w'))
    c_merged._tc.get_or_add_tcPr().append(shading)

    p_tot = c_merged.paragraphs[0]
    p_tot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tot.paragraph_format.space_before = Pt(0)
    p_tot.paragraph_format.space_after = Pt(0)
    r = p_tot.add_run("Tổng cộng")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    c_val = row_tot.cells[1] # Sau khi merge ô 0-2, ô tiếp theo là ô index 1 trong row_tot.cells
    c_val.width = Inches(1.5)
    set_cell_margins(c_val, 70, 70, 100, 100)
    set_cell_box_borders(c_val)
    shading2 = parse_xml(r'<w:shd %s w:fill="F9F9F9"/>' % nsdecls('w'))
    c_val._tc.get_or_add_tcPr().append(shading2)
    p_v = c_val.paragraphs[0]
    p_v.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_v.paragraph_format.space_before = Pt(0)
    p_v.paragraph_format.space_after = Pt(0)
    r = p_v.add_run("27.000.000")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # 3. Kiến nghị đề xuất
    add_heading_section("3. Kiến nghị, đề xuất:")
    add_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 kính đề nghị Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, chỉ đạo việc đăng ký sử dụng thông tin dữ liệu đo đạc và bản đồ nhằm cung cấp thông tin dữ liệu thu nhận từ mạng lưới trạm định vị vệ tinh quốc gia về dữ liệu đo đạc thời gian thực (RTK) cho 04 thiết bị nêu trên để phục vụ kịp thời công tác đo đạc, lập bản đồ và giải quyết thủ tục hành chính cho người dân, doanh nghiệp.")
    add_p("Kính trình Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, giải quyết./.", italic=True)

    # ==========================================
    # KHỐI NƠI NHẬN VÀ CHỮ KÝ (BẢNG 2 CỘT KHÔNG VIỀN)
    # ==========================================
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(8)
    p_space.paragraph_format.space_after = Pt(0)

    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = False
    remove_table_borders(t_sig)

    t_sig.rows[0].cells[0].width = Inches(3.2)
    t_sig.rows[0].cells[1].width = Inches(3.3)
    set_cell_margins(t_sig.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_sig.rows[0].cells[1], 0, 0, 0, 0)

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
        "- Như trên (để kính trình);",
        "- Phòng Kỹ thuật địa chính và Lưu trữ;",
        "- Phòng Kế hoạch - Tài chính;",
        "- Phòng Hành chính – Tổng hợp;",
        "- Ban Giám đốc Chi nhánh 23;",
        "- Lưu: VT, Tổ KTĐC-LT."
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
    p_ky_head.paragraph_format.space_after = Pt(2)
    r = p_ky_head.add_run("KT. GIÁM ĐỐC\nPHÓ GIÁM ĐỐC")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_empty = cell_ky.add_paragraph()
    p_empty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_empty.paragraph_format.space_before = Pt(0)
    p_empty.paragraph_format.space_after = Pt(45)
    r = p_empty.add_run("(Ký, đóng dấu và ghi rõ họ tên)")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_ky_name = cell_ky.add_paragraph()
    p_ky_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ky_name.paragraph_format.space_before = Pt(0)
    p_ky_name.paragraph_format.space_after = Pt(0)
    r = p_ky_name.add_run("Nguyễn Thị Lệ Hằng")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    out_file = "OUTPUT/To_trinh_dang_ky_thong_tin_do_dac_CN23.docx"
    doc.save(out_file)
    print(f"Generated successfully: {out_file}")

if __name__ == "__main__":
    create_formatted_totrinh()
