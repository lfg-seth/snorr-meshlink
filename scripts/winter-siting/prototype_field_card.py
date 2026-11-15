"""Printable field-card prototype. Run with the private winter study directory as its argument."""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from study import configure

root = Path(sys.argv[1]).resolve()
configure(root)

import numpy as np
import rasterio
from PIL import Image
from matplotlib.colors import LightSource
from rasterio.windows import from_bounds
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from shapely.geometry import Point
from shapely.ops import linemerge, unary_union
from cartography import features
from expansion_pages import stage
from terrain import forward
from field_names import field_name

INK = '#192e38'
SOFT = '#405b62'
GRAY = '#7b888b'
BLUE = '#155d81'
GOLD = '#965b13'
RED = '#9f364b'
PAPER = '#ffffff'
RULE = '#c5cfcc'
TEAL = '#1b615a'
ROAD_COLORS = [GRAY, BLUE, GOLD, RED]

for font, filename in [('Text', 'segoeui.ttf'), ('Bold', 'segoeuib.ttf'), ('Title', 'georgiab.ttf')]:
    pdfmetrics.registerFont(TTFont(font, str(Path('C:/Windows/Fonts')/filename)))

pdf = canvas.Canvas(str(root/'Lee-Canyon-winter-trial-field-card.pdf'),
                    pagesize=landscape(letter), pageCompression=1)
pdf.setTitle('Lee Canyon winter relay trial | Field card')
pdf.setAuthor('SNORR MeshLink')
pdf.setSubject('Driver stops and dispatch acceptance for the two winter repeater trials')


def text(x,y,s,size=10,font='Text',color=INK,align='left'):
    pdf.setFont(font,size)
    pdf.setFillColor(HexColor(color))
    {'left':pdf.drawString,'right':pdf.drawRightString,'center':pdf.drawCentredString}[align](x,y,s)


def line(x1,y1,x2,y2,color,width=1):
    pdf.setStrokeColor(HexColor(color));pdf.setLineWidth(width)
    pdf.line(x1,y1,x2,y2)


def box(x,y,w,h,color):
    pdf.setFillColor(HexColor(color));pdf.rect(x,y,w,h,stroke=0,fill=1)


def lines_of(g):
    if g.geom_type=='LineString':return [g]
    return [line for part in getattr(g,'geoms',[]) for line in lines_of(part)]


def road_style(category, path):
    # Each category has a unique stroke pattern for monochrome field copies.
    pdf.saveState()
    pdf.setLineCap(1);pdf.setLineJoin(1)
    width=[2.5,4.6,5.3,3.3][category]
    pdf.setLineWidth(width+1.9);pdf.setStrokeColor(HexColor(PAPER));pdf.drawPath(path)
    pdf.setLineWidth(width);pdf.setStrokeColor(HexColor(ROAD_COLORS[category]))
    if category==3:
        pdf.setDash([3.1,2.1]);pdf.setLineCap(0)
    pdf.drawPath(path)
    if category==2:
        pdf.setStrokeColor(HexColor('#fff5dd'));pdf.setLineWidth(1.15);pdf.drawPath(path)
    pdf.restoreState()


def pill(x,y,value,fill,size=15,diamond=False):
    pdf.setFillColor(HexColor(fill));pdf.setStrokeColor(HexColor(PAPER));pdf.setLineWidth(1.2)
    if diamond:
        p=pdf.beginPath();p.moveTo(x,y+size/2);p.lineTo(x+size/2,y)
        p.lineTo(x,y-size/2);p.lineTo(x-size/2,y);p.close()
        pdf.drawPath(p,stroke=1,fill=1)
    else:
        pdf.roundRect(x-size/2,y-size/2,size,size,2.6,stroke=1,fill=1)
    if value:text(x,y-3,value,8.4,'Bold',PAPER,'center')


