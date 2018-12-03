# Main python file
# Reads the ADC values and uploads them to the server

import requests
from time import sleep

from mcp3002 import MCP3002
from RPCObjects import *

tmp = "TMP35"

device_id = 1
location_id = 1

class BeatsByDavid:

    def __init__(self):
        # Connect to the ADC
        self.adc = MCP3002()
        self.server_addr = 'https://davidkopala.com:8000/api'

    def read_sound(self):
        return self.adc.read(0)

    def read_temp(self):
        p_adc = self.adc.read(1)
        v_adc = n_adc * 5

        if tmp == "TMP35":
            offset = 0
            slope = 1/10
        elif tmp == "TMP36":
            offset = 0.5
            slope = 1/10
        elif tmp == "TMP37":
            offset = 0
            slop = 1/20
        else:
            offset = -1
            slope = 0
        
        deg_c = offset + (v_adc * slope)
        deg_f = 32 + (9/5)*deg_c

        return (deg_c, deg_f)

    def measure_and_upload(self):
        sound = self.read_sound()
        (deg_c, deg_f) = self.read_temp()

        sound_req = {
            "id": 'DEVICE_{0}_UPLOAD'.format(device_id),
            "method": "up.upload_new_data_cel",
            "params": {
                "type": "Sound",
                "value": sound,
                "units": "p_adc",
                "deviceid": device_id,
                "locationid": location_id
            }
        }

        temp_req = {
            "id": 'DEVICE_{0}_UPLOAD'.format(device_id),
            "method": "up.upload_new_data_cel",
            "params": {
                "type": "Temperature",
                "value": deg_f,
                "units": "F",
                "deviceid": device_id,
                "locationid": location_id
            }
        }

        r_sound = requests.post(self.server_addr, sound_req)
        print r_sound.status_code, r_sound.reason
        print r_sound.text

        r_temp = requests.post(self.server_addr, temp_req)
        print r_temp.status_code, r_sound.reason
        print r_temp.text


if __name__ == "__main__":
    print 'Beats By David - Raspberry Pi Core Code'
    print 'Reads Sound and Temperature data, and uploads it to a server'
    print 'This script measures and uploads data every 5 seconds'

    core = BeatsByDavid()

    while True:
        core.measure_and_upload()
        sleep(5)