from flask_app import app
from flask_app.controllers import user_routes, window_routes
from flask_app.models import user_extractions, window_extractions



if __name__=='__main__':
    app.run(debug=True)