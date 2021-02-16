# Main file where individual .py files are combined and HRV analysis will be done

## 1. INPUT RAW ECG

# Import ECG (.csv), get fs

# Split signal into chunks

# Interpolate

# Resample

# Output: 'feather'/'pickle' format?


## 2. PRE-PROCESSING

# Baseline offset removal

# Baseline drift removal (high-pass filter)

# Mains noise removal (notch filter)

# High-frequency noise removal (low-pass filter)

# consider: anomalous/atopic beats


## 3. R PEAK DETECTION

## 4. RR INTERVALS

## consider: frequency domain conversion