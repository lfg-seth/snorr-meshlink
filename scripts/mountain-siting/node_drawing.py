"""Typography, page geometry and stable page destinations for the node atlas."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab import rl_config
from node_model import REGIONAL, SITES, neighbors

# Embed compressed binary images directly, preserving the native map resolution.
rl_config.useA85=0

W,H=842,595
PAPER="#FAF9F4"
INK="#152B32"
TEAL="#126B64"
SOFT="#54696D"
GRID="#CAD3CC"
FONT=Path("C:/Windows/Fonts")
for alias,name in (("Sans","segoeui.ttf"),("Bold","segoeuib.ttf"),("Serif","georgia.ttf")):
    pdfmetrics.registerFont(TTFont(alias,str(FONT/name)))

def txt(c,x,y,s,size=10,font="Sans",color=INK,right=False):
    c.setFillColor(colors.HexColor(color)); c.setFont(font,size)
    if right:c.drawRightString(x,y,str(s))
    else:c.drawString(x,y,str(s))

def rule(c,x,y,end,color=GRID):
    c.setStrokeColor(colors.HexColor(color));c.setLineWidth(.65);c.setDash([]);c.line(x,y,end,y)

def fillbox(c,x,y,w,h,color):
    c.setFillColor(colors.HexColor(color));c.rect(x,y,w,h,fill=1,stroke=0)

def para(c,x,y,text,width,size=10,leading=15,color=INK,font="Sans"):
    line=""
    for word in text.split():
        check=(line+" "+word).strip()
        if line and c.stringWidth(check,font,size)>width:
            txt(c,x,y,line,size,font,color);y-=leading;line=word
        else: line=check
    if line:
        txt(c,x,y,line,size,font,color);y-=leading
    return y

def psite(k):
    return 10+len(REGIONAL)+sum(2+len(neighbors(site)) for site in SITES[:SITES.index(k)])

def chapter_end(k):
    return psite(k)+1+len(neighbors(k))

def ppath(a,b):
    return psite(a)+2+neighbors(a).index(b)

def link(links,x,y,w,h,dest):
    links.append([x,y,w,h,dest])

def start(c,number,section,title,sub=""):
    fillbox(c,0,0,W,H,PAPER)
    txt(c,32,568,section.upper(),9,"Bold",TEAL)
    txt(c,32,534,title,25,"Serif")
    if sub:txt(c,33,512,sub,10,"Sans",SOFT)
    rule(c,32,35,810)
    txt(c,32,19,"SNORR MeshLink   /   Mount Charleston repeater study   ·   18 November 2026",7.6,"Sans",SOFT)
    txt(c,810,19,str(number),8.2,"Bold",INK,True)

def nav(c,links,left=560):
    txt(c,left,19,"Contents",8.2,"Bold",TEAL);link(links,left,12,45,17,4)
    txt(c,left+62,19,"Node directory",8.2,"Bold",TEAL);link(links,left+62,12,70,17,5)

def table(c,cols,widths,rows,x,y,rowheight=22,size=9):
    """Return the vertical midlines for linked body rows."""
    total=sum(widths)
    fillbox(c,x,y-rowheight,total,rowheight,"#DCE9E2")
    offset=x
    for text,w in zip(cols,widths):
        txt(c,offset+5,y-rowheight*.65,text,size,"Bold","#244D4D");offset+=w
    mids=[]
    for i,row in enumerate(rows):
        top=y-(i+1)*rowheight
        if i%2==0:fillbox(c,x,top-rowheight,total,rowheight,"#FFFFFF")
        rule(c,x,top-rowheight,x+total)
        mid=top-rowheight*.65; mids.append(mid); off=x
        for text,w in zip(row,widths):
            txt(c,off+5,mid,text,size);off+=w
    return mids

def summary_stat(c,x,y,value,label):
    txt(c,x,y,value,24,"Bold",TEAL);txt(c,x,y-19,label,9,"Sans",SOFT)
