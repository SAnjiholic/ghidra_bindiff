import sqlite3
import pandas as pd
import glob
import subprocess, os
import glob
from pathlib import Path

from config import *

def make_pairs(files):
    originals = [file for file in files if "_patched" not in file]
    patched = [(file.replace('.BinExport', '_patched.BinExport')) for file in originals]
    pairs = dict(zip(originals, patched))
    return pairs

def make_bindiff(original, patched):
    output_dir = BASE_DIR
    output_name = f'{os.path.basename(original).replace(".BinExport","")}_vs_{os.path.basename(patched).replace(".BinExport","")}.BinDiff'
    full_path = Path(output_dir, output_name)
    cmd = [BINDIFF_PATH, original, patched, '--output_dir='+ output_dir]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    return full_path

def bindiff_to_csv(bindiff_diff):
    try:        
        db = sqlite3.connect(bindiff_diff)
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        fun_table = tables[4]
        table = pd.read_sql_query("SELECT * from %s" % fun_table, db)

        name = Path(BASE_DIR, os.path.basename(bindiff_diff) + '_funtable.csv')
        table.to_csv(name, index_label='index')
        cursor.close()
        db.close()
        Path(bindiff_diff).unlink()
        return name
    except:
        return 'error'

def get_fcn(name_sample_addr):
    try:
        index = fun_df.index[fun_df['sample_name_addr'] == name_sample_addr].tolist()[0]
        fun_name = fun_df.iloc[index]['fun_name']
    except:
        fun_name='not_found'
    return fun_name

def coorelate_fun_names(table_path):
    bindiff_df = pd.read_csv(table_path, index_col=[0])
    name = list(os.path.basename(table_path).replace('_funtable.csv','').replace('.BinDiff','').split('_vs_'))
    bindiff_df['original_sample'] = name[0]
    bindiff_df['patched_sample'] = name[1].replace('_funtable.csv', '')

    bindiff_df['original_sample_addr'] = bindiff_df['original_sample'] + '_' + bindiff_df['address1'].apply(str)
    bindiff_df['patched_sample_addr'] = bindiff_df['patched_sample'] + '_' + bindiff_df['address2'].apply(str)

    bindiff_df['orig_fun_name'] = bindiff_df['original_sample_addr'].apply(lambda x: get_fcn(x))
    bindiff_df['patched_fun_name'] = bindiff_df['patched_sample_addr'].apply(lambda x: get_fcn(x))

    csv_name =  BASE_DIR + os.path.basename(table_path).replace('.BinDiff','').replace('_funtable.csv','') + '_finaldf.csv'
    bindiff_df.to_csv(csv_name)
    Path(table_path).unlink()
    return bindiff_df

def collect_dfs(base_dir):
    dfs = []
    for fp in glob.glob(base_dir+ '*_finaldf.csv'):
        dfs.append(pd.read_csv(fp, index_col=[0]))
        Path(fp).unlink()
    return dfs

def diffing(file1, file2):    
    fun_df = pd.read_csv(Path(GHIDRA_FUNCTION_DATA_PATH, 'sample_functions_addresses.csv'))
    fun_df.columns = ['path', 'fun_name', 'addr']
    fun_df['name'] = fun_df['path'].apply(lambda x: x.split('/')[-1])
    fun_df['sample_name_addr'] = fun_df['name'] + '_' + fun_df['addr'].apply(str)
    
    pairs = {file1:file2}
    bindiffs = [make_bindiff(k, v) for k, v in pairs.items()]
    bindiff_fcn_paths = [bindiff_to_csv(bindiff) for bindiff in bindiffs]
    final_dfs = [coorelate_fun_names(bindiff_fcn_path) for bindiff_fcn_path in bindiff_fcn_paths if bindiff_fcn_path != 'error']
    frames = collect_dfs(BASE_DIR)
    final_combined_path = Path(BASE_DIR , 'final_combined.csv')
    if os.path.isfile(final_combined_path):
        final_combined_path.unlink()

    final_combined = pd.concat(frames, axis=0)
    final_combined.query('similarity < 1.0')
    final_combined.to_csv(Path(BASE_DIR , 'final_combined.csv'))
    print (f"combined output: {Path(BASE_DIR , 'final_combined.csv').as_posix()}")