from flask import Flask, jsonify, request
import random
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.lines import Line2D
matplotlib.use('agg')
import seaborn as sns
import pymongo
from pymongo import MongoClient
# import boto3
import io

 
app = Flask(__name__)

client = MongoClient()
portfolio_sims_db = client["portfolio_sims"]
sims_col = portfolio_sims_db["sims"]

folder_path = "..\\portfolio_main\\static\\imgs"

def make_graph(mean_list, error_list, username, portfolio_name, fig_name):

          
    
    n_groups = len(mean_list)

    year_lables = [x+1 for x in range(len(mean_list))]

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}


    fig, ax = plt.subplots()
    plt.bar(index, mean_list, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=error_list,
                 error_kw=error_config)
    
    plt.xlabel('Year')
    plt.ylabel('$ Value') 
    plt.xticks(index, year_lables)


    custom_lines = [Line2D([0], [0], color="b", lw=4),
                Line2D([0], [0], color="black", lw=4)]
   

    plt.legend(custom_lines, ['$', 'Standard Deviation'], loc="upper left")
   
    path_add = f"\\{username}-{portfolio_name}-{fig_name}.png"
    filepath = folder_path + path_add
    
    plt.savefig(filepath)
    plt.clf()
    plt.cla()



@app.route("/analysis", methods=["GET", "POST"])
def analysis():

    try:
        username = request.args.get("username")
        portfolio_name = request.args.get("portfolio_name")
        

        sim_results = sims_col.find_one({"username": username, "portfolio_name": portfolio_name})
        
        inflation_results = sim_results["Inflation"]

        nominal_bonds_results = sim_results["bond_vals_nominal"]
        real_bonds_results = sim_results["bond_vals_real"]

        nominal_cash_results = sim_results["cash_vals_nominal"]
        real_cash_results = sim_results["cash_vals_real"]

        nominal_stock_results = sim_results["stock_vals_nominal"]
        real_stock_results = sim_results["stock_vals_real"]

        nominal_portfolio_results = sim_results["portfolio_vals_nominal"]
        real_portfolio_results = sim_results["portfolio_vals_real"]


        inflation_mean_list = []
        inflation_std_list = []

        stocks_nominal_mean_list = []
        stocks_nominal_std_list = []
        stocks_real_mean_list = []
        stocks_real_std_list = []

        bonds_nominal_mean_list = []
        bonds_nominal_std_list = []
        bonds_real_mean_list = []
        bonds_real_std_list = []

        cash_nominal_mean_list = []
        cash_nominal_std_list = []
        cash_real_mean_list = []
        cash_real_std_list = []

        portfolio_nominal_mean_list = []
        portfolio_nominal_std_list = []
        portfolio_real_mean_list = []
        portfolio_real_std_list = []

        list_of_lists = []

        for x in range(len(inflation_results)):

            # inflation 
            year_inflation = np.array(inflation_results[x])
            year_inflation_mean = np.mean(year_inflation)
            year_inflation_std = np.std(year_inflation)

            inflation_mean_list.append(year_inflation_mean)
            inflation_std_list.append(year_inflation_std)

            # stocks nominal
            year_stocks_nominal = np.array(nominal_stock_results[x])
            year_stocks_nominal_mean = np.mean(year_stocks_nominal)
            year_stocks_nominal_std = np.std(year_stocks_nominal)

            stocks_nominal_mean_list.append(year_stocks_nominal_mean)
            stocks_nominal_std_list.append(year_stocks_nominal_std)


            # stocks real
            year_stocks_real = np.array(real_stock_results[x])
            year_stocks_real_mean = np.mean(year_stocks_real)
            year_stocks_real_std = np.std(year_stocks_real)

            stocks_real_mean_list.append(year_stocks_real_mean)
            stocks_real_std_list.append(year_stocks_real_std)

            # bonds nominal
            year_bonds_nominal = np.array(nominal_bonds_results[x])
            year_bonds_nominal_mean = np.mean(year_bonds_nominal)
            year_bonds_nominal_std = np.std(year_bonds_nominal)

            bonds_nominal_mean_list.append(year_bonds_nominal_mean)
            bonds_nominal_std_list.append(year_bonds_nominal_std)

            # bonds real
            year_bonds_real = np.array(real_bonds_results[x])
            year_bonds_real_mean = np.mean(year_bonds_real)
            year_bonds_real_std = np.std(year_bonds_real)

            bonds_real_mean_list.append(year_bonds_real_mean)
            bonds_real_std_list.append(year_bonds_real_std)

            # cash nominal
            year_cash_nominal = np.array(nominal_cash_results[x])
            year_cash_nominal_mean = np.mean(year_cash_nominal)
            year_cash_nominal_std = np.std(year_cash_nominal)

            cash_nominal_mean_list.append(year_cash_nominal_mean)
            cash_nominal_std_list.append(year_cash_nominal_std)

            # cash real
            year_cash_real = np.array(real_cash_results[x])
            year_cash_real_mean = np.mean(year_cash_real)
            year_cash_real_std = np.std(year_cash_real)

            cash_real_mean_list.append(year_cash_real_mean)
            cash_real_std_list.append(year_cash_real_std)

            # portfolio nominal
            year_portfolio_nominal = np.array(nominal_portfolio_results[x])
            year_portfolio_nominal_mean = np.mean(year_portfolio_nominal)
            year_portfolio_nominal_std = np.std(year_portfolio_nominal)

            portfolio_nominal_mean_list.append(year_portfolio_nominal_mean)
            portfolio_nominal_std_list.append(year_portfolio_nominal_std)

            # portfolio real
            year_portfolio_real = np.array(real_portfolio_results[x])
            year_portfolio_real_mean = np.mean(year_portfolio_real)
            year_portfolio_real_std = np.std(year_portfolio_real)

            portfolio_real_mean_list.append(year_portfolio_real_mean)
            portfolio_real_std_list.append(year_portfolio_real_std)

        
        list_of_lists = [
            (stocks_nominal_mean_list, stocks_nominal_std_list, "stocks-nominal"),
            (stocks_real_mean_list, stocks_real_std_list, "stocks-real"),
            (bonds_nominal_mean_list, bonds_nominal_std_list, "bonds-nominal"),
            (bonds_real_mean_list, bonds_real_std_list, "bonds-real"),
            (cash_nominal_mean_list, cash_nominal_std_list, "cash-nominal"),
            (cash_real_mean_list, cash_real_std_list, "cash-real"),
            (portfolio_nominal_mean_list, portfolio_nominal_std_list, "portfolio-nominal"),
            (portfolio_real_mean_list, portfolio_real_std_list, "portfolio-real"),
            ]
        
        for y in list_of_lists:
            make_graph(y[0], y[1], username, portfolio_name, y[2])

        results = {"success": 1}

    except:

        results = {"success": 0, "error_msg": "Something has gone wrong in the matrix"}
      

    return jsonify({"results": results})




if __name__ == "__main__":
    app.run(port=8004, debug=True)