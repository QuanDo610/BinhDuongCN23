import pandas as pd
import sys

def analyze_excel(file_path):
    print(f"=== Analyzing: {file_path} ===")
    try:
        # Read all sheets
        xl = pd.ExcelFile(file_path)
        print(f"Sheets: {xl.sheet_names}")
        
        for sheet in xl.sheet_names:
            print(f"\n--- Sheet: {sheet} ---")
            df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
            print("Columns:", df.columns.tolist())
            print("Preview data:")
            print(df.to_string())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    analyze_excel("/Users/admin/Desktop/BINHDUONG/BẢNG KPI CÔNG VIỆC - KẾ HOẠCH 9999 mới.xlsx")
    print("\n" + "="*50 + "\n")
    analyze_excel("/Users/admin/Desktop/BINHDUONG/DS BAO CAO 9999 THEO NGAY.xlsx")
