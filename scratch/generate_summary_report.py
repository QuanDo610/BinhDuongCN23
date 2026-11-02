#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.path.insert(0, os.path.abspath('.'))
from tools.nd30_engine import ND30Document

def build_report():
    doc = ND30Document(font_size_body=13.0)

    # 1. Khối Header chuẩn NĐ 30
    doc.add_header(
        agency_parent="VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI TP.HCM",
        agency_name="CHI NHÁNH SỐ 23",
        doc_code="Số:      /BC-CN23",
        location_date="Thủ Dầu Một, ngày 30 tháng 10 năm 2026"
    )

    # 2. Tiêu đề Báo cáo
    doc.add_title(
        doc_type="BÁO CÁO",
        title="TỔNG HỢP RÀ SOÁT 03 VĂN BẢN MỚI VỀ AN NINH MẠNG VÀ ĐÁNH GIÁ CẤP ĐỘ AN TOÀN HỆ THỐNG THÔNG TIN TẠI CHI NHÁNH SỐ 23",
        subtitle="(Kèm theo kết quả xác định hiện trạng an toàn hệ thống mạng nội bộ)"
    )

    # 3. Nội dung văn bản
    # Phần I
    doc.add_heading_1("I. TỔNG QUAN 03 VĂN BẢN MỚI TIẾP NHẬN TRONG THƯ MỤC DOCUMENTS")
    doc.add_paragraph(
        "Thực hiện công tác quản trị vận hành công nghệ thông tin và bảo đảm an toàn, an ninh mạng hệ thống thông tin, Chi nhánh Văn phòng Đăng ký đất đai số 23 tiến hành kiểm tra, rà soát 03 tài liệu mới được tiếp nhận và lưu trữ trong hệ thống tài liệu (thư mục documents/), bao gồm:"
    )

    headers = ["STT", "Tên tệp tin / Số hiệu", "Trích yếu nội dung", "Cơ quan ban hành", "Ngày ban hành", "Ghi chú"]
    rows_data = [
        [
            "1",
            "183_0001  QD phe Duyet cap do.pdf\n(Số: 183/QĐ-STTTT)",
            "Về việc phê duyệt cấp độ an toàn hệ thống thông tin đối với Hệ thống mạng nội bộ tại Chi nhánh Văn phòng Đăng ký đất đai Thành phố Thủ Dầu Một",
            "Sở Thông tin và Truyền thông tỉnh Bình Dương",
            "29/06/2023",
            "Bản scan (02 trang), có dấu đỏ và chữ ký Giám đốc Sở Lê Tuấn Anh. Dấu đến Chi nhánh ngày 03/7/2023."
        ],
        [
            "2",
            "8771-CATP_signed.pdf\n(Số: 8771/CATP-PA05)",
            "V/v hướng dẫn tổ chức thực hiện bảo vệ an ninh mạng đối với hệ thống thông tin theo cấp độ (cẩm nang hướng dẫn chuyên môn và quy chuẩn)",
            "Công an TP. Hồ Chí Minh\n(Phòng PA05)",
            "03/10/2026",
            "Bản điện tử (21 trang), ký bởi Đại tá Lê Công Anh - Phó Giám đốc CATP."
        ],
        [
            "3",
            "đôn đốc thực hiện hồ sơ ĐXCĐ.pdf\n(Số: .../TCTANM)",
            "V/v thực hiện đảm bảo an ninh mạng hệ thống thông tin theo cấp độ (văn bản đôn đốc khẩn cấp)",
            "Tổ công tác về an ninh mạng - Ban Chỉ đạo TP.HCM về PT KHCN, ĐMST và CĐS",
            "Tháng 10/2026",
            "Bản điện tử (03 trang), ký bởi Đại tá Lê Công Anh - Tổ phó thường trực. Hạn báo cáo: 30/10/2026."
        ]
    ]

    col_widths = [0.45, 1.4, 2.0, 1.25, 0.7, 0.7]
    alignments = [
        WD_ALIGN_PARAGRAPH.CENTER,
        WD_ALIGN_PARAGRAPH.LEFT,
        WD_ALIGN_PARAGRAPH.LEFT,
        WD_ALIGN_PARAGRAPH.LEFT,
        WD_ALIGN_PARAGRAPH.CENTER,
        WD_ALIGN_PARAGRAPH.LEFT
    ]
    doc.add_table_data(headers=headers, rows_data=rows_data, col_widths=col_widths, alignments=alignments)

    # Phần II
    doc.add_heading_1("II. TÓM TẮT CHI TIẾT NỘI DUNG TỪNG VĂN BẢN")

    doc.add_heading_2("1. Quyết định số 183/QĐ-STTTT ngày 29/06/2023 của Sở TT&TT tỉnh Bình Dương")
    doc.add_paragraph(
        "- Căn cứ pháp lý: Luật An toàn thông tin mạng năm 2015; Nghị định số 85/2016/NĐ-CP ngày 01/7/2016 của Chính phủ; Thông tư số 12/2022/TT-BTTTT ngày 12/8/2022 của Bộ Thông tin và Truyền thông; Báo cáo thẩm định số 05/BCTĐ-HĐTĐ ngày 27/6/2023 của Hội đồng thẩm định."
    )
    doc.add_paragraph(
        "- Nội dung phê duyệt (Điều 1): Phê duyệt cấp độ an toàn hệ thống thông tin đối với Chi nhánh Văn phòng Đăng ký đất đai Thành phố Thủ Dầu Một với các thông số cụ thể:"
    )
    doc.add_bullet_point("Tên hệ thống thông tin: Hệ thống mạng nội bộ tại Chi nhánh Văn phòng Đăng ký đất đai Thành phố Thủ Dầu Một.")
    doc.add_bullet_point("Đơn vị vận hành: Chi nhánh Văn phòng Đăng ký đất đai Thành phố Thủ Dầu Một.")
    doc.add_bullet_point("Địa điểm: Số 358 đường Huỳnh Văn Cù, phường Chánh Mỹ (nay là phường Thủ Dầu Một), TP. Thủ Dầu Một.")
    doc.add_bullet_point("CẤP ĐỘ AN TOÀN HỆ THỐNG THÔNG TIN: CẤP ĐỘ 2.")
    doc.add_bullet_point("Phương án bảo đảm an toàn: Đạt chuẩn TCVN 11930:2017 và Thông tư số 12/2022/TT-BTTTT.")
    doc.add_paragraph(
        "- Trách nhiệm thực thi (Điều 2, Điều 3): Chi nhánh và Văn phòng Đăng ký đất đai có trách nhiệm bảo đảm an toàn theo Điều 22 Nghị định số 85/2016/NĐ-CP; Sở TT&TT kiểm tra, giám sát định kỳ."
    )

    doc.add_heading_2("2. Công văn số 8771/CATP-PA05 ngày 03/10/2026 của Công an TP. Hồ Chí Minh")
    doc.add_paragraph(
        "- Căn cứ pháp lý mới: Căn cứ Luật An ninh mạng số 116/2025/QH15 (có hiệu lực 01/07/2026), Nghị định số 331/2026/NĐ-CP ngày 19/8/2026 của Chính phủ và Tiêu chuẩn quốc gia TCVN 14423:2026; Kế hoạch số 05-KH/BCĐTW về hành động 100 ngày xử lý điểm nghẽn chuyển đổi số."
    )
    doc.add_paragraph(
        "- Tiêu chí phân cấp 5 cấp độ an ninh mạng hệ thống thông tin:"
    )
    doc.add_bullet_point("Cấp độ 1: Phục vụ nội bộ cơ quan và chỉ xử lý thông tin công cộng.")
    doc.add_bullet_point("Cấp độ 2: Phục vụ nội bộ cơ quan có xử lý thông tin riêng, dữ liệu cá nhân (không xử lý bí mật nhà nước); hoặc dịch vụ trực tuyến phục vụ dưới 100.000 chủ thể dữ liệu cá nhân cơ bản; hạ tầng CNTT phục vụ hoạt động của 01 cơ quan, tổ chức.")
    doc.add_bullet_point("Cấp độ 3: Hệ thống xử lý thông tin bí mật nhà nước/QP-AN; hệ thống giải quyết TTHC; dịch vụ trực tuyến từ 100.000 dữ liệu cá nhân trở lên; hạ tầng cấp tỉnh hoặc bộ ngành.")
    doc.add_bullet_point("Cấp độ 4 & 5: Hệ thống Chính phủ điện tử 24/7, hạ tầng thông tin quốc gia, công trình an ninh quốc gia đặc biệt quan trọng.")
    doc.add_paragraph(
        "- Thẩm quyền phê duyệt: Cấp 1 và Cấp 2 do Đơn vị chuyên trách an ninh mạng của chủ quản hệ thống thẩm định và phê duyệt (hoặc trình chủ quản phê duyệt tuỳ phân cấp). Cấp 3 do Chủ quản phê duyệt. Cấp 4, 5 do Bộ Công an thẩm định."
    )
    doc.add_paragraph(
        "- Triển khai mô hình 4 lớp bảo đảm an ninh mạng toàn diện:"
    )
    doc.add_bullet_point("Lớp 1 (Lực lượng tại chỗ): Kiện toàn cán bộ chuyên trách CNTT/ANM, lãnh đạo đơn vị trực tiếp phụ trách, lập đội ứng cứu sự cố liên ngành.")
    doc.add_bullet_point("Lớp 2 (Giám sát, bảo vệ chuyên nghiệp): Giám sát 24/7; triển khai phần mềm giám sát và chống mã độc tập trung (Kaspersky Endpoint, NCS EDR) trên thiết bị đầu cuối.")
    doc.add_bullet_point("Lớp 3 (Kiểm tra, đánh giá độc lập): Tự kiểm tra định kỳ tối thiểu 01 năm/lần (cấp 1, 2) hoặc thuê chuyên gia độc lập đánh giá (cấp 3 trở lên).")
    doc.add_bullet_point("Lớp 4 (Kết nối, chia sẻ quốc gia): Kết nối dữ liệu giám sát và phòng chống mã độc về Trung tâm An ninh mạng quốc gia (liên tục 24/7, không đứt kết nối quá 24h, chia sẻ 100% cảnh báo mức cao/nghiêm trọng).")
    doc.add_paragraph(
        "- Yêu cầu khẩn: Rà soát lập Bản đồ số cấp độ an ninh mạng theo mẫu Phụ lục I và gửi CATP trước ngày 25/10/2026; đăng ký kết nối giám sát."
    )

    doc.add_heading_2("3. Công văn của Tổ công tác về an ninh mạng - Ban Chỉ đạo TP.HCM (Tháng 10/2026)")
    doc.add_paragraph(
        "- Bối cảnh & Cảnh báo: Tấn công ransomware mã hóa đòi tiền chuộc và lộ lọt dữ liệu cá nhân đang diễn biến phức tạp nhắm vào các hệ thống dữ liệu công vụ trên địa bàn thành phố."
    )
    doc.add_paragraph(
        "- Thực trạng toàn Thành phố Hồ Chí Minh: Qua thống kê xác định có 546 hệ thống thông tin. Tuy nhiên tiến độ phê duyệt hồ sơ đề xuất cấp độ (ĐXCĐ) còn rất hạn chế:"
    )
    doc.add_bullet_point("Đã phê duyệt hồ sơ ĐXCĐ: 65/546 hệ thống (đạt tỷ lệ rất thấp 11,9%).")
    doc.add_bullet_point("Chưa phê duyệt hồ sơ ĐXCĐ: 481/546 hệ thống (chiếm tới 88,1%).")
    doc.add_paragraph(
        "- Chỉ đạo khẩn cấp: Yêu cầu 100% hệ thống phải được thẩm định và phê duyệt cấp độ; 100% hệ thống tự kiểm tra định kỳ theo Nghị định 331/2026/NĐ-CP và TCVN 14423:2026; BÁO CÁO KẾT QUẢ VỀ TỔ CÔNG TÁC (qua Phòng PA05 CATP) TRƯỚC NGÀY 30/10/2026."
    )

    # Phần III
    doc.add_heading_1("III. KẾT LUẬN VỀ CẤP ĐỘ AN TOÀN TẠI CHI NHÁNH SỐ 23 VÀ NHIỆM VỤ CẦN TRIỂN KHAI")
    doc.add_heading_2("1. Trả lời trực tiếp về Cấp độ an toàn hệ thống thông tin của Chi nhánh số 23")
    doc.add_paragraph(
        "Căn cứ Quyết định số 183/QĐ-STTTT ngày 29/06/2023 của Giám đốc Sở Thông tin và Truyền thông tỉnh Bình Dương, hệ thống mạng nội bộ tại Chi nhánh Văn phòng Đăng ký đất đai Thành phố Thủ Dầu Một (tiền thân và là cơ sở hoạt động hiện tại của Chi nhánh Văn phòng Đăng ký đất đai số 23, địa chỉ tại 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một):"
    )
    doc.add_bullet_point("HỆ THỐNG MẠNG NỘI BỘ CHI NHÁNH SỐ 23 ĐANG Ở: CẤP ĐỘ 2 (AN TOÀN HỆ THỐNG THÔNG TIN CẤP ĐỘ 2).")
    doc.add_bullet_point("Hệ thống thuộc nhóm 11,9% (65/546 hệ thống) trên toàn địa bàn Thành phố đã hoàn thành phê duyệt hồ sơ cấp độ hợp thức bằng văn bản của cơ quan có thẩm quyền.")
    doc.add_bullet_point("Đối chiếu với Nghị định số 331/2026/NĐ-CP và Hướng dẫn số 8771/CATP-PA05: Hệ thống mạng nội bộ của Chi nhánh 23 phục vụ điều hành nội bộ và giải quyết hồ sơ nghiệp vụ địa chính (có xử lý thông tin cá nhân của người dân, không xử lý bí mật nhà nước), hoàn toàn đáp ứng đúng tiêu chí Hệ thống thông tin Cấp độ 2.")

    doc.add_heading_2("2. Các nhiệm vụ khẩn cấp cần triển khai ngay")
    doc.add_bullet_point("Khẩn trương báo cáo số liệu trước ngày 30/10/2026: Gửi văn bản trích dẫn Quyết định số 183/QĐ-STTTT ngày 29/06/2023 báo cáo về Văn phòng Đăng ký đất đai TP.HCM và Phòng PA05 CATP để xác nhận hệ thống đã được phê duyệt Cấp độ 2, bảo đảm chỉ số DTI của đơn vị.")
    doc.add_bullet_point("Thực hiện chuyển tiếp theo Nghị định 331/2026/NĐ-CP: Trong thời hạn chuyển tiếp 12 tháng, phối hợp bộ phận chuyên trách rà soát, cập nhật phương án an ninh mạng theo tiêu chuẩn kỹ thuật mới TCVN 14423:2026.")
    doc.add_bullet_point("Triển khai đầy đủ Mô hình 4 lớp: Cài đặt giải pháp phòng chống mã độc tập trung (Kaspersky Endpoint / NCS EDR) trên 100% máy trạm cán bộ Chi nhánh 23; thiết lập kết nối giám sát (Lớp 2 & Lớp 4).")
    doc.add_bullet_point("Thực hiện tự kiểm tra an ninh mạng định kỳ: Tối thiểu 01 lần/năm theo quy định tại Điều 33 Nghị định số 331/2026/NĐ-CP.")

    # 4. Chân trang chữ ký & nơi nhận
    recipients = [
        "Ban Giám đốc Chi nhánh số 23 (để báo cáo);",
        "Tổ Hành chính - Tổng hợp (để phối hợp);",
        "Bộ phận CNTT (để thực hiện);",
        "Lưu: VT, CNTT."
    ]
    doc.add_footer_signatures(
        recipients=recipients,
        signatory_title="NGƯỜI LẬP BÁO CÁO",
        signatory_name="Đỗ Trọng Minh Quân",
        signed_on_behalf=None
    )

    out_path = "OUTPUT/BAO_CAO_TONG_HOP_3_VAN_BAN_AN_NINH_MANG_CN23.docx"
    doc.save(out_path)
    print(f"Successfully generated: {out_path}")

if __name__ == "__main__":
    build_report()
