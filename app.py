from flask import Flask, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Ayush Kanade", "branch": "CSE"},
    {"id": 2, "name": "Rohan Patil", "branch": "CSE"},
    {"id": 3, "name": "Sneha Joshi", "branch": "CSE"},
]


@app.route("/")
def home():
    return "<h1>Student Info App - Version 1</h1>"


@app.route("/students")
def get_students():
    return jsonify(students)


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)