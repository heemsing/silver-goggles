#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def get_active_page_class(filepath, target):
    """Определяет, должен ли быть активный класс"""
    filename = os.path.basename(filepath)
    
    # Определяем активную страницу
    if filename == 'index.html':
        active = 'chto-takoe-rabochij-dom.html'
    elif 'adresa/' in filepath:
        active = 'adresa.html'
    elif 'vakansii/' in filepath:
        active = 'vakansii.html'
    elif 'blog/' in filepath:
        active = 'blog.html'
    elif 'vosstanovlenie-dokumentov/' in filepath:
        active = 'vosstanovlenie-dokumentov.html'
    else:
        active = filename
    
    return 'active' if active == target else ''

def update_menu_in_file(filepath):
    """Обновляет меню в файле"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим nav блок и заменяем его
        nav_pattern = r'<nav class="nav" id="nav"[^>]*>.*?</nav>'
        
        active_o_proekte = get_active_page_class(filepath, 'chto-takoe-rabochij-dom.html')
        active_vakansii = get_active_page_class(filepath, 'vakansii.html')
        active_adresa = get_active_page_class(filepath, 'adresa.html')
        active_otzyvy = get_active_page_class(filepath, 'otzyvy.html')
        active_blog = get_active_page_class(filepath, 'blog.html')
        active_kontakty = get_active_page_class(filepath, 'kontakty.html')
        
        menu_lines = []
        menu_lines.append('        <nav class="nav" id="nav" role="navigation" aria-label="Основная навигация">')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/chto-takoe-rabochij-dom.html" class="{active_o_proekte}">О проекте</a>')
        menu_lines.append('      <div class="nav-dropdown">')
        menu_lines.append('        <a href="#" class="dropdown-toggle">Кому помогаем ▾</a>')
        menu_lines.append('        <div class="dropdown-menu">')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-bezdomnyh.html">Бездомным</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-bez-dokumentov.html">Без документов</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-bezhencev.html">Беженцам</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-osvobodivshihsya.html">Освободившимся</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-zavisimyh.html">Зависимым в ремиссии</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-obmanutyh-na-vahte.html">Обманутым на вахте</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-zhenshchin.html">Женщинам</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/dlya-semejnyh-par.html">Семейным парам</a>')
        menu_lines.append('        </div>')
        menu_lines.append('      </div>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/vakansii.html" class="{active_vakansii}">Вакансии</a>')
        menu_lines.append('      <div class="nav-dropdown">')
        menu_lines.append('        <a href="#" class="dropdown-toggle">Адреса ▾</a>')
        menu_lines.append('        <div class="dropdown-menu">')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-balashiha.html">Балашиха</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-himki.html">Химки</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-podolsk.html">Подольск</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-mytyshchi.html">Мытищи</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-lyubertsy.html">Люберцы</a>')
        menu_lines.append(f'          <a href="https://дом-помощи.рф/adresa.html" class="{active_adresa}">Все адреса (157 городов)</a>')
        menu_lines.append('        </div>')
        menu_lines.append('      </div>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/otzyvy.html" class="{active_otzyvy}">Отзывы</a>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/blog.html" class="{active_blog}">Блог</a>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/kontakty.html" class="{active_kontakty}">Контакты</a>')
        menu_lines.append('      <button class="btn btn-primary" onclick="openModal()" aria-label="Заказать обратный звонок">Заказать звонок</button>')
        menu_lines.append('    </nav>')
        
        new_nav = '\n'.join(menu_lines)
        
        # Заменяем nav блок
        new_content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
        
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

# Обновляем меню во всех файлах
updated = 0
for filepath in html_files:
    if update_menu_in_file(filepath):
        updated += 1

print(f"\nОбновлено меню в {updated} файлах")
