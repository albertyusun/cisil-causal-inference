"""
Cleans ACS csv and matches column names with column names.
"""

import pandas as pd

# convert ACS_Variables_Selected csv to a dictionary
variables_raw = pd.read_csv('../../../data/ACS_Variables_Selected - Variables_Selected.csv')
col_mappings = dict(zip(variables_raw.Variable_Code, variables_raw.Description))

# read in acs_raw
acs_raw = pd.read_csv('../../../data/King_County_ACS_2019_tract.csv')

# remove 'M' columns and excess index column
acs_df = acs_raw.loc[:,~acs_raw.columns.str.endswith('M')].iloc[:,1:]

# remove 'E' suffix from summary statistics, but maintain Name as Name
acs_df.columns = acs_df.columns.str.rstrip("E")
acs_df = acs_df.rename(columns={"NAM": "NAME"})

# apply col_mappings
acs_df = acs_df.rename(columns=col_mappings)

# clean column names
acs_df.columns = acs_df.columns.str.lower()
acs_df.columns = acs_df.columns.str.replace(r'!!|, | |-', "_", regex=True)
acs_df.columns = acs_df.columns.str.replace("$", "", regex=False)
acs_df.columns = acs_df.columns.str.replace(" ", "_")
acs_df.columns = acs_df.columns.str.replace(r",|:", "", regex=True)
acs_df.columns = acs_df.columns.str.replace(r"[()]|...", "", regex=True)

# isolate census tract
acs_df['name'] = acs_df['name'].str.replace('Census Tract ','')
acs_df['name'] = acs_df['name'].str.replace(', King County, Washington','')
acs_df = acs_df.rename(columns={'name':'census_tract'})

acs_df.to_csv('../../../data/CLEAN_King_County_ACS_2019_tract.csv', index=False)