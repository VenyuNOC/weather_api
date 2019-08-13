import waitress
from backend import app


waitress.serve(app)