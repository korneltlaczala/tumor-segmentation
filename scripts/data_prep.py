import os
import shutil
import random

def create_dirs(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def get_id(fname):
    # Wyciągamy ID z nazwy pliku, np. BraTS2021_00000_flair.nii.gz -> 0
    return int(fname.split("_")[1])

def prep_data(data_dir, input_dir="input", segmentation_dir="segmentation", id_range=None, fraction=None, seed=42):
    """
    Kopiuje pliki z data_dir do input_dir i segmentation_dir.
    
    - id_range: iterable z ID pacjentów do wzięcia (np. range(0,4)), jeśli None - bierze wszystkie
    - fraction: float 0-1, jeśli podane, losowo wybiera tylko tę część unikalnych ID
    - seed: seed do losowania, żeby mieć powtarzalność
    
    Jeśli podane fraction, to id_range jest ignorowane.
    """

    create_dirs([input_dir, segmentation_dir])

    all_ids = set()
    # Najpierw zbierzemy wszystkie ID
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".nii.gz"):
                try:
                    _id = get_id(file)
                    all_ids.add(_id)
                except (IndexError, ValueError):
                    pass

    all_ids = sorted(all_ids)

    if fraction is not None:
        random.seed(seed)
        count = max(1, int(len(all_ids) * fraction))
        chosen_ids = set(random.sample(all_ids, count))
    elif id_range is not None:
        chosen_ids = set(id_range)
    else:
        chosen_ids = set(all_ids)

    print(f"Total IDs found: {len(all_ids)}. Using {len(chosen_ids)} IDs.")

    for root, _, files in os.walk(data_dir):
        for file in files:
            if not file.endswith(".nii.gz"):
                continue
            try:
                _id = get_id(file)
            except (IndexError, ValueError):
                continue
            if _id not in chosen_ids:
                continue

            src_path = os.path.join(root, file)
            if file.endswith("seg.nii.gz"):
                dst_path = os.path.join(segmentation_dir, file)
            else:
                dst_path = os.path.join(input_dir, file)

            if not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)

if __name__ == "__main__":
    # Przykłady:
    # prep_data("archive", id_range=range(0,4))           # bierzemy 4 pacjentów: 0,1,2,3
    # prep_data("archive", fraction=0.1)                   # bierzemy losowo 10% pacjentów
    # prep_data("archive", fraction=0.3, seed=123)         # 30% z seedem 123

    prep_data(data_dir = r"C:\Users\barte\Desktop\studia\SEM6\wb\brats_data\BraTS2024Pre\brats2025-gli-pre-challenge-trainingdata"
, fraction=0.01, input_dir="BraTS2025Pre\input", segmentation_dir="BraTS2025Pre\segmentation")  # przykładowo 10%
