#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_all_templates.py
Tạo trọn bộ tài liệu:
1. OUTPUT/SO_THEO_DOI_TIEP_CONG_DAN_ND154_ND30.docx (Mẫu theo dõi thực tế chuẩn Nghị định 30, lặp header từng trang)
2. OUTPUT/MAU_03_TCD_SO_TIEP_CONG_DAN_NGUYEN_BAN_ND154.docx (Mẫu số 03/TCD 13 cột nguyên bản NĐ 154)
3. OUTPUT/SO_THEO_DOI_TIEP_CONG_DAN_ND154.xlsx (Bản Excel điện tử phục vụ quản lý, lọc dữ liệu)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_expanded_logbook_docx(output_path: str):
    doc = docx.Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width = Inches(11.69)
    sec.page_height = Inches(8.27)
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.79)
    sec.left_margin = Inches(0.98)
    sec.right_margin = Inches(0.59)
    
    # Số trang Header NĐ 30 (không hiện ở trang 1)
    sec.different_first_page_header_footer = True
    header = sec.header
    header.is_linked_to_previous = False
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(0)
    fld = parse_xml(
        r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr>'
        r'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        r'<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w')
    )
    p_hdr._p.append(fld)

    # docDefaults
    styles_el = doc.styles.element
    old_docDefaults = styles_el.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}docDefaults')
    if old_docDefaults is not None:
        styles_el.remove(old_docDefaults)
    new_docDefaults = parse_xml(
        f'<w:docDefaults {nsdecls("w")}>'
        f'  <w:rPrDefault>'
        f'    <w:rPr>'
        f'      <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        f'      <w:sz w:val="26"/>'
        f'      <w:szCs w:val="26"/>'
        f'      <w:color w:val="000000"/>'
        f'      <w:lang w:val="vi-VN"/>'
        f'    </w:rPr>'
        f'  </w:rPrDefault>'
        f'  <w:pPrDefault>'
        f'    <w:pPr>'
        f'      <w:spacing w:before="0" w:after="80" w:line="240" w:lineRule="auto"/>'
        f'    </w:pPr>'
        f'  </w:pPrDefault>'
        f'</w:docDefaults>'
    )
    styles_el.insert(0, new_docDefaults)

    def add_divider_line(cell_or_doc, length_type="nation"):
        p = cell_or_doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pPr = p._p.get_or_add_pPr()
        sp = parse_xml(r'<w:spacing %s w:before="0" w:after="80" w:line="120" w:lineRule="exact"/>' % nsdecls('w'))
        pPr.append(sp)
        dash_count = 18 if length_type == "nation" else 8
        r = p.add_run("—" * dash_count)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        return p

    def set_borderless(table):
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                tcBorders = parse_xml(
                    f'<w:tcBorders {nsdecls("w")}>'
                    f'<w:top w:val="none"/><w:left w:val="none"/>'
                    f'<w:bottom w:val="none"/><w:right w:val="none"/>'
                    f'</w:tcBorders>'
                )
                tcPr.append(tcBorders)

    def set_cell_margins(cell, top=60, bottom=60, left=70, right=70):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_table_borders(table, color="000000", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # 1. Header cơ quan & Quốc hiệu
    hdr_table = doc.add_table(rows=1, cols=2)
    hdr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_table.autofit = False
    set_borderless(hdr_table)
    
    c_left = hdr_table.rows[0].cells[0]
    c_right = hdr_table.rows[0].cells[1]
    c_left.width = Inches(4.5)
    c_right.width = Inches(5.6)
    set_cell_margins(c_left, top=0, bottom=30, left=0, right=20)
    set_cell_margins(c_right, top=0, bottom=30, left=20, right=0)
    
    p1 = c_left.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.0
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TỈNH BÌNH DƯƠNG")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    
    p2 = c_left.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.line_spacing = 1.0
    p2.paragraph_format.space_after = Pt(2)
    r2 = p2.add_run("BỘ PHẬN TIẾP CÔNG DÂN")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.bold = True
    
    add_divider_line(c_left, length_type="agency")
    
    p3 = c_left.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.line_spacing = 1.0
    p3.paragraph_format.space_before = Pt(4)
    p3.paragraph_format.space_after = Pt(0)
    r3 = p3.add_run("Mẫu số: 03/TCD")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(11)
    r3.font.italic = True
    r3.font.bold = True
    
    p4 = c_right.paragraphs[0]
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p4.paragraph_format.line_spacing = 1.0
    p4.paragraph_format.space_after = Pt(2)
    r4 = p4.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM")
    r4.font.name = "Times New Roman"
    r4.font.size = Pt(13)
    r4.font.bold = True
    
    p5 = c_right.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p5.paragraph_format.line_spacing = 1.0
    p5.paragraph_format.space_after = Pt(2)
    r5 = p5.add_run("Độc lập - Tự do - Hạnh phúc")
    r5.font.name = "Times New Roman"
    r5.font.size = Pt(13)
    r5.font.bold = True
    
    add_divider_line(c_right, length_type="nation")
    
    p6 = c_right.add_paragraph()
    p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p6.paragraph_format.line_spacing = 1.0
    p6.paragraph_format.space_before = Pt(4)
    p6.paragraph_format.space_after = Pt(0)
    r6 = p6.add_run("Bình Dương, ngày      tháng      năm 2026")
    r6.font.name = "Times New Roman"
    r6.font.size = Pt(12)
    r6.font.italic = True
    
    # 2. Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing = 1.15
    r_t = p_title.add_run("SỔ THEO DÕI TIẾP CÔNG DÂN")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("(Theo dõi ngày công dân đến, Lãnh đạo chủ trì tiếp, Nội dung trao đổi, Quá trình xử lý và Kết quả giải quyết)")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    
    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref.paragraph_format.space_before = Pt(0)
    p_ref.paragraph_format.space_after = Pt(8)
    r_ref = p_ref.add_run("Căn cứ Nghị định số 154/2026/NĐ-CP của Chính phủ & Thể thức văn bản Nghị định số 30/2020/NĐ-CP")
    r_ref.font.name = "Times New Roman"
    r_ref.font.size = Pt(10.5)
    r_ref.font.italic = True
    
    # 3. Main Table
    col_widths_in = [0.38, 0.75, 1.15, 1.35, 1.95, 1.50, 1.40, 1.25, 0.45]
    
    cases = [
        (
            "1",
            "08:30\n05/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Lê Thị Mai - Tổ HCTH)",
            "Ông Nguyễn Văn Thành\nCCCD: 074082001234\nĐịa chỉ: P. Phú Hòa, TP. Thủ Dầu Một\nSĐT: 0913.456.789\n(01 người)",
            "- Nội dung trao đổi: Khiếu nại hồ sơ xin chuyển mục đích sử dụng 150m² đất nông nghiệp sang đất ở và cấp đổi GCN bị trễ hạn 15 ngày so với phiếu hẹn. Công dân cần GCN để vay vốn ngân hàng.\n- Loại đơn: Khiếu nại.",
            "- Lãnh đạo kết luận: Thuộc thẩm quyền giải quyết (Mẫu 03/TCD: đánh dấu x).\n- Chỉ đạo: Nhận trách nhiệm về việc trễ hẹn; giao Tổ Đăng ký kiểm tra ngay quy hoạch phân khu 1/2000 và hoàn tất hồ sơ trình ký trong 03 ngày làm việc.",
            "- Ngày 06/10: Tổ Kỹ thuật kiểm tra thực địa và hồ sơ địa chính.\n- Ngày 07/10: Lập phiếu chuyển thông tin nghĩa vụ tài chính sang Chi cục Thuế.\n- Ngày 08/10: Chi cục Thuế ra thông báo nộp thuế.",
            "- Đã giải quyết xong.\n- Ban hành TB số 142/TB-VPĐK ngày 09/10/2026.\n- Đã trao GCN mới cho công dân vào ngày 12/10/2026.\n- Công dân đồng thuận, hài lòng.",
            "Lưu hồ sơ: 142/KN"
        ),
        (
            "2",
            "09:45\n08/10/2026",
            "Đ/c Nguyễn Thị Lan\n- Phó Giám đốc Chi nhánh\n(Cán bộ phối hợp: Phạm Văn Tuấn - Tổ KTĐC)",
            "Bà Lê Thị Bích\nCCCD: 074185002345\nĐịa chỉ: P. Tân An, TP. Thủ Dầu Một\nSĐT: 0988.123.456\n(01 người)",
            "- Nội dung trao đổi: Phản ánh hộ liền kề (ông Đỗ Văn H) tự ý xây hàng rào bê tông lấn chiếm 0.8m vào lối đi chung đã có trên bản đồ địa chính từ năm 2010. Đề nghị chi nhánh đo đạc hiện trạng và trích lục hồ sơ.\n- Loại đơn: Kiến nghị, phản ánh.",
            "- Lãnh đạo kết luận: Chấp thuận đo đạc trích lục bản đồ phục vụ giải quyết lối đi chung.\n- Hướng xử lý: Hướng dẫn thẩm quyền hòa giải tranh chấp đất đai thuộc UBND phường Tân An (Điều 235 Luật Đất đai).",
            "- Ngày 12/10: Cán bộ địa chính phối hợp UBND phường Tân An đo đạc hiện trạng ranh giới thực địa có 2 hộ chứng kiến.\n- Ngày 16/10: Lập biên bản đo đạc xác định phần chồng lấn 0.82m vào lối đi chung.",
            "- Đã giải quyết xong.\n- Ban hành Văn bản trích sao số 856/VPĐK-KT ngày 18/10/2026 chuyển UBND P. Tân An.\n- UBND phường đã hòa giải thành công, hộ ông H tự tháo dỡ phần vi phạm.",
            "Lưu hồ sơ: 856/PA"
        ),
        (
            "3",
            "14:00\n12/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Hoàng Văn Nam - Đại diện HĐBT)",
            "Đoàn 04 hộ dân\n(Đại diện: Ông Phan Đình Trọng)\nCCCD: 074075003456\nĐịa chỉ: P. Hiệp Thành, TP. TDM\nSĐT: 0903.789.012\n(Số lượng: 04 người)",
            "- Nội dung trao đổi: Khiếu nại phương án bồi thường, hỗ trợ Dự án Nâng cấp Quốc lộ 13; kiến nghị đơn giá đền bù đất thổ cư thấp hơn thực tế và đề nghị bố trí thêm 01 suất tái định cư cho hộ phụ.\n- Loại đơn: Khiếu nại đông người.",
            "- Lãnh đạo kết luận: Đối thoại, lắng nghe từng hộ; giải thích rõ khung chính sách bồi thường theo bảng giá đất tỉnh.\n- Hướng xử lý: Chuyển văn bản kiến nghị đến Hội đồng BTGPMB TP. Thủ Dầu Một rà soát lại hiện trạng tài sản trên đất.",
            "- Ngày 14/10: Phát hành VB số 1024/VPĐK chuyển đơn đến Hội đồng Bồi thường TP. Thủ Dầu Một.\n- Ngày 19/10: Hội đồng bồi thường tổ chức kiểm đếm bổ sung tài sản cây trồng và công trình phụ.",
            "- Đã giải quyết xong.\n- UBND TP ban hành TB số 389/TB-UBND ngày 23/10/2026 phê duyệt bổ sung kinh phí bồi thường tài sản; giải thích rõ tiêu chí xét cấp suất tái định cư phụ.\n- Các hộ đồng thuận nhận tiền đợt 2.",
            "Vụ việc đông người phức tạp"
        ),
        (
            "4",
            "08:30\n15/10/2026",
            "Đ/c Võ Thành Nam\n- Phó Chủ tịch UBND tỉnh\n(Tiếp trực tuyến: Ban TCD tỉnh, Sở TN&MT, Chi nhánh)",
            "Bà Vũ Thị Hoài\nCCCD: 074180004567\nĐịa chỉ: Xã An Tây, TX. Bến Cát\nSĐT: 0979.234.567\n(Tiếp trực tuyến - 02 người)",
            "- Nội dung trao đổi: Phiên tiếp dân trực tuyến theo Chương V Nghị định 154/2026/NĐ-CP. Công dân phản ánh việc cấp GCN đất khai hoang trước 1993 bị ách tắc do hồ sơ địa chính qua các thời kỳ có sự sai lệch thông tin tờ thửa.\n- Loại đơn: Kiến nghị, phản ánh.",
            "- Lãnh đạo kết luận: Ghi âm, ghi hình trực tuyến lưu trữ bảo mật (Điều 24 NĐ 154). Giao Thanh tra tỉnh phối hợp Chi nhánh VPĐKĐĐ Bến Cát rà soát đối chiếu hồ sơ địa chính gốc năm 1993, báo cáo trước 10/11/2026.",
            "- Ngày 16/10: Ban TCD tỉnh phát hành TB kết luận số 215/TB-UBND.\n- Ngày 20/10: Đoàn liên ngành kiểm tra thực địa, lấy ý kiến nhân chứng khu dân cư xác nhận sử dụng đất ổn định, không tranh chấp.",
            "- Đang giải quyết theo lộ trình.\n- Thanh tra tỉnh đã có Báo cáo số 88/BC-TTr khẳng định đủ điều kiện công nhận QSDĐ.\n- Chi nhánh Bến Cát đang hoàn tất thủ tục cấp GCN, dự kiến trao vào ngày 10/11/2026.",
            "Tiếp trực tuyến kết nối điểm cầu"
        ),
        (
            "5",
            "15:30\n18/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Nguyễn Văn Bình - TT Nhân dân)",
            "Ông Đặng Quốc Huy\nCCCD: 074090005678\nĐịa chỉ: P. Phú Lợi, TP. Thủ Dầu Một\n(Đơn tố cáo - Giữ bí mật nhân thân theo Điều 4 NĐ 154)",
            "- Nội dung trao đổi: Tố cáo viên chức đo đạc chi nhánh có hành vi gợi ý vòi vĩnh chi phí bồi dưỡng khi đo đạc tách thửa đất số 45, tờ bản đồ 12. Công dân cung cấp tin nhắn và chứng từ ghi âm đối chất.\n- Loại đơn: Tố cáo cán bộ.",
            "- Lãnh đạo kết luận: Bảo mật thông tin người tố cáo. Lập Giấy biên nhận tài liệu theo Mẫu số 02/TCD ban hành kèm NĐ 154.\n- Chỉ đạo: Giao Tổ Giám sát nội bộ thụ lý kiểm tra kỷ luật nghiêm trong 07 ngày, không bao che.",
            "- Ngày 20/10: Ban hành Quyết định xác minh số 88/QĐ-CN23.\n- Ngày 22/10: Làm việc trực tiếp với viên chức bị tố cáo, viên chức đã tường trình thừa nhận vi phạm quy chế.",
            "- Đã giải quyết xong.\n- Ban hành QĐ kỷ luật Cảnh cáo đối với viên chức, điều chuyển công tác khác.\n- Ngày 25/10: Giám đốc ký Kết luận tố cáo số 12/KL-CN23 thông báo kết quả cho công dân.",
            "Bảo mật tài liệu theo Mẫu 02/TCD"
        ),
        (
            "6",
            "10:15\n21/10/2026",
            "Đ/c Nguyễn Thị Lan\n- Phó Giám đốc Chi nhánh\n(Cán bộ phối hợp: Cán bộ tiếp dân thường trực)",
            "Ông Lý Văn Đạt\nCCCD: 074068006789\nĐịa chỉ: P. Chánh Nghĩa, TP. TDM\nSĐT: 0918.999.888\n(01 người)",
            "- Nội dung trao đổi: Yêu cầu đòi lại 500m² đất nông nghiệp do ông bà để lại từ trước năm 1975. Vụ việc này đã được UBND TP và UBND tỉnh giải quyết khiếu nại lần 1, lần 2 đúng pháp luật; công dân không có tình tiết mới.\n- Loại đơn: Khiếu nại đã hết thẩm quyền.",
            "- Lãnh đạo kết luận: Áp dụng Điểm h Khoản 1 Điều 4 Nghị định 154/2026/NĐ-CP: Từ chối tiếp công dân do vụ việc đã được cơ quan thẩm quyền giải quyết đúng chính sách pháp luật và không có chứng cứ mới.\n- Chỉ đạo: Ban hành Thông báo từ chối tiếp công dân.",
            "- Cán bộ tiếp dân giải thích trực tiếp căn cứ pháp luật cho công dân tại bàn tiếp dân.\n- Lập hồ sơ trình ban hành Thông báo theo Mẫu số 01/TCD ban hành kèm NĐ 154 trong thời hạn 03 ngày làm việc.",
            "- Đã xử lý xong.\n- Ngày 23/10/2026: Ban hành Thông báo từ chối tiếp công dân số 68/TB-CN23 (theo Mẫu 01/TCD) giao cho công dân và gửi báo cáo Ban Tiếp công dân cấp trên.",
            "Ban hành Mẫu 01/TCD NĐ 154"
        ),
        (
            "7",
            "09:00\n23/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Đỗ Thị Cúc - Tổ Hành chính)",
            "Bà Mai Thị Hồng Loan\nCCCD: 074192007890\nĐịa chỉ: P. Phú Lợi, TP. Thủ Dầu Một\nSĐT: 0933.222.111\n(01 người)",
            "- Nội dung trao đổi: Đề nghị đính chính thông tin số căn cước công dân và cập nhật diện tích tăng thêm do đo đạc lại trên GCN quyền sở hữu nhà ở và đất ở số BD 123456.\n- Loại đơn: Kiến nghị giải quyết TTHC.",
            "- Lãnh đạo kết luận: Hồ sơ rõ ràng, thuộc thẩm quyền giải quyết ngay (Khoản 3 Điều 25 NĐ 154).\n- Chỉ đạo: Tiếp nhận hồ sơ trực tiếp, hẹn thời gian trả kết quả sau 03 ngày làm việc (không yêu cầu nộp thêm giấy tờ thừa).",
            "- Ngày 23/10: Cán bộ tiếp nhận vào sổ và chuyển ngay cho Tổ Đăng ký biến động.\n- Ngày 24/10: Tổ Đăng ký in trang bổ sung đính chính thông tin CCCD và diện tích.",
            "- Đã giải quyết xong.\n- Trao GCN đã đính chính cho bà Loan vào ngày 26/10/2026.\n- Bà Loan ký nhận và đánh giá rất hài lòng trên Cổng Dịch vụ công.",
            "Giải quyết nhanh trong 3 ngày"
        ),
        (
            "8",
            "14:30\n24/10/2026",
            "Đ/c Nguyễn Thị Lan\n- Phó Giám đốc Chi nhánh\n(Cán bộ phối hợp: Tổ Kỹ thuật địa chính)",
            "Ông Huỳnh Tấn Phát\nCCCD: 074085008901\nĐịa chỉ: P. Định Hòa, TP. Thủ Dầu Một\nSĐT: 0908.333.444\n(01 người)",
            "- Nội dung trao đổi: Phản ánh việc cán bộ tiếp nhận tại Bộ phận Một cửa yêu cầu cung cấp trích lục khai sinh của cha mẹ khi làm thủ tục thừa kế nhà đất là gây khó khăn, không đúng danh mục TTHC công bố.\n- Loại đơn: Phản ánh thủ tục hành chính.",
            "- Lãnh đạo kết luận: Tiếp thu phản ánh; đối chiếu quy định tại Nghị định hướng dẫn Luật Đất đai mới, việc liên thông dữ liệu dân cư VNeID đã thay thế giấy tờ hộ tịch giấy tờ cũ.\n- Chỉ đạo: Chấn chỉnh ngay bộ phận tiếp nhận.",
            "- Phó Giám đốc trực tiếp hướng dẫn cán bộ Một cửa tra cứu CSDL Quốc gia về dân cư để hoàn thiện hồ sơ nhận thừa kế cho ông Phát.\n- Tiếp nhận ngay hồ sơ thừa kế trong buổi chiều 24/10.",
            "- Đã giải quyết xong.\n- Hồ sơ đã được chuyển thụ lý theo đúng quy trình hẹn trả ngày 03/11/2026.\n- Công dân cảm ơn sự chỉ đạo sâu sát kịp thời của Lãnh đạo.",
            "Cải cách TTHC & Đề án 06"
        ),
        (
            "9",
            "08:45\n25/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Trưởng phòng Tài chính)",
            "Ông Lương Gia Bảo\nCCCD: 074078009012\nĐịa chỉ: P. Hòa Phú, TP. Thủ Dầu Một\nSĐT: 0945.666.777\n(01 người)",
            "- Nội dung trao đổi: Kiến nghị xem xét lại cách tính tiền sử dụng đất khi chuyển mục đích 80m² đất vườn sang đất ở tại vị trí đường số 7, cho rằng áp dụng sai hệ số điều chỉnh vị trí hẻm.\n- Loại đơn: Kiến nghị nghĩa vụ tài chính.",
            "- Lãnh đạo kết luận: Tiếp nhận đơn kiến nghị; giải thích thẩm quyền quyết định hệ số giá đất và thông báo thuế thuộc Chi cục Thuế khu vực.\n- Hướng xử lý: Có phiếu rà soát vị trí đất gửi Chi cục Thuế để phối hợp kiểm tra.",
            "- Ngày 25/10: Phát hành Phiếu phối hợp thông tin số 312/PPH-VPĐK gửi Chi cục Thuế rà soát lại thông tin vị trí tuyến đường và độ rộng lộ giới.\n- Chi cục Thuế đối chiếu lại Quyết định bảng giá đất.",
            "- Đang giải quyết.\n- Chi cục Thuế đang tính lại nghĩa vụ tài chính theo vị trí hẻm cấp 2, dự kiến ban hành thông báo thuế điều chỉnh giảm vào ngày 28/10/2026.",
            "Phối hợp liên ngành Thuế - Đất đai"
        ),
        (
            "10",
            "15:00\n26/10/2026",
            "Đ/c Nguyễn Thị Lan\n- Phó Giám đốc Chi nhánh\n(Cán bộ phối hợp: Cán bộ tiếp dân thường trực)",
            "Bà Hoàng Diệu Linh\nCCCD: 074198000123\nĐịa chỉ: P. Phú Cường, TP. Thủ Dầu Một\nSĐT: 0912.888.999\n(01 người)",
            "- Nội dung trao đổi: Hỏi về thủ tục xin cấp lại GCN quyền sử dụng đất bị thất lạc do hỏa hoạn và thời gian niêm yết công khai tại UBND phường theo quy định mới.\n- Loại đơn: Kiến nghị, hướng dẫn thủ tục.",
            "- Lãnh đạo kết luận: Thuộc trường hợp hướng dẫn trực tiếp (Mẫu 03/TCD cột 10).\n- Chỉ đạo: Cán bộ tiếp dân cung cấp biểu mẫu đơn cớ mất, hướng dẫn thủ tục niêm yết 15 ngày tại phường theo Luật Đất đai 2024.",
            "- Cán bộ tiếp dân trực tiếp in biểu mẫu, hỗ trợ bà Linh điền thông tin và ký xác nhận.\n- Cung cấp số điện thoại đường dây nóng hỗ trợ khi nộp hồ sơ.",
            "- Đã giải quyết xong.\n- Đã hướng dẫn chi tiết bằng văn bản tóm tắt quy trình TTHC số 15/HD-VPĐK ngày 26/10/2026.\n- Công dân nắm rõ thủ tục và chuẩn bị hồ sơ niêm yết.",
            "Hướng dẫn TTHC tận tình"
        ),
        ("11", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("12", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("13", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("14", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("15", "....:....\n..../..../2026", "", "", "", "", "", "")
    ]
    
    total_rows = 3 + len(cases)
    total_cols = len(col_widths_in)
    
    main_table = doc.add_table(rows=total_rows, cols=total_cols)
    main_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    main_table.autofit = False
    set_table_borders(main_table, color="000000", sz="4")
    
    # tblHeader & cantSplit cho 3 hàng header
    for r_h_idx in [0, 1, 2]:
        r_h = main_table.rows[r_h_idx]
        trPr = r_h._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def format_cell(cell, text, font_size=10.0, bold=True, bg_color="F2F4F7", align=WD_ALIGN_PARAGRAPH.CENTER):
        set_cell_margins(cell, top=70, bottom=70, left=50, right=50)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if bg_color:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
            tcPr.append(shd)
            
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        
        # Xóa các run cũ nếu có
        p.text = ""
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold

    row0 = main_table.rows[0]
    row1 = main_table.rows[1]
    
    # Hàng 0: Đặt text ban đầu
    format_cell(row0.cells[0], "STT", font_size=10.5)
    format_cell(row0.cells[1], "THÔNG TIN BUỔI TIẾP", font_size=10.5)
    format_cell(row0.cells[2], "", font_size=10.5) # Để trống trước khi merge
    format_cell(row0.cells[3], "THÔNG TIN CÔNG DÂN\n(Họ tên, CCCD/SĐT, Địa chỉ)", font_size=10.0)
    format_cell(row0.cells[4], "NỘI DUNG VỤ VIỆC & TRAO ĐỔI\n(Tóm tắt nội dung đối thoại, loại đơn)", font_size=10.0)
    format_cell(row0.cells[5], "CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT", font_size=10.5)
    format_cell(row0.cells[6], "", font_size=10.5) # Để trống trước khi merge
    format_cell(row0.cells[7], "", font_size=10.5) # Để trống trước khi merge
    format_cell(row0.cells[8], "GHI CHÚ\n(Hồ sơ lưu)", font_size=10.0)
    
    # Hàng 1: Đặt text cho các ô con
    format_cell(row1.cells[0], "", font_size=10.0) # Để trống trước khi merge dọc
    format_cell(row1.cells[1], "Thời gian tiếp\n(Ngày, giờ)", font_size=9.5)
    format_cell(row1.cells[2], "Lãnh đạo chủ trì &\nCán bộ phối hợp tiếp", font_size=9.5)
    format_cell(row1.cells[3], "", font_size=10.0) # Để trống trước khi merge dọc
    format_cell(row1.cells[4], "", font_size=10.0) # Để trống trước khi merge dọc
    format_cell(row1.cells[5], "Chỉ đạo của Lãnh đạo &\nHướng xử lý (Mẫu 03/TCD)", font_size=9.5)
    format_cell(row1.cells[6], "Quá trình theo dõi, thụ lý\n& Đơn vị giải quyết", font_size=9.5)
    format_cell(row1.cells[7], "Kết quả giải quyết\n(Văn bản & Ngày trả lời)", font_size=9.5)
    format_cell(row1.cells[8], "", font_size=10.0) # Để trống trước khi merge dọc
    
    # Merge ngang hàng 0
    row0.cells[1].merge(row0.cells[2])
    row0.cells[5].merge(row0.cells[6]).merge(row0.cells[7])
    
    # Merge dọc giữa hàng 0 và hàng 1
    row0.cells[0].merge(row1.cells[0])
    row0.cells[3].merge(row1.cells[3])
    row0.cells[4].merge(row1.cells[4])
    row0.cells[8].merge(row1.cells[8])

    # Hàng 2: Đánh số thứ tự các cột (1) đến (9)
    row2 = main_table.rows[2]
    col_labels = ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)"]
    for idx, lbl in enumerate(col_labels):
        format_cell(row2.cells[idx], lbl, font_size=9.0, bold=False, bg_color="EAECEF")

    # Dữ liệu các hàng
    for case_idx, case_data in enumerate(cases):
        r_row = main_table.rows[3 + case_idx]
        trPr = r_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        row_bg = "FAFAFB" if case_idx % 2 == 1 else "FFFFFF"
        
        for col_idx, cell_value in enumerate(case_data):
            cell = r_row.cells[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            
            if row_bg != "FFFFFF":
                tcPr = cell._tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{row_bg}"/>')
                tcPr.append(shd)
                
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            
            if col_idx in [0, 1, 8]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            lines = cell_value.split('\n')
            p.text = "" # Clear default text
            for l_i, line in enumerate(lines):
                if l_i > 0:
                    p = cell.add_paragraph()
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(2)
                    if col_idx in [0, 1, 8]:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        
                r = p.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                
                if col_idx == 0:
                    r.font.bold = True
                elif col_idx == 2 and ("Đ/c" in line or "Lãnh đạo" in line):
                    r.font.bold = True
                elif col_idx == 3 and ("Ông" in line or "Bà" in line or "Đoàn" in line):
                    r.font.bold = True
                elif col_idx in [4, 5, 6, 7] and (line.startswith("- Lãnh đạo") or line.startswith("- Đã giải quyết") or line.startswith("- Nội dung") or line.startswith("- Loại đơn")):
                    r.font.bold = True
                    if "Đã giải quyết xong" in line:
                        r.font.color.rgb = RGBColor(0, 100, 0)
                    elif "Đang giải quyết" in line:
                        r.font.color.rgb = RGBColor(180, 80, 0)

    for row in main_table.rows:
        for idx, w in enumerate(col_widths_in):
            row.cells[idx].width = Inches(w)

    # 4. Hướng dẫn ghi sổ
    p_note_title = doc.add_paragraph()
    p_note_title.paragraph_format.space_before = Pt(12)
    p_note_title.paragraph_format.space_after = Pt(2)
    r_nt = p_note_title.add_run("Hướng dẫn ghi sổ (Căn cứ Mẫu số 03/TCD ban hành kèm Nghị định số 154/2026/NĐ-CP):")
    r_nt.font.name = "Times New Roman"
    r_nt.font.size = Pt(10)
    r_nt.font.bold = True
    r_nt.font.italic = True
    
    notes = [
        "(1) Số thứ tự ghi liên tục theo từng năm quản lý tiếp công dân.",
        "(2) Ghi rõ giờ và ngày, tháng, năm tiếp công dân (định kỳ hoặc đột xuất).",
        "(3) Họ tên, chức vụ của Lãnh đạo cơ quan chủ trì buổi tiếp (Giám đốc, Phó Giám đốc, Chủ tịch, Phó Chủ tịch...) và cán bộ chuyên môn được phân công cùng dự.",
        "(4) Ghi đầy đủ họ tên, số CCCD/Định danh cá nhân, nơi cư trú, số điện thoại liên lạc của công dân; trường hợp nhiều người cùng khiếu nại về 1 nội dung thì cử người đại diện và ghi rõ số lượng người tham dự.",
        "(5) Tóm tắt cô đọng, trung thực nội dung trình bày, kiến nghị, phản ánh hoặc khiếu nại, tố cáo của công dân; phân loại chính xác tính chất vụ việc.",
        "(6) Ý kiến chỉ đạo kết luận của Lãnh đạo chủ trì tại buổi tiếp; phân loại hướng xử lý theo Mẫu 03/TCD (Thụ lý giải quyết / Hướng dẫn công dân / Chuyển đơn đến cơ quan có thẩm quyền / Vụ việc đã giải quyết hết thẩm quyền).",
        "(7) Phân công cụ thể phòng, ban, đơn vị hoặc cán bộ thụ lý theo dõi; ghi chép chi tiết tiến độ xác minh thực địa, đôn đốc giải quyết.",
        "(8) Ghi rõ số hiệu, ngày ban hành Thông báo Kết luận tiếp công dân, Văn bản trả lời hoặc Quyết định giải quyết; ngày gửi trả lời công dân; cập nhật trạng thái đã giải quyết xong hay đang xử lý.",
        "(9) Ký nhận của công dân hoặc ghi chú lưu trữ số hồ sơ phục vụ tra cứu trên Cơ sở dữ liệu quốc gia về tiếp công dân theo Điều 27 Nghị định 154/2026/NĐ-CP."
    ]
    for n in notes:
        pn = doc.add_paragraph()
        pn.paragraph_format.line_spacing = 1.05
        pn.paragraph_format.space_before = Pt(0)
        pn.paragraph_format.space_after = Pt(1)
        pn.paragraph_format.left_indent = Inches(0.2)
        rn = pn.add_run(n)
        rn.font.name = "Times New Roman"
        rn.font.size = Pt(9.5)
        rn.font.italic = True

    # 5. Chân trang chữ ký
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    set_borderless(sig_table)
    
    c_sig_left = sig_table.rows[0].cells[0]
    c_sig_right = sig_table.rows[0].cells[1]
    c_sig_left.width = Inches(4.5)
    c_sig_right.width = Inches(5.6)
    set_cell_margins(c_sig_left, top=80, bottom=40, left=0, right=20)
    set_cell_margins(c_sig_right, top=80, bottom=40, left=20, right=0)
    
    pn_lbl = c_sig_left.paragraphs[0]
    pn_lbl.paragraph_format.line_spacing = 1.05
    pn_lbl.paragraph_format.space_after = Pt(2)
    rn_lbl = pn_lbl.add_run("Nơi nhận:")
    rn_lbl.font.name = "Times New Roman"
    rn_lbl.font.size = Pt(11)
    rn_lbl.font.bold = True
    rn_lbl.font.italic = True
    
    recipients = [
        "- Giám đốc Chi nhánh (để b/c);",
        "- Ban Tiếp công dân cấp trên;",
        "- Các Tổ chuyên môn (để p/h thực hiện);",
        "- Lưu: VT, Bộ phận Tiếp công dân."
    ]
    for rec in recipients:
        pr = c_sig_left.add_paragraph()
        pr.paragraph_format.line_spacing = 1.05
        pr.paragraph_format.space_before = Pt(0)
        pr.paragraph_format.space_after = Pt(1)
        pr.paragraph_format.left_indent = Inches(0.15)
        rr = pr.add_run(rec)
        rr.font.name = "Times New Roman"
        rr.font.size = Pt(10)
        
    ps1 = c_sig_right.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps1.paragraph_format.line_spacing = 1.1
    ps1.paragraph_format.space_after = Pt(2)
    rs1 = ps1.add_run("CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI\nGIÁM ĐỐC")
    rs1.font.name = "Times New Roman"
    rs1.font.size = Pt(12)
    rs1.font.bold = True
    
    ps_sign = c_sig_right.add_paragraph()
    ps_sign.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps_sign.paragraph_format.space_before = Pt(45)
    ps_sign.paragraph_format.space_after = Pt(2)
    rs_sign = ps_sign.add_run("Trần Văn Minh")
    rs_sign.font.name = "Times New Roman"
    rs_sign.font.size = Pt(13)
    rs_sign.font.bold = True

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Xong file: {output_path}")

def create_verbatim_mau03_docx(output_path: str):
    """Tạo Mẫu số 03/TCD 13 cột nguyên văn kèm theo Nghị định 154/2026/NĐ-CP."""
    doc = docx.Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width = Inches(11.69)
    sec.page_height = Inches(8.27)
    sec.top_margin = Inches(0.60)
    sec.bottom_margin = Inches(0.60)
    sec.left_margin = Inches(0.60)
    sec.right_margin = Inches(0.50)
    
    sec.different_first_page_header_footer = True
    header = sec.header
    header.is_linked_to_previous = False
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(0)
    fld = parse_xml(
        r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr>'
        r'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        r'<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w')
    )
    p_hdr._p.append(fld)

    def set_cell_margins(cell, top=50, bottom=50, left=40, right=40):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_table_borders(table, color="000000", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Tiêu đề trên cùng
    p_m = doc.add_paragraph()
    p_m.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_m.paragraph_format.space_before = Pt(0)
    p_m.paragraph_format.space_after = Pt(2)
    r_m = p_m.add_run("Mẫu số 03/TCD")
    r_m.font.name = "Times New Roman"
    r_m.font.size = Pt(12)
    r_m.font.bold = True

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(6)
    r_t = p_t.add_run("SỔ TIẾP CÔNG DÂN")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.font.bold = True

    # 13 Cột nguyên văn Nghị định 154:
    # 1: STT
    # 2: Ngày tiếp
    # 3: Họ tên, địa chỉ
    # 4: CCCD
    # 5: Nội dung vụ việc
    # 6: Phân loại đơn
    # 7: Số người
    # Hướng xử lý:
    # 8: Cơ quan đã giải quyết hết thẩm quyền
    # 9: Thụ lý để giải quyết
    # 10: Trả lại đơn và hướng dẫn
    # 11: Chuyển đơn đến cơ quan, tổ chức đơn vị có thẩm quyền
    # 12: Theo dõi kết quả giải quyết
    # 13: Ghi chú
    widths = [0.35, 0.65, 1.25, 0.85, 1.55, 0.70, 0.45, 0.75, 0.60, 0.85, 1.00, 1.15, 0.50] # tổng = 10.65 in
    
    # 3 hàng header + 10 hàng data
    tbl = doc.add_table(rows=13, cols=13)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="000000", sz="4")
    
    for r_i in [0, 1, 2]:
        trPr = tbl.rows[r_i]._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def format_cell(cell, text, font_size=9.0, bold=True, bg="F2F4F7"):
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if bg:
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg}"/>'))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.text = ""
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold

    r0 = tbl.rows[0]
    r1 = tbl.rows[1]
    
    # Hàng 0
    format_cell(r0.cells[0], "STT")
    format_cell(r0.cells[1], "Ngày tiếp")
    format_cell(r0.cells[2], "Họ tên, địa chỉ")
    format_cell(r0.cells[3], "CCCD")
    format_cell(r0.cells[4], "Nội dung vụ việc")
    format_cell(r0.cells[5], "Phân loại đơn")
    format_cell(r0.cells[6], "Số người")
    format_cell(r0.cells[7], "Hướng xử lý")
    format_cell(r0.cells[8], "")
    format_cell(r0.cells[9], "")
    format_cell(r0.cells[10], "")
    format_cell(r0.cells[11], "Theo dõi kết quả giải quyết")
    format_cell(r0.cells[12], "Ghi chú")
    
    # Hàng 1
    format_cell(r1.cells[0], "")
    format_cell(r1.cells[1], "")
    format_cell(r1.cells[2], "")
    format_cell(r1.cells[3], "")
    format_cell(r1.cells[4], "")
    format_cell(r1.cells[5], "")
    format_cell(r1.cells[6], "")
    format_cell(r1.cells[7], "Cơ quan đã giải quyết hết thẩm quyền", font_size=8.5)
    format_cell(r1.cells[8], "Thụ lý để giải quyết", font_size=8.5)
    format_cell(r1.cells[9], "Trả lại đơn và hướng dẫn", font_size=8.5)
    format_cell(r1.cells[10], "Chuyển đơn đến cơ quan, tổ chức đơn vị có thẩm quyền", font_size=8.5)
    format_cell(r1.cells[11], "")
    format_cell(r1.cells[12], "")
    
    # Merge ngang hàng 0 cho Hướng xử lý: cột 7, 8, 9, 10
    r0.cells[7].merge(r0.cells[8]).merge(r0.cells[9]).merge(r0.cells[10])
    
    # Merge dọc
    for c_i in [0, 1, 2, 3, 4, 5, 6, 11, 12]:
        r0.cells[c_i].merge(r1.cells[c_i])
        
    # Hàng 2: Đánh số 1 đến 13
    r2 = tbl.rows[2]
    for i in range(13):
        format_cell(r2.cells[i], str(i + 1), font_size=8.5, bold=False, bg="EAECEF")
        
    # Áp dụng widths
    for r in tbl.rows:
        for idx, w in enumerate(widths):
            r.cells[idx].width = Inches(w)
            
    # Hàng trống
    for r_idx in range(3, 13):
        row = tbl.rows[r_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx in range(13):
            c = row.cells[c_idx]
            set_cell_margins(c, top=40, bottom=40, left=40, right=40)
            p = c.paragraphs[0]
            p.text = str(r_idx - 2) if c_idx == 0 else ""
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 6, 8, 12] else WD_ALIGN_PARAGRAPH.LEFT

    # Ghi chú chân trang Mẫu 03
    p_notes_title = doc.add_paragraph()
    p_notes_title.paragraph_format.space_before = Pt(8)
    p_notes_title.paragraph_format.space_after = Pt(2)
    r_nt = p_notes_title.add_run("Ghi chú:")
    r_nt.font.name = "Times New Roman"
    r_nt.font.size = Pt(10)
    r_nt.font.bold = True
    
    orig_notes = [
        "(1) Số thứ tự.",
        "(2) Ngày tiếp.",
        "(3) Họ tên, địa chỉ.",
        "(4) CCCD/Hộ chiếu của công dân (nếu công dân không có CCCD/Hộ chiếu thì ghi các thông tin theo giấy tờ tùy thân).",
        "(5) Tóm tắt nội dung vụ việc.",
        "(6) Phân loại đơn của công dân (khiếu nại, tố cáo, kiến nghị, phản ánh).",
        "(7) Số công dân có đơn cùng một nội dung.",
        "(8) Ghi rõ cơ quan, tổ chức, đơn vị đã giải quyết hết thẩm quyền.",
        "(9) Đánh dấu (x) nếu thuộc thẩm quyền giải quyết.",
        "(10) Ghi rõ hướng dẫn công dân đến cơ quan, tổ chức, đơn vị nào, số văn bản hướng dẫn.",
        "(11) Ghi rõ tên cơ quan, tổ chức, đơn vị có thẩm quyền thụ lý giải quyết, số văn bản chuyển đơn.",
        "(12) Người tiếp dân ghi chép, theo dõi quá trình, kết quả giải quyết đơn của công dân.",
        "(13) Ghi chú."
    ]
    for n in orig_notes:
        pn = doc.add_paragraph()
        pn.paragraph_format.line_spacing = 1.05
        pn.paragraph_format.space_before = Pt(0)
        pn.paragraph_format.space_after = Pt(1)
        pn.paragraph_format.left_indent = Inches(0.2)
        rn = pn.add_run(n)
        rn.font.name = "Times New Roman"
        rn.font.size = Pt(9)
        rn.font.italic = True

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Xong file: {output_path}")

def create_excel_logbook(output_path: str):
    """Tạo file Excel Sổ theo dõi tiếp công dân chuyên nghiệp, hỗ trợ filter & thống kê."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "So_Theo_Doi_TCD_2026"
    ws.views.sheetView[0].showGridLines = True
    
    # Font và Style
    font_agency = Font(name="Times New Roman", size=11, bold=False)
    font_agency_sub = Font(name="Times New Roman", size=11, bold=True)
    font_title = Font(name="Times New Roman", size=16, bold=True, color="002060")
    font_subtitle = Font(name="Times New Roman", size=10, italic=True)
    font_header_grp = Font(name="Times New Roman", size=10.5, bold=True, color="FFFFFF")
    font_header_sub = Font(name="Times New Roman", size=9.5, bold=True)
    font_header_num = Font(name="Times New Roman", size=9, bold=False, italic=True)
    font_data = Font(name="Times New Roman", size=10)
    font_data_bold = Font(name="Times New Roman", size=10, bold=True)
    
    fill_grp = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    fill_sub = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    fill_num = PatternFill(start_color="E9EDF4", end_color="E9EDF4", fill_type="solid")
    fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    
    thin_border_side = Side(border_style="thin", color="000000")
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    
    # 1. Tiêu ngữ & Cơ quan
    ws["A1"] = "VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TỈNH BÌNH DƯƠNG"
    ws["A1"].font = font_agency
    ws["A2"] = "BỘ PHẬN TIẾP CÔNG DÂN"
    ws["A2"].font = font_agency_sub
    ws["A3"] = "Mẫu số 03/TCD (Nghị định 154/2026/NĐ-CP)"
    ws["A3"].font = font_subtitle
    
    ws["G1"] = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
    ws["G1"].font = font_agency_sub
    ws["G2"] = "Độc lập - Tự do - Hạnh phúc"
    ws["G2"].font = font_agency_sub
    ws["G3"] = "Bình Dương, năm 2026"
    ws["G3"].font = font_subtitle
    
    # 2. Tiêu đề sổ
    ws.merge_cells("A5:I5")
    ws["A5"] = "SỔ THEO DÕI TIẾP CÔNG DÂN NĂM 2026"
    ws["A5"].font = font_title
    ws["A5"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells("A6:I6")
    ws["A6"] = "Theo dõi ngày công dân đến, Lãnh đạo chủ trì tiếp, Nội dung trao đổi, Quá trình xử lý và Kết quả giải quyết"
    ws["A6"].font = font_subtitle
    ws["A6"].alignment = Alignment(horizontal="center", vertical="center")

    # 3. Header Bảng (Hàng 8, 9, 10)
    # Nhóm Hàng 8
    ws["A8"] = "STT"
    ws.merge_cells("B8:C8")
    ws["B8"] = "THÔNG TIN BUỔI TIẾP"
    ws["D8"] = "THÔNG TIN CÔNG DÂN"
    ws["E8"] = "NỘI DUNG VỤ VIỆC & TRAO ĐỔI"
    ws.merge_cells("F8:H8")
    ws["F8"] = "CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT"
    ws["I8"] = "GHI CHÚ"
    
    for c in ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8"]:
        cell = ws[c]
        cell.font = font_header_grp
        cell.fill = fill_grp
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
        
    # Chi tiết Hàng 9
    sub_headers = [
        "STT",
        "Thời gian tiếp\n(Ngày, giờ)",
        "Lãnh đạo chủ trì &\nCán bộ phối hợp tiếp",
        "Họ tên, CCCD/SĐT &\nĐịa chỉ công dân",
        "Tóm tắt nội dung trao đổi,\nđối thoại & Phân loại đơn",
        "Ý kiến chỉ đạo của Lãnh đạo &\nHướng xử lý (Mẫu 03/TCD)",
        "Quá trình theo dõi, thụ lý &\nĐơn vị chuyên môn giải quyết",
        "Kết quả giải quyết\n(Văn bản & Ngày trả lời)",
        "Ghi chú\n(Hồ sơ lưu)"
    ]
    for col_idx, text in enumerate(sub_headers, start=1):
        cell = ws.cell(row=9, column=col_idx, value=text)
        cell.font = font_header_sub
        cell.fill = fill_sub
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
        
    # Merge dọc Hàng 8 & 9
    ws.merge_cells("A8:A9")
    ws.merge_cells("D8:D9")
    ws.merge_cells("E8:E9")
    ws.merge_cells("I8:I9")
    
    # Hàng 10: Đánh số
    for col_idx in range(1, 10):
        cell = ws.cell(row=10, column=col_idx, value=f"({col_idx})")
        cell.font = font_header_num
        cell.fill = fill_num
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    # Điền 10 ca mẫu
    sample_rows = [
        (
            1, "08:30 05/10/2026", "Đ/c Trần Văn Minh - Giám đốc Chi nhánh (Lê Thị Mai - HCTH)",
            "Nguyễn Văn Thành (CCCD: 074082001234, ĐT: 0913.456.789, P. Phú Hòa, TDM)",
            "Khiếu nại hồ sơ chuyển mục đích 150m² đất và cấp đổi GCN trễ hạn 15 ngày. [Khiếu nại]",
            "Thuộc thẩm quyền. Lãnh đạo nhận trách nhiệm trễ hạn, giao Tổ Đăng ký duyệt ký trong 03 ngày.",
            "06/10 kiểm tra thực địa; 07/10 chuyển thông tin thuế; 08/10 thuế ra thông báo.",
            "Đã giải quyết xong. TB 142/TB-VPĐK; trao GCN ngày 12/10/2026. Công dân hài lòng.",
            "Lưu hồ sơ 142/KN"
        ),
        (
            2, "09:45 08/10/2026", "Đ/c Nguyễn Thị Lan - Phó Giám đốc (Phạm Văn Tuấn - KTĐC)",
            "Lê Thị Bích (CCCD: 074185002345, ĐT: 0988.123.456, P. Tân An, TDM)",
            "Phản ánh hộ liền kề (ông Đỗ Văn H) xây hàng rào lấn 0.8m lối đi chung. [Kiến nghị, phản ánh]",
            "Chấp thuận đo đạc trích lục bản đồ. Hướng dẫn thẩm quyền hòa giải thuộc UBND phường Tân An.",
            "12/10 phối hợp UBND phường đo đạc; 16/10 lập BB xác định lấn chiếm 0.82m.",
            "Đã giải quyết xong. Văn bản trích lục 856/VPĐK-KT ngày 18/10. Phường hòa giải thành, ông H tự tháo dỡ.",
            "Lưu hồ sơ 856/PA"
        ),
        (
            3, "14:00 12/10/2026", "Đ/c Trần Văn Minh - Giám đốc (Hoàng Văn Nam - HĐBT)",
            "Đoàn 04 hộ dân (Đại diện: Phan Đình Trọng - CCCD: 074075003456, P. Hiệp Thành, TDM)",
            "Khiếu nại phương án bồi thường DA QL13, giá đất thấp, xin thêm 01 suất TĐC phụ. [KN đông người]",
            "Giải thích khung chính sách bồi thường. Chuyển văn bản kiến nghị đến Hội đồng BTGPMB TP. TDM.",
            "14/10 phát hành VB 1024/VPĐK chuyển đơn; 19/10 Hội đồng bồi thường họp thẩm định bổ sung kiểm đếm.",
            "Đã giải quyết xong. UBND TP ra TB 389/TB-UBND bổ sung tiền tài sản; giải thích tiêu chuẩn TĐC. Dân đồng thuận nhận tiền.",
            "Vụ việc đông người"
        ),
        (
            4, "08:30 15/10/2026", "Đ/c Võ Thành Nam - Phó Chủ tịch UBND tỉnh (Tiếp trực tuyến liên ngành)",
            "Vũ Thị Hoài (CCCD: 074180004567, ĐT: 0979.234.567, Xã An Tây, Bến Cát) - Điểm cầu Bến Cát",
            "Tiếp trực tuyến NĐ 154: Cấp GCN đất khai hoang trước 1993 sai lệch số tờ số thửa qua các thời kỳ. [KNPA]",
            "Ghi âm ghi hình trực tuyến bảo mật. Giao Thanh tra tỉnh phối hợp rà soát hồ sơ gốc năm 1993.",
            "16/10 TB kết luận 215/TB-UBND; 20/10 kiểm tra hồ sơ lưu trữ và lấy ý kiến nhân chứng.",
            "Đang giải quyết theo tiến độ. Thanh tra tỉnh đã có BC 88/BC-TTr đủ điều kiện cấp GCN. Dự kiến trao GCN ngày 10/11/2026.",
            "Tiếp trực tuyến NĐ 154"
        ),
        (
            5, "15:30 18/10/2026", "Đ/c Trần Văn Minh - Giám đốc (Nguyễn Văn Bình - TT Nhân dân)",
            "Đặng Quốc Huy (CCCD: 074090005678, P. Phú Lợi, TDM) - Giữ bí mật người tố cáo",
            "Tố cáo viên chức đo đạc vòi vĩnh chi phí bồi dưỡng ngoài quy định khi đo tách thửa 45. [Tố cáo]",
            "Bảo mật thông tin. Lập Giấy biên nhận Mẫu 02/TCD NĐ 154. Giao Tổ Giám sát nội bộ xác minh trong 07 ngày.",
            "20/10 ra QĐ xác minh 88/QĐ; 22/10 làm việc với viên chức, viên chức thừa nhận sai phạm.",
            "Đã giải quyết xong. Giám đốc ký QĐ kỷ luật Cảnh cáo, điều chuyển công tác; ban hành Kết luận tố cáo 12/KL gửi công dân.",
            "Bảo mật Mẫu 02/TCD"
        ),
        (
            6, "10:15 21/10/2026", "Đ/c Nguyễn Thị Lan - Phó Giám đốc (Cán bộ thường trực tiếp dân)",
            "Lý Văn Đạt (CCCD: 074068006789, ĐT: 0918.999.888, P. Chánh Nghĩa, TDM)",
            "Đòi lại 500m² đất do ông bà để lại trước 1975 đã giải quyết hết thẩm quyền đúng pháp luật, không có chứng cứ mới. [KN hết TQ]",
            "Áp dụng Điểm h Khoản 1 Điều 4 NĐ 154: Từ chối tiếp công dân. Lập Thông báo từ chối theo Mẫu số 01/TCD.",
            "Cán bộ giải thích trực tiếp căn cứ pháp luật; soạn thảo dự thảo Thông báo từ chối.",
            "Đã xử lý xong. Ngày 23/10/2026 ban hành Thông báo từ chối tiếp công dân số 68/TB-CN23 (theo Mẫu 01/TCD) giao cho công dân.",
            "Ban hành Mẫu 01/TCD"
        ),
        (
            7, "09:00 23/10/2026", "Đ/c Trần Văn Minh - Giám đốc (Đỗ Thị Cúc - Tổ Hành chính)",
            "Mai Thị Hồng Loan (CCCD: 074192007890, ĐT: 0933.222.111, P. Phú Lợi, TDM)",
            "Đề nghị đính chính thông tin số CCCD và cập nhật diện tích đo đạc thực tế trên GCN số BD 123456. [TTHC]",
            "Hồ sơ rõ ràng, thuộc thẩm quyền giải quyết ngay (K3 Điều 25 NĐ 154). Tiếp nhận trực tiếp, hẹn trả sau 03 ngày.",
            "23/10 chuyển hồ sơ sang Tổ Đăng ký biến động; 24/10 in trang bổ sung đính chính thông tin.",
            "Đã giải quyết xong. Trao GCN đã đính chính ngày 26/10/2026. Công dân ký nhận, đánh giá rất hài lòng.",
            "Giải quyết trong 3 ngày"
        ),
        (
            8, "14:30 24/10/2026", "Đ/c Nguyễn Thị Lan - Phó Giám đốc (Tổ Kỹ thuật địa chính)",
            "Huỳnh Tấn Phát (CCCD: 074085008901, ĐT: 0908.333.444, P. Định Hòa, TDM)",
            "Phản ánh Bộ phận Một cửa đòi trích lục khai sinh thừa kế gây khó khăn, không đúng danh mục TTHC công bố. [Phản ánh TTHC]",
            "Tiếp thu phản ánh. Khai thác dữ liệu VNeID thay thế giấy tờ cũ theo Đề án 06. Chấn chỉnh bộ phận tiếp nhận.",
            "Phó Giám đốc trực tiếp hướng dẫn cán bộ Một cửa tra cứu CSDL Dân cư, hoàn tất hồ sơ ngay trong buổi chiều 24/10.",
            "Đã giải quyết xong. Hồ sơ đã chuyển thụ lý hẹn trả kết quả 03/11/2026. Công dân gửi lời cảm ơn.",
            "Cải cách Đề án 06"
        ),
        (
            9, "08:45 25/10/2026", "Đ/c Trần Văn Minh - Giám đốc (Trưởng phòng Tài chính)",
            "Lương Gia Bảo (CCCD: 074078009012, ĐT: 0945.666.777, P. Hòa Phú, TDM)",
            "Kiến nghị xem xét lại cách tính tiền sử dụng đất chuyển mục đích 80m² đất vườn, cho rằng áp dụng sai vị trí hẻm. [Nghĩa vụ tài chính]",
            "Tiếp nhận đơn. Thẩm quyền quyết định bảng giá đất của Chi cục Thuế. Phát hành phiếu phối hợp rà soát.",
            "25/10 phát hành Phiếu phối hợp 312/PPH gửi Chi cục Thuế rà soát lộ giới và cấp vị trí hẻm.",
            "Đang giải quyết. Chi cục Thuế đang tính lại theo vị trí hẻm cấp 2, dự kiến thông báo thuế điều chỉnh giảm ngày 28/10.",
            "Phối hợp Thuế - Đất đai"
        ),
        (
            10, "15:00 26/10/2026", "Đ/c Nguyễn Thị Lan - Phó Giám đốc (Cán bộ thường trực tiếp dân)",
            "Hoàng Diệu Linh (CCCD: 074198000123, ĐT: 0912.888.999, P. Phú Cường, TDM)",
            "Hỏi thủ tục cấp lại GCN quyền sử dụng đất bị cháy thất lạc và thời hạn niêm yết tại phường theo Luật Đất đai 2024. [Hướng dẫn TTHC]",
            "Thuộc trường hợp hướng dẫn trực tiếp (Mẫu 03 cột 10). Cung cấp biểu mẫu cớ mất, hướng dẫn niêm yết 15 ngày.",
            "Cán bộ in biểu mẫu, hỗ trợ bà Linh điền thông tin, cung cấp hotline hướng dẫn bổ sung.",
            "Đã giải quyết xong. Ban hành văn bản tóm tắt quy trình TTHC 15/HD-VPĐK ngày 26/10/2026. Công dân nắm rõ quy trình.",
            "Hướng dẫn tận tình"
        )
    ]
    
    start_row = 11
    for r_i, r_data in enumerate(sample_rows):
        cur_row = start_row + r_i
        for c_i, val in enumerate(r_data, start=1):
            cell = ws.cell(row=cur_row, column=c_i, value=val)
            cell.font = font_data
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c_i in [1, 2, 9] else "left", vertical="top", wrap_text=True)
            if r_i % 2 == 1:
                cell.fill = fill_zebra
            if c_i == 1:
                cell.font = font_data_bold
                
    # 5 hàng trống sẵn sàng nhập
    for r_i in range(10, 15):
        cur_row = start_row + r_i
        for c_i in range(1, 10):
            cell = ws.cell(row=cur_row, column=c_i, value=r_i + 1 if c_i == 1 else "")
            cell.font = font_data
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c_i in [1, 2, 9] else "left", vertical="top", wrap_text=True)

    # Đặt độ rộng các cột tối ưu
    col_widths = {
        "A": 7,   # STT
        "B": 18,  # Thời gian
        "C": 30,  # Lãnh đạo tiếp
        "D": 35,  # Công dân
        "E": 45,  # Nội dung trao đổi
        "F": 42,  # Chỉ đạo & Hướng xử lý
        "G": 38,  # Quá trình xử lý
        "H": 38,  # Kết quả giải quyết
        "I": 18   # Ghi chú
    }
    for col_l, width in col_widths.items():
        ws.column_dimensions[col_l].width = width
        
    ws.row_dimensions[8].height = 25
    ws.row_dimensions[9].height = 32
    ws.row_dimensions[10].height = 18
    
    # Auto-fit print setup
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"Xong file Excel: {output_path}")

if __name__ == "__main__":
    create_expanded_logbook_docx("OUTPUT/SO_THEO_DOI_TIEP_CONG_DAN_ND154_ND30.docx")
    create_verbatim_mau03_docx("OUTPUT/MAU_03_TCD_SO_TIEP_CONG_DAN_NGUYEN_BAN_ND154.docx")
    create_excel_logbook("OUTPUT/SO_THEO_DOI_TIEP_CONG_DAN_ND154.xlsx")
