"""252-savol: olti shakldan tuzilgan raketa va uch mos tarkib kartochkasi.

Imagegen rasterlari saqlanadi. SVG aniq shakl chegarasi, o‘lcham va sonlarni
belgilaydi. Takroriy bo‘laklar bitta symbol tasviridan olinadi.
"""
import base64
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent / 'variantlar'
PIECES = {
    'raketa252-uch': (140, 120, 'triangle', '#a77a2e'),
    'raketa252-korpus': (140, 165, 'rectangle', '#267591'),
    'raketa252-qanot': (95, 130, 'triangle', '#b55348'),
    'raketa252-doira': (70, 70, 'circle', '#735096'),
}
ROCKET = [
    ('raketa252-uch', 290, 100, 140, 120, False),
    ('raketa252-korpus', 290, 220, 140, 165, False),
    ('raketa252-korpus', 290, 385, 140, 165, False),
    ('raketa252-qanot', 195, 420, 95, 130, False),
    ('raketa252-qanot', 430, 420, 95, 130, True),
    ('raketa252-doira', 325, 270, 70, 70, False),
]
INVENTORIES = {
    1: ['raketa252-uch', 'raketa252-qanot', 'raketa252-korpus', 'raketa252-korpus', 'raketa252-korpus', 'raketa252-doira'],
    2: ['raketa252-uch', 'raketa252-qanot', 'raketa252-qanot', 'raketa252-korpus', 'raketa252-korpus', 'raketa252-doira'],
    3: ['raketa252-uch', 'raketa252-qanot', 'raketa252-qanot', 'raketa252-korpus', 'raketa252-doira', 'raketa252-doira'],
}


def create_piece(name, width, height, kind, stroke):
    file = ASSETS / (name + '.webp')
    with Image.open(file) as image:
        alpha = image.convert('RGBA').getchannel('A')
        bounds = alpha.point(lambda value: 255 if value >= 128 else 0).getbbox()
        if not bounds:
            raise ValueError(f'{name}: bo‘lak ko‘rinmayapti')
        left, top, right, bottom = bounds
        iw, ih = image.size
    if name == 'raketa252-qanot':
        shape = f'<polygon points="{width},0 {width},{height} 0,{height}"/>'
    elif kind == 'triangle':
        shape = f'<polygon points="{width / 2},0 {width},{height} 0,{height}"/>'
    elif kind == 'circle':
        shape = f'<circle cx="{width / 2}" cy="{height / 2}" r="{width / 2}"/>'
    else:
        shape = f'<rect width="{width}" height="{height}" rx="2"/>'
    encoded = base64.b64encode(file.read_bytes()).decode('ascii')
    clip_id = name + '-clip'
    sx = width / (right - left)
    sy = height / (bottom - top)
    body = (
        f'<defs><clipPath id="{clip_id}">{shape}</clipPath></defs>'
        f'<image x="{-left * sx}" y="{-top * sy}" width="{iw * sx}" height="{ih * sy}"'
        f' href="data:image/webp;base64,{encoded}" preserveAspectRatio="none" clip-path="url(#{clip_id})"/>'
        + shape.replace('/>', f' fill="none" stroke="{stroke}" stroke-width="1" stroke-linejoin="round"/>')
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">{body}</svg>'
    )
    (ASSETS / (name + '.svg')).write_text(svg, encoding='utf8')
    return body, width, height


def place(name, x, y, width, height, mirror=False):
    shape = PIECES[name][2]
    transform = f'translate({x + width},{y}) scale(-1,1)' if mirror else f'translate({x},{y})'
    return (
        f'<g data-shape="{shape}" data-piece="{name}" transform="{transform}">'
        f'<use href="#{name}-symbol" width="{width}" height="{height}"/></g>'
    )


def save_diagram(name, width, height, layers, content):
    definitions = ''.join(
        f'<symbol id="{piece}-symbol" viewBox="0 0 {pw} {ph}" preserveAspectRatio="none">{body}</symbol>'
        for piece, (body, pw, ph) in layers.items()
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" role="img"><defs>{definitions}</defs>{content}</svg>'
    )
    (ASSETS / (name + '.svg')).write_text(svg, encoding='utf8')


def main():
    layers = {name: create_piece(name, *values) for name, values in PIECES.items()}
    content = '<rect x="110" y="40" width="500" height="570" rx="36" fill="#f4f9ff"/>'
    content += ''.join(place(*entry) for entry in ROCKET)
    save_diagram('raketa252', 720, 650, layers, content)
    for number, names in INVENTORIES.items():
        content = ''
        for index, name in enumerate(names):
            _, pw, ph = layers[name]
            scale = min(58 / pw, 72 / ph)
            width = pw * scale
            height = ph * scale
            x = 8 + (index % 3) * 72 + (64 - width) / 2
            y = 13 + (index // 3) * 92 + (76 - height) / 2
            mirror = name == 'raketa252-qanot' and index == 2
            content += place(name, x, y, width, height, mirror)
        save_diagram(f'raketa252-toplam-{number}', 224, 198, layers, content)
    print('252-savol: raketa namunasi va 3 ta olti shaklli javob kartochkasi yaratildi.')


if __name__ == '__main__':
    main()
