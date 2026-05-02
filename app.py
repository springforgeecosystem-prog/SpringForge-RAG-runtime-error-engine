import time
from flask import Flask, request, jsonify
from llm.pipeline import run

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "running"})

@app.route("/analyze-error", methods=["POST"])
def analyze_error():
    payload = request.json
    
    # print payload received from frontend for debugging
    print("Received payload from frontend:", payload)
    
    error = payload["error"]
    code_context = payload["code_context"]
    use_rag = payload.get("use_rag", True)
    
    env_data = payload.get("environment", {})
    print("Received env_data keys:", list(env_data.keys()) if isinstance(env_data, dict) else type(env_data))

    retries = 3
    last_error = None
    for attempt in range(retries):
        try:
            result = run(error, code_context, env_data=env_data, use_rag=use_rag)
            return jsonify(result)
        except Exception as exc:
            last_error = exc
            print(f"analyze_error attempt {attempt + 1}/{retries} failed: {exc}")
            if attempt < retries - 1:
                time.sleep(1)
                continue
            break
    
    return jsonify({"error": "Internal server error", "details": str(last_error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
