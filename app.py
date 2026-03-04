from flask import Flask, request, jsonify
from llm.pipeline import run

app = Flask(__name__)

@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    payload = request.json
    
    # print payload received from frontend for debugging
    print("Received payload from frontend:", payload)
    
    error = payload["error"]
    code_context = payload["code_context"]
    use_rag = payload.get("use_rag", True)
    
    env_data = payload.get("env_data", {})
    result = run(error, code_context, env_data=env_data, use_rag=use_rag)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
