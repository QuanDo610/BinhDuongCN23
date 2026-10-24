import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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

# Load existing phuong an CN23.docx
doc = docx.Document("documents/phuong an CN23.docx")

# Find the signature table (Table 3)
sig_table = doc.tables[2]

# Remove all paragraphs and tables after the signature table
# In docx, we find the index of the element after Table 3
parent_elm = doc._body._element
sig_table_elm = sig_table._tbl

# Collect all elements after sig_table_elm to delete
elms_to_remove = []
found = False
for child in parent_elm:
    if found:
        elms_to_remove.append(child)
    elif child == sig_table_elm:
        found = True

for elm in elms_to_remove:
    parent_elm.remove(elm)

# Now add a new LANDSCAPE section for the appendix (like CN33 pages 8-10)
sec_landscape = doc.add_section()
sec_landscape.orientation = WD_ORIENT.LANDSCAPE
sec_landscape.page_width = Inches(11.69)  # 297 mm
sec_landscape.page_height = Inches(8.27)  # 210 mm
sec_landscape.top_margin = Inches(0.79)   # 20 mm
sec_landscape.bottom_margin = Inches(0.79)# 20 mm
sec_landscape.left_margin = Inches(0.79)  # 20 mm
sec_landscape.right_margin = Inches(0.79) # 20 mm

# 1. Header above table in Landscape
p_unit = doc.add_paragraph()
p_unit.paragraph_format.space_before = Pt(4)
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
p_sub.paragraph_format.space_after = Pt(6)
r_s = p_sub.add_run("NHU CẦU DIỆN TÍCH LÀM VĂN PHÒNG LÀM VIỆC VÀ KHO LƯU TRỮ CẦN THIẾT THEO ĐỊNH MỨC NHÀ NƯỚC")
r_s.font.name = "Times New Roman"
r_s.font.size = Pt(12)
r_s.font.bold = True

p_bases = doc.add_paragraph()
p_bases.paragraph_format.space_before = Pt(0)
p_bases.paragraph_format.space_after = Pt(8)
p_bases.paragraph_format.line_spacing = 1.15
r_b = p_bases.add_run(
    "- Căn cứ định mức tại Nghị định số 155/2025/NĐ-CP ngày 16 tháng 6 năm 2025 của Chính phủ quy định tiêu chuẩn, định mức sử dụng trụ sở làm việc, cơ sở hoạt động sự nghiệp;\n"
    "- Căn cứ Thông tư số 09/2007/TT-BNV ngày 26 tháng 11 năm 2007 của Bộ Nội vụ hướng dẫn kho lưu trữ chuyên dùng;\n"
    "- Căn cứ TCVN 4319:2012 về Nhà và công trình công cộng - Nguyên tắc cơ bản để thiết kế."
)
r_b.font.name = "Times New Roman"
r_b.font.size = Pt(10)
r_b.font.italic = True

# 2. Main Comparison Table (7 columns, exact CN33 format)
tbl = doc.add_table(rows=2, cols=7)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.autofit = False
set_table_borders(tbl, color="000000", sz="4")

col_widths = [
    Inches(0.6),  # STT
    Inches(3.3),  # Chỉ tiêu
    Inches(1.1),  # Hiện trạng diện tích (m2)
    Inches(1.0),  # Số người hoặc số mét tài liệu
    Inches(1.1),  # Diện tích cần thiết theo định mức Nhà nước
    Inches(1.0),  # So sánh: Hiện trạng - Nhu cầu
    Inches(2.0)   # Ghi chú: định mức Nhà nước quy định
]

# Set column widths
for r in tbl.rows:
    for i, w in enumerate(col_widths):
        r.cells[i].width = w

# Row 0 cells
r0 = tbl.rows[0]
r1 = tbl.rows[1]

# Header row 0 & 1 text & merging
# Merges:
# Col 0 (STT): merge r0.c0 with r1.c0
# Col 1 (Chỉ tiêu): merge r0.c1 with r1.c1
# Col 2 (Hiện trạng): merge r0.c2 with r1.c2
# Col 3 & 4 (Nhu cầu diện tích sàn): merge r0.c3 with r0.c4
# Col 5 (So sánh): merge r0.c5 with r1.c5
# Col 6 (Ghi chú): merge r0.c6 with r1.c6

cell_stt = r0.cells[0].merge(r1.cells[0])
cell_stt.text = "STT"

