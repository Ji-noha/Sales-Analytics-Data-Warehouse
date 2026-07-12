import pandas as pd
from pathlib import Path

"""
    Reads all CSV files from the data folder.

    Returns:
        dict: Dictionary where
            key = dataset name
            value = pandas DataFrame
"""
def extract():
    data_folder= Path("data")
    csv_files= data_folder.glob("*.csv")
    datasets={}
    
    for csv_file in csv_files:
        csv_name=csv_file.stem
        df=pd.read_csv(csv_file)
        datasets[csv_name]= df

    return datasets










