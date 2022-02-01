# hrv

## Overview
A program that extracts measurements for Heart Rate Variability (HRV), given an input electrocardiogram (ECG) dataset. Currently, measurements include:
- Average RR interval, or the mean time between heartbeats
- Standard deviation of NN inntervals (SDNN), or the variation in time between heartbeats (relative to the mean)
- Root mean squared of successive differences (RMSSD), or the variation in time between heartbeats (relative to adjacent heartbeats)

## Related links
- The datasets of all ECGs were obtained from the Physiobank database. These were converted to CSV files on the site before downloading onto the `/mit-bih-database/' folder: https://archive.physionet.org/cgi-bin/atm/ATM
- A database of normal sinus rhythms were obtained from the Kaggle site. These are available in .dat and .atr formats: https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

## Technologies
This project was created using Python 3.8. Graphs are visualised using the Matplotlib library.

## Installation
```
pip3 install -r requirements.txt
```

## Usage
```
cd src
python3 main.py
```

main.py will run modules from the following files in order:
1. The program will ask the user to define the input ECG desired, by selecting from either option A or B:
  A) A real ECG from the `/mit-bih-database/` folder. This will run the file `input_real_ecg_1a.py`. Next, the user is to input the name of the ECG file to analyse. (e.g. "MITBIH_AFib04936.csv"). ECG data from either the 1st or 2nd lead must be chosen.
  B) A pre-made artificial ECG, resembling a typical ECG with varying noise to test the robustness of the program. This will run the file `artificial_ecg_1b.py`.
Regardless, the program will output a 60-second sample of the ECG dataset. The user may have to select between the 1st or 2nd lead of the chosen ECG dataset. This is followed by a resampled version of the ECG.
2. The modules from the file `filter_ecg_2.py` filters any noise from the input ECG. This is done by removing low, mains and high frequency noises. The denoised ECG is displayed.
3. `r_peak_detection_3.py` will detect R peaks from the filtered ECG. Certain conditions will require the ECG to be mirrored along the x-axis; this graph is displayed. Next, the local peaks are indicated on the following graph, and from this the R peaks are calculated and displayed on another graph.
4. The time intervals betweem the R peaks are calculated, known as RR intervals. A graph of the time series of the RR intervals is displayed.
5. HRV measurements are calculated from the RR intervals, and are output onto the command line.


## Description of files

/archive
files that were originally part of the program pipeline, but are no longer used.

/mit-bih-database
manually created .csv files of the ECGs for following conditions:
  - Normal sinus rhythms (16265, 16272, 16273)
  - Atrial Fibrillation (AFib)
  - Malignant Ventricular Ectopy (MalVE)
  - ST Change (STChange)
  - Supraventricular Arrythmia (SuperArrythmia)
  - Arrhythmia (100,101,102)

/src
contains main script `main.py`, numbered modules of the programming pipeline, and unit testing script `testing.py`.

Any other "lefttover" folders created by local installation on other systems (such as `__pycache__` and `.idea`) can be safely deleted.