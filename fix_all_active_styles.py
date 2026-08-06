#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def fix_active_style(filepath):
    """Исправляет стиль для активного пункта меню"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже отдельный стиль для .nav a.active
        if '.nav a.active{color:var(--accent);font-weight:700}' in content:
            return False
        
        # Если есть объединенный стиль .nav a:hover,.nav a.active - разделяем их
        pattern1 = r'(\.nav a:hover\{color:var\(--accent\)\},\.nav a\.active\{color:var\(--accent\)\})'
        replacement1 = r'.nav a:hover{color:var(--accent)}\n.nav a.active{color:var(--accent);font-weight:700}'
        
        new_content = re.sub(pattern1, replacement1, content)
        
        # Если нет ни одного из стилей - добавляем
        if '.nav a.active' not in new_content:
            pattern2 = r'(\.nav a:hover\{color:var\(--accent\)\})'
            replacement2 = r'\1\n.nav a.active{color:var(--accent);font-weight:700}'
            new_content = re.sub(pattern2, replacement2, new_content)
        
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
    if fix_active_style(filepath):
        updated += 1

print(f"\nИсправлен стиль active в {updated} файлах")
