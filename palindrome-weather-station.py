#########################################################
# PALINDROME RASPBERRY PI SOLAR POWERED WEATHER STATION #
#########################################################
# This code requires the DS18B20 Digital Thermometer    #
# attached to a Model B Raspberry Pi to run the         #
# following code.  It also requires certificates that   #
# are pre-generated within the AWS IoT console to send  #
# the data back to the AWS cloud.                       #
#########################################################

# Import AWS IoT packages and other modules
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import os
import glob

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
 
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'

iot_endpoint = "a18p2ffxiq3zuq-ats.iot.eu-west-1.amazonaws.com" # Custom endpoint to connect to AWS IoT
iot_rootca = "/home/jeg1972/Documents/weather-station/root-CA.crt" # Amazon CA Root Certificate
iot_cert = "/home/jeg1972/Documents/weather-station/weather-pi.cert.pem" # AWS IoT Certificate
iot_private_key = "/home/jeg1972/Documents/weather-station/weather-pi.private.key" # Private Key for IoT Thing
iot_clientid = "basicPubSub" # ClientID which is used as a Resource in the iot:Connect part of the policy
iot_topic = "sdk/test/Python" # Name of the IoT Topic which is used in iot:Publish, iot:Receive and iot:Subscribe actions in the policy
iot_message = "Coming from The Solar Weather Station" # Message used to test publishing to topic 

#def read_temp_raw():
#    f = open(device_file, 'r')
#    lines = f.readlines()
#    f.close()
#    return lines
 
#def read_temp():
#    lines = read_temp_raw()
#    while lines[0].strip()[-3:] != 'YES':
#        time.sleep(0.2)
#        lines = read_temp_raw()
#    equals_pos = lines[1].find('t=')
#    if equals_pos != -1:
#        temp_string = lines[1][equals_pos+2:]
#        temp_c = float(temp_string) / 1000.0
#        return temp_c

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("\n\n") 
    print("--------------")   
    print("RECEIVED MESSAGE: ")
    print(message.payload)
    print("FROM TOPIC: ")
    print(message.topic)
    print("--------------\n\n")

# Configure logging
#logger = logging.getLogger("AWSIoTPythonSDK.core")
#logger.setLevel(logging.DEBUG)
#streamHandler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#streamHandler.setFormatter(formatter)
#logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(iot_clientid)
myAWSIoTMQTTClient.configureEndpoint(iot_endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(iot_rootca, iot_private_key, iot_cert)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(iot_topic, 1, customCallback)

loopCount = 0
while True:
    message = {}
    message['message'] = iot_message #read_temp()
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(iot_topic, messageJson, 1)
    print('Published topic %s: %s\n' % (iot_topic, messageJson))
    loopCount += 1
time.sleep(1)

myAWSIoTMQTTClient.disconnect()