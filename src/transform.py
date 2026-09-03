import pandas as pd
from extract import datasets
import datetime

validation_errors={}

required_columns = {
    "olist_customers_dataset": ["customer_id"],
    "olist_geolocation_dataset": ["geolocation_zip_code_prefix"],
    "olist_orders_dataset": ["order_id"],
    "olist_order_items_dataset": ["order_id", "order_item_id"],
    "olist_order_payments_dataset": ["order_id"],
    "olist_order_reviews_dataset": ["review_id", "order_id"],
    "olist_products_dataset": ["product_id"],
    "olist_sellers_dataset": ["seller_id"],
    "product_category_name_translation": ["product_category_name"]
}

datetime_columns={
    "olist_orders_dataset":[
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
        ],
        "olist_order_items_dataset": [
        "shipping_limit_date"
    ],
    "olist_order_reviews_dataset": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
}


for name, df in datasets.items():
    dtypes=df.dtypes
    duplicate_rows=df.duplicated().sum()
    missing=df.isna().sum()
    missing=missing[missing>0]

    required=required_columns[name]
    missing_required=[column for column in required if column not in df.columns]

    if name in datetime_columns:
            for column in datetime_columns[name]:
                df[column]= pd.to_datetime(df[column],errors="coerce")

    
    validation_errors[name]={
        "duplicate_rows":duplicate_rows,
        "missing_values":missing,
        "missing_required":missing_required,
        "dtypes":dtypes
    }

    datasets["olist_order_reviews_dataset"]["review_comment_title"] = datasets["olist_order_reviews_dataset"]["review_comment_title"].fillna("No comment")
    datasets["olist_order_reviews_dataset"]["review_comment_message"] = datasets["olist_order_reviews_dataset"]["review_comment_message"].fillna("No comment")
    datasets["olist_products_dataset"]["product_category_name"]  =datasets["olist_products_dataset"]["product_category_name"] .fillna("Unknown")
    print(datasets["olist_orders_dataset"][[
    "order_delivered_customer_date",
    "order_purchase_timestamp"
    ]].dtypes)
    #datasets["olist_orders_dataset"]["delivery_days"] = (datasets["olist_orders_dataset"]["order_delivered_customer_date"] - datasets["olist_orders_dataset"]["order_purchase_timestamp"]).dt.days
    orders = datasets["olist_orders_dataset"]

    orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"],
        errors="coerce"
    )

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
    ).dt.days

    datasets["olist_orders_dataset"]["order_year"]=datasets["olist_orders_dataset"]["order_purchase_timestamp"].dt.year
    datasets["olist_orders_dataset"]["order_month"]=datasets["olist_orders_dataset"]["order_purchase_timestamp"].dt.month

    datasets["olist_order_items_dataset"]["total_sales"] = (datasets["olist_order_items_dataset"]["price"]+datasets["olist_order_items_dataset"]["freight_value"])

"""
print(validation_errors)   
print(datasets["olist_orders_dataset"].dtypes)

print(datasets["olist_orders_dataset"][["order_purchase_timestamp","order_delivered_customer_date","delivery_days","order_year","order_month"]].head())
print(
    datasets["olist_order_items_dataset"][
        ["price", "freight_value", "total_sales"]
    ].head()
)

print(datasets["olist_orders_dataset"]["delivery_days"].describe())

print(datasets["olist_orders_dataset"][
    ["delivery_days", "order_year", "order_month"]
].dtypes)

print(datasets["olist_order_items_dataset"][
    ["price", "freight_value", "total_sales"]
].dtypes)
"""