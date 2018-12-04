# Main python file
# Reads the ADC values and uploads them to the server

import requests
from time import sleep
import json
import sys

from mcp3002 import MCP3002

tmp = "TMP36"

class BeatsByDavid:

    def __init__(self, locationid, deviceid):
        # Connect to the ADC
        self.adc = MCP3002()
        self.server_addr = 'http://davidkopala.com:8000/api'
	self.deg_c_values = []
	self.deviceid = deviceid
	self.locationid = locationid

    def read_sound(self):
        # return 5
        return self.adc.read(1)

    def read_temp(self):
        # return (6, 6*(5/9) + 32)
        p_adc = self.adc.read(0)
        v_adc = p_adc * 5 * 1.2
	mv_adc = v_adc * 1000
	print 'mv_adc: {0}'.format(mv_adc)

        if tmp == "TMP35":
            offset = 0
            slope = 1/100.0
        elif tmp == "TMP36":
#            offset = 500
#            slope = 1/100.0
		offset = -500
		slope = 1/10.0
        elif tmp == "TMP37":
            offset = 0
            slope = 1/200.0
        else:
            offset = -1
            slope = 0
        
        deg_c = (offset + mv_adc) * slope
        deg_f = 32 + (9.0/5.0)*deg_c

        return (deg_c, deg_f)

    def deg_c_to_f(self, deg_c):
	return 32 + (9.0/5.0)*deg_c

    def measure_and_upload(self):
	print ''
        sound = self.read_sound()
        (deg_c, deg_f) = self.read_temp()

	if len(self.deg_c_values) < 5:
		self.deg_c_values.append(deg_c)
	else:
		self.deg_c_values.pop(0)
		self.deg_c_values.append(deg_c)

	deg_c = sum(self.deg_c_values) / float(len(self.deg_c_values))
	deg_f = self.deg_c_to_f(deg_c)

	print 'Temp:  {0} C'.format(deg_c)
	print 'Temp:  {0} F'.format(deg_f)
	print 'Sound: {0} p_adc'.format(sound)

        headers = {
            "Content-Type": "application/json"
        }

        sound_req = {
            "id": 'DEVICE_{0}_UPLOAD'.format(self.deviceid),
            "method": "tasks.upload_new_data_cel",
            "params": {
                "type": "Sound",
                "value": sound,
                "units": "p_adc",
                "deviceid": self.deviceid,
                "locationid": self.locationid
            }
        }

        temp_req = {
            "id": 'DEVICE_{0}_UPLOAD'.format(self.deviceid),
            "method": "tasks.upload_new_data_cel",
            "params": {
                "type": "Temperature",
                "value": deg_f,
                "units": "F",
                "deviceid": self.deviceid,
                "locationid": self.locationid
            }
        }

	try:
	        r_sound = requests.post(self.server_addr, json.dumps(sound_req), headers=headers)
#        print r_sound.status_code, r_sound.reason
#        print r_sound.text

        	r_temp = requests.post(self.server_addr, json.dumps(temp_req), headers=headers)
#        print r_temp.status_code, r_sound.reason
#        print r_temp.text
	except:
		print 'Could not upload data!\n'


if __name__ == "__main__":
    print 'Beats By David - Raspberry Pi Core Code'
    print 'Reads Sound and Temperature data, and uploads it to a server'
    print 'This script measures and uploads data every 5 seconds'

    if len(sys.argv) != 3:
	print 'Invalid Usage!'
	print '{0} [device_id] [location_id]'.format(sys.argv[0])
	exit(0)

    core = BeatsByDavid(sys.argv[1], sys.argv[2])

    while True:
        core.measure_and_upload()
        sleep(5)
