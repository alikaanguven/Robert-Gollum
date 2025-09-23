from subprocess import run, PIPE
import re
import json
import os
import glob

import inspect

def print_info():
    # Get the caller's local variables
    caller_locals = inspect.currentframe().f_back.f_locals

    # Define which variables to print and how to label them
    keys = {
        's_type':  's_type',
        'json_db': 'json',
        'tier':    'tier',
        'year':    'year',
        'outDir':  'outDir',
        'config':  'config'
    }
    print()
    for key, label in keys.items():
        if key in caller_locals:
            # For 'json_db' and 'tier', assume you want to use the key from 's_type'
            if key in ['json_db', 'tier'] and 's_type' in caller_locals:
                value = caller_locals[key][caller_locals['s_type']]
            else:
                value = caller_locals[key]
            print(f'INFO:    {label}: {value}')
    print('-' * 80)
    print()

input_dict = {
    "TT2lUnbinned_2016": "/scratch-cbe/users/robert.schoefbeck/TT2lUnbinned/nanoTuples/TT2lUnbinned_v7/UL2016/dilep/TTLep_pow_CP5"
}



autoplotter_path = "$CMSSW_BASE/src/Plotter/autoplotter.py"
config           = "$CMSSW_BASE/src/Plotter/configs/gluon2.yaml"
unique_dir       = "test4"

work_dir = os.path.join("/scratch-cbe/users/alikaan.gueven/Gollum/plots")
outBaseDir = os.path.join(work_dir, str(unique_dir))

files_per_job = 2

samples_to_plot = []

isData = False


for sampleName, sampleDir in input_dict.items():
    job_dict = {}
    outDir = os.path.join(outBaseDir, sampleName)
    fileListDir = os.path.join(outDir, 'fileList')
    os.makedirs(outDir, exist_ok=True)
    os.makedirs(fileListDir, exist_ok=True)
    print_info()


    # all about getting file_paths to text file.
    # ------------------------------------------------------------

    files = glob.glob(sampleDir + "/**/*.root", recursive=True)
    print("Reading ", sampleDir)
    len_files = len(files)
    chunks = [files[i:i+files_per_job] for i in range(0, len(files), files_per_job)]
    for i, chunk in enumerate(chunks):
        fileList_path = os.path.join(fileListDir, f"{sampleName}_{i}.txt")
        with open(fileList_path, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk) + "\n")
    # ------------------------------------------------------------
        if isData:
            command = f'submit_to_cpu_rapid.sh "python3 -u {autoplotter_path} --name {sampleName} --filelist {fileList_path} --postfix {i} --output {outDir} --config {config} --data"'
        else:
            command = f'submit_to_cpu_rapid.sh "python3 -u {autoplotter_path} --name {sampleName} --filelist {fileList_path} --postfix {i} --output {outDir} --config {config}"'

        result = run(f'sbatch {command}', shell=True, capture_output = True, text = True)
        job_id = re.search("\d+", result.stdout).group()    # Get the number with '\d+'
        info_dict = {'command': f'sbatch {command}',        # Save command [important for resubmitting]
                    'jobid':   job_id}                      # Save job_id  [identify the status with sacct]
        job_dict[f'{sampleName}_{i}'] = info_dict           # Add to dict
        print(result.stdout[:-1])
    
    out_json_path = os.path.join(outDir, 'job_ids.json')
    print(f"\nWriting to {out_json_path}...\n")
    with open(out_json_path, 'w') as f:
        json.dump(job_dict, f, indent=2)

print('\nFinished. Exiting...')