from flask import Flask, request, jsonify
from rag.pipeline import run

app = Flask(__name__)

@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    payload = request.json

    error = payload["error"]
    code_context = payload["code_context"]

    result = run(error, code_context)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
