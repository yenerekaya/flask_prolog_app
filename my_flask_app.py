from flask import Flask, jsonify
from pyswip import Prolog
import os

app = Flask(__name__)


prolog = Prolog()


current_dir = os.path.dirname(os.path.abspath(__file__))  
prolog_file_path = os.path.join(current_dir, "prolog_rules.pl")

if not os.path.exists(prolog_file_path):
    raise FileNotFoundError(f"Prolog dosyası bulunamadı: {prolog_file_path}")
prolog.consult(prolog_file_path)


@app.route("/")
def index():
    try:
        
        result = list(prolog.query("merhaba(Mesaj)"))
        if result:
            message = result[0]["Mesaj"]
            if isinstance(message, bytes):  
                message = message.decode("utf-8")
        else:
            message = "Prolog'tan mesaj alınamadı."
    except Exception as e:
        message = f"Prolog hatası: {str(e)}"


    return jsonify({"message": message})



if __name__ == "__main__":
    app.run(debug=True, port=5000)