def map_text(x,y,s,size=9.5,color=INK,align='left'):
    width=pdfmetrics.stringWidth(s,'Bold',size)
    left=x if align=='left' else x-width
    obj=pdf.beginText(left,y);obj.setFont('Bold',size);obj.setTextRenderMode(2)
    pdf.saveState();pdf.setStrokeColor(HexColor('#ffffff'));pdf.setFillColor(HexColor(color))
    pdf.setLineWidth(3);pdf.setLineJoin(1);obj.textOut(s);pdf.drawText(obj);pdf.restoreState()
    text(x,y,s,size,'Bold',color,align)


r=json.loads((root/'tables/results.json').read_bytes())
trial=r['expansion']['access_pair']
assert trial['sites']==['JS','MN'] and trial['paths']['MN']==['MN','JS','GL']
sites={s['id']:s for s in r['sites']}
stops={}
for wp in ET.parse(root/'expansion-trials.gpx').getroot():
    name=wp.findtext('{*}name','')
    if name[:4] in ('C - ','E - ','F - '):
        ll=float(wp.get('lon')),float(wp.get('lat'))
        stops[name[0]]=(ll,Point(forward.transform(*ll)))
study_roads=features(root,'winter-trial-roads')
assert set(stops)=={'C','E','F'}
for k,name,category in [('C','SR 156',0),('E','SR 156',1),('F','Macks Canyon',2)]:
    segments=[g for g,p in study_roads if p['name']==name and stage(p)==category]
    assert min(g.distance(stops[k][1]) for g in segments)<0.1,(k,'waypoint outside expected road class')

# Map geometry is uniformly scaled in UTM metres. The label offsets are in print points.
MX,MY,MW,MH=24,128,442,391
main=unary_union([g for g,_ in study_roads])
x0,y0,x1,y1=main.bounds
mp=(max((x1-x0)/(MW-96),(y1-y0)/(MH-37)))
cx=(x1+x0)/2;cy=(y1+y0)/2
west,south=cx-MW*mp/2,cy-MH*mp/2
east,north=west+MW*mp,south+MH*mp
def xy(x,y):return MX+(x-west)/mp,MY+(y-south)/mp


def path_for(geoms):
    p=pdf.beginPath()
    for g in geoms:
        for seg in lines_of(g):
            coords=list(seg.coords);p.moveTo(*xy(*coords[0][:2]))
            for point in coords[1:]:p.lineTo(*xy(*point[:2]))
    return p


