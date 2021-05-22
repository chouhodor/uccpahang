
import os
import json
import gspread
import pprint
from datetime import datetime
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)
app.config['SECRET_KEY'] = 'uccpahangtopsecret'



#live test
scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
client = gspread.authorize(creds)
##live test
'''
#local test
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('ucc-pahang.json', scope)
client = gspread.authorize(creds)
##local test
'''

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/14vFutdJuHcszQKIpAcqyQ106AtBSebeghrRxTp9ittQ")
sheet = spreadsheet.sheet1

now = datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")

def maxhour (h):
    if h > 24:
        return 24
    else:
         return h

def bor_color (color):
    red = 'red'
    orange = 'orange'
    white = 'white'
    yellow = 'yellow'

    if color >= 90:
        return red
    elif 75 <= color <= 89.9:
        return orange
    elif 50 <= color <= 74.9:
        return yellow
    else:
        return white


@app.route('/', methods=['POST','GET'])
def index():

    maxhours=maxhour
    bor_colors = bor_color
      
    dict_sheet = sheet.get_all_records()
    date_times = date_time
    
    return render_template('index.html',  
    dict_sheet = dict_sheet,
    date_times=date_times,
    maxhours=maxhours,
    bor_colors=bor_colors,
    )

@app.route("/update")
def update():
    return render_template('update.html')

@app.route('/result', methods = ['POST'])
def result():

    date_times = date_time
    pkrc = request.form['pkrc']
    a_male = int(request.form['a_male'])
    a_female = int(request.form['a_female'])
    passkey = request.form['passkey']
    
    a_male_dict = { 'sukpa' : 'C20', 'illkkm' : 'C21', 'ikpkt' : 'C22', 'hjka' : 'C23', 'kuipsas' : 'C24', 'penjara' : 'C25'}
    a_female_dict = { 'sukpa' : 'D20', 'illkkm' : 'D21', 'ikpkt' : 'D22', 'hjka' : 'D23', 'kuipsas' : 'D24', 'penjara' : 'D25'}
    passkey_dict = { 'sukpa' : '7789', 'illkkm' : '5526', 'ikpkt' : '1297', 'hjka' : '3654', 'kuipsas' : '8794', 'penjara' : '6779'}
    date_times_dict = { 'sukpa' : 'F20', 'illkkm' : 'F21', 'ikpkt' : 'F22', 'hjka' : 'F23', 'kuipsas' : 'F24', 'penjara' : 'F25'}

    if passkey == passkey_dict[pkrc]:
        sheet.update(a_male_dict[pkrc] , a_male)
        sheet.update(a_female_dict[pkrc] , a_female)
        sheet.update(date_times_dict[pkrc], date_times)
        status = 'Success'
    else:
        status = 'Error'

    
    return render_template('result.html',
    date_times = date_times,
    pkrc=pkrc,
    a_male=a_male,
    a_female=a_female, 
    a_male_dict=a_male_dict, 
    a_female_dict=a_female_dict,
    passkey=passkey,
    passkey_dict=passkey_dict,
    date_times_dict=date_times_dict,
    status=status
    )



    


   
    

    

    

if __name__ == '__main__':
    app.run(debug=True)