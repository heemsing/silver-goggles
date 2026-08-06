#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления всех ссылок и путей на сайте для хостинга на дом-помощи.рф
"""

import os
import re

BASE_DOMAIN = "https://дом-помощи.рф"
WORKSPACE = "/workspace"

ROOT_DIRS = {'adresa', 'vakansii', 'blog', 'vosstanovlenie-dokumentov', 'css', 'img'}

def get_html_files():
    html_files = []
    for root, dirs, files in os.walk(WORKSPACE):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def normalize_path(href_value, current_file_path):
    # Если это якорь, tel:, mailto: или внешний URL - возвращаем как есть
    if href_value.startswith(('#', 'tel:', 'mailto:', 'http://', 'https://')):
        return href_value
    
    # Получаем путь относительно workspace
    rel_path = os.path.relpath(current_file_path, WORKSPACE)
    current_dir = os.path.dirname(rel_path)
    
    # Удаляем ведущие ./
    while href_value.startswith('./'):
        href_value = href_value[2:]
    
    # Подсчитываем количество ../
    parent_count = 0
    temp_href = href_value
    while temp_href.startswith('../'):
        parent_count += 1
        temp_href = temp_href[3:]
    
    # Проверяем, начинается ли путь с известной корневой директории
    starts_with_root_dir = False
    for root_dir in ROOT_DIRS:
        if href_value.startswith(root_dir + '/') or href_value == root_dir:
            starts_with_root_dir = True
            break
    
    # Если путь начинается с корневой директории или мы поднялись достаточно высоко
    if starts_with_root_dir or parent_count >= (current_dir.count('/') + 1 if current_dir else 0):
        # Это ссылка на файл в корне или в одной из основных директорий
        return f"{BASE_DOMAIN}/{href_value}" if href_value else BASE_DOMAIN
    
    # Если мы в поддиректории и ссылка на файл в той же директории
    if current_dir:
        return f"{BASE_DOMAIN}/{current_dir}/{href_value}"
    else:
        return f"{BASE_DOMAIN}/{href_value}"

def fix_all_paths(content, current_file_path):
    def replace_href(match):
        href_value = match.group(1)
        new_url = normalize_path(href_value, current_file_path)
        return f'href="{new_url}"'
    
    def replace_src(match):
        src_value = match.group(1)
        new_url = normalize_path(src_value, current_file_path)
        return f'src="{new_url}"'
    
    content = re.sub(r'href="([^"]*)"', replace_href, content)
    content = re.sub(r'src="([^"]*)"', replace_src, content)
    
    return content

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_all_paths(content, file_path)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Ошибка обработки {file_path}: {e}")
        return False

def main():
    html_files = get_html_files()
    print(f"Найдено HTML файлов: {len(html_files)}")
    
    updated_count = 0
    for file_path in html_files:
        if process_file(file_path):
            updated_count += 1
            print(f"Обновлен: {os.path.relpath(file_path, WORKSPACE)}")
    
    print(f"\nВсего обновлено файлов: {updated_count}")

if __name__ == "__main__":
    main()