def draw_map():
    pdf.saveState()
    clip=pdf.beginPath();clip.rect(MX,MY,MW,MH);pdf.clipPath(clip,stroke=0)
    with rasterio.open(root/'cache/terrain-local.tif') as src:
        w,h=1100,round(1100*MH/MW)
        z=src.read(1,window=from_bounds(west,south,east,north,src.transform),out_shape=(h,w),
                   boundless=True,masked=True,resampling=rasterio.enums.Resampling.bilinear)
        heights=z.filled(float(np.ma.median(z))).astype(float)
        shade=LightSource(azdeg=306,altdeg=39).hillshade(heights,dx=(east-west)/w,dy=(north-south)/h)
        tone=np.clip(220+33*shade,214,253)
        rgb=np.stack([tone,tone+1,tone-2],axis=-1).clip(0,255).astype('uint8')
        pdf.drawImage(ImageReader(Image.fromarray(rgb)),MX,MY,MW,MH)
    context=features(root,'routes')
    pdf.setLineJoin(1);pdf.setLineWidth(.55);pdf.setStrokeColor(HexColor('#b8c0b5'))
    pdf.drawPath(path_for([g for g,p in context if p['kind']=='trail' and g.bounds[2]>=west and g.bounds[0]<=east]))
    pdf.setLineWidth(1.0);pdf.setStrokeColor(HexColor('#9caaa8'))
    pdf.drawPath(path_for([g for g,p in context if p['kind']=='road' and p['name'] not in ('Macks Canyon','SR 156')]))
    for category in (0,1,3,2):
        group=unary_union([g for g,p in study_roads if stage(p)==category])
        if group.geom_type=='MultiLineString':group=linemerge(group)
        road_style(category,path_for([group]))
    for k,num,offset,color in [('SI','10',(-12,0),INK),('GL','',(-9,-1),TEAL),
                               ('JS','11',(12,0),BLUE),('MN','12',(-12,1),GOLD)]:
        s=sites[k];x,y=xy(s['x'],s['y'])
        pill(x,y,num,color,16,diamond=k=='GL')
        dx,dy=offset
        map_text(x+dx,y-3+dy,field_name(k),9.0,color,'left' if dx>0 else 'right')
        if k=='GL':map_text(x-10,y-14,'RF receiver / dispatch uplink',7.7,TEAL,'right')
    # Offset the stop letters so the short gained sections stay visible underneath.
    for key,(dx,dy) in {'C':(21,7),'E':(-20,10),'F':(-22,-18)}.items():
        px,py=xy(stops[key][1].x,stops[key][1].y)
        x,y=px+dx,py+dy
        line(px,py,x,y,INK,.9)
        pdf.setFillColor(HexColor(INK));pdf.circle(px,py,1.5,fill=1,stroke=0)
        pdf.setFillColor(HexColor(PAPER));pdf.setStrokeColor(HexColor(INK));pdf.setLineWidth(1.5)
        pdf.circle(x,y,7.8,fill=1,stroke=1);text(x,y-3.2,key,9.4,'Bold',INK,'center')
    for name,title,frac,dx,dy in [('SR 156','SR 156  /  Lee Canyon Rd',.89,6,4),
                                  ('Macks Canyon','Macks Canyon Rd',.52,-4,13),
                                  ('SR 158','SR 158',.77,5,-8)]:
        route=max([g for g,p in context if p.get('kind')=='road' and p['name']==name],key=lambda g:g.length)
        pt=route.interpolate(frac,normalized=True);x,y=xy(pt.x,pt.y)
        if MX+10<x+dx<MX+MW-18 and MY+12<y+dy<MY+MH-12:
            map_text(x+dx,y+dy,title,8,SOFT)
    x,y=MX+18,MY+17
    length=1000/mp
    box(x-5,y-6,length+35,16,'#fefefd')
    line(x,y,x+length,y,INK,2);line(x,y-1.5,x,y+3,INK,1);line(x+length,y-1.5,x+length,y+3,INK,1)
    text(x+length+5,y-2,'1 km',8,'Bold',INK)
    x,y=MX+MW-17,MY+MH-28
    line(x,y-3,x,y+7,INK,1.2);line(x,y+7,x-2.8,y+2,INK,1.2);line(x,y+7,x+2.8,y+2,INK,1.2)
    text(x,y+11,'N',9,'Bold',INK,'center')
    pdf.restoreState()
    pdf.setLineWidth(.55);pdf.setStrokeColor(HexColor(RULE));pdf.rect(MX,MY,MW,MH,fill=0,stroke=1)


def para(x,y,content,width=275,size=10.2,leading=14):
    words=content.split();current=''
    for word in words:
        candidate=(current+' '+word).strip()
        if current and pdfmetrics.stringWidth(candidate,'Text',size)>width:
            text(x,y,current,size);y-=leading;current=word
        else:current=candidate
    if current:text(x,y,current,size);y-=leading
    return y


text(24,582,'SNORR  /  MESH OPERATIONS',9.5,'Bold',TEAL)
text(768,582,'MOUNT CHARLESTON, NV     /     WINTER 2026–27',9,'Bold',SOFT,'right')
text(23,542,'Lee Canyon winter relay trial',31,'Title',INK)
line(24,531,768,531,INK,1)
draw_map()

# Legend and navigable driver references sit immediately below the single map.
text(24,113,'MODELED ROAD COVERAGE',8.0,'Bold',SOFT)
for x,category,caption in [(24,0,'Served with 10'),(132,1,'Gained at 11'),(236,2,'Gained at 12'),(340,3,'Gap with 12')]:
    p=pdf.beginPath();p.moveTo(x,98);p.lineTo(x+19,98)
    road_style(category,p);text(x+24,94.8,caption,8.8,'Bold',INK)
