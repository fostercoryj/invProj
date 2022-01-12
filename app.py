from flask import Flask, request, render_template, session, redirect
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = "TylerStuff"

#pick up packet number and forward to scan page
@app.route("/")
def index():
    return render_template("main.html")

#grab excel data and barcode data, forward to output template
@app.route("/scan", methods=['POST'])
def scan():
    packetNum = request.form['f_packet']
    data = pd.read_excel ("C:\\Users\\Cory Foster\\OneDrive - OMECorp\\DISPATCH\MASTER INSTALL LIST.xlsx", sheet_name="GENESIS", index_col=6) 
    df = pd.DataFrame(data)
    df1 = df.set_index(['PACKET'])
    dTable = (df1.loc[int(packetNum)])
    session['dTable'] = dTable.to_dict
    session['packetNum'] = packetNum
    return render_template("scan.html", dTable = dTable, packetNum = packetNum)
#narrow down more specific columns to pull?

#build output template with barcode data and imported excel data
@app.route("/pdfTemplate", methods=['GET'])
def pdfTemplate():
    dTable = session['dTable']
    dTable = pd.DataFrame(dTable)
    print('PDF page: '+dTable)
    return render_template ("pdfTemplate.html", dTable = dTable)

if __name__ == "__name__":
    app.run(debug=True)