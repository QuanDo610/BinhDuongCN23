import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document('documents/HD_chinh_thuc_Do_Trong_Minh_Quan.docx')

# 1. Page Margins - Standard ND 30 (Top: 20mm, Bottom: 20mm, Left: 30mm, Right: 15mm)
sec = doc.sections[0]
sec.top_margin = Mm(20)
sec.bottom_margin = Mm(20)
sec.left_margin = Mm(30)
sec.right_margin = Mm(15)
sec.page_width = Mm(210)
sec.page_height = Mm(297)

# Helper function to enforce Times New Roman font on run
def enforce_font(run, font_name="Times New Roman", size_pt=None):
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    if size_pt:
        run.font.size = Pt(size_pt)

# 2. Table 0 (Header: Agency & National Motto)
t0 = doc.tables[0]
t0.alignment = WD_TABLE_ALIGNMENT.CENTER
t0.autofit = False

col_widths = [Mm(68), Mm(97)]
for row in t0.rows:
    for idx, width in enumerate(col_widths):
        row.cells[idx].width = width

# Left cell: Agency name
cell_left = t0.rows[0].cells[0]
for p in cell_left.paragraphs:
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs:
        if 'VĂN PHÒNG ĐĂNG KÝ' in p.text:
            enforce_font(r, "Times New Roman", 12)
            r.font.bold = True
        elif 'SỞ NÔNG NGHIỆP' in p.text:
            enforce_font(r, "Times New Roman", 12)
        elif 'Số:' in p.text:
            enforce_font(r, "Times New Roman", 13)
        else:
            enforce_font(r, "Times New Roman")

# Right cell: National motto
cell_right = t0.rows[0].cells[1]
for p in cell_right.paragraphs:
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    if 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM' in p.text:
        p.text = 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.runs[0]
        enforce_font(run, "Times New Roman", 12)
        run.font.bold = True
    elif 'Độc lập - Tự do - Hạnh phúc' in p.text:
        p.text = 'Độc lập - Tự do - Hạnh phúc'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.runs[0]
        enforce_font(run, "Times New Roman", 13)
        run.font.bold = True
        run.font.underline = True
    elif 'Thành phố Hồ Chí Minh' in p.text:
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            r.font.italic = True

# 3. Body Paragraphs Processing
paras_to_remove = []

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    
    # Remove Điện thoại & Mã số thuế for Bên B
    if text == 'Điện thoại: [Trống]' or text == 'Mã số thuế (nếu có): [Trống]':
        paras_to_remove.append(p)
        continue
        
    # Update Chuyên ngành
    if 'Chuyên ngành đào tạo:' in text and 'Kỹ thuật phần mềm' in text:
        p.text = 'Chuyên ngành đào tạo: Kỹ thuật phần mềm (Kỹ sư Kỹ thuật phần mềm)'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    # Update Trình độ tin học
    elif 'Trình độ tin học:' in text:
        p.text = 'Trình độ tin học: Thạc sĩ Kỹ sư phần mềm'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    # Update Trình độ ngoại ngữ
    elif 'Trình độ ngoại ngữ:' in text:
        p.text = 'Trình độ ngoại ngữ: B2'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    # Update Điểm d Điều 1 (Nhiệm vụ)
    elif text.startswith('d) Nhiệm vụ:'):
        p.text = 'd) Nhiệm vụ: Thống kê, tổng hợp báo cáo số liệu; nghiên cứu, phát triển và quản trị vận hành các ứng dụng phần mềm, website cổng dịch vụ nội bộ và hệ thống phần mềm chuyên dụng của Chi nhánh; tham mưu các giải pháp công nghệ thông tin và chuyển đổi số; các công việc hành chính khác theo sự điều động của Giám đốc Chi nhánh Văn phòng đăng ký đất đai số 23.'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    # Update Điều 4: Vi phạm hợp đồng
    elif 'khoản 2 Điều này' in text and 'Khi bên B vi phạm hợp đồng' in text:
        p.text = 'Khi bên B vi phạm hợp đồng thuộc một trong các trường hợp nêu trên thì tùy theo tính chất, mức độ vi phạm, bên A có quyền đơn phương chấm dứt hợp đồng lao động; xử lý kỷ luật lao động theo quy định của pháp luật và yêu cầu bên B bồi thường thiệt hại (nếu có).'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    # Update Điều 4: Xóa triệt để câu thử việc
    elif 'Trong thời gian thử việc' in text:
        p.text = 'Việc giải quyết chế độ, chính sách đối với bên B khi chấm dứt hợp đồng lao động được thực hiện theo quy định của pháp luật về lao động.'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            enforce_font(r, "Times New Roman", 13)
            
    else:
        # Enforce Times New Roman on all remaining body runs
        for r in p.runs:
            enforce_font(r, "Times New Roman")

# Remove paragraphs
for p in paras_to_remove:
    p._element.getparent().remove(p._element)

# Remove trailing empty paragraphs
while len(doc.paragraphs) > 0 and not doc.paragraphs[-1].text.strip():
    p = doc.paragraphs[-1]
    p._element.getparent().remove(p._element)

# 4. Table 1 (Signatures)
t1 = doc.tables[1]
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1.autofit = False
for row in t1.rows:
    row.cells[0].width = Mm(80)
    row.cells[1].width = Mm(85)
    for c in row.cells:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            for r in p.runs:
                enforce_font(r, "Times New Roman", 13)

# Save output
output_path = 'OUTPUT/HD_chinh_thuc_Do_Trong_Minh_Quan.docx'
doc.save(output_path)
print(f'Successfully finalized and saved to {output_path}')
