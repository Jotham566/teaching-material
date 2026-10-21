import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import local_ai_resources as resources


class LocalAIResourcesTests(unittest.TestCase):
    def test_process_detection(self):
        with patch.object(resources.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0,
                '/Applications/Docker.app/Contents/MacOS/com.docker.backend\n')):
            self.assertTrue(resources.desktop_running())
        with patch.object(resources.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0,
                '/usr/bin/python3\n/Library/PrivilegedHelperTools/com.docker.vmnetd\n')):
            self.assertFalse(resources.desktop_running())

    @patch.object(resources.sys, 'platform', 'darwin')
    def test_already_stopped_does_not_start_or_stop_anything(self):
        with patch.object(resources, 'desktop_running', return_value=False), patch.object(resources.subprocess, 'run') as run:
            resources.ensure_docker_stopped()
            run.assert_not_called()

    @patch.object(resources.sys, 'platform', 'darwin')
    def test_stop_then_verify(self):
        with patch.object(resources, 'desktop_running', side_effect=[True, False]), \
             patch.object(resources.shutil, 'which', return_value='/usr/local/bin/docker'), \
             patch.object(resources.subprocess, 'run') as run:
            resources.ensure_docker_stopped()
            self.assertEqual(run.call_args.args[0], ['/usr/local/bin/docker','desktop','stop','--timeout','30'])

    @patch.object(resources.sys, 'platform', 'darwin')
    def test_shutdown_failure_blocks_grading(self):
        with patch.object(resources, 'desktop_running', return_value=True), \
             patch.object(resources.shutil, 'which', return_value='docker'), \
             patch.object(resources.subprocess, 'run', side_effect=subprocess.TimeoutExpired('docker',35)), \
             patch.object(resources.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'still running'):
                resources.ensure_docker_stopped()

    @patch.object(resources.sys, 'platform', 'darwin')
    def test_missing_cli_blocks_grading(self):
        with patch.object(resources, 'desktop_running', return_value=True), patch.object(resources.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'CLI is unavailable'):
                resources.ensure_docker_stopped()
