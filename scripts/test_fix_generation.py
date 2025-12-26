import requests, json

with open("data/sample_payload.json") as f:
    payload = json.load(f)

res = requests.post("http://127.0.0.1:5000/analyze-error", json=payload)

print(res.status_code)
print(res.json())
