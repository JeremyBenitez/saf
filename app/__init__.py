from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'deiker040601'
    # Registro de blueprints
    from .app_tiendas.routes import tiendas_bp
    from .busqueda_fechas.routes import fechas_bp
    from .busqueda_marcas.routes import marcas_bp
    from .index.routes import index_bp
    from .loggin.routes import loggin_bp
    from .tendencias.routes import tendecias_bp
    from .inventario.routes import inventario_bp
    from .appi_create.routes import appi
    from .app_resumen2024.routes import app_resumen
    
    app.register_blueprint(loggin_bp, url_prefix='/')
    app.register_blueprint(index_bp, url_prefix='/index')
    app.register_blueprint(tiendas_bp, url_prefix='/tiendas')
    app.register_blueprint(fechas_bp, url_prefix='/fechas')
    app.register_blueprint(marcas_bp, url_prefix='/marcas')
    app.register_blueprint(tendecias_bp, url_prefix='/tendencias')
    app.register_blueprint(inventario_bp, url_prefix='/inventario')
    app.register_blueprint(appi, url_prefix='/crear')
    app.register_blueprint(app_resumen, url_prefix='/2024')
    return app
