"""Explicitly retrieve attributed snapshots; refuse changed existing data."""
from pathlib import Path
import urllib.request,json,zipfile,io,csv,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'DataAnalysis_Track/data/sector_snapshots';out.mkdir(exist_ok=True)
manifest=[]
def fetch(url):
 with urllib.request.urlopen(url,timeout=60) as response:data=response.read(20_000_001)
 if len(data)>20_000_000:raise ValueError('Oversized download')
 return data
def save(name,data,source,notes):
 p=out/name
 if p.exists() and p.read_bytes()!=data:raise ValueError('Existing snapshot changed; explicitly version it')
 p.write_bytes(data);manifest.append(dict(file=name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),source=source,notes=notes))
u='https://archive.ics.uci.edu/static/public/222/bank%2Bmarketing.zip'
z=zipfile.ZipFile(io.BytesIO(fetch(u)));inner=zipfile.ZipFile(io.BytesIO(z.read('bank.zip')))
for name in ('bank-full.csv','bank-names.txt'):save(name,inner.read(name),u,'Unmodified member of bank.zip; older full variant, not bank-additional-full.csv. CC BY 4.0; Moro, Rita and Cortez, UCI DOI 10.24432/C5K306.')
u='https://archive.ics.uci.edu/static/public/601/ai4i%2B2020%2Bpredictive%2Bmaintenance%2Bdataset.zip'
z=zipfile.ZipFile(io.BytesIO(fetch(u)));save('ai4i2020.csv',z.read('ai4i2020.csv'),u,'Unmodified original synthetic dataset. CC BY 4.0; AI4I 2020, UCI DOI 10.24432/C5HS5C. Not measured Ugandan machinery data.')
u='https://api.worldbank.org/v2/country/UG/indicator/NY.GDP.MKTP.CD?format=json&date=2000:2023&per_page=100'
data=fetch(u);payload=json.loads(data);assert isinstance(payload,list) and len(payload)==2 and payload[0]['pages']==1
assert len(payload[1])==24 and {r['countryiso3code'] for r in payload[1]}=={'UGA'}
save('uganda_gdp_2000_2023.source.json',data,u,'Unmodified API response, including update metadata and nulls; current-US-dollar GDP, not real growth or household income.')
s=io.StringIO(newline='');w=csv.writer(s);w.writerow(['country_code','year','gdp_current_usd'])
for r in sorted(payload[1],key=lambda r:r['date']):w.writerow([r['countryiso3code'],r['date'],'' if r['value'] is None else r['value']])
save('uganda_gdp_2000_2023.csv',s.getvalue().encode(),u,'Derived by selecting country ISO3, year and value, sorting ascending year, preserving null as blank; no imputation. World Bank WDI; CC BY 4.0 with World Bank additional terms.')
(out/'manifest.json').write_text(json.dumps(dict(retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=manifest),indent=2)+'\n')
print(json.dumps(manifest,indent=2))
