import os
import json
import pandas as pd
import seaborn as sns


dirname = os.path.dirname(__file__)


def farm_energy_production_calculation():
    farm_energy_production_data = pd.read_csv(
        os.path.join(dirname, "netlogo/farm-energy-production.csv"),
        delimiter="\t",
        header=None,
    )

    # Preprocess the DataFrame
    df = pd.DataFrame(farm_energy_production_data)

    df = df.drop(df.index[0:14])
    df = df[0].str.split(",", expand=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df.columns = [
        "year",
        "Wind",
        "color_0",
        "pen_down_0",
        "year_1",
        "Solar",
        "color_1",
        "pen_down_1",
        "year_2",
        "0 MWh",
        "color_2",
        "pen_down_2",
    ]

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Convert columns to integers
    df["Wind"] = df["Wind"].str.replace('"', "").astype(float)
    df["Solar"] = df["Solar"].str.replace('"', "").astype(float)
    df["0 MWh"] = df["0 MWh"].str.replace('"', "").astype(float)

    df = df[["year", "Wind", "Solar", "0 MWh"]]

    temp = {
        "energy": {
            "Year": df["year"].values.tolist(),
            "Wind": df["Wind"].values.tolist(),
            "Solar": df["Solar"].values.tolist(),
            "zeroMWh": df["0 MWh"].values.tolist(),
        }
    }

    print(temp)

    return json.dumps(temp)


def energy_net_income_calculation():
    energy_net_income_data = pd.read_csv(
        os.path.join(dirname, "netlogo/energy-net-income.csv"),
        delimiter="\t",
        header=None,
    )

    df = energy_net_income_data

    df = df.drop(df.index[0:14])

    df = df[0].str.split(",", expand=True)

    df.columns = df.iloc[0]
    df = df.iloc[1:]

    df.columns = [
        "year",
        "Wind",
        "color_0",
        "pen_down_0",
        "year_1",
        "Solar",
        "color_1",
        "pen_down_1",
        "year_2",
        "US$0",
        "color_2",
        "pen_down_2",
    ]

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    df["Wind"] = df["Wind"].str.replace('"', "")

    df["Wind"] = df["Wind"].str.replace('"', "").astype(float)

    df["Solar"] = df["Solar"].str.replace('"', "").astype(float)

    df["US$0"] = df["US$0"].str.replace('"', "").astype(float)

    df = df[["year", "Wind", "Solar", "US$0"]]

    temp = {
        "Income": {
            "Year": df["year"].values.tolist(),
            "Wind": df["Wind"].values.tolist(),
            "US$0": df["US$0"].values.tolist(),
            "Solar": df["Solar"].values.tolist(),
        }
    }

    return json.dumps(temp)


def energy_calc(
    energy_value,
    loan_term,
    interest,
    nyear_w,
    num_wind_turbines,
    cost_w,
    capacity_w,
    degrade_w,
    wind_factor,
    num_panel_sets,
    nyear_s,
    cost_s,
    capacity_s,
    degrade_s,
    sun_hrs,
    ptc_w,
    itc_s,
    ptc_s,
    num_of_years,
):
    # Set the style and context for the plots
    sns.set_style("white")
    sns.set_context("talk")
    from netlogo_instance import get_netlogo_instance
    netlogo = get_netlogo_instance()

    # Set NetLogo variables
    netlogo.command(f"set Energy_value {energy_value}")
    netlogo.command(f"set Loan_term {loan_term}")
    netlogo.command(f"set interest {interest}")
    netlogo.command(f"set Nyear_W {nyear_w}")
    netlogo.command(f"set #wind_turbines {num_wind_turbines}")
    netlogo.command(f"set Cost_W {cost_w}")
    netlogo.command(f"set Capacity_W {capacity_w}")
    netlogo.command(f"set Degrade_W {degrade_w}")
    netlogo.command(f"set wind_factor {wind_factor}")
    netlogo.command(f"set #Panel_sets {num_panel_sets}")
    netlogo.command(f"set Nyear_S {nyear_s}")
    netlogo.command(f"set Cost_S {cost_s}")
    netlogo.command(f"set Capacity_S {capacity_s}")
    netlogo.command(f"set Degrade_S {degrade_s}")
    netlogo.command(f"set Sun_hrs {sun_hrs}")
    netlogo.command(f"set PTC_W {ptc_w}")
    netlogo.command(f"set ITC_S {itc_s}")
    netlogo.command(f"set PTC_S {ptc_s}")

    # Setup and run the NetLogo model
    netlogo.command("setup")
    netlogo.command(f"repeat {num_of_years}  [go]")
    netlogo.command("go")

    # Close the NetLogo workspace
    netlogo.kill_workspace()

    # Open the CSV file and read the data into a Pandas DataFrame
    farm_energy_production_img_data = farm_energy_production_calculation()

    energy_net_calc_img_data = energy_net_income_calculation()

    result = {
        "farm_energy_production_img_data": farm_energy_production_img_data,
        "energy_net_calc_img_data": energy_net_calc_img_data,
    }

    return result
