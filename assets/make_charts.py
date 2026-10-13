import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; PURPLE="#7048e8"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/cv_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def box(ax,x,y,w,h,c,fc="white",lw=1.8): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.08",fc=fc,ec=c,lw=lw))

# 1 Program map
fig,ax=plt.subplots(figsize=(10,3.4)); ax.axis("off"); ax.set_xlim(0,6.3); ax.set_ylim(-.1,2.85)
top=[("A","AU → km"),("B","mi → km"),("C","nmi → km"),("D","yd → m"),("E","ft → m"),("F","× rate")]
bot=[("G","km → AU"),("H","km → mi"),("I","km → nmi"),("J","m → yd"),("K","m → ft"),("L","÷ rate")]
for row,(items,y,col) in enumerate([(top,1.5,BLUE),(bot,.1,GREEN)]):
    for i,(k,t) in enumerate(items):
        c=ORANGE if k in "FL" else col
        box(ax,i*1.03+.12,y,.92,.95,c)
        ax.text(i*1.03+.58,y+.65,f"LBL {k}",ha="center",va="center",fontsize=12,fontweight="bold",color=c)
        ax.text(i*1.03+.58,y+.3,t,ha="center",va="center",fontsize=10.5)
for i in range(6): ax.annotate("",xy=(i*1.03+.58,1.07),xytext=(i*1.03+.58,1.48),arrowprops=dict(arrowstyle="<->",color=GREY,lw=1))
ax.text(.12,2.72,"Program Map: top row converts to metric (×), second row converts back (÷)",fontsize=12,fontweight="bold",va="center")
save(fig,"program_map")

# 2 Unit sizes
units=[("Foot","0.3048 m",0.3048,BLUE),("Yard","0.9144 m",0.9144,BLUE),("Metre","1 m",1,GREY),("Kilometre","1,000 m",1000,GREY),
       ("Mile","1,609.344 m",1609.344,BLUE),("Nautical mile","1,852 m",1852,BLUE),("Astronomical unit","149,597,870,700 m",1.495978707e11,PURPLE)]
fig,ax=plt.subplots(figsize=(9.5,4.2)); ax.grid(axis="y",visible=False)
ys=np.arange(len(units))[::-1]
for (n,lab,v,c),y in zip(units,ys):
    ax.barh(y,np.log10(v)+1,left=-1,color=c,alpha=.85,height=.62)
    ax.text(np.log10(v)+.15,y,lab,va="center",fontsize=10,fontweight="bold",color=c)
ax.set_yticks(ys); ax.set_yticklabels([u[0] for u in units])
ax.set_xticks([0,3,6,9,12]); ax.set_xticklabels(["1 m","1 km","1,000 km","1 million km","1 billion km"],fontsize=9.5)
ax.set_xlim(-1,16.2); ax.set_xlabel("Length (log scale)")
ax.set_title("Exact Definitions Behind Every Factor",loc="left"); save(fig,"unit_sizes")

# 3 Currency registers
fig,ax=plt.subplots(figsize=(10.5,4.6)); ax.axis("off"); ax.set_xlim(0,10.5); ax.set_ylim(0,5.6)
ax.text(0,5.4,"Currency: rate table in Extended registers, active rate in Global register −200",fontsize=12.5,fontweight="bold",va="center")
ax.text(.2,4.75,"Extended registers (saved in the Statefile)",fontsize=10,color=GREEN,fontweight="bold")
rates=[("201","USD","0.73"),("202","EUR","0.62"),("203","GBP","0.54"),("204","JPY","108.50"),("205","…","…")]
for i,(r,cur,v) in enumerate(rates):
    y=4.0-i*.8; box(ax,.2,y,3.3,.62,GREEN)
    ax.text(.45,y+.31,r,va="center",fontsize=11,fontweight="bold",color=GREEN,family="DejaVu Sans Mono")
    ax.text(1.45,y+.31,cur,va="center",fontsize=11)
    ax.text(3.3,y+.31,v,va="center",ha="right",fontsize=11,family="DejaVu Sans Mono")
ax.add_patch(FancyArrowPatch((3.6,4.31),(4.55,2.65),arrowstyle="-|>",mutation_scale=18,color=GREY,lw=1.8,connectionstyle="arc3,rad=-0.2"))
ax.text(4.35,4.25,"copy the rate\nneeded",fontsize=9.5,color=GREY)
box(ax,4.6,2.0,2.2,1.2,ORANGE,lw=2.4)
ax.text(5.7,2.85,"Global −200",ha="center",fontsize=12,fontweight="bold",color=ORANGE)
ax.text(5.7,2.35,"0.73",ha="center",fontsize=14,family="DejaVu Sans Mono",fontweight="bold")
ax.text(5.7,1.65,"shared by all States,\nlost on RESET",ha="center",va="top",fontsize=9,color=GREY)
for y,lab,res,c in [(3.3,"100  XEQ F","= 73.00 USD",BLUE),(1.4,"50  XEQ L","= 68.49 CAD",GREEN)]:
    ax.add_patch(FancyArrowPatch((6.85,2.6),(7.4,y+.15),arrowstyle="-|>",mutation_scale=16,color=c,lw=1.8))
    box(ax,7.45,y-.35,2.95,1.0,c)
    ax.text(7.62,y+.33,lab,va="center",fontsize=11,family="DejaVu Sans Mono",fontweight="bold",color=c)
    ax.text(7.62,y-.05,res,va="center",fontsize=11)
ax.text(7.45,4.55,"F: home → foreign  (× rate)",fontsize=9.5,color=BLUE); ax.text(7.45,.7,"L: foreign → home  (÷ rate)",fontsize=9.5,color=GREEN)
ax.text(.2,.2,"Rates are illustrative, in units of foreign currency per 1 CAD.",fontsize=9,color=GREY)
save(fig,"currency_registers")

# 4 Global register map across statefiles
fig,ax=plt.subplots(figsize=(10,2.9)); ax.set_xlim(-1000,-90); ax.set_ylim(-.3,2.4); ax.grid(False)
ax.spines["left"].set_visible(False); ax.set_yticks([]); ax.invert_xaxis()
ax.barh(.7,910,left=-1000,height=.5,color="#eef1f4")
uses=[(-102,-100,"astrodynamics32\n−100 to −102",PURPLE,1.75),(-200,-200,"conversion32\n−200",ORANGE,1.15),(-333,-328,"layover32\n−328 to −333",BLUE,1.75),(-929,-900,"astrodynamics32\n−900 to −929",PURPLE,1.15)]
for a,b,lab,c,yy in uses:
    lo=min(a,b); w=max(abs(b-a),5)
    ax.barh(.7,w,left=lo,height=.5,color=c)
    ax.plot([(a+b)/2,(a+b)/2],[.97,yy-.02],color=c,lw=.8)
    ax.text((a+b)/2,yy,lab,ha="center",va="bottom",fontsize=9.2,color=c)
ax.set_xticks([-100,-200,-300,-400,-500,-600,-700,-800,-900,-999]); ax.set_xticklabels(["−100","−200","−300","−400","−500","−600","−700","−800","−900","−999"])
ax.set_xlabel("Global register")
ax.set_title("Global Register Use Across jacober-calc Statefiles",loc="left",pad=14); save(fig,"global_registers")
