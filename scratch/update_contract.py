import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document('documents/HD_chinh_thuc_Do_Trong_Minh_Quan.docx')

# 1. Page Setup / Margins according to ND 30
sec = doc.sections[0]
sec.top_margin = Mm(20)
sec.bottom_margin = Mm(20)
sec.left_margin = Mm(30)
sec.right_margin = Mm(15)
sec.page_width = Mm(210)
sec.page_height = Mm(297)

# 2. Fix Table 0 (Header table)
t0 = doc.tables[0]
t0.alignment = WD_TABLE_ALIGNMENT.CENTER
t0.autofit = False

# Set column widths: Left 68mm, Right 97mm (Sum = 165mm)
col_widths = [Mm(68), Mm(97)]
for row in t0.rows:
    for idx, width in enumerate(col_widths):
        row.cells[idx].width = width

# In Table 0, ensure Quoc hieu is clean, 12pt bold, doesn't drop "NAM"
cell_right = t0.rows[0].cells[1]
for p in cell_right.paragraphs:
    if 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM' in p.text:
        p.text = 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        run = p.runs[0]
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
    elif 'Độc lập - Tự do - Hạnh phúc' in p.text:
        p.text = 'Độc lập - Tự do - Hạnh phúc'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.0
        run = p.runs[0]
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.underline = True
    elif 'Thành phố Hồ Chí Minh' in p.text:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            r.font.italic = True

cell_left = t0.rows[0].cells[0]
for p in cell_left.paragraphs:
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs:
        r.font.name = 'Times New Roman'
        if 'VĂN PHÒNG ĐĂNG KÝ' in p.text:
            r.font.size = Pt(12)
            r.font.bold = True
        elif 'SỞ NÔNG NGHIỆP' in p.text:
            r.font.size = Pt(12)
        elif 'Số:' in p.text:
            r.font.size = Pt(13)

# 3. Iterate through paragraphs to update content
paras_to_remove = []

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    
    # Remove Điện thoại and Mã số thuế for Bên B
    if text == 'Điện thoại: [Trống]':
        paras_to_remove.append(p)
    elif text == 'Mã số thuế (nếu có): [Trống]':
        paras_to_remove.append(p)
    
    # Update Chuyên ngành
    elif 'Chuyên ngành đào tạo:' in text and 'Kỹ thuật phần mềm' in text:
        p.text = 'Chuyên ngành đào tạo: Kỹ thuật phần mềm (Kỹ sư Kỹ thuật phần mềm)'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            
    # Update Trình độ tin học
    elif 'Trình độ tin học:' in text:
        p.text = 'Trình độ tin học: Thạc sĩ Kỹ sư phần mềm'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            
    # Update Trình độ ngoại ngữ
    elif 'Trình độ ngoại ngữ:' in text:
        p.text = 'Trình độ ngoại ngữ: B2'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            
    # Update Nhiệm vụ
    elif text.startswith('d) Nhiệm vụ:'):
        p.text = 'd) Nhiệm vụ: Thống kê, tổng hợp báo cáo số liệu; nghiên cứu, phát triển và quản trị vận hành các ứng dụng phần mềm, website cổng dịch vụ nội bộ và hệ thống phần mềm chuyên dụng của Chi nhánh; tham mưu các giải pháp công nghệ thông tin và chuyển đổi số; các công việc hành chính khác theo sự điều động của Giám đốc Chi nhánh Văn phòng đăng ký đất đai số 23.'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            
    # Update Điều 4: vi phạm
    elif 'khoản 2 Điều này' in text and 'Khi bên B vi phạm hợp đồng' in text:
        p.text = 'Khi bên B vi phạm hợp đồng thuộc một trong các trường hợp nêu trên thì tùy theo tính chất, mức độ vi phạm, bên A có quyền đơn phương chấm dứt hợp đồng lao động; xử lý kỷ luật lao động theo quy định của pháp luật và yêu cầu bên B bồi thường thiệt hại (nếu có).'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            
    # Update Điều 4: Bỏ câu thử việc
    elif 'Trong thời gian thử việc' in text:
        p.text = 'Việc giải quyết chế độ, chính sách đối với bên B khi chấm dứt hợp đồng lao động được thực hiện theo quy định của pháp luật về lao động.'
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)

# Perform paragraph deletions
for p in paras_to_remove:
    p._element.getparent().remove(p._element)

# Remove excessive trailing empty paragraphs at the end of the document
while len(doc.paragraphs) > 0 and not doc.paragraphs[-1].text.strip():
    p = doc.paragraphs[-1]
    p._element.getparent().remove(p._element)

# 4. Fix Table 1 (Signatures) widths and formatting
t1 = doc.tables[1]
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1.autofit = False
for row in t1.rows:
    row.cells[0].width = Mm(80)
    row.cells[1].width = Mm(85)
    for c in row.cells:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                if not r.font.size:
                    r.font.size = Pt(13)

# Save to OUTPUT
output_path = 'OUTPUT/HD_chinh_thuc_Do_Trong_Minh_Quan.docx'
doc.save(output_path)
print(f'Successfully saved to {output_path}')
