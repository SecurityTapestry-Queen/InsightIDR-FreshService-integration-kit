import base64

string1 = "b64"

string2 = base64.b64decode(string1).decode("UTF-8")

string3 = "string"

print(string2)



if string2 == string3:
    print("match")
else:
    print("fail")