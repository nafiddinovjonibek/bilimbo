"""Yog‘och uycha namunasi va bo‘laklarini mavjud uyalar bilan aynan moslash.

Illyustratsiyalar imagegen bilan alohida yaratilgan. SVG qatlamlari shaffof
rasmlarni aniq shakl va o‘lchamga joylashtiradi; namuna ham shu qatlamlardan
yig‘iladi. Boshqa topshiriq rasmlariga tegilmaydi.
"""
import base64
import json
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
ASSETS=Path(__file__).resolve().parent/'variantlar'
PIECES={
    'uy237-tom':(560,300,'triangle','#9d342c'),
    'uy237-devor':(260,260,'square','#28518b'),
    'uy237-eshik':(130,210,'square','#78502f'),
}


def create_piece(name,width,height,kind,stroke):
    file=ASSETS/(name+'.webp')
    with Image.open(file) as image:
        # Faqat alfa chegaralarini o‘qiymiz; raster pikselini tahrirlamaymiz.
        alpha=image.convert('RGBA').getchannel('A')
        bounds=alpha.point(lambda value:255 if value>=128 else 0).getbbox()
        if not bounds:
            raise ValueError(f'{name}: bo‘lak ko‘rinmayapti')
        left,top,right,bottom=bounds
        iw,ih=image.size
    if kind=='triangle':
        shape=f'<polygon points="{width/2},0 {width},{height} 0,{height}"/>'
    else:
        shape=f'<rect x="0" y="0" width="{width}" height="{height}" rx="{min(width,height)*.015}"/>'
    data=base64.b64encode(file.read_bytes()).decode('ascii')
    clip_id=name+'-clip'
    sx=width/(right-left);sy=height/(bottom-top)
    body=(f'<defs><clipPath id="{clip_id}">{shape}</clipPath></defs>'
          f'<image x="{-left*sx}" y="{-top*sy}" width="{iw*sx}" height="{ih*sy}"'
          f' href="data:image/webp;base64,{data}" preserveAspectRatio="none" clip-path="url(#{clip_id})"/>'
          +shape.replace('/>',f' fill="none" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'))
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
         f' viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">{body}</svg>')
    (ASSETS/(name+'.svg')).write_text(svg,encoding='utf8')
    return body,width,height


def main():
    layers={name:create_piece(name,*values) for name,values in PIECES.items()}
    spec=json.loads((ROOT/'home/migrations/0024_yogoch_uycha_topshirigi.json').read_text(encoding='utf8'))
    content='<rect x="1" y="1" width="98" height="68" rx="4" fill="#f4f9ff"/>'
    for index,entry in enumerate(spec['variants_after']):
        x,y,w,h=map(float,entry['slot'].split(','))
        y*=.7;h*=.7
        name=Path(entry['rasm']).stem
        body,pw,ph=layers[name]
        # Ikkala devorning clipPath identifikatorlari ham alohida bo‘lsin.
        body=body.replace(name+'-clip',name+'-clip-'+str(index))
        content+=(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {pw} {ph}"'
                  f' preserveAspectRatio="none">{body}</svg>')
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="70" viewBox="0 0 100 70" role="img">'+content+'</svg>'
    (ASSETS/'namuna-uy237.svg').write_text(svg,encoding='utf8')
    print('237-savol uchun 3 bo‘lak rasmi va to‘rtta bo‘lakdan tuzilgan namuna yaratildi.')


if __name__=='__main__':
    main()
