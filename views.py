
from flask import Flask, render_template, jsonify, request
from . import app
from . import owidutils


parameters = ["co2_growth_prct", 
            "co2_growth_abs", 
            "co2", 
            "trade_co2", 
            "co2_per_capita",
            "share_global_co2",
            "cumulative_co2",
            "share_global_cumulative_co2",
            "co2_per_gdp",
            "energy_per_capita",
            "energy_per_gdp"
            ]


@app.route("/")
def co2():

    # Get request parameters and check validity
    args = request.args

    param = args.get("param",parameters[0], type= str)

    if not param in parameters:
        return jsonify({ "Error": "parameter is not valid. Please select from the list on the appropriate page!"})

    
    options, start_year, latest_year = owidutils.get_owid_param_options(param)
    
    return render_template("map.html", 
                                        params = parameters,
                                        options= options,
                                        param_q = param,
                                        start_year = start_year,
                                        latest_year = latest_year
                                        )

@app.route("/top")
def topemissions():
    """
    Show top 10 countries by different selectable criteria e.g. total, cum, per capita etc over time

    Runs an animation and shows change over the years

    """

    # Get request parameters and check validity
    args = request.args

    param = args.get("param",parameters[0], type= str)

    if not param in parameters:
        return jsonify({ "Error": "parameter is not valid. Please select from the list on the appropriate page!"})

    
    dataset, start_year, latest_year = owidutils.get_owid_top2(param)

    return render_template("top.html", 
                                        params = parameters,
                                        dataset= dataset,
                                        param_q = param,
                                        start_year = start_year,
                                        latest_year = latest_year
                                        )
