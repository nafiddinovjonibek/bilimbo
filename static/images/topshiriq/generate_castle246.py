"""246-savolning qasr bo‘laklari va aynan ulardan tuzilgan namunasi."""
import json
from pathlib import Path

# Bu yordamchi faqat berilgan rasmni joylashtiradi; robot rasmlari o‘zgarmaydi.
from generate_robot242 import ASSETS, ROOT, create_piece

PIECES = {
    'qasr246-tom': (220, 200, 'triangle', '#9d342c'),
    'qasr246-minora': (180, 400, 'rectangle', '#586b7e'),
    'qasr246-devor': (480, 260, 'rectangle', '#586b7e'),
    'qasr246-darvoza': (140, 160, 'rectangle', '#78502f'),
}


def main():
    layers = {name: create_piece(name, *values) for name, values in PIECES.items()}
    spec = json.loads((ROOT / 'home/migrations/0026_qasr_topshirigini_yangilash.json').read_text(encoding='utf8'))
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
    (ASSETS / 'namuna-qasr246.svg').write_text(svg, encoding='utf8')
    print('246-savol: 4 xil bo‘lak tasviri va 6 bo‘lakdan yig‘ilgan qasr namunasi tayyor.')


if __name__ == '__main__':
    main()
