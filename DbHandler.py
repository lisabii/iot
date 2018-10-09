import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def put(data):
    logging.warning('Watch out!')
    myMQTTClient = AWSIoTMQTTClient(
        "Rasp")  # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
    
    myMQTTClient.configureEndpoint("a1hnafryz8rtde.iot.us-west-2.amazonaws.com", 8883)
    
    certRootPath = '/home/pi/aws-iot-keys/'
    myMQTTClient.configureCredentials("{}root_ca.pem".format(certRootPath), "{}private.pem.key".format(certRootPath),
                                      "{}certificate.crt".format(certRootPath))
    
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    myMQTTClient.connect()
    myMQTTClient.publish("my/topic", data, 0)
    myMQTTClient.disconnect()
