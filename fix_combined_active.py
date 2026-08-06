#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def fix_combined_active(filepath):
    """Исправляет объединенный стиль для активного пункта меню"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Если есть объединенный стиль .nav a:hover,.nav a.active - разделяем их
        pattern = r'\.nav a:hover,\s*\.nav a\.active\{color:var\(--accent\)\}'
        replacement = '.nav a:hover{color:var(--accent)}\n.nav a.active{color:var(--accent);font-weight:700}'
        
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

# Исправляем стиль во всех файлах
updated = 0
for filepath in html_files:
    if fix_combined_active(filepath):
        updated += 1

print(f"\nИсправлен объединенный стиль active в {updated} файлах")
