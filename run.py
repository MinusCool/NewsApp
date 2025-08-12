import subprocess
import sys
import os

backend_dir = os.path.join(os.getcwd(), 'backend/app')
# frontend_dir = os.path.join(os.getcwd(), 'frontend', 'newsApp')

backend_cmd = ['uvicorn', 'main:app', '--reload']
# frontend_cmd = ['npm', 'run', 'dev']

backend_process = subprocess.Popen(backend_cmd, cwd=backend_dir)
# frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir, shell=True)

try:
    backend_process.wait()
    # frontend_process.wait()
except KeyboardInterrupt:
    backend_process.terminate()
    # frontend_process.terminate()
    print("Processes terminated.")
finally:
    backend_process.kill()
    # frontend_process.kill()
    print("All processes killed.")