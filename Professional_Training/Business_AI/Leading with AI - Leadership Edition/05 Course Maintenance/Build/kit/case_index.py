"""Build research/case_index.json and print a theme x case summary from the coverage tables in research/*.md."""
import json, re, glob, os, collections
R = os.path.join(os.path.dirname(__file__), '..', 'research')
cases = {}
for f in sorted(glob.glob(os.path.join(R, '*.md'))):
    hdr = None
    for line in open(f):
        if line.startswith('| ID |'):
            hdr = [c.strip() for c in line.strip().strip('|').split('|')]
            continue
        if hdr and line.startswith('|') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) != len(hdr) or not re.match(r'[A-Z]{3}-\d+', cells[0]):
                continue
            d = dict(zip(hdr, cells))
            th = [h for h in hdr if re.match(r'(S\d+|PEOPLE)$', h) and d.get(h, '').lower().startswith('x')]
            org = next((d[h] for h in hdr if h.startswith('Org')), '')
            cases[cells[0]] = dict(org=org, region=d.get('Region', d.get('Country', '')), themes=th, file=os.path.basename(f))
        elif hdr and not line.startswith('|'):
            hdr = None
json.dump(cases, open(os.path.join(R, 'case_index.json'), 'w'), indent=1)
by = collections.defaultdict(list)
for k, v in cases.items():
    for t in v['themes']:
        by[t].append(k)
print(len(cases), 'cases')
for t in sorted(by, key=lambda x: (x != 'PEOPLE', int(x[1:]) if x != 'PEOPLE' else 0)):
    print(t, len(by[t]))
