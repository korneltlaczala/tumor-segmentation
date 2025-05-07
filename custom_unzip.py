import os
import shutil

original_folder = "archive"
target_folder = "input"


def extract_files(ext, original_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, _, files in os.walk(original_folder):
        for file in files:
            if file.endswith(ext):
                if not os.path.exists(os.path.join(target_folder, file)):
                    shutil.copy2(os.path.join(root, file), os.path.join(target_folder, file))


def remove_files(ext, target_folder):
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file.endswith(ext):
                os.remove(os.path.join(root, file))

def rename_files(base, mapping):
    for fname in os.listdir(base):
        for old_suffix, new_suffix in mapping.items():
            if fname.endswith(old_suffix):
                new_name = fname.replace(old_suffix, new_suffix)
                print(f"{fname} → {new_name}")
                os.rename(os.path.join(base, fname), os.path.join(base, new_name))

if __name__ == "__main__":

    mapping = {
        "_t1.nii.gz": "_0000.nii.gz",
        "_t1ce.nii.gz": "_0001.nii.gz",
        "_t2.nii.gz": "_0002.nii.gz",
        "_flair.nii.gz": "_0003.nii.gz",
    }

    # extract_files(".nii.gz", original_folder, target_folder)
    # remove_files("seg.nii.gz", "input2")
    rename_files("input2", mapping)