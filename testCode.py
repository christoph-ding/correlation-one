import re
import numpy as np
import pandas as pd

df  =  pd.read_csv("input_data.csv")

df["entry_recorded"] =  pd.to_datetime(df["RECORD_CREATION_DATE"], format='%d%b%Y:%H:%M:%S.%f')

# Returns monthly net income if it appears in the AGENT_NOTES field (divide annual income by 12)
# Field should be a float datatype
def monthly_income_parser(x):
    month_match = 'Monthly gross income' in str(x)
    annual_match = 'Annual gross income' in str(x)
    if month_match:
        return re.findall('\d+', x )
    elif annual_match:
        return re.findall('\d+', x )
    else:
        return np.nan

df["monthly_income"] =  df["AGENT_NOTES"].apply(monthly_income_parser)

print(df)