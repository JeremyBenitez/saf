from flask import Blueprint, render_template, request,redirect,session,flash,url_for
from ..querys_sqlite_data import conexion_sqlite

from datetime import datetime,timedelta
import pandas as pd


tendecias_bp = Blueprint('tendencias', __name__)

@tendecias_bp.route('/',methods=['GET', 'POST'])
def tendencias():
  
   
    # Renderizamos la plantilla y pasamos las variables necesarias
    return render_template('tendencias.html')