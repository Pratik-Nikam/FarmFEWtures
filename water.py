import os
import json
import pandas as pd
from netlogo_instance import get_netlogo_instance

dirname = os.path.dirname(__file__)
def crop_groundwater_irrigation():
    crop_groundwater_irrigation_data = pd.read_csv(os.path.join(dirname, "netlogo/crop-groundwater-irrigation.csv"), delimiter="\t", header=None)

    df = pd.DataFrame(crop_groundwater_irrigation_data)

    df = df.drop(df.index[0:15])
    df = df[0].str.split(',', expand=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df.columns = ['year', "Corn", "color_0", "pen_down_0", 
                "year_1","Wheat", "color_1", "pen_down_1",
                "year_2","Soybean", "color_2", "pen_down_2",
                "year_3","SG", "color_3", "pen_down_3"]

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Convert columns to integers
    df['Corn'] = df['Corn'].str.replace('"', '').astype(int)
    df['Wheat'] = df['Wheat'].str.replace('"', '').astype(int)
    df['Soybean'] = df['Soybean'].str.replace('"', '').astype(int)
    df['SG'] = df['SG'].str.replace('"', '').astype(int)

    df=df[['year','Corn','Wheat','Soybean','SG']]

    temp = {"irrigation": {
        'Year': df['year'].values.tolist(),
        'Corn': df['Corn'].values.tolist(),
        'Wheat': df['Wheat'].values.tolist(),
        'Soybean': df['Soybean'].values.tolist(),
        'SG': df['SG'].values.tolist()
    }}

    
    print(temp)

    return json.dumps(temp)


def groundwater_level():
    
    groundwater_level_data = pd.read_csv(os.path.join(dirname, "groundwater-level.csv"), delimiter="\t", header=None)

    df = groundwater_level_data

    df = df.drop(df.index[0:14])



    df = df[0].str.split(',', expand=True)

    df.columns = df.iloc[0]
    df = df.iloc[1:]

    df.columns = ['year', "GW level", "color_0", "pen_down_0", 
                "year_1","Min. Aq.", "color_1", "pen_down_1",
                "year_2","Min. +30", "color_2", "pen_down_2"]

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    df['GW level'] = df['GW level'].str.replace('"', '')


    df['GW level'] = df['GW level'].str.replace('"', '').astype(float)

    df['Min. Aq.'] = df['Min. Aq.'].str.replace('"', '').astype(float)
    df['Min. +30'] = df['Min. +30'].str.replace('"', '').astype(float)


    df=df[['year','GW level','Min. Aq.','Min. +30']]


    temp = {
        "gw_level": {
            'Year': df['year'].values.tolist(),
            'GW_level': df['GW level'].values.tolist(),
            'Min_Aq': df['Min. Aq.'].values.tolist(),
            'MinPlus30': df['Min. +30'].values.tolist()
        }
    }

    return json.dumps(temp)





