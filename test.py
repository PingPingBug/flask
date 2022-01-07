import requests

json= {
    "name": "bill",
    "birthdate" : "01/01/2002",
    "status" : "Active"
}
r = requests.post("http://127.0.0.1:5000/profiles", json=json)

print(r)