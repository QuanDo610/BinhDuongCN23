import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def add_horizontal_line(paragraph, width_inches=1.85, height_pt=0.75):
    """Vẽ đường kẻ ngang nét liền chính xác tuyệt đối bằng Drawing ML"""
    cx = int(width_inches * 914400)
    cy = int(height_pt * 12700)
    line_xml = parse_xml(r'''
    <w:r %s>
        <w:drawing>
            <wp:inline distT="0" distB="0" distL="0" distR="0">
                <wp:extent cx="%d" cy="%d"/>
                <wp:docPr id="1" name="Line"/>
                <wp:cNvGraphicFramePr/>
                <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/main">
                        <a:xfrm>
                            <a:off x="0" y="0"/>
                            <a:ext cx="%d" cy="%d"/>
                        </a:xfrm>
                        <a:prstGeom prst="rect">
                            <a:avLst/>
                        </a:prstGeom>
                        <a:solidFill>
                            <a:srgbClr val="000000"/>
                        </a:solidFill>
                    </a:graphicData>
                </a:graphic>
            </wp:inline>
        </w:drawing>
    </w:r>
    ''' % (nsdecls('w', 'wp'), cx, cy, cx, cy))
    paragraph._p.append(line_xml)

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(r'<w:tcMar %s><w:top w:w="%d" w:type="dxa"/><w:bottom w:w="%d" w:type="dxa"/><w:left w:w="%d" w:type="dxa"/><w:right w:w="%d" w:type="dxa"/></w:tcMar>' % (nsdecls('w'), top, bottom, left, right))
    tcPr.append(tcMar)

def remove_table_borders(table):
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>' % nsdecls('w'))
            tcPr.append(tcBorders)

def set_cell_box_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>' % nsdecls('w'))
    tcPr.append(tcBorders)

