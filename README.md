# hrv

## Links
Database of normal sinus rhythms: https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

Download the database through the above link,
Unzip the download to get a folder called "mit-bih-normal-sinus-rhythm-database-1.0.0". It should contain lots of files including some ending with .dat
Keep a note of the file path where you saved the folder in your local computer i.e. "[file paths]/mit-bih-normal-sinus-rhythm-database-1.0.0"


## File descriptions
### Databases
mit-bih-normal-sinus-rhythm-database-1.0.0 (folder)
- Files from Kaggle database of normal sinus rhythms
- Manually created .csv files of these samples

### Week of 9/2
filter.py
- Filters for ECG

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
52.py
53.py
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