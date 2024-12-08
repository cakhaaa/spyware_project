from flask import Flask, request

app = Flask(__name__)

# Endpoint untuk menerima data teks
@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.form.to_dict()
    print("Data received:", data)
    with open("received_data.txt", "a") as f:
        f.write(str(data) + "\n")
    return "Data received successfully", 200

# Endpoint untuk menerima file
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    file.save(f"./uploads/{file.filename}")
    print(f"File {file.filename} saved.")
    return "File received successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
