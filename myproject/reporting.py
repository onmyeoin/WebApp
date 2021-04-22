import pandas as pd
from pandas import ExcelWriter
import numpy as np
import os

def save_xls(df_list, xls_path):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(df_list):
            df.to_excel(writer,'sheet%s' % n)
        writer.save()
        print("Saved")

def create_VAT_Report(csv_path, xls_path):
    sales_report = pd.read_csv(csv_path)

    ### ZERO VAT

    zero_VAT = sales_report[sales_report["Category"] == "Milkshakes"].copy()
    zero_VAT["VAT"] = zero_VAT["Subtotal"] * 0
    zero_VAT["Cumulative Sales"] = zero_VAT["Subtotal"].cumsum()
    zero_VAT["Cumulative VAT"] = zero_VAT["VAT"].cumsum()

    ### REDUCED RATE

    reduced_Rate_Category = ['Modifiers', 'All Day Brunch', 'Burgers', 'Fries, Sides','Nachos','Fries/Sides']
    reduced_Rate = sales_report[sales_report["Category"].isin(reduced_Rate_Category)].copy()
    reduced_Rate["VAT"] = round(reduced_Rate["Subtotal"] - (reduced_Rate["Subtotal"] / 1.135), 2)
    reduced_Rate["Cumulative Sales"] = reduced_Rate["Subtotal"].cumsum()
    reduced_Rate["Cumulative VAT"] = reduced_Rate["VAT"].cumsum()

    ### STANDARD RATE

    standard_Rate_Category = ['Soft Drinks and Non Alcoholic','Mega Cocktail Jars (700ml)', 'Cocktails (250ml)', 'Craft Cans and Bottles','Drinks', 'Beer']
    standard_Rate = sales_report[sales_report["Category"].isin(standard_Rate_Category)].copy()
    standard_Rate["VAT"] = round(standard_Rate["Subtotal"] - (standard_Rate["Subtotal"] / 1.21), 2)
    standard_Rate["Cumulative Sales"] = standard_Rate["Subtotal"].cumsum()
    standard_Rate["Cumulative VAT"] = standard_Rate["VAT"].cumsum()

    VAT_List = [zero_VAT, reduced_Rate, standard_Rate]

    save_xls(VAT_List, xls_path)
