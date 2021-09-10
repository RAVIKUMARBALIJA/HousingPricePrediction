from flask import Flask, request, render_template, jsonify
from numpy.core.numeric import True_
import pandas as pd
from kafka import KafkaProducer
import json
from threading import Thread
from werkzeug.utils import redirect
from random import randint
# from pyhive import hive

import pickle

from preprocessor import *
from transformer_utils import perform_predictions

import os
path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates")
app.config.from_pyfile('application.cfg', silent=True)
# hive_engine = hive.Connection(
#     host = app.config["HIVE_HOST"], 
#     port = app.config["HIVE_PORT"],
#     username = app.config["HIVE_USERNAME"],
#     password = app.config["HIVE_PASSWORD"],
# )


producer = KafkaProducer(
    bootstrap_servers = app.config["KAFKA_SERVER"],
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template(
            "test_model.html",
        )

def df_send_kafka(df, test_id=None):
    print('send thread started')
    for data in json.loads(df.to_json(orient="records")):
        if test_id:
            data["test_id"] = test_id
        producer.send(topic=app.config["TOPIC"], value=data)


@app.route("/test_report", methods=["GET", "POST"])
def test_model():
    if request.method == "GET":
        return render_template(
            "test_model.html",
        )
    elif request.method == "POST":
        test_set = pd.read_csv(request.files["file"])
        test_id = str(randint(0,99999999999))+str(randint(0,99999999999))+str(randint(0,99999999999))
        thread = Thread(target=df_send_kafka, args=(test_set,test_id))
        thread.start()
        return redirect("/test_report?test_id="+test_id)


@app.route("/house_price_predict", methods=["GET", "POST"])
def house_price_predict():
    predict_sale = ""
    requst_data = dict(request.form)
    columns = pickle.load(open("data/columns", "rb"))
    form_fields = json.load(open(path+"/model_form.json"))
    form_fields_new = []
    for obj in form_fields:
        if obj["field"] not in columns:
            continue
        if requst_data:
            obj["value"] = requst_data.get(obj["field"], "")
        if obj.get("type") == "str":
            obj["options"] = globals()[f'lst_{obj["field"]}_cat']
        form_fields_new.append(obj)
    
    if request.method == "POST":
        line = [requst_data[col] for col in columns]
        producer.send(topic=app.config["TOPIC"], value=line)
        predict_sale = perform_predictions(line)
    return render_template(
        "houseprice.html",
        form_fields=form_fields_new,
        predict_sale=predict_sale
    )

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)