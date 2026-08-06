#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# Новый HTML код меню без пункта "Главная"
NEW_MENU = '''        <nav class="nav" id="nav" role="navigation" aria-label="Основная навигация">
      <a href="https://дом-помощи.рф/chto-takoe-rabochij-dom.html" class="">О проекте</a>
      <div class="nav-dropdown">
        <a href="#" class="dropdown-toggle">Кому помогаем ▾</a>
        <div class="dropdown-menu">
          <a href="https://дом-помощи.рф/dlya-bezdomnyh.html">Бездомным</a>
          <a href="https://дом-помощи.рф/dlya-bez-dokumentov.html">Без документов</a>
          <a href="https://дом-помощи.рф/dlya-bezhencev.html">Беженцам</a>
          <a href="https://дом-помощи.рф/dlya-osvobodivshihsya.html">Освободившимся</a>
          <a href="https://дом-помощи.рф/dlya-zavisimyh.html">Зависимым в ремиссии</a>
          <a href="https://дом-помощи.рф/dlya-obmanutyh-na-vahte.html">Обманутым на ваhte</a>
          <a href="https://дом-помощи.рф/dlya-zhenshchin.html">Женщинам</a>
          <a href="https://дом-помощи.рф/dlya-semejnyh-par.html">Семейным парам</a>
        </div>
      </div>
      <a href="https://дом-помощи.рф/vakansii.html" class="">Вакансии</a>
      <div class="nav-dropdown">
        <a href="#" class="dropdown-toggle">Адреса ▾</a>
        <div class="dropdown-menu">
          <a href="https://дом-помощи.рф/adresa/rabochij-dom-balashiha.html">Балашиха</a>
          <a href="https://дом-помощи.рф/adresa/rabochij-dom-himki.html">Химки</a>
          <a href="https://дом-помощи.рф/adresa/rabochij-dom-podolsk.html">Подольск</a>
          <a href="https://дом-помощи.рф/adresa/rabochij-dom-mytyshchi.html">Мытищи</a>
          <a href="https://дом-помощи.рф/adresa/rabochij-dom-lyubertsy.html">Люберцы</a>
          <a href="https://дом-помощи.рф/adresa.html">Все адреса (157 городов)</a>
        </div>
      </div>
      <a href="https://дом-помощи.рф/otzyvy.html" class="">Отзывы</a>
      <a href="https://дом-помощи.рф/blog.html" class="">Блог</a>
      <a href="https://дом-помощи.рф/kontakty.html" class="">Контакты</a>
      <button class="btn btn-primary" onclick="openModal()" aria-label="Заказать обратный звонок">Заказать звонок</button>
    </nav>'''

def get_active_page(filepath):
    """Определяет, какая страница должна быть активной"""
    filename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)
    
    # Определяем активную страницу
    if filename == 'index.html':
        return 'chto-takoe-rabochij-dom.html'  # Для главной делаем активной "О проекте"
    elif 'adresa/' in filepath:
        return 'adresa.html'
    elif 'vakansii/' in filepath:
        return 'vakansii.html'
    elif 'blog/' in filepath:
        return 'blog.html'
    elif 'vosstanovlenie-dokumentov/' in filepath:
        return 'vosstanovlenie-dokumentov.html'
    else:
        return filename

def update_menu_in_file(filepath):
    """Обновляет меню в файле"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим nav блок и заменяем его
        nav_pattern = r'<nav class="nav" id="nav"[^>]*>.*?</nav>'
        
        active_page = get_active_page(filepath)
        
        # Создаем меню с правильным активным классом
        menu_lines = []
        menu_lines.append('        <nav class="nav" id="nav" role="navigation" aria-label="Основная навигация">')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/chto-takoe-rabochij-dom.html" class="{"active" if active_page == "chto-takoe-rabochij-dom.html" else ""}">О проекте</a>')
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
        menu_lines.append(f'      <a href="https://дом-помощи.рф/vakansii.html" class="{"active" if active_page == "vakansii.html" else ""}">Вакансии</a>')
        menu_lines.append('      <div class="nav-dropdown">')
        menu_lines.append('        <a href="#" class="dropdown-toggle">Адреса ▾</a>')
        menu_lines.append('        <div class="dropdown-menu">')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-balashiha.html">Балашиха</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-himki.html">Химки</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-podolsk.html">Подольск</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-mytyshchi.html">Мытищи</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa/rabochij-dom-lyubertsy.html">Люберцы</a>')
        menu_lines.append('          <a href="https://дом-помощи.рф/adresa.html" class="{"active" if active_page == "adresa.html" else ""}">Все адреса (157 городов)</a>')
        menu_lines.append('        </div>')
        menu_lines.append('      </div>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/otzyvy.html" class="{"active" if active_page == "otzyvy.html" else ""}">Отзывы</a>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/blog.html" class="{"active" if active_page == "blog.html" else ""}">Блог</a>')
        menu_lines.append(f'      <a href="https://дом-помощи.рф/kontakty.html" class="{"active" if active_page == "kontakty.html" else ""}">Контакты</a>')
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
        print(f"Обновлено: {filepath}")

print(f"\nОбновлено меню в {updated} файлах")
