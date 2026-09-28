from schools_camp_content import ROOT
import shutil,zipfile,json
for code in ['ML','DA']:
 folder=ROOT/'student_materials'/code
 start=(ROOT/'teaching/START_HERE.md').read_text()
 if code=='DA':
  start=start.replace('ML adds F01 after ML03, F02 after ML06, F03 after ML09 and F04 after ML12; see FOUNDATION_LABS.md. These are taught labs on a fourth day in weeks 1–4. Both tracks otherwise have three classes per week.','Your Data Analysis track has three core classes per week. The extra foundation labs belong to the Machine Learning track only.')
 (folder/'START_HERE.md').write_text(start)
 shutil.copy2(ROOT/'teaching/ASSESSMENT_AND_SHOWCASE.md',folder/'ASSESSMENT_AND_SHOWCASE.md')
 shutil.copy2(ROOT/'teaching/MODERN_AI_ORIENTATION.md',folder/'MODERN_AI_ORIENTATION.md')
 for policy_file in ['AI_USE_POLICY.md','AI_CODING_ASSISTANTS_LAB.md','PROJECT_RUBRIC.md']:
  shutil.copy2(ROOT/'teaching'/policy_file,folder/policy_file)
 shutil.copy2(ROOT/'operations/requirements-tested.txt',folder/'requirements-tested.txt')
 # Prevent an irrelevant earlier build artifact from being included.
 extras=[p for p in folder.glob('*.sqlite')] if code=='ML' else []
 for p in extras:p.unlink()
 with zipfile.ZipFile(ROOT/f'{code}_Beginner_Student_Pack.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(folder.rglob('*')):
   if p.is_file():z.write(p,code+'/'+str(p.relative_to(folder)))
 with zipfile.ZipFile(ROOT/f'{code}_Beginner_Student_Pack.zip') as z:
  assert not any('instructor' in n or 'reference_values' in n or 'guide.md' in n for n in z.namelist())
  assert f'{code}/START_HERE.md' in z.namelist()
  assert len([n for n in z.namelist() if n.endswith('.md') and n.split('/')[-1][:2]==code and n.split('/')[-1][2:4].isdigit()])==24
  if code=='ML':
   assert all(f'ML/F{i:02}.ipynb' in z.namelist() and f'ML/F{i:02}.md' in z.namelist() for i in range(1,5))
  print(code,len(z.namelist()),'student-only files')
