#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def add_active_style(filepath):
    """Добавляет стиль для активного пункта меню"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже стиль для .nav a.active
        if '.nav a.active' in content or '.nav a.active{' in content:
            return False
        
        # Находим место после .nav a:hover и добавляем стиль для active
        pattern = r'(\.nav a:hover\{color:var\(--accent\)\})'
        replacement = r'\1\n.nav a.active{color:var(--accent);font-weight:700}'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")
        return False

# Находим все HTML файлы
html_files = []
for root, dirs, files in os.walk('/workspace'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"Найдено {len(html_files)} HTML файлов")

# Добавляем стиль во все файлы
updated = 0
for filepath in html_files:
    if add_active_style(filepath):
        updated += 1

print(f"\nДобавлен стиль active в {updated} файлах")
