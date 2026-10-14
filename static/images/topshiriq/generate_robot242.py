"""242-savolning AI bo‘laklarini aniq geometriya va namuna bilan moslash.

Raster tasvirlar tahrirlanmaydi. SVG ularni kerakli geometrik chegaralarda
joylashtiradi; namuna ham shu bo‘laklardan va mavjud uyalar ta'rifidan yig‘iladi.
"""
import base64
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
ASSETS = Path(__file__).resolve().parent / 'variantlar'
PIECES = {
    'robot242-bosh': (260, 260, 'circle', '#aa721d'),
    'robot242-tana': (400, 300, 'rectangle', '#315b94'),
    'robot242-qol': (150, 150, 'rectangle', '#447637'),
    'robot242-oyoq': (170, 200, 'triangle', '#b66722'),
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
    if kind == 'circle':
        shape = f'<circle cx="{width / 2}" cy="{height / 2}" r="{width / 2}"/>'
    elif kind == 'triangle':
        shape = f'<polygon points="{width / 2},0 {width},{height} 0,{height}"/>'
    else:
        shape = f'<rect x="0" y="0" width="{width}" height="{height}" rx="{min(width, height) * .015}"/>'
    encoded = base64.b64encode(file.read_bytes()).decode('ascii')
    clip_id = name + '-clip'
    sx = width / (right - left)
    sy = height / (bottom - top)
    body = (
        f'<defs><clipPath id="{clip_id}">{shape}</clipPath></defs>'
        f'<image x="{-left * sx}" y="{-top * sy}" width="{iw * sx}" height="{ih * sy}"'
        f' href="data:image/webp;base64,{encoded}" preserveAspectRatio="none" clip-path="url(#{clip_id})"/>'
        + shape.replace('/>', f' fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">{body}</svg>'
    )
    (ASSETS / (name + '.svg')).write_text(svg, encoding='utf8')
    return body, width, height


def main():
    layers = {name: create_piece(name, *values) for name, values in PIECES.items()}
    spec = json.loads((ROOT / 'home/migrations/0025_robot_topshirigini_yangilash.json').read_text(encoding='utf8'))
    content = '<rect x="1" y="1" width="98" height="68" rx="4" fill="#f4f9ff"/>'
    for index, entry in enumerate(spec['variants_after']):
        x, y, width, height = map(float, entry['slot'].split(','))
        y *= .7
        height *= .7
        name = Path(entry['rasm']).stem
        body, pw, ph = layers[name]
        body = body.replace(name + '-clip', name + '-clip-' + str(index))
        content += (
            f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 {pw} {ph}"'
            f' preserveAspectRatio="none">{body}</svg>'
        )
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="70" viewBox="0 0 100 70" role="img">' + content + '</svg>'
    (ASSETS / 'namuna-robot242.svg').write_text(svg, encoding='utf8')
    print('242-savol: 4 xil bo‘lak tasviri va 6 bo‘lakdan yig‘ilgan namuna tayyor.')


if __name__ == '__main__':
    main()
