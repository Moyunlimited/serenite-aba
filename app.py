from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import db

# Import Blueprints
from routes.auth import auth_bp
from routes.study_guide import guide_bp
from routes.quiz import quiz_bp
from routes.progress import progress_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_VERIFY_SUB'] = False

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)  # ✅ assign to a variable (not required but standard)

# ✅ Proper CORS setup
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "https://serenite-aba-front-c7xn.vercel.app",  # ✅ Your Vercel frontend
])

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(guide_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(progress_bp)  

@app.route("/")
def index():
    return {"message": "Serenité ABA API is running."}

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    app.run(debug=True)
