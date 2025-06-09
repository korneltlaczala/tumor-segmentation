import os
import pandas as pd
import glob

def load_allowed_ids(glioma_ids_folder="brats_data/glioma_ids"):
    all_csvs = glob.glob(os.path.join(glioma_ids_folder, "*.csv"))
    allowed_ids = set()

    for csv_path in all_csvs:
        ids = pd.read_csv(csv_path, header=None)[0]  # firts column = BraTS Subject ID
        allowed_ids.update(ids.tolist())

    return allowed_ids