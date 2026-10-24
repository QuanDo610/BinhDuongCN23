#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_pipeline.py - Pipeline Tự động Xử lý, Bóc tách Text & OCR Tài liệu
========================================================================
Tự động quét tài liệu trong documents/, bóc tách nội dung ra scratch/cache_texts/
kèm theo bảng chỉ mục MD5 (scratch/documents_index.json) để không bao giờ phải
xử lý lại tài liệu cũ.

Hỗ trợ các định dạng:
- PDF (Tự động nhận diện PDF văn bản hay PDF scan đóng dấu để gọi Apple Vision OCR)
- Word (.docx, .doc)
- Excel (.xlsx, .xls) & CSV
- Ảnh chụp scan (.png, .jpg, .jpeg, .tiff)
"""

import os
import sys
import json
import hashlib
import subprocess
import datetime
from typing import Dict, Any, Optional, Tuple

import pypdf
import docx
import openpyxl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch")
CACHE_DIR = os.path.join(SCRATCH_DIR, "cache_texts")
INDEX_FILE = os.path.join(SCRATCH_DIR, "documents_index.json")
OCR_TOOL = os.path.join(BASE_DIR, "tools", "ocr_vision")

os.makedirs(CACHE_DIR, exist_ok=True)

def calculate_md5(filepath: str) -> str:
    """Tính mã băm MD5 của tệp tin."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def sanitize_filename(filename: str) -> str:
    """Tạo tên file an toàn cho cache text."""
    keepchars = ('_', '-', '.')
    clean = "".join(c if (c.isalnum() or c in keepchars) else "_" for c in filename)
    return clean

def load_index() -> Dict[str, Any]:
    """Tải bảng chỉ mục cache hiện tại."""
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_index(index_data: Dict[str, Any]):
    """Lưu bảng chỉ mục cache."""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

def extract_docx(filepath: str) -> str:
    """Trích xuất toàn bộ text và bảng biểu từ file DOCX."""
    doc = docx.Document(filepath)
    lines = []
    
    # 1. Các đoạn văn bản
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            lines.append(t)
            
    # 2. Dữ liệu các bảng biểu
    if doc.tables:
        lines.append("\n=== [DANH SÁCH BẢNG BIỂU TRONG TÀI LIỆU] ===")
        for t_idx, table in enumerate(doc.tables, 1):
            lines.append(f"\n--- Bảng số {t_idx} ({len(table.rows)} hàng, {len(table.columns)} cột) ---")
            for row in table.rows:
                row_cells = [c.text.strip().replace("\n", " ") for c in row.cells]
                # Loại bỏ ô trùng lặp khi merge
                clean_cells = []
                for val in row_cells:
                    if not clean_cells or val != clean_cells[-1]:
                        clean_cells.append(val)
                lines.append(" | ".join(clean_cells))
                
    return "\n".join(lines)

def extract_excel(filepath: str) -> str:
    """Trích xuất cấu trúc và nội dung bảng tính Excel."""
    wb = openpyxl.load_workbook(filepath, data_only=True)
    lines = []
    lines.append(f"Danh sách Sheets: {', '.join(wb.sheetnames)}\n")
    
    for s_name in wb.sheetnames:
        sheet = wb[s_name]
        lines.append(f"=== SHEET: {s_name} (Kích thước: {sheet.max_row} hàng x {sheet.max_column} cột) ===")
        row_count = 0
        for row in sheet.iter_rows(values_only=True):
            if any(cell is not None for cell in row):
                row_vals = [str(c if c is not None else "").strip() for c in row]
                lines.append(" | ".join(row_vals))
                row_count += 1
                if row_count >= 500:  # Giới hạn 500 hàng mẫu nếu file quá lớn
                    lines.append(f"... (Còn {sheet.max_row - 500} hàng tiếp theo)")
                    break
        lines.append("")
    return "\n".join(lines)

