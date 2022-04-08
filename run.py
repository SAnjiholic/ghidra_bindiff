import os, sys, hashlib, subprocess
from pathlib import Path

from config import *
from binexport_automation import *

if not os.path.isdir(BASE_DIR):
    os.mkdir(BASE_DIR)
if not os.path.isdir(BINDIFF_EXPORT_PATH):
    os.mkdir(BINDIFF_EXPORT_PATH)
if not os.path.isdir(GHIDRA_FUNCTION_DATA_PATH):
    os.mkdir(GHIDRA_FUNCTION_DATA_PATH)
if not os.path.isdir(GHIDRA_LOG):
    os.mkdir(GHIDRA_LOG)
    

def binExport(filepath):
    md5 = hashlib.md5(open(filepath,'rb').read()).hexdigest()
    path = Path(BINDIFF_EXPORT_PATH, md5+".BinExport")
    if os.path.isfile(path):
        print (f"already binExport file : {md5}")
        return path

    else:
        cmd = [GHIDRA_PATH, 
            './output', 
            GHIDRA_TEMP_PROJECT_NAME,
            '-import',
            filepath,
            '-deleteProject',
            '-analysisTimeoutPerFile',
            GHIDRA_TIMEOUT,
            '-scriptPath',
            './',
            '-postScript',
            f'./{GHIDRA_SCRIPT_NAME}',
            '-scriptlog',
            GHIDRA_LOG]

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        print (f"success binExport: {md5}")
        return path

if __name__ == "__main__":
    if not GHIDRA_PATH or not os.path.isfile(GHIDRA_PATH):
        print ("Error: ghidra not found")   
        sys.exit(1)
    if len(sys.argv) == 3:         
        if not os.path.isfile(sys.argv[1]):
            print (f"Error: file not found - {sys.argv[1]}")
            sys.exit(1)
        elif not os.path.isfile(sys.argv[2]):
            print (f"Error: file not found - {sys.argv[2]}")
            sys.exit(1)
        else:
            file1 = binExport(sys.argv[1])
            file2 = binExport(sys.argv[2])
            diffing(file1.as_posix(), file2.as_posix())
            
    else:
        print (f"USAGE: python run.py binary1_path, binary2_path")
        sys.exit(1)
        