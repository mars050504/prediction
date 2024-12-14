from app import create_app
from flask import jsonify

app = create_app()

# Tambahkan route untuk menampilkan pesan "Welcome to Recipe API"
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Recipe API"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
