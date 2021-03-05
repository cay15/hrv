# hrv

## Links
- Database of all ECGs (converted to CSV on site): https://archive.physionet.org/cgi-bin/atm/ATM
- Database of normal sinus rhythms (dat,atr): https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

## File descriptions
### Databases
mit-bih-normal-sinus-rhythm-database-1.0.0 (folder)
- Manually created .csv files of the ECGs for following conditions:
  - Normal sinus rhythms (16265, 16272, 16273)
  - Atrial Fibrillation (AFib)
  - Malignant Ventricular Ectopy (MalVE)
  - ST Change (STChange)
  - Supraventricular Arrythmia (SuperArrythmia)

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
