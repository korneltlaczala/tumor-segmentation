import os
import pandas as pd

file_path = "brats_data/BraTS-PTG supplementary demographic information and metadata.xlsx"
data = pd.read_excel(file_path)

def select_ids_by_glioma_type():
    data["patient_id"] = data["BraTS Subject ID"].apply(lambda x: x[:-4])
    data = data[data["Train/Test/Validation "] == "Train"]
    patient_data = data.groupby("patient_id", as_index=False)[["Glioma type ", "BraTS Subject ID"]].first()
    print(patient_data.head())

    glioma_counts = patient_data["Glioma type "].value_counts()
    glioma_counts = glioma_counts[glioma_counts > 50]
    glioma_types = glioma_counts.index

    ids_path = "brats_data/glioma_ids"
    os.makedirs(ids_path, exist_ok=True)
    for glioma_type in glioma_types:
        glioma_ids = patient_data[patient_data["Glioma type "] == glioma_type].sample(n=50)[["BraTS Subject ID"]]
        glioma_ids.to_csv(os.path.join(ids_path, f"{glioma_type}.csv"), index=False, header=False)

    print(f"Saved {len(glioma_types)} files to {ids_path}")

def patient_prep():
    pass