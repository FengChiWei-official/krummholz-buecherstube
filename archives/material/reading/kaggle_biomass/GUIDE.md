# Study Guide — Image2Biomass (Swin + DINOv2 + XGBoost)

> **Goal:** Help a semi-intermediate practitioner understand, run, and extend the `ref.md` script that trains a Swin transformer, extracts DINOv2 embeddings, trains XGBoost models on the embeddings, and ensembles predictions for the CSIRO Image2Biomass task.

---

## 🚀 Learning Objectives
- Understand the dataset shape and how targets are prepared (pivoting to per-image targets). ✅
- Walk through the dataset class and augmentation pipeline (Albumentations). ✅
- Understand the Swin backbone + regression head and how forward features are pooled. ✅
- Learn the training loop (AMP, gradient clipping, scheduler, early stopping) and evaluation (R²). ✅
- Extract fixed DINOv2 embeddings and train XGBoost regressors. ✅
- Create and evaluate a weighted ensemble and find the best ensemble weight.

---

## Prerequisites
- Python 3.8+ and familiarity with PyTorch and basic ML tooling.
- Basic knowledge of transformers for vision (Swin/Vit) and tree-based models (XGBoost).
- Familiarity with NumPy, pandas, matplotlib.


## Quick Start — files & how to run
- Main content lives inside `ref.md` as a single script. If you prefer to run it directly, copy the code block into a file named `train.py` and run:

```bash
python train.py
```

- Notes:
  - The script expects the Kaggle dataset to be mounted at `/kaggle/input/csiro-biomass/` (paths are hard-coded).
  - If you run locally, change `Config.TRAIN_CSV` and image path roots accordingly.

---

## File map & high-level overview (what to read first) 🔍
1. **CONFIG** — `Config` class: hyperparameters, image sizes, model names, device, and seed.
2. **DATA LOADING** — `get_data()` and `BiomassDataset`:
   - `get_data()` reads `train.csv`, pivots targets to per-image rows, computes target mean/std for normalization.
   - `BiomassDataset.__getitem__()` reads images via OpenCV, applies transforms, returns normalized targets.
3. **AUGMENTATIONS** — `get_transforms()` using Albumentations for train/val.
4. **MODEL** — `SwinRegressor`:
   - Uses TIMM to create a pretrained Swin backbone and adds an MLP head for 5 targets.
5. **TRAINING** — `train_swin()`:
   - Uses AMP, AdamW, CosineAnnealingLR, SmoothL1Loss, gradient clipping, early stopping, and weighted R² validation.
6. **FEATURE EXTRACTION** — `extract_dinov2_embeddings()`:
   - Loads DINOv2, resizes to 518×518, forward_features, pools spatial dims, stores embeddings.
7. **TABULAR MODEL** — `train_xgboost()` trains one XGBoost per target on embeddings.
8. **ENSEMBLE** — `find_best_ensemble_weights()` grid-searches weights and plots results.
9. **UTILS** — `plot_history()`, `save_models()` (exports models & ensemble config).
10. **MAIN** — The `if __name__ == '__main__':` block sequences the full pipeline: train Swin → extract emb → train XGBoost → ensemble → save.

---

## Detailed Walkthrough: recommended reading order (with exercises) ✍️

1. **Data & EDA (30–60 min)**
   - Read `get_data()` and the pivot logic. Load the CSV yourself in a notebook and print head, dtypes, missing values, and distribution of targets.
   - Exercise: Create a small plot of the `Dry_Total_g` distribution and check correlations between targets.
   - Checkpoint: You can reproduce `Config.TARGET_MEAN` and `Config.TARGET_STD`.

2. **Dataset & Augmentations (40–80 min)**
   - Study `BiomassDataset.__getitem__()` and `get_transforms()`.
   - Run a few augmentation passes and visualize augmented images.
   - Exercise: Create a small script/notebook that shows 16 augmented images in a grid.
   - Checkpoint: Confirm that transforms produce tensors of shape `[3, IMG_SIZE, IMG_SIZE]` and normalized values.

3. **Model architecture (30–60 min)**
   - Inspect `SwinRegressor`: how TIMM model is created and how features are pooled.
   - Exercise: Print `backbone` summary and `num_features`, then feed a random tensor through `forward()` and inspect outputs.
   - Checkpoint: Forward pass on a dummy batch returns shape `[batch, 5]`.

4. **Training loop (60–120 min)**
   - Read `train_swin()`: loss, optimizer, scheduler, AMP usage, gradient clipping, early stopping.
   - Exercise: Run a 1-epoch training using a subset of data (e.g., 64 samples) to verify the loop works.
   - Checkpoint: Training runs without CUDA OOM; loss decreases a bit within 1 epoch.

5. **Embedding extraction & XGBoost (60–90 min)**
   - Read `extract_dinov2_embeddings()` and `train_xgboost()`.
   - Exercise: Extract embeddings for 100 samples and train XGBoost for one target, compute R².
   - Checkpoint: Embedding matrix shape and XGBoost validation R² printed.

6. **Ensembling & analysis (30–60 min)**
   - Study `find_best_ensemble_weights()` and plotting logic.
   - Exercise: Run the grid search on validation preds and confirm the best weight matches the printed best.
   - Checkpoint: You can reproduce the ensemble R² improvement plot `ensemble_weight_search.png`.

7. **Saving & reproducibility (20–30 min)**
   - Inspect `save_models()` outputs and `ensemble_config.json` contents.
   - Exercise: Write an inference script that loads `swin_best.pth` and `xgboost_*.json` and computes ensemble predictions on new images.
   - Checkpoint: The inference script outputs predictions consistent with the ensemble formula in the main block.

---

## Suggested experiments & extensions (great for learning) 💡
- Replace the MLP head with a light attention head or a small conv head — compare results.
- Try different augmentation mixes (reduce CoarseDropout or add color jitter) and measure effect on R².
- Fine-tune DINOv2 instead of only extracting embeddings (if you have enough GPU memory).
- Train a small tabular NN on embeddings vs XGBoost and compare performance and speed.
- Try stacking (train a small meta-regressor on the predictions of Swin + XGB).

---

## Common issues & fixes ⚠️
- `image is None`: The script handles missing images by inserting a zero image; consider logging missing paths for debug.
- GPU OOM: reduce `BATCH_SIZE` or `IMG_SIZE`, or use `num_workers=0`.
- TimM model names not available: update timm or pick a model that exists in your timm version.
- XGBoost device errors: either remove `device='cuda'` or install an appropriate GPU-build of XGBoost.

---

## Time estimate & study plan (solo study)
- Quick pass (read + run tiny examples): 4–6 hours.
- Deep dive (run full experiment + multiple ablations): 1–3 days depending on GPU availability.

---

## Next steps I can take (pick one)
- Add `README_ref.md` (per-module annotated doc) for each section above.
- Produce one or more short notebooks (data EDA, model forward pass, train-on-mini-batch, infer script) — *you asked for MD only; I can give notebook content as Markdown cells if preferred.*
- Create a short `INFERENCE.md` describing how to use saved models in production.

---

## Resources & further reading 📚
- TIMM models: https://rwightman.github.io/pytorch-image-models/
- DINOv2 paper / code: https://github.com/facebookresearch/dinov2
- Albumentations docs: https://albumentations.ai/docs/
- XGBoost docs: https://xgboost.readthedocs.io/

---

If you'd like, I can also: add per-section `README.md` files inside the workspace (each mirroring a section above) or produce a concise `INFERENCE.md` next. Which would you like me to do next? ✅
