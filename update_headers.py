#!/usr/bin/env python3
"""
SEO-оптимизированное обновление header на всех страницах проекта.
Структура меню основана на реальной архитектуре сайта.
"""

import os
import re
from pathlib import Path

def get_page_type(filepath):
    """Определяет тип страницы для установки активного класса"""
    # filepath может быть строкой или Path объектом
    if isinstance(filepath, str):
        fp = Path(filepath)
    else:
        fp = filepath
    
    filepath_str = str(fp)
    basename = fp.stem
    
    # Главная страница
    if basename == 'index':
        return 'home'
    
    # Страницы в корне
    if basename == 'chto-takoe-rabochij-dom':
        return 'about'
    if basename == 'vakansii':
        return 'jobs'
    if basename == 'otzyvy':
        return 'reviews'
    if basename == 'blog':
        return 'blog'
    if basename == 'kontakty':
        return 'contacts'
    if basename == 'vosstanovlenie-dokumentov':
        return 'documents'
    
    # Целевые страницы помощи
    if basename.startswith('dlya-'):
        return 'help'
    
    # Страницы городов
    if 'adresa/' in filepath_str or fp.parent.name == 'adresa':
        return 'address'
    
    return 'other'

def generate_nav_html(page_type):
    """Генерирует HTML навигации с активным классом для текущей страницы"""
    
    home_active = ' active' if page_type == 'home' else ''
    about_active = ' active' if page_type == 'about' else ''
    help_active = ' active' if page_type == 'help' else ''
    jobs_active = ' active' if page_type == 'jobs' else ''
    address_active = ' active' if page_type == 'address' else ''
    reviews_active = ' active' if page_type == 'reviews' else ''
    blog_active = ' active' if page_type == 'blog' else ''
    contacts_active = ' active' if page_type == 'contacts' else ''
    
    nav_html = f'''    <nav class="nav" id="nav" role="navigation" aria-label="Основная навигация">
      <a href="./" class="{home_active}">Главная</a>
      <a href="./chto-takoe-rabochij-dom" class="{about_active}">О проекте</a>
      <div class="nav-dropdown">
        <a href="#" class="dropdown-toggle{help_active}">Кому помогаем ▾</a>
        <div class="dropdown-menu">
          <a href="./dlya-bezdomnyh">Бездомным</a>
          <a href="./dlya-bez-dokumentov">Без документов</a>
          <a href="./dlya-bezhencev">Беженцам</a>
          <a href="./dlya-osvobodivshihsya">Освободившимся</a>
          <a href="./dlya-zavisimyh">Зависимым в ремиссии</a>
          <a href="./dlya-obmanutyh-na-vahte">Обманутым на вахте</a>
          <a href="./dlya-zhenshchin">Женщинам</a>
          <a href="./dlya-semejnyh-par">Семейным парам</a>
        </div>
      </div>
      <a href="./vakansii" class="{jobs_active}">Вакансии</a>
      <div class="nav-dropdown">
        <a href="#" class="dropdown-toggle{address_active}">Адреса ▾</a>
        <div class="dropdown-menu">
          <a href="./adresa/rabochij-dom-balashiha">Балашиха</a>
          <a href="./adresa/rabochij-dom-khimki">Химки</a>
          <a href="./adresa/rabochij-dom-podolsk">Подольск</a>
          <a href="./adresa/rabochij-dom-mytiwchi">Мытищи</a>
          <a href="./adresa/rabochij-dom-lyubercy">Люберцы</a>
          <a href="./adresa">Все адреса (157 городов)</a>
        </div>
      </div>
      <a href="./otzyvy" class="{reviews_active}">Отзывы</a>
      <a href="./blog" class="{blog_active}">Блог</a>
      <a href="./kontakty" class="{contacts_active}">Контакты</a>
      <button class="btn btn-primary" onclick="openModal()" aria-label="Заказать обратный звонок">Заказать звонок</button>
    </nav>'''
    
    return nav_html

def update_header_in_file(filepath):
    """Обновляет header в файле"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        page_type = get_page_type(filepath)
        new_nav = generate_nav_html(page_type)
        nav_pattern = r'<nav\s+class="nav"[^>]*>.*?</nav>'
        
        if re.search(nav_pattern, content, re.DOTALL):
            new_content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, 'updated'
        else:
            return False, 'no_nav_found'
            
    except Exception as e:
        return False, f'error: {str(e)}'

def add_dropdown_css(filepath):
    """Добавляет CSS для dropdown меню если его нет"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '.nav-dropdown' in content or '.dropdown-menu' in content:
            return False, 'already_has_css'
        
        style_pattern = r'(</style>\s*</head>)'
        
        dropdown_css = '''
    /* Dropdown Navigation */
    .nav-dropdown { position: relative; display: inline-block; }
    .dropdown-toggle { cursor: pointer; padding: 0.5rem 0; }
    .dropdown-menu {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      background: #fff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      border-radius: 8px;
      min-width: 220px;
      z-index: 1000;
      padding: 0.5rem 0;
    }
    .nav-dropdown:hover .dropdown-menu { display: block; }
    .dropdown-menu a {
      display: block;
      padding: 0.6rem 1.2rem;
      color: #333;
      text-decoration: none;
      transition: background 0.2s;
    }
    .dropdown-menu a:hover { background: #f5f5f5; }
    @media (max-width: 768px) {
      .nav-dropdown { display: block; }
      .dropdown-menu {
        position: static;
        box-shadow: none;
        background: #f9f9f9;
        display: none;
      }
      .nav-dropdown.active .dropdown-menu { display: block; }
    }
'''
        
        if re.search(style_pattern, content):
            new_content = re.sub(style_pattern, dropdown_css + r'\1', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, 'css_added'
        
        return False, 'no_style_tag'
        
    except Exception as e:
        return False, f'error: {str(e)}'

def main():
    workspace = Path('/workspace')
    html_files = list(workspace.rglob('*.html'))
    html_files = [f for f in html_files if not f.name.startswith('google')]
    
    updated = 0
    skipped = 0
    
    print(f"Найдено HTML файлов: {len(html_files)}")
    print("Обновление header на всех страницах...\n")
    
    for filepath in html_files:
        success, status = update_header_in_file(filepath)
        
        if success:
            updated += 1
            print(f"✓ {filepath.relative_to(workspace)} - {status}")
        else:
            skipped += 1
            print(f"○ {filepath.relative_to(workspace)} - {status}")
    
    print(f"\n{'='*60}")
    print(f"Готово! Обновлено: {updated}, Пропущено: {skipped}")
    
    print("\nДобавление CSS для dropdown меню...")
    main_files = [
        workspace / 'index.html',
        workspace / 'vakansii.html',
        workspace / 'otzyvy.html',
        workspace / 'kontakty.html',
    ]
    
    css_added = 0
    for filepath in main_files:
        if filepath.exists():
            success, status = add_dropdown_css(filepath)
            if success:
                css_added += 1
                print(f"✓ CSS добавлен в {filepath.name}")
    
    print(f"\nCSS добавлен в {css_added} файлов")

if __name__ == '__main__':
    main()
