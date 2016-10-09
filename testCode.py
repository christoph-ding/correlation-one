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
        return float(('').join(re.findall('\d+', x )))
    elif annual_match:
        return float(('').join(re.findall('\d+', x ))) / 12
    else:
        return np.nan

df["monthly_income"] =  df["AGENT_NOTES"].apply(monthly_income_parser)

# Set to be equal to the lower bound of the credit score range. Datatype should be a float.
df["credit_score"] = df["CREDIT_RANGE"].apply(lambda x: float(re.findall('\d+', x )[0]))

# Set to be equal to the lower bound of the debt range. Datatype should be a float.
df["debt"] = df["EXISTING_DEBT"].fillna('0').str.replace(',','').apply(lambda x: float(re.findall('\d+', x )[0]))

# grouped_df has the (1) count and (2) average loan amount of grouping the records by OFFICE_LOCATION (first) and by CREDIT_RANGE (second)
grouped_df  =  df.groupby(['OFFICE_LOCATION', 'CREDIT_RANGE']).agg([np.count_nonzero, np.mean])

df['time_delta'] = (df['entry_recorded']-df['entry_recorded'].shift()).fillna(0)

# print(df.groupby('OFFICE_LOCATION').count())

# print(df[df['OFFICE_LOCATION'] == 'NORTHERN CALIFORNIA']['RECORD_CREATION_DATE'].count() + df[df['OFFICE_LOCATION'] == 'SOUTHERN CALIFORNIA']['RECORD_CREATION_DATE'].count())

print(df)

print( (8000 - df['monthly_income'].count()) / 8000 )



