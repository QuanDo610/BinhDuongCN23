import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

out_dir = "/Users/admin/Desktop/BINHDUONG/OUTPUT"
os.makedirs(out_dir, exist_ok=True)
doc_path = os.path.join(out_dir, "Quyet_dinh_phan_cong_CN23.docx")

doc = docx.Document()

# 1. Định dạng trang A4 & Căn lề chuẩn NĐ 30/2020
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.79)
section.bottom_margin = Inches(0.79)
section.left_margin = Inches(1.18)
section.right_margin = Inches(0.59)

# 2. Header
section.different_first_page_header_footer = True
header = section.header
header_p = header.paragraphs[0]
header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = header_p.add_run()
fldChar1 = OxmlElement('w:fldChar')
fldChar1.set(qn('w:fldCharType'), 'begin')
instrText = OxmlElement('w:instrText')
instrText.set(qn('xml:space'), 'preserve')
instrText.text = 'PAGE'
fldChar2 = OxmlElement('w:fldChar')
fldChar2.set(qn('w:fldCharType'), 'separate')
fldChar3 = OxmlElement('w:fldChar')
fldChar3.set(qn('w:fldCharType'), 'end')
run._r.append(fldChar1)
run._r.append(instrText)
run._r.append(fldChar2)
run._r.append(fldChar3)

# 3. Phông chữ mặc định toàn bộ tài liệu
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(13)
font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(6)

