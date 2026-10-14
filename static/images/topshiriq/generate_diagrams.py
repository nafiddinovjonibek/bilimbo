"""Sanoq, shakl, naqsh va konstruktor rasmlarini aniq SVG sifatida yaratish.

Ishga tushirish: env\\Scripts\\python.exe static/images/topshiriq/generate_diagrams.py
Rasmli sahnalar va buyumlar imagegen bilan alohida yaratiladi. Bu fayl faqat
aniq geometriya, joylashuv va sanoq talab qiladigan ta'lim tasvirlarini yaratadi.
"""
import base64
import json
import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
ASSETS = Path(__file__).resolve().parent / 'variantlar'
CONTENT = ROOT / 'home/migrations/0022_topshiriqlarni_takomillashtirish.json'
INK = '#24364d'
COLORS = {'qizil': '#e94b4b', 'kok': '#3d7be0', 'yashil': '#4caf50',
          'sariq': '#f2c230', 'tosariq': '#ff9f43', 'binafsha': '#a06cf0',
          'jigar': '#92683e', 'kulrang': '#91a2b4'}
CREATED = set()
BODIES = {}


def svg(name, body, width=400, height=400):
    text = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">'
            '<defs><linearGradient id="shine" x1="0" y1="0" x2="1" y2="1">'
            '<stop stop-color="#fff" stop-opacity=".26"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            '</linearGradient></defs>' + body + '</svg>')
    (ASSETS / f'{name}.svg').write_text(text, encoding='utf8')
    CREATED.add(name)
    BODIES[name] = (body, width, height)
    return text


