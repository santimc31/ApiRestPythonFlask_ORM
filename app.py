from flask import Flask
from extensions import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registrar blueprints
    from routes.cliente_routes import cliente_bp
    app.register_blueprint(cliente_bp)

    # Crear tablas automáticamente
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
