#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_so_tiep_cong_dan.py
Tạo Sổ theo dõi tiếp công dân (.docx) chuẩn Nghị định 30/2020/NĐ-CP
và tuân thủ Mẫu số 03/TCD ban hành kèm theo Nghị định số 154/2026/NĐ-CP của Chính phủ.
Lặp lại Header trên mọi trang (tblHeader) giống hệt PL2_final_da_nhap_bac_luong.docx.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_so_tiep_cong_dan_docx(output_path: str):
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # 1. Cấu hình Section: Khổ A4 Landscape & Định lề chuẩn NĐ 30
    # -------------------------------------------------------------
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    # Chuẩn A4 Landscape: Rộng 297mm (11.69 in), Cao 210mm (8.27 in)
    sec.page_width = Inches(11.69)
    sec.page_height = Inches(8.27)
    
    # Lề trang theo Nghị định 30 (khổ ngang):
    # Top: 20mm (0.79 in), Bottom: 20mm (0.79 in)
    # Left: 25mm (0.98 in - để đóng gáy sổ), Right: 15mm (0.59 in)
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.79)
    sec.left_margin = Inches(0.98)
    sec.right_margin = Inches(0.59)
    
    # -------------------------------------------------------------
    # 2. Đánh số trang chuẩn NĐ 30 trên Header (Không hiện ở trang 1)
    # -------------------------------------------------------------
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
    
    # -------------------------------------------------------------
    # 3. Cấu hình Styles mặc định toàn tài liệu
    # -------------------------------------------------------------
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

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    
    # Helper gạch ngang chuẩn NĐ 30
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

    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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

    # -------------------------------------------------------------
    # 4. Header cơ quan & Quốc hiệu (Bảng 2 cột không viền - Landscape)
    # -------------------------------------------------------------
    hdr_table = doc.add_table(rows=1, cols=2)
    hdr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_table.autofit = False
    set_borderless(hdr_table)
    
    # Rộng trang in khả dụng: ~10.12 inches = 728 pt
    c_left = hdr_table.rows[0].cells[0]
    c_right = hdr_table.rows[0].cells[1]
    c_left.width = Inches(4.5)
    c_right.width = Inches(5.6)
    set_cell_margins(c_left, top=0, bottom=40, left=0, right=20)
    set_cell_margins(c_right, top=0, bottom=40, left=20, right=0)
    
    # Cột trái: Cơ quan
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
    
    # Cột phải: Quốc hiệu & Tiêu ngữ
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
    
    # -------------------------------------------------------------
    # 5. Tiêu đề văn bản: SỔ THEO DÕI TIẾP CÔNG DÂN
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
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
    
    # -------------------------------------------------------------
    # 6. Thiết kế Bảng chính (Main Table) với lặp Header trên từng trang
    # -------------------------------------------------------------
    # Bảng gồm 9 cột chính khoa học:
    # Col 1: STT
    # Col 2: Thời gian tiếp (Ngày, giờ)
    # Col 3: Lãnh đạo chủ trì & Cán bộ cùng tiếp
    # Col 4: Họ tên, CCCD & Địa chỉ công dân
    # Col 5: Nội dung trao đổi & Phân loại vụ việc
    # Col 6: Ý kiến chỉ đạo của Lãnh đạo & Hướng xử lý
    # Col 7: Quá trình theo dõi & Xử lý vụ việc
    # Col 8: Kết quả giải quyết (Văn bản, ngày trả lời)
    # Col 9: Ghi chú
    
    col_widths_in = [0.38, 0.75, 1.15, 1.35, 1.95, 1.50, 1.40, 1.25, 0.45]
    total_w = sum(col_widths_in) # 10.18 in (~258 mm) - khớp trọn vẹn bề rộng trang in A4 Landscape
    
    # Dữ liệu các ca thực tế (10 ca điển hình phong phú + 5 hàng trống)
    cases = [
        (
            "1",
            "08:30\n05/10/2026",
            "Đ/c Trần Văn Minh\n- Giám đốc Chi nhánh\n(Cán bộ phối hợp: Lê Thị Mai - Tổ HCTH)",
            "Ông Nguyễn Văn Thành\nCCCD: 074082001234\nĐịa chỉ: P. Phú Hòa, TP. Thủ Dầu Một\nSĐT: 0913.456.789\n(01 người)",
            "- Nội dung trao đổi: Khiếu nại hồ sơ xin chuyển mục đích sử dụng 150m² đất và cấp đổi GCN bị trễ hạn 15 ngày so với phiếu hẹn. Bức xúc do cần làm thủ tục vay vốn ngân hàng.\n- Loại đơn: Khiếu nại.",
            "- Lãnh đạo kết luận: Thuộc thẩm quyền giải quyết (Mẫu 03/TCD: đánh dấu x).\n- Chỉ đạo: Nhận trách nhiệm về việc trễ hẹn; giao Tổ Đăng ký kiểm tra ngay quy hoạch phân khu 1/2000 và hoàn tất hồ sơ trình ký trong 03 ngày làm việc.",
            "- Ngày 06/10: Tổ Kỹ thuật kiểm tra thực địa và nguồn gốc đất.\n- Ngày 07/10: Lập phiếu chuyển thông tin nghĩa vụ tài chính sang Chi cục Thuế.\n- Ngày 08/10: Chi cục Thuế ra thông báo nộp thuế.",
            "- Đã giải quyết xong.\n- Ban hành TB số 142/TB-VPĐK ngày 09/10/2026.\n- Đã trao GCN mới cho công dân vào ngày 12/10/2026.\n- Công dân đồng thuận, hài lòng.",
            "Lưu hồ sơ số: 142/KN"
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
        # 5 Hàng mẫu để trống sẵn sàng sử dụng
        ("11", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("12", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("13", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("14", "....:....\n..../..../2026", "", "", "", "", "", "", ""),
        ("15", "....:....\n..../..../2026", "", "", "", "", "", "")
    ]
    
    # Số hàng = 3 hàng header + số cases
    total_rows = 3 + len(cases)
    total_cols = len(col_widths_in)
    
    main_table = doc.add_table(rows=total_rows, cols=total_cols)
    main_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    main_table.autofit = False
    set_table_borders(main_table, color="000000", sz="4")
    
    # -------------------------------------------------------------
    # Cấu hình w:tblHeader cho TẤT CẢ các hàng header (Row 0, 1, 2)
    # Đây chính là mấu chốt để Header tự động lặp lại trên từng trang!
    # -------------------------------------------------------------
    for r_h_idx in [0, 1, 2]:
        r_h = main_table.rows[r_h_idx]
        trPr = r_h._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    # Helper định dạng cell header
    def format_header_cell(cell, text, font_size=10.0, bold=True, bg_color="F2F4F7"):
        set_cell_margins(cell, top=70, bottom=70, left=50, right=50)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        
        # Nền ô
        if bg_color:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
            tcPr.append(shd)
            
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold

    # Hàng 0: Nhóm tiêu đề chính (Có merge dọc và ngang)
    row0 = main_table.rows[0]
    format_header_cell(row0.cells[0], "STT", font_size=10.5)
    format_header_cell(row0.cells[1], "THÔNG TIN BUỔI TIẾP", font_size=10.5)
    format_header_cell(row0.cells[2], "THÔNG TIN BUỔI TIẾP", font_size=10.5)
    format_header_cell(row0.cells[3], "THÔNG TIN CÔNG DÂN", font_size=10.5)
    format_header_cell(row0.cells[4], "NỘI DUNG VỤ VIỆC & TRAO ĐỔI", font_size=10.5)
    format_header_cell(row0.cells[5], "CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT", font_size=10.5)
    format_header_cell(row0.cells[6], "CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT", font_size=10.5)
    format_header_cell(row0.cells[7], "CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT", font_size=10.5)
    format_header_cell(row0.cells[8], "GHI CHÚ", font_size=10.5)
    
    # Hàng 1: Chi tiết từng cột
    row1 = main_table.rows[1]
    format_header_cell(row1.cells[0], "STT", font_size=10.0)
    format_header_cell(row1.cells[1], "Thời gian tiếp\n(Ngày, giờ)", font_size=9.5)
    format_header_cell(row1.cells[2], "Lãnh đạo chủ trì &\nCán bộ phối hợp tiếp", font_size=9.5)
    format_header_cell(row1.cells[3], "Họ tên, CCCD/SĐT\n& Địa chỉ công dân", font_size=9.5)
    format_header_cell(row1.cells[4], "Tóm tắt nội dung trao đổi,\nđối thoại & Phân loại đơn", font_size=9.5)
    format_header_cell(row1.cells[5], "Chỉ đạo của Lãnh đạo &\nHướng xử lý (Mẫu 03/TCD)", font_size=9.5)
    format_header_cell(row1.cells[6], "Quá trình theo dõi, thụ lý\n& Đơn vị giải quyết", font_size=9.5)
    format_header_cell(row1.cells[7], "Kết quả giải quyết\n(Văn bản & Ngày trả lời)", font_size=9.5)
    format_header_cell(row1.cells[8], "Ghi chú\n(Hồ sơ lưu)", font_size=9.5)
    
    # Thực hiện merge Row 0 và Row 1
    # Merge ngang hàng 0: Col 1 & 2 -> THÔNG TIN BUỔI TIẾP
    row0.cells[1].merge(row0.cells[2])
    # Merge ngang hàng 0: Col 5, 6, 7 -> CHỈ ĐẠO, QUÁ TRÌNH XỬ LÝ & KẾT QUẢ GIẢI QUYẾT
    row0.cells[5].merge(row0.cells[6]).merge(row0.cells[7])
    
    # Merge dọc: Col 0 (STT)
    row0.cells[0].merge(row1.cells[0])
    # Merge dọc: Col 3 (THÔNG TIN CÔNG DÂN)
    row0.cells[3].merge(row1.cells[3])
    # Merge dọc: Col 4 (NỘI DUNG VỤ VIỆC)
    row0.cells[4].merge(row1.cells[4])
    # Merge dọc: Col 8 (GHI CHÚ)
    row0.cells[8].merge(row1.cells[8])

    # Hàng 2: Đánh số thứ tự các cột (1) đến (9)
    row2 = main_table.rows[2]
    col_labels = ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)"]
    for idx, lbl in enumerate(col_labels):
        format_header_cell(row2.cells[idx], lbl, font_size=9.0, bold=False, bg_color="EAECEF")

    # -------------------------------------------------------------
    # Điền Dữ liệu các hàng (Row 3 trở đi) + gắn cantSplit
    # -------------------------------------------------------------
    for case_idx, case_data in enumerate(cases):
        r_row = main_table.rows[3 + case_idx]
        trPr = r_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        # Nền so le (zebra striping) nhẹ nhàng cho dễ tra cứu
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
            
            # Căn lề
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx in [8]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            # Parse từng dòng để tô đậm tiêu đề phụ nếu có
            lines = cell_value.split('\n')
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
                
                # Format đậm cho tên Lãnh đạo hoặc tên người
                if col_idx == 0:
                    r.font.bold = True
                elif col_idx == 2 and ("Đ/c" in line or "Lãnh đạo" in line):
                    r.font.bold = True
                elif col_idx == 3 and ("Ông" in line or "Bà" in line or "Đoàn" in line):
                    r.font.bold = True
                elif col_idx in [4, 5, 6, 7] and (line.startswith("- Lãnh đạo") or line.startswith("- Đã giải quyết") or line.startswith("- Nội dung") or line.startswith("- Loại đơn")):
                    r.font.bold = True
                    if "Đã giải quyết xong" in line:
                        r.font.color.rgb = RGBColor(0, 100, 0) # Xanh lá đậm thành công
                    elif "Đang giải quyết" in line:
                        r.font.color.rgb = RGBColor(180, 80, 0) # Cam đậm đang xử lý

    # Áp dụng bề rộng cột cho mọi hàng trong bảng
    for row in main_table.rows:
        for idx, w in enumerate(col_widths_in):
            row.cells[idx].width = Inches(w)

    # -------------------------------------------------------------
    # 7. Khối Chân trang: Ghi chú, Nơi nhận & Chữ ký chuẩn NĐ 30
    # -------------------------------------------------------------
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

    # Bảng Chữ ký & Nơi nhận (Bảng 2 cột không viền)
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
    
    # Nơi nhận bên trái
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
        
    # Chữ ký bên phải
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
    ps_sign.paragraph_format.space_before = Pt(45) # Khoảng trống ký tên
    ps_sign.paragraph_format.space_after = Pt(2)
    rs_sign = ps_sign.add_run("Trần Văn Minh")
    rs_sign.font.name = "Times New Roman"
    rs_sign.font.size = Pt(13)
    rs_sign.font.bold = True

    # Lưu tài liệu
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Đã tạo thành công file Word: {output_path}")

if __name__ == "__main__":
    out_file = "OUTPUT/SO_THEO_DOI_TIEP_CONG_DAN_ND154_ND30.docx"
    build_so_tiep_cong_dan_docx(out_file)
