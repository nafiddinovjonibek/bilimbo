"""247-savol: organik kapalak bo‘laklari va ularning aniq oyna aksi.

Imagegen rasterlari o‘zgartirilmaydi. SVG tasvirni joylashtiradi, tanani markazdan
ikkiga ajratadi va o‘ng bo‘laklarni gorizontal aks ettiradi.
"""
import base64
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
ASSETS = Path(__file__).resolve().parent / 'variantlar'
PIECES = {
    'yuqori': ('kapalak247-yuqori-qanot', 360, 290, False),
    'quyi': ('kapalak247-quyi-qanot', 270, 220, False),
    'tana': ('kapalak247-tana', 100, 540, True),
}


def create_pair(kind, source, width, height, half_body):
    file = ASSETS / (source + '.webp')
    with Image.open(file) as image:
        bounds = image.convert('RGBA').getchannel('A').point(lambda value: 255 if value >= 128 else 0).getbbox()
        if not bounds:
            raise ValueError(f'{source}: rasm ko‘rinmayapti')
        left, top, right, bottom = bounds
        iw, ih = image.size
    target_width = width * 2 if half_body else width
    sx = target_width / (right - left)
    sy = height / (bottom - top)
    data = base64.b64encode(file.read_bytes()).decode('ascii')
    original = (
        f'<image x="{-left * sx}" y="{-top * sy}" width="{iw * sx}" height="{ih * sy}"'
        f' href="data:image/webp;base64,{data}" preserveAspectRatio="none"/>'
    )
    layers = {}
    for side in ('chap', 'ong'):
        name = f'kapalak247-{side}-{kind}'
        clip_id = name + '-clip'
        body = (
            f'<defs><clipPath id="{clip_id}"><rect width="{width}" height="{height}"/></clipPath></defs>'
            f'<g clip-path="url(#{clip_id})">'
            + (f'<g transform="translate({width},0) scale(-1,1)">{original}</g>' if side == 'ong' else original)
            + '</g>'
        )
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
            f' viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">{body}</svg>'
        )
        (ASSETS / (name + '.svg')).write_text(svg, encoding='utf8')
        layers[name] = (body, width, height)
    return layers


def main():
    layers = {}
    for kind, values in PIECES.items():
        layers.update(create_pair(kind, *values))
    spec = json.loads((ROOT / 'home/migrations/0027_kapalak_simmetriyasini_yangilash.json').read_text(encoding='utf8'))
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
    (ASSETS / 'namuna-kapalak247.svg').write_text(svg, encoding='utf8')
    print('247-savol: kapalakning 6 organik bo‘lagi va ulardan tuzilgan simmetrik namuna tayyor.')


if __name__ == '__main__':
    main()