def extract_csv(filepath: str) -> str:
    """Đọc file CSV."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_pdf(filepath: str) -> Tuple[str, str, int]:
    """
    Trích xuất file PDF:
    - Thử đọc text layer bằng pypdf.
    - Nếu text rỗng hoặc dưới 250 ký tự -> Tự động gọi Apple Vision OCR (ocr_vision).
    Trả về: (nội dung text, phương thức 'text'|'ocr', số trang)
    """
    try:
        reader = pypdf.PdfReader(filepath)
        page_count = len(reader.pages)
        raw_text_parts = []
        for idx, page in enumerate(reader.pages, 1):
            t = page.extract_text() or ""
            raw_text_parts.append((idx, t.strip()))
            
        total_len = sum(len(t) for _, t in raw_text_parts)
        
        # Nếu có text layer sạch và đủ dài
        if total_len > 250:
            formatted_pages = []
            for idx, t in raw_text_parts:
                formatted_pages.append(f"=== TRANG {idx}/{page_count} ===\n{t}")
            return "\n\n".join(formatted_pages), "text", page_count
    except Exception as e:
        page_count = 1

    # Nếu là PDF scan dạng ảnh -> Gọi Apple Vision OCR
    if os.path.exists(OCR_TOOL):
        res = subprocess.run([OCR_TOOL, filepath], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip(), "ocr_vision", page_count
        else:
            return f"[Lỗi OCR]: {res.stderr}", "ocr_error", page_count
    else:
        return "[Lỗi]: Không tìm thấy công cụ ocr_vision", "error", page_count

def extract_image(filepath: str) -> str:
    """OCR file hình ảnh bằng Apple Vision."""
    if os.path.exists(OCR_TOOL):
        res = subprocess.run([OCR_TOOL, filepath], capture_output=True, text=True)
        return res.stdout.strip() if res.returncode == 0 else f"[Lỗi OCR]: {res.stderr}"
    return "[Lỗi]: Không tìm thấy công cụ ocr_vision"

def process_file(filepath: str, index_data: Dict[str, Any], force: bool = False) -> Optional[Dict[str, Any]]:
    """Xử lý trích xuất cho 1 file duy nhất với cơ chế kiểm tra Cache MD5."""
    rel_path = os.path.relpath(filepath, BASE_DIR)
    filename = os.path.basename(filepath)
    
    if filename.startswith(".") or filename in [".DS_Store", ".gitkeep"]:
        return None
        
    ext = os.path.splitext(filename)[1].lower()
    supported_exts = [".pdf", ".docx", ".xlsx", ".xls", ".csv", ".png", ".jpg", ".jpeg", ".tiff"]
    if ext not in supported_exts:
        return None

    current_md5 = calculate_md5(filepath)
    file_size = os.path.getsize(filepath)
    
    # Kiểm tra Cache Hit
    if not force and rel_path in index_data:
        cached = index_data[rel_path]
        if cached.get("md5") == current_md5 and os.path.exists(cached.get("cache_file", "")):
            return cached  # Đã có cache và file không thay đổi

    print(f"[*] Đang bóc tách dữ liệu: {rel_path} ({file_size / 1024:.1f} KB)...")
    
    safe_name = sanitize_filename(filename) + ".txt"
    cache_path = os.path.join(CACHE_DIR, safe_name)
    method = "unknown"
    page_count = 1
    content = ""
    
    try:
        if ext == ".docx":
            content = extract_docx(filepath)
            method = "docx_native"
        elif ext in [".xlsx", ".xls"]:
            content = extract_excel(filepath)
            method = "excel_native"
        elif ext == ".csv":
            content = extract_csv(filepath)
            method = "csv_native"
        elif ext == ".pdf":
            content, method, page_count = extract_pdf(filepath)
        elif ext in [".png", ".jpg", ".jpeg", ".tiff"]:
            content = extract_image(filepath)
            method = "ocr_vision"
            
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        meta = {
            "file": rel_path,
            "filename": filename,
            "md5": current_md5,
            "size_bytes": file_size,
            "ext": ext,
            "method": method,
            "page_count": page_count,
            "char_count": len(content),
            "cache_file": os.path.relpath(cache_path, BASE_DIR),
            "updated_at": datetime.datetime.now().isoformat()
        }
        index_data[rel_path] = meta
        print(f" -> Thành công! Lưu cache tại: {meta['cache_file']} ({meta['char_count']} ký tự, mode: {method})")
        return meta
    except Exception as e:
        print(f" [!] Thất bại khi xử lý {rel_path}: {e}")
        return None

def sync_all(force: bool = False):
    """Quét và đồng bộ toàn bộ tài liệu trong documents/."""
    print("=== BẮT ĐẦU ĐỒNG BỘ KHO TÀI LIỆU (DOCUMENT PIPELINE) ===")
    index_data = load_index()
    processed_count = 0
    cache_hit_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for f in sorted(files):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, BASE_DIR)
            md5_before = index_data.get(rel_path, {}).get("md5")
            res = process_file(full_path, index_data, force=force)
            if res:
                if res.get("md5") == md5_before and not force:
                    cache_hit_count += 1
                else:
                    processed_count += 1
                    
    save_index(index_data)
    print("=== ĐỒNG BỘ HOÀN TẤT ===")
    print(f"Tổng số tài liệu sẵn sàng: {len(index_data)}")
    print(f"Mới xử lý / Cập nhật: {processed_count} file")
    print(f"Đã có sẵn trong Cache (Hit): {cache_hit_count} file")

def list_documents():
    """Liệt kê danh sách tài liệu trong kho và trạng thái bóc tách."""
    index_data = load_index()
    print(f"\n=== DANH MỤC {len(index_data)} TÀI LIỆU TRONG KHO (CACHE READY) ===")
    for rel_path, meta in sorted(index_data.items(), key=lambda x: x[0]):
        fn = meta.get("filename", "")
        method = meta.get("method", "")
        chars = meta.get("char_count", 0)
        print(f"- [{method.upper():<12}] {fn:<60} ({chars:,} ký tự)")

def search_text(query: str):
    """Tìm kiếm nội dung tức thì trong kho cache text."""
    index_data = load_index()
    print(f"\n=== TÌM KIẾM TỪ KHÓA: '{query}' ===")
    matches = []
    
    for rel_path, meta in index_data.items():
        cache_file = os.path.join(BASE_DIR, meta.get("cache_file", ""))
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8", errors="ignore") as f:
                c = f.read()
                if query.lower() in c.lower():
                    matches.append((meta["filename"], cache_file, c.lower().count(query.lower())))
                    
    print(f"Tìm thấy trong {len(matches)} tài liệu:")
    for fn, cf, count in sorted(matches, key=lambda x: x[2], reverse=True):
        print(f" -> {fn} ({count} lần xuất hiện) -> {cf}")

def get_text(filename_keyword: str):
    """In ra toàn bộ nội dung text của tài liệu tìm thấy."""
    index_data = load_index()
    for rel_path, meta in index_data.items():
        if filename_keyword.lower() in meta["filename"].lower():
            cache_file = os.path.join(BASE_DIR, meta.get("cache_file", ""))
            if os.path.exists(cache_file):
                print(f"=== NỘI DUNG TÀI LIỆU: {meta['filename']} ===")
                with open(cache_file, "r", encoding="utf-8") as f:
                    print(f.read())
                return
    print(f"Không tìm thấy tài liệu phù hợp từ khóa: '{filename_keyword}'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "sync":
            force_flag = "--force" in sys.argv
            sync_all(force=force_flag)
        elif cmd == "list":
            list_documents()
        elif cmd == "search" and len(sys.argv) > 2:
            search_text(sys.argv[2])
        elif cmd == "get" and len(sys.argv) > 2:
            get_text(sys.argv[2])
        else:
            print("Cú pháp: python3 tools/doc_pipeline.py [sync|list|search <query>|get <filename>]")
    else:
        sync_all()
