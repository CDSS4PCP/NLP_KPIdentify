# 📊 Active Learning Hyperparameter Tuning Experiments

This directory contains the results of hyperparameter tuning experiments performed during Active Learning runs.

## 📁 Contents

- Each file in this directory corresponds to a different hyperparameter configuration tested (e.g., dropout rates, sequence lengths, batch sizes).
- Each experiment file is a Google Sheet export (or similar spreadsheet) containing detailed results across Active Learning cycles.
- Files are typically named in a way that reflects the hyperparameter being tested (e.g., `dropout_0.3_results.xlsx`, `seq_len_128_results.xlsx`).

## 📄 Inside Each Experiment File

- Every experiment file includes:
  - Sheets for each Active Learning cycle (e.g., `M0`, `M1`, etc.), containing performance metrics like F1, Recall, and Precision.
  - A summary sheet aggregating metrics across cycles.
  - A `README` sheet inside each file, describing:
    - The specific hyperparameter configuration used,
    - The structure of the file,
    - Details on Active Learning cycles and metrics.

## 📝 How to Use These Results

- Use the individual experiment `README` sheets for detailed information on the context and results of each hyperparameter setting.
- Compare summary sheets across files to evaluate the effect of different hyperparameters on Active Learning performance.
- Look for trends such as:
  - Improvements or degradation in F1/Recall across Active Learning cycles.
  - How different hyperparameters impact convergence speed or performance stability.

## ⚙️ Hyperparameters Tested

This directory includes experiments for various hyperparameters, including but not limited to:
- Dropout rates (e.g., 0.2, 0.3, 0.4)
- Sequence lengths (e.g., 10, 20, 30, etc)
