from flask import Blueprint, render_template,request,jsonify
import sqlite3
app_ajustes = Blueprint('app_ajustes', __name__)









@app_ajustes.route('/') 
def index():

    return render_template('ajustes.html')