"""Expand one graded team submission to its registered members.
Membership CSV: team_id,student_id. Grade CSV: team_id,status,score,maximum.
Individual contribution/viva components remain individual; this only expands
the shared project mark, once, avoiding repeated grading of the same report.
"""
import argparse,csv

def expand(members,grades):
    seen=set();teams={}
    for row in members:
        sid=row['student_id'].strip().upper();team=row['team_id'].strip()
        if not sid or not team or sid in seen:raise ValueError('Missing/duplicate team membership '+sid)
        seen.add(sid);teams.setdefault(team,[]).append(sid)
    out=[];graded=set()
    for row in grades:
        team=row['team_id'].strip()
        if team not in teams or team in graded:raise ValueError('Unknown/duplicate graded team '+team)
        graded.add(team)
        for sid in teams[team]:out.append(dict(student_id=sid,status=row['status'],score=row['score'],maximum=row['maximum']))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ('members','grades','out'):ap.add_argument('--'+name,required=True)
    args=ap.parse_args();rows=expand(list(csv.DictReader(open(args.members))),list(csv.DictReader(open(args.grades))))
    with open(args.out,'w') as f:
        w=csv.DictWriter(f,fieldnames=['student_id','status','score','maximum']);w.writeheader();w.writerows(rows)
