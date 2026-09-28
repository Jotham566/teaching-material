"""Validate fixed, attributed sector inputs without any network access."""
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def verify(folder=None):
 folder=Path(folder or ROOT/'DataAnalysis_Track/data/sector_snapshots')
 manifest=json.loads((folder/'manifest.json').read_text())
 for row in manifest['files']:
  if Path(row['file']).name!=row['file']:raise ValueError('Invalid snapshot filename')
  raw=(folder/row['file']).read_bytes()
  if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Snapshot changed: '+row['file'])
 counts={}
 for name,delimiter,expected in [('bank-full.csv',';',45211),('ai4i2020.csv',',',10000),('uganda_gdp_2000_2023.csv',',',24)]:
  with (folder/name).open(newline='') as f:rows=list(csv.DictReader(f,delimiter=delimiter))
  if len(rows)!=expected:raise ValueError('Wrong snapshot variant: '+name)
  counts[name]=len(rows)
  if name.startswith('uganda'):
   if [int(r['year']) for r in rows]!=list(range(2000,2024)) or {r['country_code'] for r in rows}!={'UGA'}:raise ValueError('Wrong Uganda population/window')
 return counts
if __name__=='__main__':print('Verified local sector snapshots:',verify())
