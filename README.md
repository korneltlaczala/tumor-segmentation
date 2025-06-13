# 🧠 BraTS Generalization Study – Segmentation Inference with nnU-Net (Brats21_KAIST_MRI_Lab)

This repository contains scripts and resources used in our study on the generalization ability of a pre-trained nnU-Net model for brain tumor segmentation across various BraTS datasets (2021–2024, including Africa and post-treatment cases).

The segmentation model was taken from [Brats21_KAIST_MRI_Lab](https://github.com/rixez/Brats21_KAIST_MRI_Lab) and used via its Docker-based inference setup.

---

## 📁 Repository Structure

- `scripts/`
  - `data_prep_21.py` — Prepares BraTS 2021 data for Docker inference
  - `data_prep_new.py` — Prepares BraTS 2024-Pre data
  - `predict_notlikeachimpanzee` — Inference script using Docker image (24-Pre)
  - `predict_notlikeachimpanzee2021` — Inference script using Docker image (21)
  - `predict_notlikeachimpanzeeAfrica` — Inference script using Docker image (Africa)
- `brats_data/` — Hidden folder (acquire data directly from BraTS Challenge organizers via Synapse and then use `data_download.py`)


## ⚙️ Data Preparation

Before running the Docker image with the pretrained model, your data must be organized in the correct structure.

We provide two Python scripts to help you prepare the data:

- `data_prep_21.py` — for BraTS 2021 data  
- `data_prep_new.py` — for newer datasets (e.g., BraTS 2024-Pre, BraTS 2024-Post, BraTS Africa)

### How to Use

1. Set the `data_dir` variable to the path containing subfolders for each patient (e.g., `Patient_001/`, `Patient_002/`, etc.).
2. Adjust the following variables in the script to point to your desired output locations:
   - `input_dir`
   - `input_dir2`
   - `segmentation_dir`

Make sure the following folder names are preserved in your output directory:
- `\all_inputs`
- `\input`
- `\segmentation`

These folders are required by the Docker-based inference pipeline and will be created automatically when running the script.
