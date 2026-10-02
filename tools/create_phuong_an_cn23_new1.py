import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
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

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

# Open 1656_new.docx which has the pristine body and Table 2 (signatures)
doc = docx.Document("documents/1656_new.docx")

# In 1656_new.docx, Table 2 (index 2) is the signature block.
# Let's find Table 2 element and remove anything after it.
sig_table = doc.tables[2]
parent_elm = doc._body._element
sig_table_elm = sig_table._tbl

elms_to_remove = []
found = False
for child in parent_elm:
    if found:
        elms_to_remove.append(child)
    elif child == sig_table_elm:
        found = True

for elm in elms_to_remove:
    parent_elm.remove(elm)

# Add Landscape Section for Appendix
sec_landscape = doc.add_section()
sec_landscape.orientation = WD_ORIENT.LANDSCAPE
sec_landscape.page_width = Inches(11.69)   # A4 Landscape 297mm
sec_landscape.page_height = Inches(8.27)   # A4 Landscape 210mm
sec_landscape.top_margin = Inches(0.6)
sec_landscape.bottom_margin = Inches(0.6)
sec_landscape.left_margin = Inches(0.6)
sec_landscape.right_margin = Inches(0.6)

# Header Paragraphs
p_unit = doc.add_paragraph()
p_unit.paragraph_format.space_before = Pt(0)
p_unit.paragraph_format.space_after = Pt(2)
r_u = p_unit.add_run("Đơn vị: CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23")
r_u.font.name = "Times New Roman"
r_u.font.size = Pt(11)
r_u.font.bold = True

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(4)
p_title.paragraph_format.space_after = Pt(2)
r_t = p_title.add_run("BẢNG ĐỐI CHIẾU")
r_t.font.name = "Times New Roman"
r_t.font.size = Pt(14)
r_t.font.bold = True

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(4)
r_s = p_sub.add_run("NHU CẦU DIỆN TÍCH LÀM VĂN PHÒNG LÀM VIỆC VÀ KHO LƯU TRỮ CẦN THIẾT THEO ĐỊNH MỨC NHÀ NƯỚC")
r_s.font.name = "Times New Roman"
r_s.font.size = Pt(12)
r_s.font.bold = True

p_bases = doc.add_paragraph()
p_bases.paragraph_format.space_before = Pt(0)
p_bases.paragraph_format.space_after = Pt(6)
p_bases.paragraph_format.line_spacing = 1.15
r_b = p_bases.add_run(
    "- Căn cứ định mức tại Nghị định số 155/2025/NĐ-CP ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;\n"
    "- Căn cứ Thông tư số 09/2007/TT-BNV ngày 26 tháng 11 năm 2007 của Bộ Nội vụ hướng dẫn kho lưu trữ chuyên dùng;\n"
    "- Căn cứ Tiêu chuẩn quốc gia TCVN 4319:2012 về Nhà và công trình công cộng - Nguyên tắc cơ bản để thiết kế;\n"
    "- Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 30 tháng 3 năm 2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh."
)
r_b.font.name = "Times New Roman"
r_b.font.size = Pt(9.5)
r_b.font.italic = True

# Main Comparison Table (7 columns, exact CN33 merged layout)
tbl = doc.add_table(rows=2, cols=7)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.autofit = False
set_table_borders(tbl, color="000000", sz="4")

col_widths = [
    Inches(0.55), # STT
    Inches(3.35), # Chỉ tiêu
    Inches(1.10), # Hiện trạng
    Inches(1.05), # Số người / mét TL
    Inches(1.15), # Định mức NN
    Inches(1.05), # So sánh
    Inches(2.24)  # Ghi chú
] # Sum = 10.49 Inches (fits 11.69 - 1.2 = 10.49 Inches perfectly)

for r in tbl.rows:
    for i, w in enumerate(col_widths):
        r.cells[i].width = w

r0 = tbl.rows[0]
r1 = tbl.rows[1]

# Header Row 0 & 1 with merges matching CN33:
cell_stt = r0.cells[0].merge(r1.cells[0])
cell_stt.text = "STT"

cell_ct = r0.cells[1].merge(r1.cells[1])
cell_ct.text = "Chỉ tiêu"

cell_ht = r0.cells[2].merge(r1.cells[2])
cell_ht.text = "Hiện trạng\ndiện tích (m²)"

cell_nc = r0.cells[3].merge(r0.cells[4])
cell_nc.text = "Nhu cầu diện tích sàn"

r1.cells[3].text = "Số người\nhoặc số mét\ntài liệu"
r1.cells[4].text = "Diện tích cần\nthiết theo định\nmức Nhà nước (m²)"

cell_ss = r0.cells[5].merge(r1.cells[5])
cell_ss.text = "So sánh:\nHiện trạng -\nNhu cầu (m²)"

cell_gc = r0.cells[6].merge(r1.cells[6])
cell_gc.text = "Ghi chú: định mức\nNhà nước quy định"

# Style header rows
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

# Data rows - 100% CONTENT CỦA CHI NHÁNH 23
data = [
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
        "chỉ_tiêu": "Cơ sở đề nghị điều chuyển: Điểm trạm y tế 3 (P. Chánh Mỹ cũ)\n- Vị trí: Đường Huỳnh Văn Cù (liền kề số 358)\n- Diện tích khuôn viên đất: 1.276,20 m²",
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
        "chỉ_tiêu": "Diện tích sử dụng chung toàn trụ sở gồm:\n- Bộ phận Một cửa tiếp nhận và trả kết quả: 26 m²\n- Phòng họp chuyên môn kết hợp tiếp dân: 26 m²\n- Phòng máy chủ, CNTT: 15 m²\n- Sảnh, hành lang, cầu thang, khu vệ sinh, PCCC: 123,30 m²",
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
        "ht": "300,00",
        "sl": ">3.000m TL",
        "dm": "1.000,00",
        "ss": "-700,00",
        "gc": "Căn cứ Thông tư số 09/2007/TT-BNV hướng dẫn kho lưu trữ chuyên dùng",
        "bold": True, "align_left": True, "bg": "F2F2F2"
    },
    {
        "stt": "1",
        "chỉ_tiêu": "Diện tích sàn kho bảo quản hồ sơ địa chính gốc:\n- Hiện trạng kho tại 358 Huỳnh Văn Cù: 300 m² (lấp kín 100%)\n- Nhu cầu kho bảo quản hồ sơ biến động tích lũy và phát sinh",
        "ht": "300,00",
        "sl": ">3.000m\ngiá tài liệu",
        "dm": "600,00",
        "ss": "-300,00",
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
        "gc": "Tối ưu hóa tài sản công dôi dư, tránh lãng phí theo NĐ 186/2025/NĐ-CP và CV 223/BTC-QLCS.",
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

for row_info in data:
    new_row = tbl.add_row()
    make_row_cant_split(new_row)
    
    for i, w in enumerate(col_widths):
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

# Save to destination files
doc.save("documents/phuong an CN23 new1.docx")
doc.save("documents/phuong_an_CN23_new1.docx")
doc.save("phuong an CN23 new1.docx")
# Also update documents/phuong an CN23.docx so the main file is correct too!
doc.save("documents/phuong an CN23.docx")
doc.save("phuong an CN23.docx")

print("Saved successfully to documents/phuong an CN23 new1.docx and related files!")
