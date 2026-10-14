"""254-savol: ravoq, yo‘lak va tayanchlardan tuzilgan mos ko‘prik namunasi."""
import base64
import json
from pathlib import Path

from PIL import Image

from generate_robot242 import ASSETS, ROOT, create_piece

PIECES = {
    'koprik254-yolak': (230, 80, 'rectangle', '#267591'),
    'koprik254-tayanch': (160, 180, 'rectangle', '#586b7e'),
}


def create_arch():
    name = 'koprik254-ravoq'
    width, height = 690, 230
    file = ASSETS / (name + '.webp')
    with Image.open(file) as image:
        bounds = image.convert('RGBA').getchannel('A').point(lambda value: 255 if value >= 128 else 0).getbbox()
        if not bounds:
            raise ValueError('Ravoq rasmi ko‘rinmayapti')
        left, top, right, bottom = bounds
        iw, ih = image.size
    sx = width / (right - left)
    sy = height / (bottom - top)
    encoded = base64.b64encode(file.read_bytes()).decode('ascii')
    body = (
        f'<image x="{-left * sx}" y="{-top * sy}" width="{iw * sx}" height="{ih * sy}"'
        f' href="data:image/webp;base64,{encoded}" preserveAspectRatio="none"/>'
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        f' viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">{body}</svg>'
    )
    (ASSETS / (name + '.svg')).write_text(svg, encoding='utf8')
    return body, width, height


def main():
    layers = {name: create_piece(name, *values) for name, values in PIECES.items()}
    layers['koprik254-ravoq'] = create_arch()
    spec = json.loads((ROOT / 'home/migrations/0029_koprik_loyihasini_yangilash.json').read_text(encoding='utf8'))
    content = '<rect x="1" y="1" width="98" height="68" rx="4" fill="#f4f9ff"/>'
    for index, entry in enumerate(spec['variants_after']):
        x, y, width, height = map(float, entry['slot'].split(','))
        name = Path(entry['rasm']).stem
        body, pw, ph = layers[name]
        body = body.replace(name + '-clip', name + '-clip-' + str(index))
        content += (
            f'<svg x="{x}" y="{y * .7}" width="{width}" height="{height * .7}" viewBox="0 0 {pw} {ph}"'
            f' preserveAspectRatio="none">{body}</svg>'
        )
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="70" viewBox="0 0 100 70" role="img">' + content + '</svg>'
    (ASSETS / 'namuna-koprik254.svg').write_text(svg, encoding='utf8')
    print('254-savol: 3 xil bo‘lak tasviri va 6 bo‘lakdan yig‘ilgan ko‘prik namunasi tayyor.')


if __name__ == '__main__':
    main()
