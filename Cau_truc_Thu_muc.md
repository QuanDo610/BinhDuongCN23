# Quy Định Tổ Chức Thư Mục Dự Án (Folder Structure Best Practices)

Dự án này được thiết kế để xử lý dữ liệu và văn bản cho văn phòng, do đó việc tổ chức thư mục một cách khoa học, gọn gàng là yếu tố tiên quyết.

## 1. Cấu trúc thư mục chuẩn

```text
BINHDUONG/
│
├── documents/          # CHỈ chứa tài liệu đầu vào (PDF, DOCX, XLSX). Không chứa file code.
├── OUTPUT/             # CHỈ chứa kết quả đầu ra (báo cáo, file DOCX/XLSX mới, file HTML, PDF).
├── tools/              # CHỈ chứa các mã nguồn (Python scripts, JS, v.v) thực thi tác vụ.
├── venv/               # Môi trường ảo Python (Không đụng vào).
│
├── Gemini.md           # Hướng dẫn tổng quan cho AI (Bắt buộc).
├── Agent.md            # Hành vi và tính cách của AI.
├── Rule.md             # Quy tắc nghiêm ngặt mà AI phải tuân theo.
├── Skill.md            # Các kỹ năng và nghiệp vụ khả dụng.
├── QUY_CHUAN_DOCX_ND30.md # Tiêu chuẩn kỹ thuật định dạng văn bản (NĐ 30).
├── Cau_truc_Thu_muc.md # Cấu trúc dự án (File này).
└── Quy_trinh_Don_dep.md# Quy trình dọn dẹp và bảo trì hệ thống.
```

## 2. Quy tắc cốt lõi (Best Practices)

- **Không vứt file rác ở thư mục gốc (Root):** Thư mục gốc chỉ chứa các thư mục con chính, các file Markdown (`.md`) về kiến trúc hệ thống, `README.md`, và `.gitignore`. Bất kỳ file `.py`, `.docx`, `.pdf`, v.v nào ở thư mục gốc đều bị coi là "sai quy chuẩn".
- **Phân tách Rõ Ràng (Separation of Concerns):** 
  - Code nằm ở `tools/`. Tuyệt đối không để `.py` lạc ra ngoài.
  - Dữ liệu thô nằm ở `documents/`. Không sửa trực tiếp file trong này.
  - Kết quả xuất ra nằm ở `OUTPUT/`.
- **Tên File (Naming Convention):** Sử dụng `_` thay vì khoảng trắng (VD: `Bao_cao_thang_1.docx` thay vì `Bao cao thang 1.docx`). Các file nháp hoặc đang chỉnh sửa nên có hậu tố version (`_v1`, `_v2`), file chốt phải có `_FINAL`.
