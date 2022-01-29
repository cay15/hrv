# hrv

## Overview
A program that extracts measurements for Heart Rate Variability (HRV), given an input electrocardiogram (ECG) dataset. Currently, measurements include:
- Average RR interval, or the mean time between heartbeats
- Standard deviation of NN inntervals (SDNN), or the variation in time between heartbeats (relative to the mean)
- Root mean squared of successive differences (RMSSD), or the variation in time between heartbeats (relative to adjacent heartbeats)

## Related links
- Database of all ECGs (converted to CSV on site): https://archive.physionet.org/cgi-bin/atm/ATM
- Database of normal sinus rhythms (dat,atr): https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

## Technologies
This project was created using Python 3.8.

## Setup and Usage
Enter the following on the command line to run the program:
```
pip3 install -r requirements.txt

cd src
python3 main.py
```

main.py will run modules from the following files in order:
1. The program will ask the user to define the input ECG desired, by selecting from either option A or B:
  A) A real ECG from the `/mit-bih-database/` folder. This will run the file `input_real_ecg_1a.py`. Next, the user is to input the name of the ECG file to analyse. (e.g. "MITBIH_AFib04936.csv")
  B) A pre-made artificial ECG, resembling a typical ECG with varying noise to test the robustness of the program. This will run the file `artificial_ecg_1b.py`.
Regardless, the program will output a 60-second sample of the ECG dataset, followed by a resampled version.
2. The modules from the file `filter_ecg_2.py` filters any noise from the input ECG. This is done by removing low, mains and high frequency noises.
3. `r_peak_detection_3.py` will detect R peaks from the filtered ECG. 
4. The time intervals betweem the R peaks are calculated, known as RR intervals.
5. HRV measurements are calculated from the RR intervals.


## File descriptions
### Databases
mit-bih-normal-sinus-rhythm-database-1.0.0 (folder)
- Manually created .csv files of the ECGs for following conditions:
  - Normal sinus rhythms (16265, 16272, 16273)
  - Atrial Fibrillation (AFib)
  - Malignant Ventricular Ectopy (MalVE)
  - ST Change (STChange)
  - Supraventricular Arrythmia (SuperArrythmia)
  - Arrhythmia (100,101,102)

### Week of 2/3
Outdated, unused files have been moved into the folder "archives".
Files that are included in our current coding pipeline have been numbered based on when they occur.

hrv.py
- main12.py, renamed

Ammendement on hrv.py, resulting in it being moved to "archives"
whole_hrv.py now fully processes the whole ECG

### Week of 26/2
main12.py
- Same functions as main.py, with the addition of allowing the user to select between a raw ECG or artificial ECG, and different leads

### Week of 16/2
main.py
- Prime file for HRV extraction. It is a combination of functions imported from other individual files in this repo.

testFilter.py
- Testing of filter.py using fakeecg.py

upsample_ecg.py
- Upsampling of ECG to 1kHz or otherwise defined

### Week of 9/2
filter.py
- Filters for ECG
- Adapted from From https://python-heart-rate-analysis-toolkit.readthedocs.io/en/latest/_modules/heartpy/filtering.html

resample_ecg.py
- Resampling of ECG at different frequencies

fakeecg.py
- Articifial creation of ECG

peak_detection.py
- Detection and indication of R peaks of ECG
- Returns an array of RR intervals in given graph

ecgSample.csv
- .csv version of sample 16265 (see mit-bih-normal-sinus-rhythm-database-1.0.0)

### Week of 2/2
52.py, 53.py
- Simple plotting of ECG using matplotlib

derivative_approach.py
- Attempt at directly converting .dat file to .csv
- Time-consuming; .csv files have been manually created instead

### Week of 26/1
ecg_read_v1.0.py
- code adapted from https://www.kaggle.com/khatri007/detection-of-congestive-heart-failure-using-ecg/notebook
- documentation of wfdb functions: https://wfdb.readthedocs.io/en/latest/processing.html
- Enter the following on terminal to import relevant packages:
pip3 install wfdb
pip3 install keras