cell_ct = r0.cells[1].merge(r1.cells[1])
cell_ct.text = "Chỉ tiêu"

cell_ht = r0.cells[2].merge(r1.cells[2])
cell_ht.text = "Hiện trạng\ndiện tích (m2)"

cell_nc = r0.cells[3].merge(r0.cells[4])
cell_nc.text = "Nhu cầu diện tích sàn"

r1.cells[3].text = "Số người\nhoặc số mét\ntài liệu"
r1.cells[4].text = "Diện tích cần\nthiết theo định\nmức Nhà nước"

cell_ss = r0.cells[5].merge(r1.cells[5])
cell_ss.text = "So sánh:\nHiện trạng-\nNhu cầu"

cell_gc = r0.cells[6].merge(r1.cells[6])
cell_gc.text = "Ghi chú: định mức\nNhà nước quy định"

# Style header rows
for r in [r0, r1]:
    make_row_header(r)
    for c in r.cells:
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9.5)
                run.font.bold = True

# Data rows (Exact CN33 structure with CN23 verified data)
data = [
    # A. HIỆN TRẠNG NHÀ, ĐẤT ĐỀ NGHỊ
    {
        "stt": "A", "chỉ_tiêu": "HIỆN TRẠNG NHÀ, ĐẤT ĐỀ NGHỊ",
        "ht": "", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": True, "align_left": True
    },
    {
        "stt": "", "chỉ_tiêu": "Địa chỉ: Số 358 Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh",
        "ht": "", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": False, "align_left": True
    },
    {
        "stt": "", "chỉ_tiêu": "Diện tích đất:",
        "ht": "1417.7", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": False, "align_left": True
    },
    {
        "stt": "", "chỉ_tiêu": "Diện tích sàn:",
        "ht": "835.3", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": False, "align_left": True
    },
    {
        "stt": "", "chỉ_tiêu": "Cấp nhà: cấp 3",
        "ht": "", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": False, "align_left": True
    },
    {
        "stt": "", "chỉ_tiêu": "Kết cấu: khung, sàn, mái bê tông cốt thép, tường xây gạch",
        "ht": "", "sl": "", "dm": "", "ss": "", "gc": "",
        "bold": False, "align_left": True
    },

    # B. DIỆN TÍCH SÀN LÀM VIỆC
    {
        "stt": "B", "chỉ_tiêu": "DIỆN TÍCH SÀN LÀM VIỆC",
        "ht": "835.3", "sl": "85", "dm": "2104", "ss": "-1268.7", "gc": "",
        "bold": True, "align_left": True
    },
    {
        "stt": "1", "chỉ_tiêu": "Diện tích làm việc của các chức danh",
        "ht": "462", "sl": "85", "dm": "1230", "ss": "(768)",
        "gc": "Phụ lục II Nghị định số 155/2025/NĐ-CP ngày 16/6/2025 của Chính phủ",
        "bold": True, "align_left": True
    },
    {
        "stt": "1.1", "chỉ_tiêu": "Ban Giám đốc: 03 người",
        "ht": "60", "sl": "3", "dm": "60", "ss": "0",
        "gc": "20 m²/người",
        "bold": False, "align_left": True
    },
    {
        "stt": "1.2", "chỉ_tiêu": "Viên chức, người làm việc trong định mức được duyệt: 79 người",
        "ht": "372", "sl": "79", "dm": "1140", "ss": "(768)",
        "gc": "15 m²/người",
        "bold": False, "align_left": True
    },
    {
        "stt": "1.3", "chỉ_tiêu": "Cá nhân ký hợp đồng lao động theo quy định của Chính phủ về hợp đồng đối với một số loại công việc trong cơ quan hành chính, đơn vị sự nghiệp công lập: 03 người",
        "ht": "30", "sl": "3", "dm": "30", "ss": "0",
        "gc": "10 m²/người",
        "bold": False, "align_left": True
    },
    {
        "stt": "2", "chỉ_tiêu": "Diện tích sử dụng chung gồm:\n- Phòng tiếp nhận và trả hồ sơ (bộ phận một cửa); phòng tiếp dân; phòng văn thư, đánh máy, hành chính, quản trị; phòng nhân sao tài liệu;\n- Phòng tiếp khách;\n- Hội trường, phòng họp;\n- Phòng lưu trữ, phòng hồ sơ, phòng tư liệu và sách;\n- Phòng trung tâm dữ liệu, phòng máy tính, quản trị mạng, phòng đặt thiết bị kỹ thuật, quản lý toà nhà;\n- Phòng thường trực, bảo vệ hoặc phòng bảo vệ có yêu cầu trực đêm; phòng truyền thống; phòng y tế; nhà ăn; kho thiết bị, dụng cụ, văn phòng phẩm; sảnh, hành lang; ban công, lô gia; nơi thu gom giấy loại và rác thải; nhà làm việc của đội xe; khu vệ sinh; diện tích phục vụ công tác phòng cháy, chữa cháy.",
        "ht": "193.3", "sl": "", "dm": "369", "ss": "(175.7)",
        "gc": "Tối đa không quá 85% tổng diện tích làm việc phục vụ công tác các chức danh của cơ quan, tổ chức",
        "bold": False, "align_left": True
    },
    {
        "stt": "3", "chỉ_tiêu": "Diện tích nhà để xe (Chỉ tính cho CBCNV, chưa tính cho khách hàng)",
        "ht": "180", "sl": "", "dm": "505", "ss": "(325)",
        "gc": "Theo định mức tại mục 5.2.10 của TCVN 4319: 2012:\n+ Môto, xe máy: 3 m²/xe\n+ Ôtô: 25 m²/xe.\n- Số xe CBCNV là 85 xe máy/ngày.\n- Số ô tô CBCNV là 10 xe/ngày.\nHiện trạng, đang sử dụng chung vỉa hè cho xe ô tô",
        "bold": False, "align_left": True
    },

    # C. DIỆN TÍCH LƯU TRỮ VÀ XỬ LÝ NGHIỆP VỤ LƯU TRỮ
    {
        "stt": "", "chỉ_tiêu": "DIỆN TÍCH LƯU TRỮ VÀ XỬ LÝ NGHIỆP VỤ LƯU TRỮ",
        "ht": "171.2", "sl": "", "dm": "750", "ss": "(578.8)",
        "gc": "Căn cứ Thông tư số 09/2007/TT-BNV ngày 26/11/2007 của Bộ Nội vụ hướng dẫn kho lưu trữ chuyên dùng",
        "bold": True, "align_left": True
    },
    {
        "stt": "1", "chỉ_tiêu": "Diện tích sàn kho bảo quản tài liệu",
        "ht": "171.2", "sl": "2500", "dm": "500", "ss": "(328.8)",
        "gc": "Theo điểm a, khoản 1, mục III, Thông tư số 09/2007/TT-BNV ngày 26/11/2007:\nLoại 4: bảo quản từ 1 - 3 km giá tài liệu, diện tích sàn 312 - 936 m²\n=> trong tương lai, do nhu cầu lưu trữ hồ sơ phát sinh tại đơn vị rất lớn nên nhu cầu diện tích sàn khoảng 500m² theo quy định này.",
        "bold": False, "align_left": True
    },
    {
        "stt": "2", "chỉ_tiêu": "Khu vực xử lý nghiệp vụ lưu trữ (tiếp nhận, chỉnh lý), lắp đặt thiết bị kỹ thuật, phục vụ khai thác tài liệu",
        "ht": "0", "sl": "", "dm": "250", "ss": "(250.0)",
        "gc": "Theo Thông tư số 09/2007/TT-BNV ngày 26/11/2007 là 50% tổng diện tích sàn kho bảo quản tài liệu",
        "bold": False, "align_left": True
    },

    # CỘNG DIỆN TÍCH SÀN (B+C)
    {
        "stt": "", "chỉ_tiêu": "CỘNG DIỆN TÍCH SÀN (B+C)",
        "ht": "1128.24", "sl": "", "dm": "2854", "ss": "(1,725.8)",
        "gc": "",
        "bold": True, "align_left": True
    }
]

for row_info in data:
    new_row = tbl.add_row()
    make_row_cant_split(new_row)
    
    # Assign widths
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
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        
        if c_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif c_idx == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        elif c_idx in [2, 3, 4, 5]:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if text and not text.isalpha() else WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
        for r_item in p.runs:
            r_item.font.name = "Times New Roman"
            r_item.font.size = Pt(9.5)
            if row_info["bold"]:
                r_item.font.bold = True

# Save updated files
doc.save("documents/phuong an CN23.docx")
doc.save("phuong an CN23.docx")
doc.save("documents/Phuong_an_CN23_1656_new.docx")
print("Successfully updated phuong an CN23.docx and Phuong_an_CN23_1656_new.docx with exact CN33 Appendix format!")
