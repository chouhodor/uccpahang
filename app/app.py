
import os
import json
import gspread
import datetime
from flask import Flask, render_template, jsonify, request, abort
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)


scopes = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
client = gspread.authorize(creds)

'''
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('ucc-pahang.json', scope)
client = gspread.authorize(creds)


spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OQ8WUVFJJxKEkve0BvUi7t4G1K2d_RAB_YtE1chzKws")
sheet = spreadsheet.sheet1
currentdate = datetime.datetime.now()
'''

@app.route('/', methods=['GET'])
def index():
    
    sheets = sheet
    currentdates = currentdate
    x = currentdates.strftime("%d %B %Y")

    return render_template('index.html',  
    sheets = sheets,
    x = x)

if __name__ == '__main__':
    app.run(debug=True)