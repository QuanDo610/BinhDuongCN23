import zipfile
import xml.etree.ElementTree as ET
import sys
import re

def analyze_excel_builtin(file_path):
    print(f"=== Analyzing: {file_path} ===")
    try:
        with zipfile.ZipFile(file_path, 'r') as archive:
            # Get shared strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in archive.namelist():
                xml_content = archive.read('xl/sharedStrings.xml')
                root = ET.fromstring(xml_content)
                # the namespace is usually xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in root.findall('.//ns:t', ns):
                    shared_strings.append(t.text if t.text else "")
            
            # Get workbook to find sheets
            workbook_xml = archive.read('xl/workbook.xml')
            root = ET.fromstring(workbook_xml)
            ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            sheets = []
            for sheet in root.findall('.//ns:sheet', ns):
                name = sheet.attrib.get('name')
                rId = sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                sheets.append((name, rId))
            print(f"Sheets found: {[s[0] for s in sheets]}")

            # Get sheet relations to map rId to target file
            rels_xml = archive.read('xl/_rels/workbook.xml.rels')
            rels_root = ET.fromstring(rels_xml)
            rels_ns = {'ns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            rel_map = {}
            for rel in rels_root.findall('.//ns:Relationship', rels_ns):
                rel_map[rel.attrib['Id']] = rel.attrib['Target']

            # Read first few rows of each sheet
            for name, rId in sheets:
                print(f"\n--- Sheet: {name} ---")
                target = rel_map.get(rId)
                if not target:
                    continue
                # target might be 'worksheets/sheet1.xml' etc
                sheet_path = f"xl/{target}"
                if sheet_path not in archive.namelist():
                    continue
                
                sheet_xml = archive.read(sheet_path)
                sheet_root = ET.fromstring(sheet_xml)
                
                row_count = 0
                for row in sheet_root.findall('.//ns:row', ns):
                    if row_count >= 15: # preview first 15 rows
                        break
                    row_data = []
                    for c in row.findall('.//ns:c', ns):
                        t = c.attrib.get('t')
                        v = c.find('ns:v', ns)
                        val = v.text if v is not None else ""
                        if t == 's' and val: # shared string
                            try:
                                idx = int(val)
                                if idx < len(shared_strings):
                                    val = shared_strings[idx]
                            except ValueError:
                                pass
                        row_data.append(val)
                    print(f"Row {row_count + 1}: {row_data}")
                    row_count += 1
                    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    analyze_excel_builtin("/Users/admin/Desktop/BINHDUONG/BẢNG KPI CÔNG VIỆC - KẾ HOẠCH 9999 mới.xlsx")
    print("\n" + "="*50 + "\n")
    analyze_excel_builtin("/Users/admin/Desktop/BINHDUONG/DS BAO CAO 9999 THEO NGAY.xlsx")
