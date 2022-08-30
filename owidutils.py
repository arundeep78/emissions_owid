

from datetime import datetime
import calendar
import pandas as pd
import numpy as np
import glob
from flask import json




# country names in owid db to be changed and aligned with UN naming
replace_countries = { "United States": "United States of America", "Democratic Republic of Congo": "Democratic Republic of the Congo" }
url = "https://github.com/owid/co2-data/blob/master/owid-co2-data.csv"
url_dd = "https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv"
url_xl = "https://github.com/owid/co2-data/raw/master/owid-co2-data.xlsx"
url_local = "./data/t_emissions_owid.csv"
url_dd_local = "./data/owid-co2-codebook.txt"


def get_jsons():
    
    files = glob.glob("./static/jsons/*")
    #files = [f.split("\\")[1] for f in files]

    json_dict = { f.split("\\")[1]: json.load(open(f)) for f in files}
    return json_dict

def get_owid_co2dd(url):
  return pd.read_csv(url,index_col="column")

def get_owid_co2data(url, replace_countries): 
    """
    Get emissions data from OWID and replace country names to match with world Map naming

    Args:
        url (string): URL to OWID CO2 emissions csv file: local or web
        replace_countries (Dict): dictionary to replace country names to match with map country names

    Returns:
        [DatafFrame]: DataFrame with OWID CO2 data
            """

    exclude_cc = ["EU-27", "EU-28", "Europe", "Europe (excl. EU-27)",
            "Europe (excl. EU-28)",
            "World",
            "North America (excl. USA)",
            "North America",
            "Asia (excl. China & India)",
            "Asia"
            ]
    df= pd.read_csv(url)
    # align country names with UN
    df["country"] = df["country"].replace(replace_countries)

    df = df[~df["country"].isin(exclude_cc)]

    return df 

def get_owid_param_options(param):
    """
    data for the given emissions parameter and return options for echart world map

    Args:
        param (string): Co2 emissions parameters for OWID emissions data
    """

    # Get OWID CO2 emissions data dictionary
    df_owid_dd = get_owid_co2dd(url_dd_local)

    # get OWID co2 emissions data
    df = get_owid_co2data(url_local,replace_countries=replace_countries)

    df = df[["year","country", param]]

    # cleanup data for the selected parameter
    df[param] = df[param].replace(np.nan,0)

    # select years for which there is no change in data. Select only data for which there is a variation atleast
    df_n = df.groupby("year")[param].nunique()>1
    years = df_n.index[df_n]

    df = df[df["year"].isin(years)]
    
    max_yyyy = int(df["year"].max())
    min_yyyy = int(df["year"].min())
    # min_yyyy = np.maximum(min_yyyy, max_yyyy -150)

    options = {}

    
    for yyyy in range(min_yyyy, max_yyyy+1):


        df_data = df.loc[df["year"]== yyyy, ["country", param]].rename(columns= {"country": "name", param: "value"})

        data = df_data.to_dict("records")
        
        max_val = df_data["value"].max()
        min_val = df_data["value"].min()
       
        series =  [
            {
            "id": param,
            "name" : param,
            "top" : 100,
            "type": 'map',
            "roam": False, 
            "map": 'world',
            "animationDurationUpdate": 100,
            "universalTransition": True,
            "animationEasing": 'linear',
            "animationEasingUpdate": 'linear',
            "data": data
            }
        ]

        visualMap =    {
                
                "min": min_val,
                "max": max_val,
                "orient": "vertical",
                "left" : "right",
                "top": "center",
                "inRange": {
                    "color": ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                },
                "text": [f"{max_val:,.2f}", f"{min_val: ,.2f}"],
                "calculable": False
            }

        title = " ".join([ p.upper() for p in param.split("_")]) + " - "+ str(yyyy)
        subtitle= df_owid_dd.loc[param,"description"].replace(".", ".\n")

        option = {
                    "visualMap": visualMap,
                    "series": series,
                    
                    "title": {
                        "padding" : 10,
                        "left": "center",
                        "text" : title,
                        "subtext": subtitle,
                        "subtextStyle" : {
                            "fontSize" : 14
                            }
                        
                    },
                    "grid" :
                        {
                        "top" : 120
                        }
                    
        }

        options[int(yyyy)] = option

    return options, int(min_yyyy), int(max_yyyy)


