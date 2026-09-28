"""Create the complete small Week 2 student kit and its private solution key."""
import csv
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'IUEA_Teaching_Plan/setup'


def notebook(cells):
    return {'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},
      'cells':[dict(cell_type=kind,metadata={},source=text.splitlines(True),**({'outputs':[],'execution_count':None} if kind=='code' else {})) for kind,text in cells]}


def main():
    OUT.mkdir(exist_ok=True)
    datasets={'CML3112':('site_inspection_log.csv','crack_width_mm',[0.12,0.25,0.31,0.18]),
              'CML3113':('drill_shift_log.csv','depth_m',[100,110,121,133]),
              'CML3111':('motor_test_bench.csv','current_a',[4.0,4.5,5.0,5.5])}
    for code,(filename,column,values) in datasets.items():
        dest=OUT/code;dest.mkdir(exist_ok=True)
        with (dest/filename).open('w') as f:
            w=csv.writer(f);w.writerow(['reading_id',column]);w.writerows(enumerate(values,1))
        cells=[('markdown',f'# Week 2 proof of life\n{code}. Set STUDENT_ID to your Student Registration Number, including slashes (fictional example only: 99/TEST/000/DEMO-X). Run cells in order.\n'),
               ('code',f'STUDENT_ID = "YOUR_ID"\nCOHORT = "{code}"\n'),
               ('code',f'print("Hello from {code}")\nproof_sum = 2 + 2\nprint(proof_sum)\n'),
               ('code','readings = 12\n'),('code','readings = readings + 5\nprint(readings)\n'),
               ('markdown','Run the previous cell three times. Explain the changing result below, then restart and run all.\n'),
               ('markdown','My explanation: ...\n'),
               ('code',f'import csv\nwith open("{filename}", newline="") as f:\n    rows = list(csv.DictReader(f))\nprint(len(rows))\n'),
               ('markdown','After Restart and Run All, expected outputs include 4, 17 and 4 rows. Save with slashes replaced by underscores in the filename only, for example 99_TEST_000_DEMO-X_W02.ipynb.\n')]
        (dest/'proof_of_life.ipynb').write_text(json.dumps(notebook(cells),indent=2))
        broken=[('01_missing_module','import course_package_not_installed\n','ModuleNotFoundError: remove the intentionally unavailable import; csv is in Python itself.'),
                ('02_wrong_runtime','import sys\nassert sys.version_info.major == 2, "Notebook expects Python 2, but the course uses Python 3"\n','Change the version expectation to 3 and select a Python 3 runtime.'),
                ('03_wrong_path',f'with open("missing_folder/{filename}") as f:\n    print(f.readline())\n',f'Upload {filename} and use its actual relative path.'),
                ('04_hidden_state','readings = 12\nreadings = readings + 5\nreadings = 12\nprint(readings)  # expected fresh-run result: 17\n','The final initialization erases the increment. Initialize only before adding five, then restart and run all.')]
        for name,source,answer in broken:
            (dest/(name+'.ipynb')).write_text(json.dumps(notebook([('markdown','# Break and fix\nPredict the error, run it, explain its cause and repair it.\n'),('code',source)]),indent=2))
        (dest/'hello_engineering.py').write_text(f'print("Hello from {code}")\nprint("Four readings are available in {filename}")\n')
        (dest/'README.md').write_text(f'# {code} Week 2\n\nUpload proof_of_life.ipynb and {filename} into Colab. The four numbered notebooks deliberately fail. Diagnose and repair them; do not submit the broken originals. The dataset is a fictional four-row practice fixture, not an engineering benchmark.\n')
        with zipfile.ZipFile(OUT/(code+'_Week02.zip'),'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(dest.iterdir()):z.write(p,code+'/'+p.name)
    private=ROOT/'IUEA_Teaching_Plan/grader/week2_solution_key.md'
    private.write_text((ROOT/'IUEA_Teaching_Plan/grader/Week2_Repair_Walkthrough.md').read_text())

if __name__=='__main__':main()
