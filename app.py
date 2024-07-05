from flask import Flask, request, jsonify, abort
from flask import Flask, render_template, request, send_from_directory, abort
import os
import pandas as pd

app = Flask(__name__)

# Define the path to the Excel file
EXCEL_FILE_PATH = "C:/Users/praveenkumarnadaraja/OneDrive - virtualemployee P Ltd/Desktop/data.xlsx"
BASE_DIR="C:/Users/praveenkumarnadaraja/OneDrive - virtualemployee P Ltd/Desktop"

# Ensure the Excel file exists
if not os.path.exists(EXCEL_FILE_PATH):
    df = pd.DataFrame()
    df.to_excel(EXCEL_FILE_PATH, index=False)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        
        # Load the existing Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Create a DataFrame from the incoming data
        incoming_df = pd.DataFrame([data])

        # Merge the incoming DataFrame with the existing DataFrame
        df = pd.concat([df, incoming_df], ignore_index=True).fillna('')

        # Save the updated DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)

        return jsonify({"message": "Data added successfully"}), 200
    else:
        return abort(400)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    files = []
    for filename in os.listdir(abs_path):
        filepath = os.path.join(abs_path, filename)
        size = os.path.getsize(filepath) if os.path.isfile(filepath) else 0
        files.append((filename, size))
    
    return render_template('index.html', files=files, current_path=req_path)

if __name__ == '__main__':
    app.run(debug=True)
