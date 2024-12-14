import os
import uuid
from flask import Blueprint, request
from app.dto import create_response
from app.service import not_allowed, read_image, predict_image

api = Blueprint("api", __name__)

# Variabel global untuk menyimpan response resep
recipe_response = []

@api.route('/ping', methods=['GET'])
def ping():
    return create_response(status="success", message="server running",)

# Endpoint untuk POST gambar dan mendapatkan hasil prediksi
@api.route('/predict', methods=['POST'])
def predict():
    global recipe_response  # Menandakan bahwa kita menggunakan variabel global

    if 'input_image' not in request.files:
        return create_response(message="input image invalid", status="error", status_code=400)
    
    file = request.files['input_image']
    if file.filename == '' or not_allowed(file.filename):
        return create_response(message="input image invalid", status="error", status_code=400)
    
    try:
        # Membaca gambar
        image_tensor = read_image(file)
        
        # Melakukan prediksi pada gambar
        recipe_response = predict_image(image_tensor)
        for recipe in recipe_response:
            recipe["unique_id"] = str(uuid.uuid4())  # Menambahkan unique_id pada setiap resep
        
        print("Predicted Recipe Response:", recipe_response)  # Debugging: Print hasil prediksi
        
        return create_response(data=recipe_response, status="success", message="image predicted successfully")
    
    except Exception as e:
        print("error : " + str(e))
        return create_response(message="internal server error", status="error", status_code=500)

# Endpoint untuk GET resep berdasarkan unique_id
@api.route('/get', methods=['GET'])
def get_recipe_by_id():
    try:
        # Mendapatkan unique_id dari query parameter
        unique_id = request.args.get('unique_id')
        
        if not unique_id:
            return create_response(message="unique_id is required", status="error", status_code=400)
        
        print("Received unique_id:", unique_id)  # Debugging: Print unique_id yang diterima
        
        # Mencari resep berdasarkan unique_id dalam recipe_response
        recipe = next((item for item in recipe_response if str(item["unique_id"]) == str(unique_id)), None)
        
        if recipe is None:
            return create_response(message="recipe not found", status="error", status_code=404)
        
        return create_response(data=recipe, status="success", message="recipe retrieved successfully")
    
    except Exception as e:
        print("error : " + str(e))
        return create_response(message="internal server error", status="error", status_code=500)