def rect(x, y, w, h, color, radius=12, stroke=INK, sw=4, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def circle(x, y, r, color, sw=4, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="{INK}" stroke-width="{sw}" {extra}/>'


def line(x1, y1, x2, y2, color=INK, sw=4, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {extra}/>'


def poly(points, color, sw=4, extra=''):
    return f'<polygon points="{points}" fill="{color}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def label(x, y, text, size=24, color=INK):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}" font-weight="700" text-anchor="middle">{text}</text>'


def image(name, x, y, w, h, silhouette=False):
    path = ASSETS / f'{name}.webp'
    if not path.exists():
        path = ASSETS / f'{name}.png'
    if not path.exists():
        raise FileNotFoundError(path)
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    mime = 'image/webp' if path.suffix=='.webp' else 'image/png'
    im = f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:{mime};base64,{data}" preserveAspectRatio="xMidYMid meet"/>'
    if silhouette:
        return f'<mask id="silhouette" mask-type="alpha">{im}</mask><rect x="0" y="0" width="400" height="400" fill="{INK}" mask="url(#silhouette)"/>'
    return im


def cube(x, y, size, color):
    s = size
    return (poly(f'{x},{y+s*.25} {x+s*.5},{y} {x+s},{y+s*.25} {x+s*.5},{y+s*.5}', color, 2)
            + poly(f'{x},{y+s*.25} {x+s*.5},{y+s*.5} {x+s*.5},{y+s} {x},{y+s*.75}', color, 2)
            + poly(f'{x+s*.5},{y+s*.5} {x+s},{y+s*.25} {x+s},{y+s*.75} {x+s*.5},{y+s}', color, 2)
            + poly(f'{x},{y+s*.25} {x+s*.5},{y} {x+s},{y+s*.25} {x+s*.5},{y+s*.5}', '#fff', 0, 'opacity=".18"')
            + poly(f'{x+s*.5},{y+s*.5} {x+s},{y+s*.25} {x+s},{y+s*.75} {x+s*.5},{y+s}', '#000', 0, 'opacity=".12"'))


def shape(kind, color, x=70, y=70, w=260, h=260, sw=5):
    if kind == 'doira':
        return f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2-3}" ry="{h/2-3}" fill="{color}" stroke="{INK}" stroke-width="{sw}"/>'
    if kind == 'uchburchak':
        return poly(f'{x+w/2},{y+3} {x+w-3},{y+h-3} {x+3},{y+h-3}', color, sw)
    if kind == 'yulduz':
        points = []
        for i in range(10):
            a = math.pi * i / 5 - math.pi / 2
            r = min(w,h) * (.49 if i % 2 == 0 else .23)
            points.append(f'{x+w/2+math.cos(a)*r},{y+h/2+math.sin(a)*r}')
        return poly(' '.join(points), color, sw)
    return rect(x+3, y+3, w-6, h-6, color, min(w,h)*.06, sw=sw)


def simple_assets():
    for name, color in COLORS.items():
        svg('rang-' + name, rect(38,38,324,324,color,48) + rect(48,48,304,150,'url(#shine)',38,stroke='none',sw=0))
    for kind, color in [('kvadrat', COLORS['kok']), ('kvadrat-qizil', COLORS['qizil']),
                        ('uchburchak', COLORS['qizil']), ('doira', COLORS['sariq']),
                        ('yulduz', COLORS['sariq']), ('tortburchak', COLORS['yashil'])]:
        svg('shakl-'+kind, shape(kind.split('-')[0],color,70,100 if kind=='tortburchak' else 70,260,200 if kind=='tortburchak' else 260))
    for kind in ('doira','uchburchak','kvadrat'):
        svg('soya-'+kind,shape(kind,INK))
    for color_name in ('kok','qizil'):
        c = COLORS[color_name]
        svg('kub-'+color_name,cube(65,60,270,c))
        svg('quti-'+color_name,poly('58,104 335,104 310,344 80,344',c)+rect(45,86,300,42,c,15)+line(94,125,108,310,'#ffffff',7,'opacity=".2"'))
    for side in ('chapda','ongda'):
        body = cube(25,145,135,COLORS['kok']) + cube(240,145,135,COLORS['kok'])
        x = 90 if side=='chapda' else 305
        body += poly(f'{x-26},67 {x+26},67 {x+26},100 {x+41},100 {x},140 {x-41},100 {x-26},100', COLORS['sariq'],3)
        svg('kub-'+side,body)
    for name, count in [('past',3),('orta',5),('baland',7)]:
        body = line(30,355,370,355,'#bed5e2',5)
        for i in range(count):
            body += rect(135,355-(i+1)*43,130,41,COLORS['kok'],7,sw=3)
            body += line(145,355-i*43-30,250,355-i*43-30,'#fff',3,'opacity=".25"')
        svg('minora-'+name,body)
    for name, length in [('uzun',300),('orta',220),('qisqa',140)]:
        y = 350-length
        body = line(45,355,355,355,'#bed5e2',4) + rect(171,y+30,58,length-55,COLORS['sariq'],3,sw=3)
        body += poly(f'171,{y+30} 229,{y+30} 200,{y}', '#dbc2a0',3)
        body += poly(f'190,{y+10} 210,{y+10} 200,{y}', INK,1)
        body += rect(171,325,58,25,'#ee83a7',3,sw=3) + line(190,y+40,190,310,'#fff',4,'opacity=".4"')
        svg('qalam-'+name,body)
    arrow = '135,330 135,160 65,160 200,35 335,160 265,160 265,330'
    for name, angle in [('yuqori',0),('ong',90),('past',180),('chap',270)]:
        svg('strelka-'+name,f'<g transform="rotate({angle} 200 200)">'+poly(arrow,COLORS['kok'],5)+'</g>')
    for name, sign in [('katta','>'),('kichik','<')]:
        svg('belgi-'+name,rect(38,38,324,324,'#f4f8ff',40,stroke='#dce7f3')+label(200,280,sign.replace('<','&lt;').replace('>','&gt;'),210))
    svg('tanga',circle(200,200,138,COLORS['sariq'],7)+circle(200,200,108,'#ffe291',4)+shape('yulduz',COLORS['sariq'],135,135,130,130,2))
    body = rect(120,25,160,330,INK,30)+rect(184,345,32,55,'#697b8b',4)
    for cy,c in [(92,COLORS['qizil']),(190,'#705d32'),(287,'#365946')]:
        body += circle(200,cy,48,c,4)
    body += circle(186,78,11,'#ff9f9f',0)
    svg('svetofor-qizil',body)
    for mood in ('xursand','xafa','jahli','hayron'):
        body = circle(200,205,140,'#f5c8a5',5)
        body += '<path d="M70 154 Q60 40 190 52 Q310 35 332 153 Q274 95 223 103 Q156 145 91 106 Z" fill="#49382e"/>'
        body += circle(147,191,9,INK,0)+circle(253,191,9,INK,0)
        if mood=='xursand':
            body += '<path d="M143 242 Q200 294 257 242" fill="none" stroke="#713f3e" stroke-width="9" stroke-linecap="round"/>'
            body += line(125,160,157,153,sw=7)+line(241,153,275,160,sw=7)
        elif mood=='xafa':
            body += '<path d="M150 282 Q200 237 250 282" fill="none" stroke="#713f3e" stroke-width="8" stroke-linecap="round"/>'
            body += line(125,155,158,170,sw=7)+line(242,170,275,155,sw=7)
        elif mood=='jahli':
            body += line(125,155,165,177,sw=8)+line(235,177,275,155,sw=8)
            body += '<path d="M150 278 Q200 251 250 278" fill="none" stroke="#713f3e" stroke-width="8" stroke-linecap="round"/>'
        else:
            body += line(125,144,165,144,sw=7)+line(235,144,275,144,sw=7)+circle(200,268,23,'#713f3e',4)
        svg('his-'+mood,body)


def sequence_assets():
    def tiles(items, answer=False):
        cell = 95 if len(items)>4 else 110
        w = cell*len(items)+40
        b = ''
        for i,item in enumerate(items):
            x=20+i*cell
            b += rect(x,25,cell-8,100,'#f5f9ff',14,stroke='#d2dfee',sw=2)
            if item:
                kind,color=item
                b+=shape(kind,color,x+13,43,cell-34,63,3)
            else:
                b+=label(x+(cell-8)/2,99,'?',52)
        return b,w,150
    blue=('kvadrat',COLORS['kok']); red=('kvadrat',COLORS['qizil'])
    triangle=('uchburchak',COLORS['qizil']); green=('doira',COLORS['yashil'])
    for name,items in [
        ('naqsh-kvadrat-uchburchak',[blue,triangle,blue,triangle,None]),
        ('naqsh-kok-qizil',[blue,blue,red,blue,blue,red,None]),
        ('naqsh-murakkab',[triangle,blue,blue,triangle,blue,blue,None,None,None]),
        ('naqsh-qizil-yashil',[green,green,('doira',COLORS['qizil']),green,green,None]),
        ('javob-uch-kvadrat-kvadrat',[triangle,blue,blue]),
        ('javob-kvadrat-kvadrat-uch',[blue,blue,triangle]),
        ('javob-kvadrat-uch-kvadrat',[blue,triangle,blue]),
    ]:
        b,w,h=tiles(items)
        svg(name,b,w,h)
    for count in (6,8,10):
        positions={6:[(70+i%3*95,105+i//3*120) for i in range(6)],
                   8:[(25+i%4*95,110+i//4*125) for i in range(8)],
                   10:[(15+i%5*76,115+i//5*112) for i in range(10)]}[count]
        svg('sanoq-kub-'+str(count),''.join(cube(x,y,64,COLORS['kok']) for x,y in positions))
    # Har bir olma mustaqil ko‘rinadi, ustma-ust tushmaydi; jami aynan oltita.
    body=''
    for i,(x,y) in enumerate([(80,90),(230,80),(130,190),(280,190),(65,300),(225,305)]):
        body+=f'<path d="M{x} {y-27} C{x-53} {y-65} {x-60} {y+45} {x} {y+48} C{x+60} {y+45} {x+53} {y-65} {x} {y-27} Z" fill="{COLORS["qizil"]}" stroke="{INK}" stroke-width="3"/>'
        body+=line(x,y-22,x+5,y-49,'#795638',5)+f'<ellipse cx="{x+20}" cy="{y-43}" rx="17" ry="8" fill="{COLORS["yashil"]}" transform="rotate(-25 {x+20} {y-43})"/>'
    svg('sanoq-olma-6',body)
    for n in (3,4):
        path=[(0,1),(0,0),(1,0),(1,1)] if n==3 else [(0,1),(0,0),(1,0),(2,0),(2,1)]
        cols=3 if n==4 else 2; cell=100; ox=(400-cols*cell)/2; oy=100
        b=''
        for y in range(2):
            for x in range(cols):
                b+=rect(ox+x*cell,oy+y*cell,cell,cell,'#e7eff6',8,stroke='#c2d3df',sw=2)
        coords=[(ox+x*cell+50,oy+y*cell+50) for x,y in path]
        b+='<polyline points="'+' '.join(f'{x},{y}' for x,y in coords)+'" fill="none" stroke="#f2c230" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
        sx,sy=coords[0]; ex,ey=coords[-1]
        b+=rect(sx-27,sy-26,54,52,COLORS['kok'],10)+circle(sx-10,sy-7,4,'#fff',0)+circle(sx+10,sy-7,4,'#fff',0)+line(sx-10,sy+11,sx+10,sy+11,'#fff',3)
        b+=line(ex-13,ey+26,ex-13,ey-30,sw=4)+poly(f'{ex-13},{ey-30} {ex+30},{ey-16} {ex-13},{ey-3}',COLORS['qizil'],3)
        svg('yol-robot-'+str(n),b)
    for name,colors in [('1',['#255caf','#3982cb','#50a5ab','#72b98d']),
                        ('2',['#cf4a41','#ef8840','#f2b343','#f4cd64']),
                        ('3',['#cf4a41','#386fbc','#f2b343','#845bad'])]:
        b=rect(30,60,340,280,'#f5f9ff',30,stroke='#d7e3ef',sw=3)
        for i,c in enumerate(colors):
            b+=rect(57+i*73,100,64,205,c,20,stroke='none',sw=0)
        svg('uygunlik-'+name,b)
    for name,missing in [('toliq',False),('yashilsiz',True)]:
        b=''
        for i,c in enumerate(['#e94b4b','#ff9f43','#f2c230','#4caf50','#3d7be0','#a06cf0']):
            r=170-i*22
            b+=f'<path d="M{200-r} 315 A{r} {r} 0 0 1 {200+r} 315" fill="none" stroke="{c if not(missing and i==3) else "#ecf2f7"}" stroke-width="21"/>'
        svg('kamalak-'+name,b)


def construction_assets(rows):
    for row in rows:
        if row['tur']!='qurish':
            continue
        for v in row['variants_after']:
            name=Path(v['rasm']).stem
            if name in BODIES or not name.startswith('bolak-'):
                continue
            _,kind,color,dimensions=name.split('-')
            w,h=[int(x)*10 for x in dimensions.split('x')]
            if name=='bolak-uchburchak-qizil-22x26':
                body = poly(f'3,{h/2} {w-3},3 {w-3},{h-3}',COLORS[color],4)
            else:
                body = shape(kind,COLORS[color],0,0,w,h,max(2,min(w,h)*.018))
            svg(name,body,w,h)
    svg('osimlik-gul', ''.join(circle(x,y,55,COLORS['qizil'],4) for x,y in [(200,100),(285,155),(255,245),(145,245),(115,155)])+circle(200,180,47,COLORS['sariq'],4),400,330)
    svg('osimlik-barg','<path d="M18 102 Q190 -34 382 102 Q190 232 18 102 Z" fill="#4caf50" stroke="#24364d" stroke-width="6"/>'+line(26,102,369,102,'#2f7437',5),400,200)
    svg('osimlik-poya',rect(12,3,76,394,COLORS['yashil'],30,sw=5),100,400)
    svg('osimlik-ildiz','<path d="M200 7 L200 110 M200 60 Q142 82 85 147 M200 78 Q250 93 320 147 M200 110 L165 186 M200 110 L243 186 M123 108 L105 178 M278 117 L296 181" fill="none" stroke="#92683e" stroke-width="15" stroke-linecap="round"/>',400,200)
    for row in rows:
        if row['tur']!='qurish':
            continue
        sample=Path(row['after']['rasm']).stem
        b=rect(1,1,98,68,'#f4f9ff',4,stroke='#d8e5f0',sw=.7)
        b+=line(8,67,92,67,'#dceadf',.8)
        if 'simmetriya' in sample or 'kapalak-yarim' in sample:
            b+=line(50,3,50,66,'#9fb8ca',.65,'stroke-dasharray="2 2"')
        for v in row['variants_after']:
            x,y,w,h=map(float,v['slot'].split(','))
            y *= .7
            h *= .7
            name=Path(v['rasm']).stem
            if name in BODIES:
                body,pw,ph=BODIES[name]
                b+=f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {pw} {ph}" preserveAspectRatio="none">{body}</svg>'
            else:
                b+=image(name,x,y,w,h)
        svg(sample,b,100,70)


def scene_diagrams():
    for source in ('fil','baliq','qush','chotka','palitra'):
        svg('soya-'+source,image(source,35,35,330,330,True))
    # Qalam soyasi rangli variant bilan aynan bir geometriyadan olinadi.
    b,_,_=BODIES['qalam-uzun']
    b=re.sub(r'fill="#[0-9a-fA-F]+"',f'fill="{INK}"',b)
    b=re.sub(r'stroke="#[0-9a-fA-F]+"',f'stroke="{INK}"',b)
    svg('soya-qalam',b)
    for condition in ('xato-baliq-daraxtda','togri-baliq-suvda','xato-qush-suvda','togri-qush-daraxtda'):
        b=rect(5,5,390,390,'#e8f4fc',32,stroke='#d5e5ee',sw=2)+rect(10,275,380,115,'#d1e9ca',20,stroke='none',sw=0)
        if 'daraxtda' in condition:
            b+=image('daraxt',20,15,340,350)+image('baliq' if 'baliq' in condition else 'qush',120,115,100,90)
        else:
            b+=f'<path d="M20 180 Q80 155 140 180 T260 180 T380 180 L380 375 L20 375 Z" fill="#61b6de"/>'
            b+=image('baliq' if 'baliq' in condition else 'qush',125,220,160,120)
            for x,y in [(85,235),(300,305),(318,255)]:
                b+=circle(x,y,6,'#bce9ff',1)
        svg(condition,b)
    for wrong in (True,False):
        name='xato-qor-yozda' if wrong else 'togri-quyosh-yozda'
        b=rect(5,5,390,390,'#dceffa',30,stroke='none',sw=0)+rect(5,270,390,125,'#b6d992',25,stroke='none',sw=0)+image('daraxt',35,100,230,255)
        b+=label(304,312,'30°C',27)
        b+=rect(326,180,18,110,'#fff',8,sw=2)+rect(331,218,8,69,COLORS['qizil'],4,stroke='none',sw=0)+circle(335,288,15,COLORS['qizil'],2)
        if wrong:
            b+=rect(70,20,250,70,'#d3dfe8',35,stroke='none',sw=0)
            for x,y in [(70,120),(210,100),(335,125),(310,180),(130,210)]:
                b+=line(x-9,y,x+9,y,'#fff',4)+line(x,y-9,x,y+9,'#fff',4)+line(x-6,y-6,x+6,y+6,'#fff',4)+line(x-6,y+6,x+6,y-6,'#fff',4)
        else:
            b+=circle(310,75,38,COLORS['sariq'],2)
        svg(name,b)
    b=''
    for offset,after in [(0,False),(390,True)]:
        b+=rect(offset+15,20,365,300,'#f0f7fc',24,stroke='#d7e5ee',sw=2)
        b+=rect(offset+80,185,230,90,'#e1f3fc',18,stroke='#7598b1',sw=4)
        if after:
            b+=f'<path d="M{offset+94} 239 Q{offset+170} 222 {offset+218} 239 T{offset+296} 239 L{offset+296} 263 L{offset+94} 263 Z" fill="#7ac5e7"/>'
        else:
            b+=rect(offset+139,113,98,100,'#b6e5f9',14,stroke='#5794b7',sw=4)+line(offset+157,138,offset+179,125,'#fff',7)
        b+=label(offset+195,357,'KEYIN' if after else 'AVVAL',25)
    svg('tajriba-muz',b,780,390)
    b=''
    for offset,watered in [(0,True),(390,False)]:
        b+=rect(offset+15,15,365,335,'#f0f7fc',22,stroke='#d7e5ee',sw=2)+circle(offset+310,67,28,COLORS['sariq'],2)
        b+=poly(f'{offset+135},251 {offset+257},251 {offset+242},320 {offset+150},320','#d38b61',3)
        b+=f'<path d="M{offset+196} 254 Q{offset+(186 if watered else 245)} 175 {offset+(196 if watered else 269)} 104" fill="none" stroke="{COLORS["yashil"] if watered else "#9c945e"}" stroke-width="10"/>'
        for cy,side in [(168,-1),(210,1)]:
            x=offset+(196 if watered else 230)
            angle=-30*side if watered else 55*side
            b+=f'<ellipse cx="{x+side*30}" cy="{cy}" rx="40" ry="17" fill="{COLORS["yashil"] if watered else "#aaa565"}" transform="rotate({angle} {x+side*30} {cy})"/>'
        if watered:
            for x in (offset+88,offset+109,offset+130):
                b+=f'<path d="M{x} 152 Q{x-13} 177 {x} 181 Q{x+13} 177 {x} 152" fill="#3d9ad9"/>'
        b+=label(offset+195,380,'SUV BERILGAN' if watered else 'SUV BERILMAGAN',23)
    svg('tajriba-osimlik',b,780,405)
    b=''
    for offset,changed in [(0,False),(390,True)]:
        b+=rect(offset+10,15,370,355,'#eaf4fb',25,stroke='#d7e5ee',sw=2)+rect(offset+15,267,360,98,'#cfe4b6',18,stroke='none',sw=0)
        b+=circle(offset+311,68,30,COLORS['tosariq'] if changed else COLORS['sariq'],2)
        b+=rect(offset+95,193,155,112,'#92bada',8,sw=3)+poly(f'{offset+75},195 {offset+174},120 {offset+273},195',COLORS['kok'] if changed else COLORS['qizil'],3)
        b+=rect(offset+148,248,41,57,'#92683e',3,sw=2)
        for x in (offset+114,offset+204):
            b+=rect(x,214,28,25,'#fff0aa',3,sw=2)
        if changed:
            for x,y in [(offset+80,76),(offset+140,85)]:
                b+=f'<path d="M{x-12} {y} Q{x-4} {y-9} {x} {y} Q{x+5} {y-9} {x+13} {y}" fill="none" stroke="#24364d" stroke-width="4"/>'
        b+=label(offset+195,397,'B' if changed else 'A',23)
    svg('farq-namuna',b,780,420)


def coloring(rows):
    def region(tag, name, attributes, expected=None):
        attrs = f'data-soha="{name}" ' + attributes
        if expected:
            attrs += f' data-togri="{expected}"'
        return f'<{tag} {attrs}/>'

    def outline(path):
        return f'<path class="chizgi" d="{path}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" pointer-events="none"/>'

    butterfly = ''
    for side, sign in [('chap', -1), ('ong', 1)]:
        x = 150 + sign * 49
        butterfly += region('path', 'qanot-yuqori-' + side,
                            f'd="M150 102 C{x+sign*33} 2 {x+sign*63} 35 {x+sign*49} 82 C{x+sign*40} 118 {x} 131 150 122 Z"')
        butterfly += region('path', 'qanot-past-' + side,
                            f'd="M150 119 C{x+sign*39} 93 {x+sign*53} 164 {x+sign*19} 188 C{x} 208 {x-sign*18} 174 150 131 Z"')
        butterfly += region('ellipse', 'vazn-yuqori-' + side, f'cx="{x+sign*6}" cy="77" rx="18" ry="23"')
        butterfly += region('circle', 'vazn-past-' + side, f'cx="{x}" cy="157" r="15"')
    butterfly += region('ellipse', 'tana', 'cx="150" cy="127" rx="12" ry="65"')
    butterfly += region('circle', 'bosh', 'cx="150" cy="58" r="15"')
    butterfly += outline('M144 47 Q139 21 123 18 M156 47 Q161 21 177 18')

    flower = region('rect', 'poya', 'x="144" y="117" width="12" height="96" rx="6"', COLORS['yashil'])
    flower += region('path', 'barg-chap', 'd="M145 169 Q93 125 74 151 Q95 191 145 169 Z"', COLORS['yashil'])
    flower += region('path', 'barg-ong', 'd="M156 190 Q207 142 228 168 Q205 210 156 190 Z"', COLORS['yashil'])
    for i in range(6):
        angle=math.pi*i/3-math.pi/2
        x=150+math.cos(angle)*43; y=89+math.sin(angle)*43
        flower += region('ellipse', f'gulbarg-{i+1}',
                         f'cx="{x:.2f}" cy="{y:.2f}" rx="24" ry="31" transform="rotate({i*60} {x:.2f} {y:.2f})"', COLORS['qizil'])
    flower += region('circle', 'markaz', 'cx="150" cy="89" r="25"', COLORS['sariq'])

    landscape = region('rect','osmon','x="8" y="8" width="284" height="139" rx="15"')
    landscape += region('path','yer','d="M8 147 Q83 124 150 146 T292 147 L292 223 L8 223 Z"')
    landscape += region('circle','quyosh','cx="247" cy="48" r="23"')
    landscape += region('path','bulut','d="M35 57 Q26 37 47 33 Q53 13 72 26 Q94 21 98 40 Q114 44 101 58 Z"')
    landscape += region('rect','uy-devor','x="48" y="119" width="100" height="75" rx="4"')
    landscape += region('polygon','uy-tom','points="37,120 98,70 159,120"')
    landscape += region('rect','eshik','x="86" y="150" width="26" height="44" rx="3"')
    landscape += region('rect','deraza','x="57" y="133" width="22" height="21" rx="3"')
    landscape += region('rect','daraxt-tana','x="220" y="132" width="16" height="64" rx="3"')
    landscape += region('path','daraxt-barg','d="M190 119 Q168 90 194 80 Q202 47 229 69 Q254 51 267 85 Q287 114 259 133 Q225 156 190 119 Z"')
    landscape += region('path','yolak','d="M91 194 L111 194 L150 223 L61 223 Z"')
    landscape += outline('M68 135 V152 M58 144 H77 M94 172 H101')

    school = region('rect','osmon','x="8" y="8" width="284" height="148" rx="14"')
    school += region('rect','yer','x="8" y="156" width="284" height="67" rx="10"')
    school += region('circle','quyosh','cx="255" cy="43" r="23"')
    school += region('rect','bino','x="51" y="91" width="198" height="105" rx="5"')
    school += region('polygon','tom','points="39,92 150,49 261,92"')
    school += region('rect','eshik-chap','x="129" y="151" width="21" height="45" rx="2"')
    school += region('rect','eshik-ong','x="150" y="151" width="21" height="45" rx="2"')
    for i,x in enumerate((70,106,174,210)):
        school += region('rect',f'deraza-{i+1}',f'x="{x}" y="113" width="25" height="24" rx="3"')
    school += region('rect','bayroq','x="151" y="20" width="30" height="18" rx="2"')
    school += region('path','yolak','d="M129 196 L171 196 L188 223 L111 223 Z"')
    school += region('circle','gul-chap','cx="37" cy="186" r="12"')
    school += region('circle','gul-ong','cx="267" cy="186" r="12"')
    school += outline('M150 18 V51 M37 198 V216 M267 198 V216')
    drawings = {'5.1.2':butterfly, '5.2.1':flower, '5.3.1':school,
                '5.3.4':landscape, '5.3.10/1':butterfly, '5.3.10/4':landscape}
    for row in rows:
        if row['tur']!='boyash':
            continue
        drawing = '<svg viewBox="0 0 300 232" xmlns="http://www.w3.org/2000/svg" role="img">' + drawings[row['key']] + '</svg>'
        tree=ET.fromstring(drawing)
        # Dekor chiziqlar bo‘yaladigan sohalarni to‘smasin.
        for node in tree.iter():
            if node.get('class')=='chizgi':
                node.set('pointer-events','none')
        row['after']['boyash']=ET.tostring(tree,encoding='unicode').replace('ns0:','').replace(':ns0','')
        if row['key']=='5.2.1':
            for node in tree.iter():
                if node.get('data-soha'):
                    node.set('fill',node.get('data-togri','#ffffff'))
                    node.set('stroke',INK)
                    node.set('stroke-width','2.5')
            sample=ET.tostring(tree,encoding='unicode').replace('ns0:','').replace(':ns0','')
            (ASSETS/'namuna-gul.svg').write_text(sample,encoding='utf8')
            CREATED.add('namuna-gul')


def main():
    rows=json.loads(CONTENT.read_text(encoding='utf8'))
    simple_assets()
    sequence_assets()
    construction_assets(rows)
    scene_diagrams()
    coloring(rows)
    # Qayta chizilgan labirintda yo‘l oldindan mavjudligi tekshiriladi.
    for row in rows:
        if row['tur']=='labirint':
            row['after']['labirint'] = '\n'.join([
                '#############', '#R..#.......#', '###.#.###.#.#',
                '#...#.#...#.#', '#.###.#.###.#', '#.....#...#.#',
                '#.#######.#.#', '#.#.....#...#', '#.#.###.###.#',
                '#...#......H#', '#############',
            ])
    for row in rows:
        if row['after']['rasm'] and Path(row['after']['rasm']).stem in CREATED:
            row['after']['rasm']=str(Path(row['after']['rasm']).with_suffix('.svg')).replace('\\','/')
        for v in row['variants_after']:
            for field in ('rasm','juft_rasm'):
                if v[field] and Path(v[field]).stem in CREATED:
                    v[field]=str(Path(v[field]).with_suffix('.svg')).replace('\\','/')
    CONTENT.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'{len(CREATED)} ta aniq geometriyali SVG qayta yaratildi.')


if __name__=='__main__':
    main()
