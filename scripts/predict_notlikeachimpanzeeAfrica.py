import os
import shutil
import subprocess
from tqdm import tqdm

import os
import shutil
import subprocess
from tqdm import tqdm

all_inputs_dir = "/home/wojcikbart/wb/tumor-segmentation/brats_data/BraTSafrica/all_inputs"
input_dir = "/home/wojcikbart/wb/tumor-segmentation/brats_data/BraTSafrica/input"
output_dir = "/home/wojcikbart/wb/tumor-segmentation/brats_data/BraTSafrica/output"


ids = []
for file in os.listdir(all_inputs_dir):
    id = file.split("_")[1]
    if id not in ids:
        ids.append(id)
ids.sort()
    
def clear_dir(input_dir):
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

clear_dir(input_dir)
iterator = tqdm(ids, bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[32m", "\033[0m"), ncols=80)
for id in iterator:
    files = [file for file in os.listdir(all_inputs_dir) if id in file]
    for file in files:
        shutil.copy2(os.path.join(all_inputs_dir, file), os.path.join(input_dir, file))
    
    # Run Docker inference
    subprocess.run([
    "docker", "run", "--rm", "--gpus", "all",
    "-v", f"{input_dir}:/input",
    "-v", f"{output_dir}:/output",
    "rixez/brats21nnunet"
])

ids = []
for file in os.listdir(all_inputs_dir):
    id = file.split("_")[1]
    if id not in ids:
        ids.append(id)
ids.sort()
    
def clear_dir(input_dir):
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

clear_dir(input_dir)
iterator = tqdm(ids, bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[32m", "\033[0m"), ncols=80)
for id in iterator:
    files = [file for file in os.listdir(all_inputs_dir) if id in file]
    for file in files:
        shutil.copy2(os.path.join(all_inputs_dir, file), os.path.join(input_dir, file))
    
    # Run Docker inference
    subprocess.run([
        "docker", "run", "-it", "--rm", "--gpus", "device=0",
        "--name", "nnunet",
        "-v", f"{input_dir}:/input",
        "-v", f"{output_dir}:/output",
        "rixez/brats21nnunet"
    ])
    clear_dir(input_dir)


