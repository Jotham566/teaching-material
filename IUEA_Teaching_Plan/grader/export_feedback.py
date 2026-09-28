"""Create private, self-contained student feedback pages from completed grading.

Writes local files only. It does not email, publish or change Google permissions.
Do not share the whole output folder with a class: each page is individual.
"""
import argparse,csv,html,json
from pathlib import Path
from urllib.parse import quote

def page(sid,result,rubric):
    esc=lambda value:html.escape(str(value),quote=True)
    complete=result.get('status')=='AUTO_SCORED' and result.get('score') is not None
    heading=f"{result['score']:g} / {result['maximum']:g}" if complete else 'Result pending — no final mark'
    title=rubric.get('title',rubric['id']);rows=[]
    evaluations=result.get('evaluations',[])
    if len(evaluations)==2:
        marked=[{c['id']:c for c in e['criteria']} for e in evaluations]
        gates={g['parent_criterion'] for g in result.get('execution_gate_adjustments',[])}
        for criterion in rubric['criteria']:
            cid=criterion['id']
            if any(cid not in m for m in marked):continue
            score=sum(float(m[cid]['awarded']) for m in marked)/2
            if criterion.get('parent_criterion',cid) in gates:score=0
            shown=f'{score:g} / {criterion["maximum"]:g}' if complete else 'Pending'
            feedback=marked[0][cid].get('feedback','') if complete else 'A final criterion result has not been issued.'
            rows.append(f'<tr><th scope="row">{esc(criterion["title"])}</th><td>{esc(shown)}</td><td>{esc(feedback)}</td></tr>')
    notice='Your submitted work was checked against the assessment rubric.' if complete else 'The submitted work could not receive a complete automatic result. This is not a zero. Keep your original files; any resubmission follows the lecturer’s instructions.'
    numerical=result.get('deterministic')
    component=f'<p>Executed checks: {esc(numerical["notebook_total"])} / {esc(numerical["max_total"])}.</p>' if numerical and complete else ''
    adjustments=''.join('<li>'+esc(g['reason'])+'</li>' for g in result.get('execution_gate_adjustments',[]))
    adjustment_note='<p>Applied assessment requirements:</p><ul>'+adjustments+'</ul>' if adjustments else ''
    table='<div class="scroll"><table><thead><tr><th>Written criterion</th><th>Mark</th><th>Feedback</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>' if rows else ''
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — individual feedback</title><style>body{{font:17px/1.55 system-ui,sans-serif;margin:0;background:#f3f6fa;color:#162539}}main{{max-width:900px;margin:32px auto;padding:28px;background:white;border-radius:12px}}h1{{font-size:1.65rem}}.score{{font-size:1.5rem;font-weight:700}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #cbd5e1;vertical-align:top}}thead{{background:#edf2f7}}footer{{font-size:.85rem;color:#475569;margin-top:24px}}@media(max-width:600px){{main{{margin:0;padding:18px;border-radius:0}}th,td{{padding:8px}}}}</style><main><h1>{esc(title)}</h1><p>Student Registration Number / learner ID: <strong>{esc(sid)}</strong></p><p class="score">{esc(heading)}</p><p>{esc(notice)}</p>{component}{adjustment_note}{table}<footer>Individual feedback · rubric {esc(rubric['id'])}. Share this page only with the named learner. Keep the grading record if requesting a result check.</footer></main></html>'''

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('results','rubric','out'):p.add_argument('--'+name,required=True)
    a=p.parse_args();source=Path(a.results);rubric=json.loads(Path(a.rubric).read_text());out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=list(csv.DictReader((source/'results.csv').open()));seen=set()
    for row in rows:
        sid=row['student_id']
        if not sid or sid in seen:raise ValueError('Missing or duplicate feedback identity')
        seen.add(sid);encoded=quote(sid,safe='')
        result=json.loads((source/(encoded+'.json')).read_text())
        (out/(encoded+'.html')).write_text(page(sid,result,rubric))
    print(len(rows),'private feedback pages written; nothing sent or published')
if __name__=='__main__':main()