line(24,83,466,83,RULE,.65)
for x,k,caption in [(24,'E','SR 156 trial'),(170,'F','Macks trial'),(317,'C','Served control')]:
    lon,lat=stops[k][0]
    text(x,68,k+'  /  '+caption,9.4,'Bold',INK)
    text(x,53,f'{lat:.5f}, {lon:.5f}',9,'Text',SOFT)

RX=481; RW=287
def minor(y,s):text(RX,y,s,8.4,'Bold',TEAL)
def trial_heading(y,num,s,col):
    pill(RX+9,y+4,num,col,18)
    text(RX+25,y,s,13,'Bold',INK)

minor(509,'BEFORE THE FIRST RUN')
y=para(RX,493,'Measure the Lee Fire Station antenna height. Log the IDs heard by its radio. Dispatch should see the same IDs and GPS fix times in the tracking portal.',RW)
line(RX,y+4,768,y+4,RULE,.7)
y-=13
trial_heading(y,'11',field_name('JS'),BLUE)
y=para(RX,y-18,'Start at E on SR 156. Run 10 → 11 → 10 repeaters. Keep 11 if new E fixes repeatedly reach dispatch through Lee and the control at C passes. Otherwise stay at 10.',RW)
sr=trial['corridors']['SR 156']
text(RX,y-1,f"Modeled gain  +{sr['gain_km']:.2f} km   /   longest gap left  {sr['gap_km']:.2f} km",9.1,'Bold',BLUE)
y-=16;line(RX,y,768,y,RULE,.7);y-=22
trial_heading(y,'12',field_name('MN'),GOLD)
y=para(RX,y-18,'Send at F on Macks Canyon Road. Run 11 → 12 → 11. Site 12 relays through 11 to Lee. Keep 12 if dispatch repeatedly gets new F fixes and C still passes. Otherwise stop at 11.',RW)
mc=trial['corridors']['Macks Canyon']
text(RX,y-1,f"Modeled gain  +{mc['gain_km']:.2f} km   /   longest gap left  {mc['gap_km']:.2f} km",9.1,'Bold',GOLD)
y-=14
control_top=y
box(RX,y-110,RW,110,'#e8f0ed')
text(RX+10,y-17,'C  /  Does the served road still work?',12,'Bold',TEAL)
y=para(RX+10,y-34,'At C, log unique fixes delivered / sent and the 95th-percentile GPS age (time since fix). Compare with the lower-count runs before and after each addition.',RW-20,9.8,13)
y=para(RX+10,y-2,'Pass if delivery and age hold within normal variation, with no repeatable rise in fixes ≥15 min old or queue drops.',RW-20,9.8,13)
y=control_top-126
minor(y,'DRIVER PROTOCOL')
y=para(RX,y-15,'Park near each marked stop and log your actual position. Send 10 paced, numbered fixes per stop in each state. Use the same route and cadence. Allow ≥30 min per state and repeat with representative busy traffic.',RW,9.7,13)
assert y>54,('right column overflow',y)
text(RX,51,'Lee antenna',8.6,'Bold',SOFT);line(RX+54,50,RX+95,50,SOFT,.6)
text(RX+98,51,'m above ground',8.6,'Text',SOFT)
text(RX+182,51,'Run date',8.6,'Bold',SOFT);line(RX+222,50,768,50,SOFT,.6)

line(24,36,768,36,INK,.8)
text(24,21,'PRIVATE FIELD COPY     /     WGS84',7.8,'Bold',SOFT)
text(768,21,'Roads © OpenStreetMap contributors   ·   Terrain USGS 3DEP   ·   Model 13 Nov 2026',7.8,'Text',SOFT,'right')
pdf.showPage();pdf.save()
