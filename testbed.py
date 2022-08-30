from pandas.core.groupby import groupby
from pandas.core.groupby.generic import DataFrameGroupBy
import owidutils
import pandas as pd
from flask import json

url_local = "./data/t_emissions_owid.csv"


df = owidutils.get_owid_co2data(url_local,owidutils.replace_countries)

df_co2 = df[["year","country","co2"]]
df_co2 = df_co2.sort_values(["year","co2"],ascending=[False,False]).groupby("year").head(10)

df_co2.to_json()

df_2019= df_co2[df_co2["year"]==2019]
json.loads(df_2019[["country","co2"]].to_json( orient="values"))

