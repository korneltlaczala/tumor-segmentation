import os
import shutil
import random
from util import load_allowed_ids

MODALITY_SUFFIXES = {
    "flair": "0000",
    "t1": "0001",
    "t1ce": "0002",
    "t2": "0003",
}

def create_dirs(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def get_id(fname):
    # Przykład: BraTS-GLI-00000-000_flair.nii.gz
    # Chcemy wyciągnąć numer pacjenta: 0 (dla 00000)
    # Możemy rozbić po '-' i wziąć trzeci element, który jest '00000', a następnie zamienić na int
    try:
        base = fname.split("_")[0]  # np. 'BraTS-GLI-00000-000'
        patient_num_str = base.split("-")[2]  # '00000'
        return int(patient_num_str)
    except Exception:
        raise ValueError(f"Nie można wyciągnąć ID z nazwy pliku: {fname}")
    
def get_modality(file_name):
    for modality in MODALITY_SUFFIXES:
        if modality in file_name.lower():
            return modality
    return None    

def prep_data(data_dir, fraction, input_dir, segmentation_dir, allowed_ids=None):
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(segmentation_dir, exist_ok=True)

    all_patients = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    print(len(all_patients))
    if allowed_ids is not None:
        all_patients = [p for p in all_patients if p in allowed_ids]
    print(f"Total patients found: {len(all_patients)}")

    count = max(1, int(len(all_patients) * fraction))
    chosen_patients = random.sample(all_patients, count)
    print(f"Using {count} patients")

    # mapka: surowe rozszerzenia -> nnUNet
    modality_map = {
        "t1n": "t1",
        "t1c": "t1ce",
        "t2w": "t2",
        "t2f": "flair"
    }

    for patient_folder in chosen_patients:
        full_path = os.path.join(data_dir, patient_folder)
        # wyciągnij ID, np. z "BraTS-GLI-00000-000" weź "00000"
        parts = patient_folder.split("-")
        if len(parts) < 4:
            print(f"Skipping malformed folder name: {patient_folder}")
            continue
        patient_id = parts[2]

        for raw_mod, new_mod in modality_map.items():
            src = os.path.join(full_path, f"{patient_folder}-{raw_mod}.nii.gz")
            dst = os.path.join(input_dir, f"Brats2025Pre_{patient_id}_{new_mod}.nii.gz")
            if os.path.exists(src):
                shutil.copy(src, dst)
            else:
                print(f"WARNING: {src} not found!")

        # Segmentacja
        seg_src = os.path.join(full_path, f"{patient_folder}-seg.nii.gz")
        seg_dst = os.path.join(segmentation_dir, f"Brats2025Pre_{patient_id}_seg.nii.gz")
        if os.path.exists(seg_src):
            shutil.copy(seg_src, seg_dst)
        else:
            print(f"WARNING: {seg_src} not found!")

if __name__ == "__main__":
    # Przykłady:
    # prep_data("archive", id_range=range(0,4))           # bierzemy 4 pacjentów: 0,1,2,3
    # prep_data("archive", fraction=0.1)                   # bierzemy losowo 10% pacjentów
    # prep_data("archive", fraction=0.3, seed=123)         # 30% z seedem 123

    # prep_data(data_dir = r"C:\Users\barte\Desktop\studia\SEM6\wb\brats_data\BraTS2025Pre\brats2025-gli-pre-challenge-trainingdata",
    #            fraction=0.01, input_dir="BraTS2025Pre\\input", segmentation_dir="BraTS2025Pre\\segmentation")  # przykładowo 10%
    ids_path = "brats_data/glioma_ids"
    data_dir = "brats_data/BraTS2024-Post/training_data1_v2"
    input_dir = "brats_data/BraTS2024-Post/input"
    segmentation_dir = "brats_data/BraTS2024-Post/segmentation"
    ids = load_allowed_ids(ids_path)
    prep_data(data_dir=data_dir,
              fraction=1,
              input_dir=input_dir,
              segmentation_dir=segmentation_dir,
              allowed_ids=ids,
    )