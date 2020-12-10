from flask import Flask
from flask_cors import CORS

import os

from backend.routes import learning, match


# flask setup
app = Flask(__name__)
CORS(app)
app.register_blueprint(match.get_blueprint())
app.register_blueprint(learning.get_blueprint())


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
