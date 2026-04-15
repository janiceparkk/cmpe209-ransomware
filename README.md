# Ransomware ML Project

This project uses the Mendeley `combined_without_3gram.csv` dataset for ransomware vs goodware classification.

## Installation Requirements 
```
$ pip install -r requirements.txt 
```

## Dataset location
```data/raw/combined_without_3gram.csv```

## Main columns
- ID
- filename
- RG (target label)
- family

## Label meaning
- RG = 1 -> ransomware
- RG = 0 -> goodware

## Official split used
Training:
- goodware with ID <= 11133
- ransomware families 1 to 25

Testing:
- goodware with ID >= 12000
- ransomware families 26 to 40

## Run order
1. inspect_dataset.py
2. prepare_data.py
