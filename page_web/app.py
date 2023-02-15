from flask import Flask, jsonify, request   # pip install flask
from flask_cors import CORS                 # pip install -U flask-cors

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes, sinon le site n'a pas accès à la moyenne

moyenne = [1] * 18

@app.route('/moyenne', methods=['GET', 'POST'])
def update_moyenne():
    global moyenne
    if request.method == 'POST':
        moyenne = request.get_json()
        return jsonify(moyenne)
    else:
        return jsonify(moyenne)

if __name__ == '__main__':
    app.run(host="0.0.0.0")