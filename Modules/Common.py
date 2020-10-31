import os
import argparse
import json
import csv

def check_positive(x=2):
    temp_x = int(x)
    if temp_x < 0:
        raise argparse.ArgumentTypeError(f"{temp_x} must be a valid positive number")
    return temp_x

def check_output(output):
    temp_output = output + "/"
    try:
        if not os.path.exists(temp_output):
            os.makedirs(output)
    except:
        raise argparse.ArgumentTypeError(f"{temp_output} check the directory and try again")
    return temp_output

def check_format(form):
    if form not in ["csv", "json"]:
        form = "csv"

    if form is not None:
        form = form.lower()

    return form

def check_config(config):
    config_file = load_config(config)

    if "driver" not in config_file:
        raise argparse.ArgumentTypeError("Missing driver path in the configuration file")

    if "credentials" not in config_file:
        raise argparse.ArgumentTypeError("Missing discord credentials in the configuration file")
    else:
        if "email" not in config_file["credentials"]:
            raise argparse.ArgumentTypeError("Missing discord email in the configuration file")
        if "passw" not in config_file["credentials"]:
            raise argparse.ArgumentTypeError("Missing discord password in the configuration file")
    
    if "discord" not in config_file:
        raise argparse.ArgumentTypeError("Missing discord information in the configuration file")
    else:
        if len(config_file["discord"]) == 0:
            raise argparse.ArgumentTypeError("Missing discord servers and channels in the configuration file")
        else:
            for idx, discord in enumerate(config_file["discord"]):
                if "server" not in discord:
                    raise argparse.ArgumentTypeError(f"Missing discord server for item {idx} the configuration file")
                if "channels" not in discord:
                    raise argparse.ArgumentTypeError(f"Missing discord channels for item {idx} the configuration file")
                else:
                    if len(discord["channels"]) == 0:
                       raise argparse.ArgumentTypeError(f"Missing discord channels for item {idx} the configuration file")                    
                    for channel in discord["channels"]:
                        if channel == "":
                            raise argparse.ArgumentTypeError(f"Discord channels cannot be empty in the configuration file")
    
    return config

def load_config(path):
    try:
        with open(path, 'r') as j:
            return json.load(j)
    except:
        raise Exception("Error reading config file, please ensure the correct path is being used")

def to_file(data, output, fmt):
    if fmt == "csv":
        if not os.path.exists(output):
            data.to_csv(output, header=True,index=False, 
                doublequote=True, quoting=csv.QUOTE_NONNUMERIC, mode="w")
        else:
            data.to_csv(output, header=False,index=False, 
                    doublequote=True, quoting=csv.QUOTE_NONNUMERIC, mode="a")
    else:
        if not os.path.exists(output):
            data.to_json(output,orient="records", lines=True)
        else:
            open(output, "a").write(data.to_json(orient="records", lines=True))