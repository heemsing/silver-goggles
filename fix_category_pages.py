#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def get_active_for_category(filepath):
    """Определяет активный пункт для страниц категорий"""
    filename = os.path.basename(filepath)
    
    # Страницы раздела "Кому помогаем"
    category_pages = [
        'dlya-bezdomnyh.html',
        'dlya-bez-dokumentov.html',
        'dlya-bezhencev.html',
        'dlya-osvobodivshihsya.html',
        'dlya-zavisimyh.html',
        'dlya-obmanutyh-na-vahte.html',
        'dlya-zhenshchin.html',
        'dlya-semejnyh-par.html'
    ]
    
    if filename in category_pages:
        return 'kamu-pomogaem'
    
    # Страницы восстановления документов
    if 'vosstanovlenie-dokumentov' in filepath or filename == 'vosstanovlenie-dokumentov.html':
        return 'vosstanovlenie'
    
    return None

def update_category_menu(filepath):
    """Обновляет меню для страниц категорий"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        category = get_active_for_category(filepath)
        if not category:
            return False
        
        # Находим nav блок
        nav_pattern = r'<nav class="nav" id="nav"[^>]*>.*?</nav>'
        match = re.search(nav_pattern, content, flags=re.DOTALL)
        if not match:
            return False
        
        # Для страниц "Кому помогаем" - делаем активным соответствующий пункт
        if category == 'kamu-pomogaem':
            filename = os.path.basename(filepath)
            
            # Создаем меню с активным пунктом в dropdown
            menu_lines = []
            menu_lines.append('        <nav class="nav" id="nav" role="navigation" aria-label="Основная навигация">')
            menu_lines.append('      <a href="https://дом-помощи.рф/chto-takoe-rabochij-dom.html" class="">О проекте</a>')
            menu_lines.append('      <div class="nav-dropdown active">')
            menu_lines.append('        <a href="#" class="dropdown-toggle">Кому помогаем ▾</a>')
            menu_lines.append('        <div class="dropdown-menu">')
            
            pages_map = {
                'dlya-bezdomnyh.html': 'Бездомным',
                'dlya-bez-dokumentov.html': 'Без документов',
                'dlya-bezhencev.html': 'Беженцам',
                'dlya-osvobodivshihsya.html': 'Освободившимся',
                'dlya-zavisimyh.html': 'Зависимым в ремиссии',
                'dlya-obmanutyh-na-vahte.html': 'Обманутым на вахте',
                'dlya-zhenshchin.html': 'Женщинам',
                'dlya-semejnyh-par.html': 'Семейным парам'
            }
            
            for page, label in pages_map.items():
                active_class = ' class="active"' if page == filename else ''
                menu_lines.append(f'          <a href="https://дом-помощи.рф/{page}"{active_class}>{label}</a>')
            
            menu_lines.append('        </div>')
            menu_lines.append('      </div>')
            menu_lines.append('      <a href="https://дом-помощи.рф/vakansii.html" class="">Вакансии</a>')
            menu_lines.append('      <div class="nav-dropdown">')
            menu_lines.append('        <a href="#" class="dropdown-toggle">Адреса ▾</a>')
            menu_lines.append('        <div class="dropdown-menu">')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-balashiha.html">Балашиха</a>')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-himki.html">Химки</a>')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-podolsk.html">Подольск</a>')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-mytyshchi.html">Мытищи</a>')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-lyubertsy.html">Люберцы</a>')
            menu_lines.append('          <a href="https://дом-помощи.рф/adresa.html">Все адреса (157 городов)</a>')
            menu_lines.append('        </div>')
            menu_lines.append('      </div>')
            menu_lines.append('      <a href="https://дом-помощи.рф/otzyvy.html" class="">Отзывы</a>')
            menu_lines.append('      <a href="https://дом-помощи.рф/blog.html" class="">Блог</a>')
            menu_lines.append('      <a href="https://дом-помощи.рф/kontakty.html" class="">Контакты</a>')
            menu_lines.append('      <button class="btn btn-primary" onclick="openModal()" aria-label="Заказать обратный звонок">Заказать звонок</button>')
            menu_lines.append('    </nav>')
            
            new_nav = '\n'.join(menu_lines)
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

# Обновляем меню для страниц категорий
updated = 0
for filepath in html_files:
    if update_category_menu(filepath):
        updated += 1
        print(f"Обновлено: {filepath}")

print(f"\nОбновлено меню в {updated} файлах категорий")
