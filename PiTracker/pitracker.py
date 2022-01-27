#!/usr/bin/python

# api-key: ezeyVrHx9VKS3TC6VNbFrGHU1FYUqRp7biATNZk3svL6ApvAmJFJExwrrmQXz7yC3NzGqcboPzGUVzgq

import subprocess
import requests
import json

#def rxg_get(path):
	#response = requests.get(base_url + path + "index.json?api_key=" + api_key)

ifconfig = subprocess.check_output('ifconfig').decode("utf-8")
hostname = subprocess.check_output('hostname').decode("utf-8")

apikey ='ezeyVrHx9VKS3TC6VNbFrGHU1FYUqRp7biATNZk3svL6ApvAmJFJExwrrmQXz7yC3NzGqcboPzGUVzgq'
base_url = 'https://rxg.nkarrick.com/admin/scaffolds'



#curl "https://rxg.nkarrick.com/admin/scaffolds/custom_data_keys/index.json?api_key=ezeyVrHx9VKS3TC6VNbFrGHU1FYUqRp7biATNZk3svL6ApvAmJFJExwrrmQXz7yC3NzGqcboPzGUVzgq"
# testing
#get_response  = rxg_get('/custom_data_keys')
print()
#print(get_response.text)
print()