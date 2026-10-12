import pandas as pd
from pathlib import Path
import time

def extract():
    #data_folder= Path("data/raw")
    data_folder = Path("/opt/airflow/data/raw")

    csv_files= list(data_folder.glob("*.csv"))
    total_files=len(csv_files)
    print("CURRENT DIRECTORY:", Path.cwd())
    print("DATA FOLDER:", data_folder.resolve())
    print("CSV FILES:", list(data_folder.glob("*.csv"))) 
    
    datasets={}
    errors={}

    start_time=time.time()

    for csv_file in csv_files:
        try: 
            csv_name=csv_file.stem
            df=pd.read_csv(csv_file)
            datasets[csv_name]= df
        
        except Exception as e:
            errors[csv_name]={
                "file":csv_file.name,
                "error_type":type(e).__name__,
                "message":str(e)
            }
            
    end_time=time.time()
    execution_time=end_time - start_time

    loaded_files=len(datasets)
    failed_files=len(errors)
    total_rows=0

    for df in datasets.values():
        total_rows+=len(df)

    statistics={
        "total_files":total_files,
        "loaded_files": loaded_files,
        "failed_files": failed_files,
        "total_rows":total_rows,
        "execution_time": execution_time
    }
    print("DATASETS EXTRACTED:")
    print(datasets.keys())
    return datasets , errors , statistics


datasets, errors, statistics=extract()

#print(statistics)
#print(errors)
#print(datasets.keys())




