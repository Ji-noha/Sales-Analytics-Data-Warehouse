import pandas as pd
import numpy

df=pd.read_csv("data/raw/product_category_name_translation.csv")
print("====data types====")
df.info()
print("====missing values====")
print(df.isnull().sum())
print("====dupicates====")
print(df.duplicated().sum())
print("====statistics====")
print(df.describe())

df["product_weight_g"]=df["product_weight_g"].fillna(df["product_weight_g"].median())

df["product_name_lenght"]=df["product_name_lenght"].fillna(df["product_name_lenght"].median())

df["product_description_lenght"]=df["product_description_lenght"].fillna(df["product_description_lenght"].median())


df["product_photos_qty "]=df["product_photos_qty"].fillna(df["product_photos_qty "].median())

df["product_length_cm  "]=df["product_length_cm"].fillna(df["product_length_cm "].median())

df["product_height_cm"]=df["product_height_cm"].fillna(df["product_height_cm"].median())

df["product_width_cm"]=df["product_width_cm"].fillna(df["product_width_cm"].median())

df["product_category_name"] = df["product_category_name"].fillna("Unknown")

