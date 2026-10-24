#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nd30_engine.py - Core Document Engine chuẩn hóa Nghị định 30/2020/NĐ-CP
========================================================================
Mô-đun dùng chung để khởi tạo và định dạng văn bản hành chính Việt Nam
(Tờ trình, Báo cáo, Quyết định, Công văn, Kế hoạch, Phương án, Quy chế...).

Tuân thủ nghiêm ngặt theo tài liệu QUY_CHUAN_DOCX_ND30.md:
- Khổ giấy A4, căn lề chuẩn: Top 20mm, Bottom 20mm, Left 30mm, Right 15mm.
- Quốc hiệu, Tiêu ngữ: Đường kẻ 18 ký tự em-dash cỡ 8.5pt, khoảng cách dòng exact 6pt.
- Cơ quan ban hành: Đường kẻ 8 ký tự em-dash cỡ 8.5pt, khoảng cách dòng exact 6pt.
- Đánh số trang: Từ trang 2 trở đi ở giữa đầu trang.
- Đoạn văn: Font Times New Roman 13pt, giãn dòng 1.2, thụt lề đầu dòng 1.27cm.
- Bảng biểu: Viền chuẩn, padding tối ưu, lặp tiêu đề trang (tblHeader), chống đứt dòng (cantSplit).
- Chân trang: Khối Nơi nhận (11-12pt) và Khối Chức vụ / Người ký chuẩn hóa.
"""

import os
from typing import List, Dict, Optional, Tuple, Any
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

class ND30Document:
    """
    Trình khởi tạo và quản lý văn bản hành chính chuẩn Nghị định 30/2020/NĐ-CP.
    """
    
    def __init__(self, font_size_body: float = 13.0):
        self.doc = docx.Document()
        self.font_name = 'Times New Roman'
        self.font_size_body = font_size_body
        self._configure_default_styles()
        self._setup_first_section()
        self.current_section = self.doc.sections[0]

    def _configure_default_styles(self):
        """Thiết lập style Normal mặc định chuẩn NĐ 30."""
        style_normal = self.doc.styles['Normal']
        style_normal.font.name = self.font_name
        style_normal.font.size = Pt(self.font_size_body)
        style_normal.font.color.rgb = RGBColor(0, 0, 0)
        style_normal.paragraph_format.line_spacing = 1.2
        style_normal.paragraph_format.space_after = Pt(6)
        style_normal.paragraph_format.space_before = Pt(0)
        style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def _setup_first_section(self):
        """Cấu hình Section đầu tiên theo chuẩn A4 Portrait."""
        sec = self.doc.sections[0]
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width = Inches(8.27)    # 210mm
        sec.page_height = Inches(11.69)  # 297mm
        # Lề chuẩn: Top 20mm, Bottom 20mm, Left 30mm, Right 15mm
        sec.top_margin = Inches(0.79)    # 20mm
        sec.bottom_margin = Inches(0.79) # 20mm
        sec.left_margin = Inches(1.18)   # 30mm
        sec.right_margin = Inches(0.59)  # 15mm
        self._configure_page_numbering(sec)

    def _configure_page_numbering(self, section):
        """
        Cấu hình số trang chuẩn NĐ 30:
        - Trang 1 KHÔNG hiển thị số trang.
        - Từ trang 2 trở đi hiển thị số trang ở chính giữa phần đầu trang (Header).
        """
        section.different_first_page_header_footer = True
        header = section.header
        header.is_linked_to_previous = False
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        # Thêm mã trường số trang Word tự động (PAGE field)
        fld = parse_xml(
            r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr>'
            r'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            r'<w:sz w:val="26"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w')
        )
        p._p.append(fld)

    @staticmethod
    def _add_divider_line(cell_or_doc, length_type="nation"):
        """
        Tạo đường kẻ ngang mảnh bằng chuỗi em-dash (—) nối liền không đứt đoạn:
        - length_type="nation": Dưới Tiêu ngữ -> 18 em-dashes (phủ trọn 100% từ 'Độc' tới 'phúc').
        - length_type="agency": Dưới cơ quan ban hành -> 8 em-dashes (xấp xỉ 2/3 độ dài).
        - length_type="subject": Dưới trích yếu -> 8 em-dashes.
        Áp dụng khoảng cách dòng cố định exact 6pt và cỡ chữ 8.5pt.
        """
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
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    @staticmethod
    def set_table_borderless(table):
        """Xóa toàn bộ viền bảng (dành cho bảng layout header & footer)."""
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

    @staticmethod
    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
        """Thiết lập lề trong của ô (padding dxa: 20 dxa = 1pt)."""
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    @staticmethod
    def set_table_borders(table, color="000000", sz="4"):
        """Đặt viền thanh lịch cho bảng dữ liệu (mặc định nét đơn mảnh 0.5pt)."""
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

    def add_header(self,
                   agency_parent: str = "VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM",
                   agency_name: str = "CHI NHÁNH SỐ 23",
                   doc_code: str = "Số:      /BC-CN23",
                   location_date: str = "Thủ Dầu Một, ngày      tháng      năm 2026"):
        """
        Tạo khối Đầu trang 2 cột không viền chuẩn Nghị định 30.
        - Cột trái: Cơ quan chủ quản (12pt đứng), Cơ quan ban hành (13pt hoa đậm) + gạch kẻ 8 em-dash + Số ký hiệu (13pt đứng).
        - Cột phải: Quốc hiệu (13pt hoa đậm), Tiêu ngữ (13pt thường đậm) + gạch kẻ 18 em-dash + Địa danh ngày tháng (13pt nghiêng).
        """
        table = self.doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        c_left = table.rows[0].cells[0]
        c_right = table.rows[0].cells[1]
        c_left.width = Inches(3.25)
        c_right.width = Inches(3.50)
        
        self.set_table_borderless(table)
        self.set_cell_margins(c_left, top=0, bottom=40, left=0, right=40)
        self.set_cell_margins(c_right, top=0, bottom=40, left=40, right=0)
        
        # Cột Trái: Tên Cơ quan
        p_p = c_left.paragraphs[0]
        p_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_p.paragraph_format.line_spacing = 1.0
        p_p.paragraph_format.space_after = Pt(2)
        r_p = p_p.add_run(agency_parent)
        r_p.font.name = self.font_name
        r_p.font.size = Pt(12)
        
        p_a = c_left.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_a.paragraph_format.line_spacing = 1.0
        p_a.paragraph_format.space_after = Pt(2)
        r_a = p_a.add_run(agency_name)
        r_a.font.name = self.font_name
        r_a.font.size = Pt(13)
        r_a.font.bold = True
        
        # Đường kẻ cơ quan
        self._add_divider_line(c_left, length_type="agency")
        
        # Số ký hiệu
        p_code = c_left.add_paragraph()
        p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_code.paragraph_format.line_spacing = 1.0
        p_code.paragraph_format.space_before = Pt(4)
        p_code.paragraph_format.space_after = Pt(0)
        r_code = p_code.add_run(doc_code)
        r_code.font.name = self.font_name
        r_code.font.size = Pt(13)
        
        # Cột Phải: Quốc hiệu & Tiêu ngữ
        p_q = c_right.paragraphs[0]
        p_q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_q.paragraph_format.line_spacing = 1.0
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM")
        r_q.font.name = self.font_name
        r_q.font.size = Pt(13)
        r_q.font.bold = True
        
        p_t = c_right.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_t.paragraph_format.line_spacing = 1.0
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run("Độc lập - Tự do - Hạnh phúc")
        r_t.font.name = self.font_name
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        
        # Đường kẻ Quốc hiệu
        self._add_divider_line(c_right, length_type="nation")
        
        # Địa danh ngày tháng
        p_date = c_right.add_paragraph()
        p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_date.paragraph_format.line_spacing = 1.0
        p_date.paragraph_format.space_before = Pt(4)
        p_date.paragraph_format.space_after = Pt(0)
        r_date = p_date.add_run(location_date)
        r_date.font.name = self.font_name
        r_date.font.size = Pt(13)
        r_date.font.italic = True
        
        # Khoảng cách trắng sau header
        p_space = self.doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(6)
        p_space.paragraph_format.space_after = Pt(6)

    def add_title(self, doc_type: str, title: str, subtitle: Optional[str] = None):
        """
        Tạo Tên loại văn bản & Trích yếu nội dung:
        - doc_type: BÁO CÁO / TỜ TRÌNH / QUYẾT ĐỊNH / KẾ HOẠCH / PHƯƠNG ÁN / THÔNG BÁO... (14pt, In hoa đậm).
        - title: Tiêu đề hoặc trích yếu nội dung (14pt, Đứng đậm).
        - subtitle: Phụ đề hoặc căn cứ trích dẫn bổ sung (nếu có).
        """
        p_type = self.doc.add_paragraph()
        p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_type.paragraph_format.space_before = Pt(12)
        p_type.paragraph_format.space_after = Pt(4)
        p_type.paragraph_format.line_spacing = 1.15
        
        r_type = p_type.add_run(doc_type.upper())
        r_type.font.name = self.font_name
        r_type.font.size = Pt(14)
        r_type.font.bold = True
        
        if title:
            p_title = self.doc.add_paragraph()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_title.paragraph_format.space_before = Pt(2)
            p_title.paragraph_format.space_after = Pt(4)
            p_title.paragraph_format.line_spacing = 1.2
            r_title = p_title.add_run(title)
            r_title.font.name = self.font_name
            r_title.font.size = Pt(14)
            r_title.font.bold = True
            
        if subtitle:
            p_sub = self.doc.add_paragraph()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_sub.paragraph_format.space_before = Pt(2)
            p_sub.paragraph_format.space_after = Pt(6)
            r_sub = p_sub.add_run(subtitle)
            r_sub.font.name = self.font_name
            r_sub.font.size = Pt(13)
            r_sub.font.italic = True
            
        # Đường kẻ phân cách trích yếu
        self._add_divider_line(self.doc, length_type="subject")
        
        p_spacer = self.doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(4)
        p_spacer.paragraph_format.space_after = Pt(6)

    def add_heading_1(self, text: str):
        """Mục cấp 1: I, II, III (13pt, In hoa đậm, cách trên 6pt, không thụt lề)."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(text)
        r.font.name = self.font_name
        r.font.size = Pt(self.font_size_body)
        r.font.bold = True
        return p

    def add_heading_2(self, text: str):
        """Mục cấp 2: 1., 2., 3. (13pt, Đứng đậm, cách trên 4pt, thụt lề 0.5 inch)."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Inches(0.25)
        r = p.add_run(text)
        r.font.name = self.font_name
        r.font.size = Pt(self.font_size_body)
        r.font.bold = True
        return p

    def add_heading_3(self, text: str):
        """Mục cấp 3: a), b), c) (13pt, Nghiêng hoặc đứng, thụt lề 0.5 inch)."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Inches(0.5)
        r = p.add_run(text)
        r.font.name = self.font_name
        r.font.size = Pt(self.font_size_body)
        r.font.italic = True
        return p

    def add_paragraph(self, text: str, bold: bool = False, italic: bool = False, indent: bool = True):
        """
        Thêm một đoạn văn bản thân bài chuẩn:
        - Thụt đầu dòng 1.27cm (0.5 inch).
        - Canh đều hai bên (Justify).
        - Giãn dòng 1.2, khoảng cách đoạn 6pt.
        """
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(0.5) if indent else Inches(0)
        
        r = p.add_run(text)
        r.font.name = self.font_name
        r.font.size = Pt(self.font_size_body)
        r.font.bold = bold
        r.font.italic = italic
        return p

    def add_bullet_point(self, text: str, bullet: str = "-"):
        """Thêm dòng gạch đầu dòng với lề thụt chuẩn."""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        
        r_b = p.add_run(f"{bullet} ")
        r_b.font.name = self.font_name
        r_b.font.size = Pt(self.font_size_body)
        r_b.font.bold = True
        
        r_t = p.add_run(text)
        r_t.font.name = self.font_name
        r_t.font.size = Pt(self.font_size_body)
        return p

    def add_table_data(self,
                       headers: List[str],
                       rows_data: List[List[str]],
                       col_widths: Optional[List[float]] = None,
                       alignments: Optional[List[WD_ALIGN_PARAGRAPH]] = None) -> docx.table.Table:
        """
        Tạo bảng số liệu chuẩn NĐ 30:
        - Viền đơn thanh mảnh (`sz="4"`).
        - Tiêu đề lặp lại trên mọi trang (`tblHeader`).
        - Chống đứt ngang dòng giữa các trang (`cantSplit`).
        - Padding ô: Trên/Dưới 60 dxa, Trái/Phải 80 dxa.
        - Căn lề từng cột linh hoạt (mặc định: cột 1 giữa, cột chữ trái, cột số phải).
        """
        num_cols = len(headers)
        num_rows = len(rows_data) + 1
        
        table = self.doc.add_table(rows=num_rows, cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        self.set_table_borders(table)
        
        # 1. Định dạng hàng Header
        header_row = table.rows[0]
        trPr = header_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for idx, text in enumerate(headers):
            cell = header_row.cells[idx]
            self.set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            r = p.add_run(text)
            r.font.name = self.font_name
            r.font.size = Pt(12)
            r.font.bold = True
            
        # 2. Điền dữ liệu các hàng
        for r_idx, row_values in enumerate(rows_data):
            row = table.rows[r_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
            for c_idx, val in enumerate(row_values):
                if c_idx >= num_cols:
                    break
                cell = row.cells[c_idx]
                self.set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                
                # Căn lề cột
                if alignments and c_idx < len(alignments):
                    p.alignment = alignments[c_idx]
                else:
                    if c_idx == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif str(val).strip().replace('.', '').replace(',', '').replace('%', '').isdigit():
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        
                r = p.add_run(str(val))
                r.font.name = self.font_name
                r.font.size = Pt(12)
                
        # 3. Áp dụng độ rộng cột (Inches)
        if col_widths and len(col_widths) == num_cols:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)
                    
        p_spacer = self.doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(4)
        p_spacer.paragraph_format.space_after = Pt(6)
        return table

    def add_footer_signatures(self,
                              recipients: List[str],
                              signatory_title: str = "GIÁM ĐỐC",
                              signatory_name: str = "Nguyễn Thị Lệ Hằng",
                              signed_on_behalf: Optional[str] = None):
        """
        Tạo khối Chân trang chuẩn NĐ 30:
        - Bảng 2 cột không viền.
        - Cột trái: "Nơi nhận:" (12pt nghiêng đậm), danh sách nhận (11pt đứng).
        - Cột phải: Chức vụ (13-14pt hoa đậm), khoảng trống chữ ký, Họ và tên (13-14pt đậm).
        """
        table = self.doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        self.set_table_borderless(table)
        
        c_left = table.rows[0].cells[0]
        c_right = table.rows[0].cells[1]
        c_left.width = Inches(3.25)
        c_right.width = Inches(3.50)
        self.set_cell_margins(c_left, top=60, bottom=0, left=0, right=20)
        self.set_cell_margins(c_right, top=60, bottom=0, left=20, right=0)
        
        # Cột Trái: Nơi nhận
        p_noi_nhan = c_left.paragraphs[0]
        p_noi_nhan.paragraph_format.line_spacing = 1.0
        p_noi_nhan.paragraph_format.space_before = Pt(0)
        p_noi_nhan.paragraph_format.space_after = Pt(2)
        r_nn = p_noi_nhan.add_run("Nơi nhận:")
        r_nn.font.name = self.font_name
        r_nn.font.size = Pt(12)
        r_nn.font.bold = True
        r_nn.font.italic = True
        
        for item in recipients:
            p_item = c_left.add_paragraph()
            p_item.paragraph_format.line_spacing = 1.0
            p_item.paragraph_format.space_before = Pt(0)
            p_item.paragraph_format.space_after = Pt(1)
            prefix = "- " if not item.startswith("-") else ""
            r_it = p_item.add_run(f"{prefix}{item}")
            r_it.font.name = self.font_name
            r_it.font.size = Pt(11)
            
        # Cột Phải: Chức vụ & Chữ ký
        p_title = c_right.paragraphs[0]
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.line_spacing = 1.0
        p_title.paragraph_format.space_before = Pt(0)
        p_title.paragraph_format.space_after = Pt(2)
        
        if signed_on_behalf:
            r_on_behalf = p_title.add_run(f"{signed_on_behalf.upper()}\n")
            r_on_behalf.font.name = self.font_name
            r_on_behalf.font.size = Pt(13)
            r_on_behalf.font.bold = True
            
        r_sig = p_title.add_run(signatory_title.upper())
        r_sig.font.name = self.font_name
        r_sig.font.size = Pt(13)
        r_sig.font.bold = True
        
        # Khoảng cách ký tên (~4 dòng trống)
        p_sign_space = c_right.add_paragraph()
        p_sign_space.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sign_space.paragraph_format.line_spacing = 1.0
        p_sign_space.paragraph_format.space_before = Pt(40)
        p_sign_space.paragraph_format.space_after = Pt(0)
        
        # Họ và tên người ký
        p_name = c_right.add_paragraph()
        p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_name.paragraph_format.line_spacing = 1.0
        p_name.paragraph_format.space_before = Pt(4)
        p_name.paragraph_format.space_after = Pt(0)
        r_name = p_name.add_run(signatory_name)
        r_name.font.name = self.font_name
        r_name.font.size = Pt(13)
        r_name.font.bold = True

    def add_landscape_section(self):
        """Thêm section xoay ngang (Landscape A4) để chứa bảng phụ lục rộng."""
        new_sec = self.doc.add_section()
        new_sec.orientation = WD_ORIENT.LANDSCAPE
        new_sec.page_width = Inches(11.69)
        new_sec.page_height = Inches(8.27)
        new_sec.top_margin = Inches(0.79)
        new_sec.bottom_margin = Inches(0.79)
        new_sec.left_margin = Inches(0.79)
        new_sec.right_margin = Inches(0.79)
        self._configure_page_numbering(new_sec)
        self.current_section = new_sec
        return new_sec

    def save(self, filepath: str) -> str:
        """
        Lưu văn bản ra file. Tự động chuyển hướng về OUTPUT/ nếu chỉ truyền tên file.
        """
        if not os.path.isabs(filepath) and not filepath.startswith("OUTPUT/"):
            filepath = os.path.join("OUTPUT", filepath)
            
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        self.doc.save(filepath)
        print(f"[ND30 Engine] Đã tạo thành công văn bản chuẩn NĐ 30: {filepath}")
        return filepath


if __name__ == "__main__":
    # Test thử nghiệm engine sinh 1 văn bản mẫu chuẩn NĐ 30
    engine = ND30Document()
    engine.add_header(
        agency_parent="VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM",
        agency_name="CHI NHÁNH SỐ 23",
        doc_code="Số: 99/TTr-CN23",
        location_date="Thủ Dầu Một, ngày 13 tháng 10 năm 2026"
    )
    engine.add_title(
        doc_type="TỜ TRÌNH",
        title="Về việc trang cấp bổ sung thiết bị tin học phục vụ chuyển đổi số",
        subtitle="(Kèm theo Bảng tổng hợp nhu cầu thiết bị năm 2026)"
    )
    engine.add_heading_1("I. SỰ CẦN THIẾT BAN HÀNH")
    engine.add_paragraph("Căn cứ chức năng, nhiệm vụ của Chi nhánh Văn phòng Đăng ký Đất đai số 23 và thực trạng hạ tầng công nghệ thông tin hiện hữu...")
    engine.add_heading_1("II. NHU CẦU TRANG CẤP THIẾT BỊ")
    
    headers = ["STT", "Tên thiết bị", "Đơn vị tính", "Số lượng", "Mục đích sử dụng"]
    data = [
        ["01", "Máy vi tính để bàn cấu hình cao", "Bộ", "15", "Xử lý bản đồ và cơ sở dữ liệu đất đai"],
        ["02", "Máy in laser tốc độ cao A4", "Cái", "08", "In ấn kết quả giải quyết hồ sơ TTHC"],
        ["03", "Máy quét chuyên dụng A3 (Scan)", "Cái", "02", "Số hóa hồ sơ tài liệu lưu trữ địa chính"]
    ]
    engine.add_table_data(headers, data, col_widths=[0.6, 2.3, 0.9, 0.8, 1.9])
    
    engine.add_footer_signatures(
        recipients=["Như kính gửi;", "Ban Giám đốc VPĐK;", "Lưu: VT, HCTH."],
        signatory_title="GIÁM ĐỐC",
        signatory_name="Nguyễn Thị Lệ Hằng"
    )
    test_out = engine.save("OUTPUT/Mau_van_ban_test_ND30.docx")
    print("Hoàn tất tạo thử nghiệm:", test_out)
