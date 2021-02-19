# hrv

## Links
- Database of all ECGs (converted to CSV on site): https://archive.physionet.org/cgi-bin/atm/ATM
- Database of normal sinus rhythms (dat,atr): https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

## File descriptions
### Databases
mit-bih-normal-sinus-rhythm-database-1.0.0 (folder)
- Manually created .csv files of the ECGs for following conditions:
  - Normal sinus rhythms (16265, 16272, 16273)
  - Arrythmia (arrythmia)
  - Malignant Ventricular Ectopy (malignant)
  - Supraventricular Arrythmia (sva)

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
