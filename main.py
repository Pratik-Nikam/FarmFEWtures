import os
import sys
import time
import queue
import subprocess
from multiprocessing import Process, Queue
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd

from agriculture import crop_production_calculation, net_income_calculation
from energy import farm_energy_production_calculation, energy_net_income_calculation
from climate import crop_income_calculation, insurance_income_calculation
from water import crop_groundwater_irrigation, groundwater_level
from netlogo_instance import get_netlogo_instance



# Initialize Flask app
app = Flask(__name__)

# Define routes for different pages

# NetLogo Input page
@app.route("/NetlogoInputV1")
def netlogoinput():
    return render_template("NetlogoInputV1.html")

# Agriculture Page
@app.route("/AgricultureV1")
def agriculture():
    return render_template("index.html")

# Water Page
@app.route("/WaterV1")
def water():
    return render_template("water.html")

# Energy Page
@app.route("/EnergyV1")
def energy():
    return render_template("energy.html")

# Chart Window
@app.route("/ChartWindow")
def ChartWindow():
    return render_template("ChartWindow.html")

# Climate Page
@app.route("/ClimateV1")
def climate():
    return render_template("climate.html")

# Define global variables
corn_area, wheat_area, soybeans_area, sg_area, num_of_years = None, None, None, None, None
aquifier_level, min_aquifier_level = None, None
energy_value, loan_term, interest, num_wind_turbines, nyear_w, capacity_w, cost_w, degrade_w, wind_factor, num_panel_sets, nyear_s, cost_s, capacity_s, degrade_s, sun_hrs, ptc_w, itc_s, ptc_s = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
future_processes, climate_model = None, None
some_queue = None

# Main calculation route
@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    global corn_area, wheat_area, soybeans_area, sg_area, num_of_years
    global energy_value, loan_term, interest, num_wind_turbines, nyear_w, capacity_w, cost_w, degrade_w, wind_factor, num_panel_sets, nyear_s, cost_s, capacity_s, degrade_s, sun_hrs, ptc_w, itc_s, ptc_s
    global aquifier_level, min_aquifier_level
    global future_processes, climate_model
    data = request.get_json()

    # Getting Agriculture Form Value

    corn_area = int(data["agriculture"]["corn_area"])
    wheat_area = int(data["agriculture"]["wheat_area"])
    soybeans_area = int(data["agriculture"]["soybeans_area"])
    sg_area = int(data["agriculture"]["sg_area"])

    # Getting Energy Form Value

    energy_value = int(data["energy"]["energy_value"])
    loan_term = int(data["energy"]["loan_term"])
    interest = int(data["energy"]["interest"])
    num_wind_turbines = int(data["energy"]["num_wind_turbines"])
    nyear_w = int(data["energy"]["nyear_w"])
    capacity_w = int(data["energy"]["capacity_w"])
    cost_w = int(data["energy"]["cost_w"])
    degrade_w = int(data["energy"]["degrade_w"])
    wind_factor = int(data["energy"]["wind_factor"])
    num_panel_sets = int(data["energy"]["num_panel_sets"])
    nyear_s = int(data["energy"]["nyear_s"])
    cost_s = int(data["energy"]["cost_s"])
    capacity_s = int(data["energy"]["capacity_s"])
    degrade_s = int(data["energy"]["degrade_s"])
    sun_hrs = int(data["energy"]["sun_hrs"])
    ptc_w = int(data["energy"]["ptc_w"])
    itc_s = int(data["energy"]["itc_s"])
    ptc_s = int(data["energy"]["ptc_s"])

    # Getting Water Form Value

    aquifier_level = int(data["irrigation"]["aquifier_level"])
    min_aquifier_level = int(data["irrigation"]["min_aquifier_level"])

    # Getting Climate Form Value

    future_processes = data["ClimateData"]["future_processes"]
    climate_model = data["ClimateData"]["climate_model"]

    num_of_years = int(data["numberofyears"]["num_of_years"])

    print("corn_area ---->", corn_area)
    print("wheat_area ---->", wheat_area)
    print("soybeans_area ----->", soybeans_area)
    print("sg_area----->", sg_area)

    print("aquifier_level ---->", aquifier_level)
    print("min_aquifier_level ---->", min_aquifier_level)
    print("num_of_years ------>", num_of_years)

    print("energy_value ---->", energy_value)
    print("loan_term ---->", loan_term)
    print("interest ---->", interest)
    print("num_wind_turbines ---->", num_wind_turbines)
    print("nyear_w ---->", nyear_w)
    print("capacity_w ----->", capacity_w)
    print("cost_w----->", cost_w)
    print("degrade_w----->", degrade_w)
    print("wind_factor ---->", wind_factor)
    print("num_panel_sets ---->", num_panel_sets)
    print("nyear_s ---->", nyear_s)
    print("cost_s ----->", cost_s)
    print("capacity_s----->", capacity_s)
    print("degrade_s----->", degrade_s)
    print("sun_hrs ---->", sun_hrs)
    print("ptc_w ---->", ptc_w)
    print("itc_s ---->", itc_s)
    print("ptc_s ---->", ptc_s)

    # print("future_processes ---->",future_processes)
    print("climate_model ---->", climate_model)

    print(f"set Future_Process '{future_processes}'")

    # Fetching Netlogo Instance

    netlogo = get_netlogo_instance()

    # Agriculture Netlogo Command

    netlogo.command(f"set corn_area {corn_area}")
    netlogo.command(f"set wheat_area {wheat_area}")
    netlogo.command(f"set soybeans_area {soybeans_area}")
    netlogo.command(f"set sg_area {sg_area}")

    # Water Netlogo Command

    netlogo.command(f"set Aquifer_thickness {aquifier_level}")
    netlogo.command(f"set Min_Aq_Thickness {min_aquifier_level}")

    # Energy Netlogo Command

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

    # Climate Netlogo Command

    # netlogo.command(f"set Future_Process {future_processes}")
    # netlogo.command(f"set Climate_Model {climate_model}")
    future_process = "Repeat Historical"
    netlogo.command(f'set Future_Process "{future_process}"')
    netlogo.command(f'set Climate_Model "{climate_model}"')

    # Setup and run the NetLogo model
    netlogo.command("setup")
    netlogo.command(f"repeat {num_of_years} [go]")

    print("Received Data:", data)
    restart()
    return jsonify(data)