def get_owid_top(param):
    """
    data for the given emissions parameter and return options for echart top 10 bar chart

    Args:
        param (string): Co2 emissions parameters for OWID emissions data
    """

    # Get OWID CO2 emissions data dictionary
    df_owid_dd = get_owid_co2dd(url_dd_local)

    # get OWID co2 emissions data
    df = get_owid_co2data(url_local,replace_countries=replace_countries)

    df = df[["year","country", param]]

    # cleanup data for the selected parameter
    df[param] = df[param].replace(np.nan,0)

    # select years for which there is no change in data. Select only data for which there is a variation atleast
    df_n = df.groupby("year")[param].nunique()>1
    years = df_n.index[df_n]

    
    df = df[df["year"].isin(years)]
    

    df = df.sort_values(["year",param],ascending=[False,False]).groupby("year").head(10)

    # select years for there is data for 10 countries

    df_10 = df.groupby("year")["country"].count()
    df10_years = df_10[df_10==10].index
    df = df[df["year"].isin(df10_years)]

    max_yyyy = int(df["year"].max())
    min_yyyy = int(df["year"].min())
    # min_yyyy = np.maximum(min_yyyy, max_yyyy -150)

    options = {}

    
    for yyyy in range(min_yyyy, max_yyyy+1):


        df_data = df.loc[df["year"]== yyyy, ["country", param]]

        option = {
                "grid": {
                    "top": 10,
                    "bottom": 30,
                    "left": 200,
                    "right": 80
                },
                "xAxis": {
                    "max": 'dataMax'
                },
                # "dataset": {
                #     "source" : df_data.T.values.tolist()
                # },
                "yAxis": {
                    "type": 'category',
                    "inverse": True,
                    "max": 9,
                    "axisLabel": {
                        "show": True,
                        "fontSize": 14
                    },
                    "data" : df_data["country"].values.tolist(),
                    "animationDuration": 300,
                    "animationDurationUpdate": 300
               },
               "series": [
                    {
                        "realtimeSort": True,
                        "seriesLayoutBy": 'column',
                        "type": 'bar',
                        # "encode": {
                        #     "x": "dimension",
                        #     "y": 2
                        # },
                        "data" : df_data[param].values.tolist(),
                        "label": {
                            "show": True,
                            "precision": 1,
                            "position": 'right',
                            "valueAnimation": True,
                            "fontFamily": 'monospace'
                        }
                    }
                ],
        #   Disable init animation.
            "animationDuration": 0,
            "animationDurationUpdate": 500,
            "animationEasing": 'linear',
            "animationEasingUpdate": 'linear',
            "graphic": {
                "elements": [
                    {
                        "type": 'text',
                        "right": 160,
                        "bottom": 60,
                        "style": {
                            "text": yyyy,
                            "font": 'bolder 80px monospace',
                            "fill": 'rgba(100, 100, 100, 0.25)'
                        },
                        "z": 100
                    }
                ]
            }
        }


        options[int(yyyy)] = option

    return options, int(min_yyyy), int(max_yyyy)



def get_owid_top2(param):
    """
    data for the given emissions parameter and return options for echart top 10 bar chart

    Args: 
        param (string): Co2 emissions parameters for OWID emissions data
    """

    # Get OWID CO2 emissions data dictionary
    df_owid_dd = get_owid_co2dd(url_dd_local)

    # get OWID co2 emissions data
    df = get_owid_co2data(url_local,replace_countries=replace_countries)

    df = df[["year","country", param]]

    # cleanup data for the selected parameter
    df[param] = df[param].replace(np.nan,0)

    # select years for which there is no change in data. Select only data for which there is a variation atleast
    df_n = df.groupby("year")[param].nunique()>1
    years = df_n.index[df_n]

    
    df = df[df["year"].isin(years)]
    

    df = df.sort_values(["year",param],ascending=[False,False]).groupby("year").head(10)

    # select years for there is data for 10 countries

    df_10 = df.groupby("year")["country"].count()
    df10_years = df_10[df_10==10].index
    df = df[df["year"].isin(df10_years)]

    max_yyyy = int(df["year"].max())
    min_yyyy = int(df["year"].min())
    # min_yyyy = np.maximum(min_yyyy, max_yyyy -150)

    dataset = {}

    
    for yyyy in range(min_yyyy, max_yyyy+1):

        
        dataset[int(yyyy)] =  json.loads(df.loc[df["year"]== yyyy, ["country", param]].\
                            to_json(orient= "values")
        )

    return dataset, int(min_yyyy), int(max_yyyy)