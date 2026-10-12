from pathlib import Path

raw_dir = Path("/opt/airflow/data/raw")

def is_valid_olist_file(filename):
    if filename.startswith("olist_") and  filename.endswith("_dataset.csv"):
        return True
    return False

def get_table_name(filename):
    name= filename.removeprefix("olist_") 
    name= name.removesuffix("_dataset.csv")
    return "raw_" + name

def discover_files():
    files= raw_dir.iterdir()
    result=[]

    for file in files:
        if is_valid_olist_file(file.name):
            table=get_table_name(file.name)
            result.append({
                "file":file.name,
                "table":table
            })
    return result


print(discover_files())