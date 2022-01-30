import requests

base_url = "http://127.0.0.1:5000/question/"

response = requests.get(base_url + "1").json()
print(response)

response = requests.delete(base_url + "1").json()
print(response)

response = requests.get(base_url + "1").json()
print(response)

response = requests.put(base_url + "500", data={
    "frage": "Wer ist der Beste",
    "difficulty":1,
    "antworten": ["Alex", "Marcel", "Simon", "Dietz"],
    "rightanswer":0
}).json()
print(response)

response = requests.get(base_url + "500").json()
print(response)

response = requests.patch(base_url + "501", data={
    "frage": "Wer ist der Beste?",
    "difficulty":1,
    "antworten": ["Alex", "Marcel", "Simon", "Dietzi"],
    "rightanswer":0
}).json()
print(response)