# Agriculture calculation route
@app.route("/calculateAgriculture", methods=["GET", "POST"])
def calculate_agriculture():
    print("corn_area ---->", corn_area)
    print("wheat_area ---->", wheat_area)
    print("soybeans_area ----->", soybeans_area)
    print("sg_area----->", sg_area)
    print("num_of_years ------>", num_of_years)

    print("Successfully Hiting the Agriculture Chart API")

    crop_production_img = crop_production_calculation()
    net_calc_img = net_income_calculation()

    result = {"crop_production_img": crop_production_img, "net_calc_img": net_calc_img}

    print("Agriculture", result)

    return jsonify(result)


# Water calculation route
@app.route("/calculateIrrigation", methods=["GET", "POST"])
def calculate_irrigation():
    print("aquifier_level ---->", aquifier_level)
    print("min_aquifier_level ---->", min_aquifier_level)

    crop_groundwater_irrigation_data_for_img = crop_groundwater_irrigation()

    groundwater_level_data_img = groundwater_level()

    result = {
        "crop_groundwater_irrigation_data_for_img": crop_groundwater_irrigation_data_for_img,
        "groundwater_level_data_img": groundwater_level_data_img,
    }

    print("Water", result)

    return jsonify(result)


# Energy calculation route
@app.route("/calculateEnergy", methods=["GET", "POST"])
def calculate_energy():
    print("energy_value ---->", energy_value)
    print("loan_term ---->", loan_term)
    print("interest ---->", interest)
    print("num_wind_turbines ---->", num_wind_turbines)
    print("nyear_w ---->", nyear_w)
    print("capacity_w ----->", capacity_w)
    print("cost_w----->", cost_w)
    print("degrade_w----->", degrade_w)
    print("wind_factor ---->", wind_factor)
    print("num_panel_sets ---->", num_panel_sets)
    print("nyear_s ---->", nyear_s)
    print("cost_s ----->", cost_s)
    print("capacity_s----->", capacity_s)
    print("degrade_s----->", degrade_s)
    print("sun_hrs ---->", sun_hrs)
    print("ptc_w ---->", ptc_w)
    print("itc_s ---->", itc_s)
    print("ptc_s ---->", ptc_s)

    farm_energy_production_img_data = farm_energy_production_calculation()

    energy_net_calc_img_data = energy_net_income_calculation()

    result = {
        "farm_energy_production_img_data": farm_energy_production_img_data,
        "energy_net_calc_img_data": energy_net_calc_img_data,
    }

    print("Energy", result)

    return jsonify(result)


# Climate calculation route
@app.route("/calculateClimate", methods=["GET", "POST"])
def calculate_climate():
    print("future_processes ---->", future_processes)
    print("climate_model ---->", climate_model)

    crop_income_img = crop_income_calculation()

    insur_income_calc_img = insurance_income_calculation()

    result = {
        "crop_income_img": crop_income_img,
        "insur_income_img": insur_income_calc_img,
    }

    print("Climate", result)

    return jsonify(result)

# Function to start Flask app
def start_flaskapp():
    app.run(host="0.0.0.0", port=5000)

# Restart route
@app.route("/restart", methods=["GET", "POST"])
def restart():
    some_queue = queue.Queue()
    some_queue.put("something")
    print("Restarted successfully")

# Download file route
@app.route("/download")
def download_file():
    file_path = "/Users/pratiknikam/Documents/FEWCalc/workspace/FinalCode/NetLogo-main/NetLogo-main/netlogo/1_Corn_inputs.csv"
    return send_file(file_path, as_attachment=True)

# Initialize some_queue
some_queue = None

# Main block to start the Flask app
if __name__ == "__main__":
    q = Queue()
    p = Process(target=start_flaskapp, args=(q,))
    p.start()
    while True:
        if q.empty():
            time.sleep(1)
        else:
            break
    p.terminate()
    args = [sys.executable] + sys.argv
    subprocess.call(args)
