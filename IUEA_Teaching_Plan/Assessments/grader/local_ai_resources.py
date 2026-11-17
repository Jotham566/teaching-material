"""Keep Docker Desktop out of the macOS local-AI grading phase."""
import shutil
import subprocess
import sys
import time


def desktop_running():
    result = subprocess.run(['/bin/ps', '-axo', 'comm='], capture_output=True,
                            text=True, timeout=5, check=True)
    names = {'Docker', 'Docker Desktop', 'com.docker.backend', 'com.docker.virtualization'}
    return any(line.strip().rsplit('/', 1)[-1] in names for line in result.stdout.splitlines())


def ensure_docker_stopped():
    """Stop local Desktop gracefully, or refuse inference; never stop a remote daemon."""
    if sys.platform != 'darwin':
        return
    if not desktop_running():
        return
    print('Stopping Docker Desktop before local AI inference...', flush=True)
    docker = shutil.which('docker')
    if not docker:
        raise RuntimeError('Quit Docker Desktop before written grading; docker CLI is unavailable.')
    try:
        subprocess.run([docker, 'desktop', 'stop', '--timeout', '30'],
                       capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        pass  # A final process check determines whether shutdown completed.
    for _ in range(10):
        if not desktop_running():
            return
        time.sleep(1)
    raise RuntimeError('Docker Desktop is still running. Quit it and retry. Local AI grading was not started.')


if __name__ == '__main__':
    ensure_docker_stopped()
    print('Docker resource check passed.')
