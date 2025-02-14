from flask import Blueprint, render_template,request,jsonify
import sqlite3
app_reposicion = Blueprint('app_reposicion', __name__)

@app_reposicion.route('/') 
def index():

    return render_template('reposicion.html')