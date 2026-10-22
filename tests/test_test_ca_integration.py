"""Synthetic test-to-CA publication checks; no student data or code execution."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import refresh_ca as r
from integrate_test_marks import integrate


def test_row(rid='test1', score=80, assessment='TEST1', **changes):
    row=dict(response_id=rid,cohort='CML3111',assessment=assessment,
             student_registration_number='SYNTHETIC-ONLY',email='test@example.test',
             full_name='Synthetic Student',submitted_at='2026-10-22T09:00:00Z',
             maximum=100,score=score,status='GRADED')
    row.update(changes)
    return row


def render(batch):
    (batch/r.BOOK).write_bytes(b'synthetic workbook')


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.private=Path(self.temp.name).resolve()/'private';self.private.mkdir()
        old=dict(cohort='CML3111',assessment='W03',student_id='SYNTHETIC-ONLY',
                 submitted_student_id='SYNTHETIC-ONLY',email='test@example.test',full_name='Synthetic Student',
                 response_id='assignment',submitted_at='2026-10-01T09:00:00Z',timing_status='ON_TIME',
                 status='GRADED',score=17,maximum=20,file_ids=[],source='synthetic')
        r.write(self.private/'ledger.json',{'attempts':[old],'sources':[]})
        (self.private/r.BOOK).write_bytes(b'original workbook')
        r.write(self.private/'reconciled/timing.json',{'assignment':{'status':'ON_TIME','evidence':'fixture'}})
        r.write(self.private/'written_queue/combined_results.json',[{'response_id':'assignment'}])
        self.input=self.private.parent/'test.json'

    def run_import(self, rows, renderer=render):
        r.write(self.input,{'attempts':rows})
        return integrate(self.input,self.private,renderer)

    def test_incremental_repeat_and_coursework_context(self):
        first=self.run_import([test_row()])
        self.assertEqual(first,self.run_import([test_row()]))
        second=self.run_import([test_row(),test_row('test2',70,'TEST2')])
        data=r.read(second/'ledger.json')
        self.assertEqual(len(data['attempts']),3)
        self.assertEqual({x['response_id']:x['score'] for x in data['current']},
                         {'assignment':17,'test1':80,'test2':70})
        self.assertEqual(r.active_base(self.private),second)
        self.assertEqual(r.read(first/'reconciled/timing.json'),r.read(second/'reconciled/timing.json'))
        self.assertEqual(r.read(first/'written_queue/combined_results.json'),r.read(second/'written_queue/combined_results.json'))
        # A partial later export cannot erase previous test attempts.
        last=self.run_import([test_row('test2',70,'TEST2')])
        self.assertEqual(len(r.read(last/'ledger.json')['attempts']),3)

    def test_new_pending_attempt_and_rehearsal(self):
        self.run_import([test_row()])
        result=self.run_import([test_row('later',None,status='GRADER_EXCEPTION',submitted_at='2026-10-23T09:00:00Z'),
                                test_row('rehearsal',status='REHEARSAL')])
        data=r.read(result/'ledger.json')
        current=next(x for x in data['current'] if x['assessment']=='TEST1')
        self.assertIsNone(current['score']);self.assertEqual(current['status'],'GRADER_EXCEPTION')
        self.assertEqual(len(data['attempts']),3)

    def test_conflict_and_render_failure_preserve_published_work(self):
        self.run_import([test_row()])
        before=(self.private/'ledger.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'identity changed'):
            self.run_import([test_row(email='different@example.test')])
        def fail(_): raise RuntimeError('render failed')
        with self.assertRaisesRegex(RuntimeError,'render failed'):
            self.run_import([test_row('test2',70,'TEST2')],fail)
        self.assertEqual(before,(self.private/'ledger.json').read_bytes())
        self.run_import([test_row('test2',70,'TEST2')])
        self.assertEqual(len(r.read(self.private/'ledger.json')['attempts']),3)

    def test_duplicates_and_invalid_scores_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            self.run_import([test_row(),test_row()])
        with self.assertRaisesRegex(ValueError,'Invalid completed'):
            self.run_import([test_row(score=110)])
        self.assertEqual((self.private/r.BOOK).read_bytes(),b'original workbook')

    def test_unfinished_weekly_batch_must_finish_first(self):
        r.write(self.private/'batches/weekly/parent.json', {})
        r.write(self.private/'batches/weekly/status.json', {'state':'STOPPED'})
        with self.assertRaisesRegex(ValueError,'unfinished weekly'):
            self.run_import([test_row()])

    def test_command_wires_saved_results_to_cumulative_update(self):
        import grade_test_batch as command
        output=self.private.parent/'tests';output.mkdir()
        r.write(output/'workbook_data.json',{'attempts':[test_row()]})
        def build_test_book(args, **kwargs):
            if len(args)>1 and str(args[1]).endswith('build_test_marks.mjs'):
                (output/'Test_Marks.xlsx').write_bytes(b'test workbook')
        with patch.object(sys,'argv',['grade_test_batch.py','synthetic.zip','--out',str(output),'--ca-private',str(self.private)]), \
             patch.object(command,'grade_batch',return_value=output), \
             patch.object(command.subprocess,'check_output',return_value=''), \
             patch.object(command.subprocess,'run',side_effect=build_test_book), \
             patch('integrate_test_marks.integrate_locked') as wired:
            command.main()
        wired.assert_called_once_with(output/'workbook_data.json',self.private)

    def test_excel_open_stops_without_change(self):
        (self.private/('~$'+r.BOOK)).touch()
        with self.assertRaisesRegex(ValueError,'Close the cumulative'):
            self.run_import([test_row()])

if __name__=='__main__':unittest.main()