# ==============================================================
# RE-GENERATE 1: To_trinh_dang_ky_thong_tin_do_dac_CN23.docx
# ==============================================================
def gen_totrinh():
    doc = docx.Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.79)
    section.bottom_margin = Inches(0.79)
    section.left_margin = Inches(1.18)
    section.right_margin = Inches(0.59)

    section.different_first_page_header_footer = True
    header = section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    header_p._p.append(fldSimple)
    for run in header_p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)

    # Header Table
    t_header = doc.add_table(rows=1, cols=2)
    t_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_header.autofit = False
    remove_table_borders(t_header)

    t_header.rows[0].cells[0].width = Inches(2.9)
    t_header.rows[0].cells[1].width = Inches(3.6)
    set_cell_margins(t_header.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_header.rows[0].cells[1], 0, 0, 0, 0)

    c0 = t_header.rows[0].cells[0]
    c1 = t_header.rows[0].cells[1]

    # Cơ quan
    p = c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)  # SIZE 12 THEO USER
    r = p.add_run("CHI NHÁNH SỐ 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13 THEO USER

    p_line_cq = c0.add_paragraph()
    p_line_cq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_cq.paragraph_format.space_before = Pt(1)
    p_line_cq.paragraph_format.space_after = Pt(4)
    add_horizontal_line(p_line_cq, width_inches=1.0, height_pt=0.75) # 1/3 - 1/2 dòng tên cơ quan

    p_so = c0.add_paragraph()
    p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_so.paragraph_format.space_before = Pt(0)
    p_so.paragraph_format.space_after = Pt(0)
    r = p_so.add_run("Số:        /TTr-CN23")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    # Quốc hiệu
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13 THEO USER
    r = p.add_run("Độc lập - Tự do - Hạnh phúc")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13 THEO USER

    p_line_qh = c1.add_paragraph()
    p_line_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_qh.paragraph_format.space_before = Pt(1)
    p_line_qh.paragraph_format.space_after = Pt(4)
    # Đường kẻ ngang dài đúng 100% dòng Tiêu ngữ: từ "Độc" đến "phúc" ≈ 1.85 inches
    add_horizontal_line(p_line_qh, width_inches=1.85, height_pt=0.75)

    p_ngay = c1.add_paragraph()
    p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ngay.paragraph_format.space_before = Pt(0)
    p_ngay.paragraph_format.space_after = Pt(0)
    r = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày 07 tháng 10 năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    # Tiêu đề TỜ TRÌNH
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
    r.font.size = Pt(13)

    p_line_ty = doc.add_paragraph()
    p_line_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_ty.paragraph_format.space_before = Pt(1)
    p_line_ty.paragraph_format.space_after = Pt(12)
    add_horizontal_line(p_line_ty, width_inches=1.8, height_pt=0.75)

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

    add_heading_section("1. Căn cứ pháp lý thực hiện:")
    add_p("Căn cứ Quyết định số 2637/QĐ-SNNMT-VP ngày 30 tháng 12 năm 2025 của Giám đốc Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh về việc ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23 trực thuộc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh;", italic=True)
    add_p("Căn cứ Thông tư số 47/2024/TT-BTC ngày 10 tháng 7 năm 2024 của Bộ Tài chính quy định mức thu, chế độ thu, nộp, miễn, quản lý và sử dụng phí khai thác, sử dụng thông tin dữ liệu đo đạc và bản đồ.", italic=True)

    add_heading_section("2. Nội dung đề xuất:")
    add_p("Hiện nay, Chi nhánh Văn phòng Đăng ký đất đai số 23 sử dụng các thiết bị định vị GNSS/GPS RTK trong quá trình hoạt động đo đạc bản đồ, trích đo địa chính, chỉnh lý biến động đất đai trên địa bàn quản lý. Theo đó, phương pháp đo RTK sử dụng trạm CORS quốc gia như một trạm Base cố định để thu nhận tín hiệu GNSS/GPS, từ đó đưa ra vị trí tọa độ thửa đất một cách nhanh chóng, đồng bộ và chuẩn xác cao.")
    add_p("Theo quy định tại Điều 2 và Biểu mức thu phí ban hành kèm theo Thông tư số 47/2024/TT-BTC ngày 10 tháng 7 năm 2024 của Bộ Tài chính, việc sử dụng dữ liệu đo động thời gian thực (dữ liệu tiếp nhận từ trạm CORS quốc gia) để thực hiện hoạt động đo đạc phải nộp phí với mức thu là 6.750.000 đồng/12 tháng/máy thu.")
    add_p("Căn cứ nhu cầu sử dụng thiết bị định vị GNSS/GPS RTK phục vụ công tác chuyên môn tại đơn vị, Chi nhánh Văn phòng Đăng ký đất đai số 23 xác định có 04 thiết bị sử dụng trạm CORS gần đến thời hạn gia hạn tài khoản dữ liệu với tổng kinh phí đăng ký sử dụng là 27.000.000 đồng (bằng chữ: Hai mươi bảy triệu đồng chẵn).")
    add_p("Danh mục chi tiết 04 thiết bị đăng ký sử dụng dữ liệu cụ thể như sau:")

    # Table
    t_tb = doc.add_table(rows=6, cols=4)
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

    for row_idx, r_data in enumerate(rows_data, start=1):
        for col_idx, val in enumerate(r_data):
            c = t_tb.rows[row_idx].cells[col_idx]
            c.width = widths_tb[col_idx]
            set_cell_margins(c, 70, 70, 100, 100)
            set_cell_box_borders(c)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            if col_idx in [0, 1, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

    row_5 = t_tb.rows[5]
    cell_tot_label = row_5.cells[0].merge(row_5.cells[2])
    cell_tot_label.width = Inches(5.0)
    set_cell_margins(cell_tot_label, 70, 70, 100, 100)
    set_cell_box_borders(cell_tot_label)
    shading_tot = parse_xml(r'<w:shd %s w:fill="F9F9F9"/>' % nsdecls('w'))
    cell_tot_label._tc.get_or_add_tcPr().append(shading_tot)
    p_tl = cell_tot_label.paragraphs[0]
    p_tl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tl.paragraph_format.space_before = Pt(0)
    p_tl.paragraph_format.space_after = Pt(0)
    r = p_tl.add_run("Tổng cộng")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    cell_tot_val = row_5.cells[3]
    cell_tot_val.width = Inches(1.5)
    set_cell_margins(cell_tot_val, 70, 70, 100, 100)
    set_cell_box_borders(cell_tot_val)
    shading_val = parse_xml(r'<w:shd %s w:fill="F9F9F9"/>' % nsdecls('w'))
    cell_tot_val._tc.get_or_add_tcPr().append(shading_val)
    p_tv = cell_tot_val.paragraphs[0]
    p_tv.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_tv.paragraph_format.space_before = Pt(0)
    p_tv.paragraph_format.space_after = Pt(0)
    r = p_tv.add_run("27.000.000")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    add_heading_section("3. Kiến nghị, đề xuất:")
    add_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 kính đề nghị Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, chỉ đạo việc đăng ký sử dụng thông tin dữ liệu đo đạc và bản đồ nhằm cung cấp thông tin dữ liệu thu nhận từ mạng lưới trạm định vị vệ tinh quốc gia về dữ liệu đo đạc thời gian thực (RTK) cho 04 thiết bị nêu trên để phục vụ kịp thời công tác đo đạc, lập bản đồ và giải quyết thủ tục hành chính cho người dân, doanh nghiệp.")
    add_p("Kính trình Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh xem xét, giải quyết./.", italic=True)

    # Signature
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
    print("Re-generated To_trinh_dang_ky_thong_tin_do_dac_CN23.docx successfully.")

# ==============================================================
# RE-GENERATE 2: Bao_cao_dan_chu_co_so_CN23.docx
# ==============================================================
def gen_baocao_danchu():
    doc = docx.Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.79)
    section.bottom_margin = Inches(0.79)
    section.left_margin = Inches(1.18)
    section.right_margin = Inches(0.59)

    section.different_first_page_header_footer = True
    header = section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    header_p._p.append(fldSimple)
    for run in header_p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)

    t_header = doc.add_table(rows=1, cols=2)
    t_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_header.autofit = False
    remove_table_borders(t_header)

    t_header.rows[0].cells[0].width = Inches(2.9)
    t_header.rows[0].cells[1].width = Inches(3.6)
    set_cell_margins(t_header.rows[0].cells[0], 0, 0, 0, 0)
    set_cell_margins(t_header.rows[0].cells[1], 0, 0, 0, 0)

    c0 = t_header.rows[0].cells[0]
    c1 = t_header.rows[0].cells[1]

    # Cơ quan
    p = c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)  # SIZE 12
    r = p.add_run("CHI NHÁNH SỐ 23")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13

    p_line_cq = c0.add_paragraph()
    p_line_cq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_cq.paragraph_format.space_before = Pt(1)
    p_line_cq.paragraph_format.space_after = Pt(4)
    add_horizontal_line(p_line_cq, width_inches=1.0, height_pt=0.75)

    p_so = c0.add_paragraph()
    p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_so.paragraph_format.space_before = Pt(0)
    p_so.paragraph_format.space_after = Pt(0)
    r = p_so.add_run("Số:        /BC-CN23")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    # Quốc hiệu
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13
    r = p.add_run("Độc lập - Tự do - Hạnh phúc")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)  # SIZE 13

    p_line_qh = c1.add_paragraph()
    p_line_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_qh.paragraph_format.space_before = Pt(1)
    p_line_qh.paragraph_format.space_after = Pt(4)
    add_horizontal_line(p_line_qh, width_inches=1.85, height_pt=0.75) # Toàn bộ tiêu ngữ

    p_ngay = c1.add_paragraph()
    p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ngay.paragraph_format.space_before = Pt(0)
    p_ngay.paragraph_format.space_after = Pt(0)
    r = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày 07 tháng 10 năm 2026")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("BÁO CÁO")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.line_spacing = 1.15
    r = p_sub.add_run("Kết quả thực hiện việc tiếp tục nâng cao chất lượng thực hiện dân chủ ở cơ sở\ngắn với trách nhiệm của người đứng đầu")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    p_line_ty = doc.add_paragraph()
    p_line_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line_ty.paragraph_format.space_before = Pt(1)
    p_line_ty.paragraph_format.space_after = Pt(12)
    add_horizontal_line(p_line_ty, width_inches=2.0, height_pt=0.75)

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

    def add_heading_I(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.45)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)

    add_p("Thực hiện Công văn số 27265/VPĐK-HC ngày 23 tháng 9 năm 2026 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc tiếp tục nâng cao chất lượng thực hiện dân chủ ở cơ sở gắn với trách nhiệm của người đứng đầu;", indent=True, italic=True)
    add_p("Chi nhánh Văn phòng Đăng ký đất đai số 23 báo cáo kết quả triển khai thực hiện tại đơn vị như sau:", indent=True)

    add_heading_I("I. MỤC ĐÍCH VÀ YÊU CẦU")
    add_heading_1("1. Mục đích")
    add_p("- Chi nhánh đã tổ chức phổ biến sâu rộng đến 100% viên chức, người lao động triển khai hiệu quả công tác dân vận chính quyền và thực hiện quy chế dân chủ ở cơ sở bảo đảm thực chất, đúng quy định pháp luật; gắn với yêu cầu hoàn thiện tổ chức bộ máy, nâng cao kỷ luật, kỷ cương hành chính và trách nhiệm của người đứng đầu tại Chi nhánh số 23.")
    add_p("- Nâng cao chất lượng giải quyết thủ tục hành chính (TTHC) về đất đai cho người sử dụng đất, chủ sở hữu tài sản gắn liền với đất là cá nhân, cộng đồng dân cư, người gốc Việt Nam định cư ở nước ngoài thuộc phạm vi đơn vị hành chính 05 phường phụ trách (Phú Lợi, Phú An, Bình Dương, Chánh Hiệp, Thủ Dầu Một); từng bước tháo gỡ các vướng mắc, tồn đọng, nâng cao mức độ hài lòng của người dân; phòng ngừa tham nhũng, tiêu cực, nhũng nhiễu trong thi hành công vụ.")
    add_p("- Phát huy quyền làm chủ của viên chức, người lao động; nâng cao trách nhiệm của Ban Giám đốc Chi nhánh và Lãnh đạo các Tổ nghiệp vụ; xây dựng đội ngũ viên chức có bản lĩnh chính trị vững vàng, đạo đức công vụ trong sáng, tinh thần trách nhiệm cao.")

    add_heading_1("2. Yêu cầu")
    add_p("- Việc triển khai phải được tiến hành đồng bộ, thường xuyên, thực chất, gắn chặt với nhiệm vụ chính trị, chuyên môn của 03 Tổ nghiệp vụ thuộc Chi nhánh số 23 (gồm: Tổ Hành chính – Tổng hợp, Tổ Đăng ký và Cấp giấy chứng nhận, Tổ Kỹ thuật Địa chính và Lưu trữ).")
    add_p("- 100% Tổ trưởng, Tổ phó các Tổ chuyên môn chịu trách nhiệm trước Giám đốc Chi nhánh và trước pháp luật trong việc tổ chức triển khai, kiểm tra, giám sát và đánh giá kết quả thực hiện tại bộ phận phụ trách.")
    add_p("- 100% viên chức, người lao động làm việc tại Chi nhánh số 23 được quán triệt, phổ biến đầy đủ các quy định của pháp luật về thực hiện dân chủ ở cơ sở; được tham gia ý kiến, giám sát các nội dung liên quan đến quyền, nghĩa vụ và trách nhiệm của mình theo quy định.")

    add_heading_I("II. NỘI DUNG VÀ KẾT QUẢ THỰC HIỆN")
    add_heading_1("1. Công tác lãnh đạo, chỉ đạo")
    add_p("- Tiếp tục quán triệt, phổ biến sâu rộng đến toàn thể viên chức, người lao động nội dung Quy định số 124-QĐ/TW ngày 02/02/2018 của Ban Bí thư về giám sát việc tu dưỡng, rèn luyện đạo đức, lối sống của người đứng đầu, gắn với trách nhiệm nêu gương trong công tác quản lý, điều hành, chống nhũng nhiễu, tiêu cực.")
    add_p("- Quán triệt thực hiện nghiêm túc Quyết định số 06/QĐ-VPĐK-HC và Quyết định số 07/QĐ-VPĐK-HC ngày 02/10/2025 của Văn phòng Đăng ký đất đai Thành phố; Chỉ thị số 7883/CT-BNNMT và Nghị quyết số 08/2026/NQ-HĐND về tăng cường kỷ luật, kỷ cương hành chính.")
    add_p("- Gắn thực hiện công tác dân vận và quy chế dân chủ ở cơ sở với việc hoàn thiện tổ chức bộ máy, cải cách hành chính, chuyển đổi số, xây dựng cơ sở dữ liệu địa chính và nâng cao chất lượng thực thi công vụ tại Chi nhánh.")
    add_p("- Phát huy vai trò, trách nhiệm của Giám đốc Chi nhánh và các Tổ trưởng chuyên môn; tăng cường tiếp xúc, đối thoại trực tiếp với viên chức, người lao động và người dân đến giao dịch TTHC.")

    add_heading_1("2. Về công tác dân vận chính quyền và giải quyết thủ tục hành chính")
    add_p("a) Thực hiện phương châm hành động chuẩn mực:")
    add_p("+ Phương châm “5 biết”: Biết nghe dân; Biết nói dân hiểu; Biết làm dân tin; Biết xin lỗi; Biết cảm ơn.")
    add_p("+ Phương châm “3 thể hiện”: Tôn trọng; Văn minh; Gần gũi.")
    add_p("+ Phương châm “6 rõ”: Rõ người, Rõ việc, Rõ tiến độ, Rõ trách nhiệm, Rõ thẩm quyền, Rõ sản phẩm.")
    add_p("+ Phương châm “3 không”: Không đổ thừa, Không được không quyết liệt, Không để không có sản phẩm.")
    add_p("b) Công khai, minh bạch TTHC:")
    add_p("Niêm yết và công khai đầy đủ các thông tin TTHC thuộc thẩm quyền. Tạo điều kiện để người dân được biết, được theo dõi, phản ánh và kiến nghị tại Bộ phận Tiếp nhận và Trả kết quả UBND các phường.")
    add_p("c) Chỉ tiêu giải quyết hồ sơ và trách nhiệm giải trình:")
    add_p("- Phấn đấu giải quyết TTHC về đất đai thuộc thẩm quyền đạt tỷ lệ đúng hạn từ 98% trở lên.")
    add_p("- Thực hiện nghiêm trách nhiệm giải trình và văn bản xin lỗi đối với các hồ sơ bị trễ hạn. Thông báo rõ tình trạng giải quyết hồ sơ, lý do trễ hạn chính xác.")
    add_p("- Giải quyết dứt điểm phản ánh, kiến nghị: Trực tiếp tiếp nhận, chỉ đạo xử lý kịp thời, dứt điểm 100% các phản ánh, kiến nghị, khiếu nại của người dân; phản hồi công khai, minh bạch kết quả. Kiên quyết xem xét trách nhiệm, xử lý nghiêm cá nhân có biểu hiện đùn đẩy, né tránh, chậm trễ hay giải quyết mang tính hình thức.")
    add_p("- Đẩy mạnh chuyển đổi số: Tích cực triển khai dịch vụ công trực tuyến toàn trình; phối hợp đẩy mạnh kết nối, chia sẻ dữ liệu lên Cổng thông tin điện tử và Hệ thống thông tin giải quyết TTHC của Thành phố.")
    add_p("- Phát huy vai trò đoàn thể: Công đoàn, Đoàn Thanh niên tích cực vận động nâng cao tinh thần phục vụ Nhân dân.")

    add_heading_1("3. Về thực hiện quy chế dân chủ ở cơ sở")
    add_p("- Rà soát toàn bộ quy chế nội bộ, tiến hành chuẩn hóa quy trình, thống nhất hệ thống biểu mẫu thực hiện dân chủ (quy trình công khai thông tin, quy trình lấy ý kiến người lao động) bám sát Luật Thực hiện dân chủ ở cơ sở và các hướng dẫn mới nhất.")
    add_p("- Quán triệt và triển khai thực chất phương châm “Dân biết, dân bàn, dân làm, dân kiểm tra, dân giám sát, dân thụ hưởng” trong nội bộ đơn vị.")
    add_p("- Tổ chức Hội nghị viên chức, người lao động hằng năm đúng quy định; tạo điều kiện để người lao động tham gia ý kiến về quyền, nghĩa vụ và lợi ích hợp pháp của mình.")
    add_p("- Thực hiện công khai, minh bạch theo quy định đối với: Công tác cán bộ (bố trí, giao nhiệm vụ, ký HĐLĐ); Quy chế làm việc nội bộ; Quy chế chi tiêu nội bộ, quản lý tài chính, tài sản công; Kê khai tài sản, thu nhập; Kết quả thanh tra, kiểm tra và giải quyết đơn thư nội bộ.")
    add_p("- Tăng cường kiểm tra, giám sát trách nhiệm của người đứng đầu trong việc thực hiện quy chế dân chủ; định kỳ rà soát, bổ sung các quy chế nội bộ phù hợp với quy định pháp luật và thực tiễn.")

    add_heading_I("III. TỔ CHỨC THỰC HIỆN")
    add_heading_1("1. Phân công trách nhiệm các Tổ nghiệp vụ thuộc Chi nhánh số 23")
    add_p("a) Tổ Hành chính – Tổng hợp:")
    add_p("- Chủ trì tham mưu, theo dõi, đôn đốc, tổng hợp chung việc triển khai các nhiệm vụ tại Chi nhánh số 23.")
    add_p("- Chủ trì rà soát, tham mưu chuẩn hóa hệ thống quy trình, biểu mẫu thực hiện dân chủ, quy trình công khai thông tin và lấy ý kiến người lao động tại đơn vị bám sát quy định mới.")
    add_p("- Quản lý, vận hành hiệu quả Bộ phận Tiếp nhận và Trả kết quả tại trụ sở số 358 đường Huỳnh Văn Cù; triển khai phiếu khảo sát đánh giá sự hài lòng của người dân.")
    add_p("- Đầu mối trực tiếp tiếp nhận, tham mưu xử lý dứt điểm, kịp thời 100% đơn thư phản ánh, kiến nghị, khiếu nại, tố cáo đúng thời hạn và thẩm quyền; kiên quyết không để xảy ra tình trạng đùn đẩy, né tránh hoặc giải quyết hình thức.")

    add_p("b) Tổ Đăng ký và Cấp Giấy chứng nhận:")
    add_p("- Thực hiện công khai, minh bạch quy trình nghiệp vụ đăng ký biến động, cấp, đính chính, thu hồi, hủy Giấy chứng nhận và đăng ký biện pháp bảo đảm.")
    add_p("- Đẩy mạnh ứng dụng công nghệ thông tin, vận hành hiệu quả Hệ thống thông tin giải quyết thủ tục hành chính của Thành phố trong công tác thụ lý hồ sơ.")
    add_p("- Tối ưu hóa quy trình xử lý hồ sơ, bảo đảm tỷ lệ đúng hạn từ 98% trở lên; thực hiện nghiêm việc giải trình và tham mưu văn bản xin lỗi nếu hồ sơ bị trễ hạn.")

    add_p("c) Tổ Kỹ thuật Địa chính và Lưu trữ:")
    add_p("- Bảo đảm công khai, đúng hẹn trong công tác đo đạc, chỉnh lý, lập bản đồ địa chính, trích lục bản đồ; cập nhật và chia sẻ dữ liệu địa chính chính xác, kịp thời.")
    add_p("- Lập, chỉnh lý, lưu trữ và quản lý hồ sơ địa chính; cung cấp hồ sơ, thông tin số liệu đất đai cho tổ chức, cá nhân đúng quy định, minh bạch.")

    add_heading_1("2. Công tác phối hợp, giám sát của các tổ chức đoàn thể")
    add_p("Ban Chấp hành Công đoàn, Đoàn Thanh niên Chi nhánh phối hợp với Lãnh đạo đơn vị trong công tác tuyên truyền; tham gia giám sát việc tu dưỡng, rèn luyện đạo đức, trách nhiệm nêu gương của người đứng đầu và tinh thần phục vụ của viên chức, người lao động.")

    add_heading_1("3. Chế độ kiểm tra, báo cáo")
    add_p("Ban Giám đốc Chi nhánh phối hợp với các Tổ trưởng đưa nội dung kiểm tra trách nhiệm người đứng đầu, công tác tiếp công dân, đối thoại và giải quyết phản ánh, kiến nghị vào kế hoạch kiểm tra thường xuyên, đột xuất. Kịp thời chấn chỉnh các cá nhân thực hiện mang tính hình thức, chậm trễ.")
    add_p("Tổ Hành chính – Tổng hợp chịu trách nhiệm tổng hợp, tham mưu báo cáo kết quả thực hiện định kỳ (gửi trước ngày 10/10 hàng năm) hoặc đột xuất gửi về Văn phòng Đăng ký đất đai Thành phố (thông qua Phòng Hành chính - Tổng hợp) theo quy định.")
    add_p("Trên đây là Báo cáo kết quả thực hiện việc tiếp tục nâng cao chất lượng thực hiện dân chủ ở cơ sở gắn với trách nhiệm của người đứng đầu của Chi nhánh Văn phòng Đăng ký đất đai số 23. Kính báo cáo Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh theo dõi, chỉ đạo./.", italic=True)

    # Khối ký
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

    p_nn_head = cell_nn.paragraphs[0]
    p_nn_head.paragraph_format.space_after = Pt(2)
    r = p_nn_head.add_run("Nơi nhận:")
    r.bold = True
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    nn_items = [
        "- VPĐKĐĐ TP.HCM (để b/c);",
        "- Phòng Hành chính - Tổng hợp (để theo dõi, b/c);",
        "- Ban Giám đốc Chi nhánh 23;",
        "- Niêm yết cơ quan;",
        "- Lưu: VT, Tổ HC-TH."
    ]
    for item in nn_items:
        p_it = cell_nn.add_paragraph()
        p_it.paragraph_format.space_before = Pt(0)
        p_it.paragraph_format.space_after = Pt(1)
        p_it.paragraph_format.line_spacing = 1.05
        r = p_it.add_run(item)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

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
    r = p_ky_name.add_run("Đặng Huy Cường")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    out_file = "OUTPUT/Bao_cao_dan_chu_co_so_CN23.docx"
    doc.save(out_file)
    print("Re-generated Bao_cao_dan_chu_co_so_CN23.docx successfully.")

if __name__ == "__main__":
    gen_totrinh()
    gen_baocao_danchu()
