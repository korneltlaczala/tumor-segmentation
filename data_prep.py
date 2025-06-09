import os
import shutil

def create_dirs(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def get_id(fname):
    return int(fname.split("_")[1])


def prep_data(data_dir, input_dir="input", output_dir="output", id_range=range(0, 4)):
    create_dirs([input_dir, output_dir])

    for root, _, files in os.walk(data_dir):
        for file in files:
            if not file.endswith(".nii.gz"):
                continue
            id = get_id(file)
            if not id in id_range:
                continue
            

            if file.endswith("seg.nii.gz") and not os.path.exists(os.path.join(output_dir, file)):
                shutil.copy2(os.path.join(root, file), os.path.join(output_dir, file))

            elif not os.path.exists(os.path.join(input_dir, file)):
                shutil.copy2(os.path.join(root, file), os.path.join(input_dir, file))



if __name__ == "__main__":
    prep_data("archive", id_range=range(0, 4))