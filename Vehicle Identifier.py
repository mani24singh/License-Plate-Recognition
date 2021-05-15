import json
import base64
import requests
from authKey import SECRET_KEY

IMAGE_PATH = 'database/10.jpg'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data=img_base64)

num_plate = (json.dumps(r.json(), indent=2))
info = (list(num_plate.split("candidates")))
print(info)
plate = info[1]
plate = plate.split(',')[0:3]
p = plate[1]
p1 = p.split(":")
number = p1[1]
number = number.replace('"', '')
number = number.lstrip()
print(number)

df = pd.read_csv("car_details.csv")

if number in df["Vehicle Number"].values:
    dff = df.set_index("Vehicle Number")
    print(dff.loc[number])
else:
    print("Information Doesn't Exist For! " + number + ", Please Add: \n \n")
    time.sleep(1)
    vnum = number
    vmake = input("Enter car Name ")
    vtype = input("Enter model of Your Car: ")
    state = input("Enter State: ")

    details = pd.DataFrame([[vmake, vnum, vtype, state]],
                           columns=['Vehicle Make', 'Vehicle Number', 'Vehicle Type', 'State'])
    df = pd.concat([details, df])
    df.to_csv('car_details.csv', mode='a', header=True)

    print("You Entered ---> ")
    print("Car Name is ", vmake)
    print("Number of your Car: ", vnum)
    print("Model Name is: ", vtype)
    print("Your State ", state)