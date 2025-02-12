from flask import Blueprint, render_template, request,redirect,session,flash, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
import bcrypt

loggin_bp = Blueprint('loggin', __name__)

# Función para leer el archivo Excel existente



from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from datetime import timedelta

loggin_bp = Blueprint('loggin', __name__)

@loggin_bp.route('/', methods=['GET', 'POST'])
def loggin():
    if request.method == "POST":
        usuario = request.form['username'].upper()
        contraseña = request.form['password']
        recordar = request.form.get('remember')

        try:
            if usuario and contraseña:
                # Recupera los datos del usuario
                user = conexion_sqlite.users(usuario)
                if user:
                    hashed_password = user[0][3]  # El hash almacenado en la base de datos
                    # Verifica la contraseña ingresada contra el hash almacenado
                    if bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password):
                        # Establece las variables de sesión
                        session['username'] = user[0][2]
                        session['rol'] = user[0][5]

                        if recordar:
                            session.permanent = True
                            loggin_bp.permanent_session_lifetime = timedelta(days=30)
                        
                        if session['rol'] == 3:
                            return redirect(url_for('marcas.departamentos_lista'))
                        else:
                            return redirect(url_for('index.index'))

                    else:
                        flash('Credenciales incorrectas')
                else:
                    flash('Usuario no encontrado')
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}")
    return render_template("loggin.html")


@loggin_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada')
    return redirect(url_for('loggin.loggin'))



