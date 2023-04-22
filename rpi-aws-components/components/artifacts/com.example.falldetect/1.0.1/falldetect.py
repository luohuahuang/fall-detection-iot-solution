"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.falldetect=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.falldetect
"""
import time
import json
import math
import numpy as np
import joblib
import warnings

from flask import Flask, request

app = Flask(__name__)

warnings.filterwarnings('ignore', message='X does not have valid feature names')


def do_fall_detection(input_json):
    input_dict = json.loads(input_json)

    # Access the values of Acc_X, Acc_Y, and Acc_Z
    Acc_X = input_dict['Acc_X']
    Acc_Y = input_dict['Acc_Y']
    Acc_Z = input_dict['Acc_Z']

    x, y, z = float(Acc_X), float(Acc_Y), float(Acc_Z)
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    is_fall =  magnitude > 1.5

    if is_fall:
        print("Fall detected:", is_fall)
        print("###############################")
        print("FALL DETECT: YES ***")
        print("###############################")
        return True
    else:
        print("###############################")
        print("FALL DETECT: NO ***")
        print("###############################")

        return False

"""
# fall = yes
curl --location --request POST 'http://localhost:5000/fall_detection' \
--header 'Content-Type: application/json' \
--data-raw '{"acc_x": 9.681701660156250000, "acc_y": 1.020812988281250000, "acc_z": 1.863098144531250000, "mag_x": -0.815185546875000000, "mag_y": 0.412353515625000000, "mag_z": 0.079833984375000000}'
# fall = no 
curl --location --request POST 'http://localhost:5000/fall_detection' \
--header 'Content-Type: application/json' \
--data-raw '{"acc_x": 9.352111816406250000, "acc_y": -2.879333496093750000, "acc_z": 1.144409179687500000, "mag_x": -0.623779296875000000, "mag_y": 0.662597656250000000, "mag_z": -0.643066406250000000}'
"""
@app.route('/fall_detection', methods=['POST'])
def post_request():
    data = request.get_json()
    Acc_X = data['acc_x']
    Acc_Y = data['acc_y']
    Acc_Z = data['acc_z']
    Mag_X = data['mag_x']
    Mag_Y = data['mag_y']
    Mag_Z = data['mag_z']
    # need to support heart rate

    input_json = '{{"Acc_X": {}, "Acc_Y": {}, "Acc_Z": {}, "Mag_X": {}, "Mag_Y": {}, "Mag_Z": {}}}'.format(Acc_X, Acc_Y,
                                                                                                           Acc_Z, Mag_X,
                                                                                                           Mag_Y, Mag_Z)
    print(input_json)
    if do_fall_detection(input_json):
        return 'yes'
    return 'no'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
