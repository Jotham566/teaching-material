"""Geometry audit of the generated slide specs: wrapped titles, small text, overlaps, off-slide objects."""
import json, glob, sys
import slidekit as K
def txt(o):
    return o['text'] if 'text' in o and o.get('text') is not None else ''.join(r['text'] for r in o.get('runs', []))
def ov(a,b):
    return min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>0.08 and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>0.08
out=[]
for f in sorted(glob.glob('_specs/*.json')):
    d=json.load(open(f)); name=f.split('/')[-1][:-5]
    for i,s in enumerate(d['slides'],1):
        t=s.get('title')
        if t and s['layout']!='dark':
            lines=len(K.wrap(t['text'],t['size'],'bold',11.9))
            if lines>1: out.append((name,i,'title wraps',f"{lines} lines @ {t['size']}: {t['text'][:50]}"))
        objs=[o for o in s['objects'] if o['type'] in('text','image')]
        for o in objs:
            if o['y']+o['h']>6.95 and s['layout']!='dark': out.append((name,i,'low',f"{o['type']} bottom {o['y']+o['h']:.2f}"))
            if o['x']<0.3 or o['x']+o['w']>13.1: out.append((name,i,'edge',f"{o['type']} x {o['x']:.2f}-{o['x']+o['w']:.2f}"))
            if o['type']=='text' and o.get('size',99)<14 and s['layout']!='dark': out.append((name,i,'small text',f"{o['size']} {txt(o)[:30]}"))
        for a in range(len(objs)):
            for b in range(a+1,len(objs)):
                if ov(objs[a],objs[b]): out.append((name,i,'overlap',f"{objs[a]['type']}/{objs[b]['type']} {txt(objs[a])[:20]!r} {txt(objs[b])[:20]!r}"))
        # title vs content
        if t and s['layout']!='dark':
            tl=len(K.wrap(t['text'],t['size'],'bold',11.9)); th=tl*t['lead']/72
            for o in objs:
                if o['y']<0.42+th-0.02: out.append((name,i,'title collision',f"{o['type']} y={o['y']:.2f} title bottom {0.42+th:.2f}"))
from collections import Counter
print(Counter(k for _,_,k,_ in out))
for r in out: print(*r)
