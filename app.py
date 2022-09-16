# Import library for Pandas
import pandas as pd

# Import library for Flask
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

#Fungsi penjumlahan
def jumlah(input1,input2):
  return input1 + input2

#API Route process penjumlahan dari form input
@swag_from("docs/add_processing.yaml", methods=['POST'])
@app.route('/add-processing', methods=['POST'])
def add_processing():

    # Get number file
    num1 = request.form.get('number1')
    num2 = request.form.get('number2')
    
    # Calculation Process
    result = jumlah(int(num1),int(num2))

    # Define API response
    json_response = {
            'status_code': 200,
            'description': "sudah dilakukan penjumlahan",
            'result': result,
            'number1': int(num1),
            'number2': int(num2),
        }

    response_data = jsonify(json_response)
    return response_data

# Define endpoint for "upload file CSV"
@swag_from("docs/add_processing_file.yaml", methods=['POST'])
@app.route('/add-processing-file', methods=['POST'])
def add_processing_file():

    # Upladed file
    file = request.files['file']

    # Import file csv ke Pandas
    df = pd.read_csv(file,header=0)

    df['hasil'] = df.apply(lambda row : jumlah(row['number1'],row['number2']), axis = 1)
    
    # Get result from file in "List" format
    result = df.hasil.to_list()

    # Define API response
    json_response = {
        'status_code': 200,
        'description': "sudah dilakukan penjumlahan",
        'data': result,
    }
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)