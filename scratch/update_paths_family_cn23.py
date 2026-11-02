# -*- coding: utf-8 -*-
import os

root_dir = '/Users/admin/Desktop/FAMILY_CN23'
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith(('.md', '.html', '.txt')):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace absolute paths
            new_content = content.replace('/Users/admin/Desktop/BINHDUONG/A_THANG', '/Users/admin/Desktop/FAMILY_CN23')
            new_content = new_content.replace('file:///Users/admin/Desktop/BINHDUONG/A_THANG/', 'file:///Users/admin/Desktop/FAMILY_CN23/')
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated: {os.path.relpath(path, root_dir)}")
