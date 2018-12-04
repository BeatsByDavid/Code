# Main python file
# Reads the ADC values and uploads them to the server

import requests
from time import sleep
import json

from mcp3002 import MCP3002

tmp = "TMP36"

device_id = 1
location_id = 1

class BeatsByDavid:

    def __init__(self):
        # Connect to the ADC
        self.adc = MCP3002()
        self.server_addr = 'http://davidkopala.com:8000/api'

    def read_sound(self):
        # return 5
        return self.adc.read(1)

    def read_temp(self):
        # return (6, 6*(5/9) + 32)
        p_adc = self.adc.read(0)
        v_adc = p_adc * 5
	mv_adc = v_adc * 1000
	print 'mv_adc: {0}'.format(mv_adc)

        if tmp == "TMP35":
            offset = 0
            slope = 1/100.0
        elif tmp == "TMP36":
            offset = 0.5
            slope = 1/100.0
        elif tmp == "TMP37":
            offset = 0
            slope = 1/200.0
        else:
            offset = -1
            slope = 0
        
        deg_c = offset + (mv_adc * slope)
        deg_f = 32 + (9.0/5.0)*deg_c

        return (deg_c, deg_f)

    def measure_and_upload(self):
        sound = self.read_sound()
        (deg_c, deg_f) = self.read_temp()

	print 'Temp:  {0} C'.format(deg_c)
	print 'Temp:  {0} F'.format(deg_f)
	print 'Sound: {0} p_adc'.format(sound)

        headers = {
            "Content-Type": "application/json"
        }

        sound_req = {
            "id": 'DEVICE_{0}_UPLOAD'.format(device_id),
            "method": "tasks.upload_new_data_cel",
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
            "method": "tasks.upload_new_data_cel",
            "params": {
                "type": "Temperature",
                "value": deg_f,
                "units": "F",
                "deviceid": device_id,
                "locationid": location_id
            }
        }

        r_sound = requests.post(self.server_addr, json.dumps(sound_req), headers=headers)
#        print r_sound.status_code, r_sound.reason
#        print r_sound.text

        r_temp = requests.post(self.server_addr, json.dumps(temp_req), headers=headers)
#        print r_temp.status_code, r_sound.reason
#        print r_temp.text


if __name__ == "__main__":
    print 'Beats By David - Raspberry Pi Core Code'
    print 'Reads Sound and Temperature data, and uploads it to a server'
    print 'This script measures and uploads data every 5 seconds'

    core = BeatsByDavid()

    while True:
        core.measure_and_upload()
        sleep(5)