def set_cell_border_none(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders %s><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>' % nsdecls('w'))
    tcPr.append(tcBorders)

# Header cơ quan & Quốc hiệu
table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
table.columns[0].width = Inches(3.5)
table.columns[1].width = Inches(3.5)

cell_left = table.cell(0,0)
cell_right = table.cell(0,1)
set_cell_border_none(cell_left)
set_cell_border_none(cell_right)

# Cell left
p_left_1 = cell_left.paragraphs[0]
p_left_1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_left_1.paragraph_format.space_after = Pt(0)
r = p_left_1.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nTHÀNH PHỐ HỒ CHÍ MINH")
r.font.size = Pt(13)
r.font.name = 'Times New Roman'

p_left_2 = cell_left.add_paragraph()
p_left_2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_left_2.paragraph_format.space_after = Pt(0)
r = p_left_2.add_run("CHI NHÁNH SỐ 23")
r.bold = True
r.font.size = Pt(13)
r.font.name = 'Times New Roman'

p_line_1 = cell_left.add_paragraph()
p_line_1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line_1.paragraph_format.space_after = Pt(0)
r_line_1 = p_line_1.add_run("__________")
r_line_1.font.size = Pt(13)

p_so = cell_left.add_paragraph()
p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_so = p_so.add_run("Số: ...../QĐ-CN23")
r_so.font.size = Pt(13)

# Cell right
p_right_1 = cell_right.paragraphs[0]
p_right_1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_right_1.paragraph_format.space_after = Pt(0)
r = p_right_1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM")
r.bold = True
r.font.size = Pt(13)
r.font.name = 'Times New Roman'

p_right_2 = cell_right.add_paragraph()
p_right_2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_right_2.paragraph_format.space_after = Pt(0)
r = p_right_2.add_run("Độc lập - Tự do - Hạnh phúc")
r.bold = True
r.font.size = Pt(14)
r.font.name = 'Times New Roman'

p_line_2 = cell_right.add_paragraph()
p_line_2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line_2.paragraph_format.space_after = Pt(0)
r_line_2 = p_line_2.add_run("________________________")
r_line_2.font.size = Pt(13)

p_ngay = cell_right.add_paragraph()
p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_ngay = p_ngay.add_run("Thành phố Hồ Chí Minh, ngày 01 tháng 10 năm 2026")
r_ngay.italic = True
r_ngay.font.size = Pt(14)

# Tên loại văn bản
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\nQUYẾT ĐỊNH")
r.bold = True
r.font.size = Pt(14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Về việc phân công công tác đối với Giám đốc\nvà các Phó Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23\n")
r.bold = True
r.font.size = Pt(14)

# Cơ quan ban hành
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("GIÁM ĐỐC CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23")
r.bold = True
r.font.size = Pt(14)

# Căn cứ
def add_can_cu(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(14)

add_can_cu("Căn cứ Quyết định số …… bổ nhiệm Giám đốc Chi nhánh Văn phòng Đăng ký đất đai số 23;")
add_can_cu("Căn cứ đơn xin nghỉ việc ký ngày 20/8/2026 của ông Đặng Huy Cường;")
add_can_cu("Căn cứ đơn xin nghỉ việc ký ngày 22/9/2026 của bà Nguyễn Thị Lệ Hằng;")
add_can_cu("Trên cơ sở Biên bản họp Ban Lãnh đạo Chi nhánh Văn phòng Đăng ký đất đai số 23 ngày 01/10/2026;")
add_can_cu("Theo đề nghị của Tổ trưởng Tổ Hành chính - Tổng hợp.")

# Quyết định
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("QUYẾT ĐỊNH:")
r.bold = True
r.font.size = Pt(14)

# Điều 1
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Inches(0.5)
r1 = p.add_run("Điều 1. ")
r1.bold = True
r2 = p.add_run("Nguyên tắc phân công và quan hệ công tác giữa Giám đốc và các Phó Giám đốc")
r2.bold = True

def add_khoan(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.add_run(text)

add_khoan("1. Giám đốc Chi nhánh chịu trách nhiệm cá nhân trước Giám đốc Văn phòng Đăng ký đất đai thành phố Hồ Chí Minh về toàn bộ hoạt động thuộc chức năng, nhiệm vụ được giao cho Chi nhánh.")
add_khoan("2. Giám đốc phân công các Phó Giám đốc chỉ đạo, xử lý các công việc cụ thể. Các Phó Giám đốc chủ động giải quyết các công việc đã được phân công và chịu trách nhiệm trước Giám đốc và trước pháp luật về quyết định của mình.")
add_khoan("3. Trong phạm vi quyền hạn và nhiệm vụ được giao, các Phó Giám đốc chủ động giải quyết công việc. Trong quá trình thực hiện, nếu phát sinh những vấn đề lớn, những nội dung quan trọng, phức tạp, phải kịp thời báo cáo, xin ý kiến Giám đốc.")
add_khoan("4. Trường hợp cần thiết hoặc khi một Phó Giám đốc Chi nhánh vắng mặt từ 02 ngày làm việc trở lên thì Giám đốc phân công Phó Giám đốc kia giải quyết công việc của người vắng mặt.")

# Điều 2
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Inches(0.5)
r1 = p.add_run("Điều 2. ")
r1.bold = True
r2 = p.add_run("Chế độ báo cáo và hội họp")
r2.bold = True

add_khoan("1. Việc kiểm soát công tác tiếp nhận, tiến độ thụ lý hồ sơ thủ tục hành chính được thống kê báo cáo Lãnh đạo Chi nhánh hàng ngày qua điện thoại trước 17h, cụ thể: Lượng hồ sơ đã nhận, lượng hồ sơ đã giải quyết, lượng hồ sơ quá hạn đã giải quyết, lượng hồ sơ quá hạn chưa giải quyết. Số lượng hồ sơ được tổng hợp theo Ngày và luỹ kế từ ngày 01 của tháng cuối quý trước đến ngày cuối cùng của tháng thứ hai quý sau.")
add_khoan("2. Việc kiểm soát công tác tiếp nhận, tiến độ thụ lý hồ sơ dịch vụ được thống kê báo cáo Lãnh đạo Chi nhánh hàng tuần qua điện thoại trước 17h ngày thứ Sáu, cụ thể: Lượng hồ sơ đã nhận, lượng hồ sơ đã giải quyết, lượng hồ sơ quá hạn đã giải quyết, lượng hồ sơ quá hạn chưa giải quyết. Số lượng hồ sơ được tổng hợp theo Tuần và luỹ kế từ ngày 01 của tháng cuối quý trước đến ngày cuối cùng của tháng thứ hai quý sau.")
add_khoan("3. Lãnh đạo Chi nhánh và Tổ trưởng Tổ chuyên môn họp giao ban vào chiều thứ Hai hàng tuần. Tuỳ theo tình hình thực tế, yêu cầu công tác đột xuất sẽ điều chỉnh thời gian, hình thức giao ban cho phù hợp.")

# Điều 3
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Inches(0.5)
r1 = p.add_run("Điều 3. ")
r1.bold = True
r2 = p.add_run("Phân công nhiệm vụ của Giám đốc và các Phó Giám đốc")
r2.bold = True

add_khoan("1. Ông Nguyễn Chiến Thắng - Giám đốc Chi nhánh")
add_khoan("a) Phụ trách lãnh đạo, chỉ đạo, quản lý toàn bộ hoạt động của Chi nhánh Văn phòng Đăng ký đất đai số 23.")
add_khoan("b) Chịu trách nhiệm trước Giám đốc Sở Tài nguyên và Môi trường, Giám đốc Văn phòng Đăng ký đất đai về hoạt động của Chi nhánh Văn phòng Đăng ký đất đai số 23 từ ngày 01/10/2026.")
add_khoan("c) Trực tiếp chỉ đạo, điều hành, giải quyết hoạt động của Tổ Hành chính - Tổng hợp từ ngày 01/10/2026.")
add_khoan("d) Trực tiếp chỉ đạo, điều hành, giải quyết toàn bộ hoạt động của Tổ Đăng ký và cấp Giấy chứng nhận từ ngày 01/11/2026.")

add_khoan("2. Bà Nguyễn Thị Lệ Hằng - Phó Giám đốc Chi nhánh")
add_khoan("a) Trực tiếp chỉ đạo, điều hành, giải quyết toàn bộ hoạt động của Tổ Kỹ thuật địa chính và Lưu trữ đến hết ngày 30/11/2026.")
add_khoan("b) Thực hiện một số công việc khác do Giám đốc Nguyễn Chiến Thắng phân công.")
add_khoan("c) Ký và chịu trách nhiệm về quyết định của mình trước pháp luật, trước Giám đốc Văn phòng Đăng ký đất đai, trước Phó Giám đốc Văn phòng đăng ký đất đai – phụ trách Chi nhánh số 23 đối với văn bản, hồ sơ, tài liệu trong phạm vi, lĩnh vực, công việc được phân công.")

add_khoan("3. Ông Đặng Huy Cường - Phó Giám đốc Chi nhánh")
add_khoan("a) Trực tiếp điều hành, giải quyết toàn bộ hoạt động của Tổ Đăng ký và cấp Giấy chứng nhận đến hết ngày 31/10/2026.")
add_khoan("b) Thực hiện một số công việc khác do Giám đốc Nguyễn Chiến Thắng phân công.")
add_khoan("c) Ký và chịu trách nhiệm về quyết định của mình trước pháp luật, trước Giám đốc Văn phòng Đăng ký đất đai, trước Phó Giám đốc Văn phòng đăng ký đất đai – phụ trách Chi nhánh số 23 đối với văn bản, hồ sơ, tài liệu trong phạm vi, lĩnh vực, công việc được phân công.")

# Điều 4
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Inches(0.5)
r1 = p.add_run("Điều 4. ")
r1.bold = True
r2 = p.add_run("Tổ chức thực hiện")
r2.bold = True

add_khoan("Các ông (bà) Phó Giám đốc, Tổ trưởng các Tổ chuyên môn, cá nhân có liên quan chịu trách nhiệm thi hành Quyết định này, kể từ ngày ký./.")

# Chữ ký và nơi nhận
table2 = doc.add_table(rows=1, cols=2)
table2.alignment = WD_TABLE_ALIGNMENT.CENTER
table2.autofit = False
table2.columns[0].width = Inches(3.5)
table2.columns[1].width = Inches(3.5)

c1 = table2.cell(0,0)
c2 = table2.cell(0,1)
set_cell_border_none(c1)
set_cell_border_none(c2)

p_n = c1.paragraphs[0]
r = p_n.add_run("Nơi nhận:")
r.italic = True
r.bold = True
r.font.size = Pt(12)

def add_noi_nhan(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text)
    r.font.size = Pt(11)

add_noi_nhan(c1, "- Như Điều 4;")
add_noi_nhan(c1, "- Văn phòng ĐKĐĐ TP.HCM (để b/c);")
add_noi_nhan(c1, "- Lưu: VT, HC-TH.")

p_k = c2.paragraphs[0]
p_k.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_k.add_run("GIÁM ĐỐC")
r.bold = True
r.font.size = Pt(14)

p_k2 = c2.add_paragraph()
p_k2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_k2.add_run("\n\n\n\nNguyễn Chiến Thắng")
r.bold = True
r.font.size = Pt(14)

doc.save(doc_path)
