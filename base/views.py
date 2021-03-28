from django.shortcuts import render
import paho.mqtt.client as mqtt
import datetime
import json

default_port = 1883
broker_address = "192.168.9.20"
mqtt_topic = 'smart_water/49'
mqtt_user = 'participant'
mqtt_password = 'participant'

subscribed = False
# Create your views here.


def index(request):
    data = {}
    return render(request, "index.html", data)

def admin_home(request):
    data={"title":"Admin"}
    return render(request,"admin/home.html",data)


def subscription(request):
    data = {}
    return render(request, "subscription.html", data)


def read_message():
    try:
        f = open("messages.log", "r+")
        message = f.read()
        f.close()
    except Exception as e:
        message = "No messages found"
    return message


# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code {0}".format(str(rc)))
    # Subscribe to the topic “digitest/test1”, receive any messages published on it
    client.subscribe(mqtt_topic)


def on_message(client, userdata, message):
    print("\n\n\n")
    print("time ", datetime.datetime.now())
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    #formated_message = str(datetime.datetime.now()) + "- Received message: "+ str(message.payload.decode("utf-8")) + ", on topic: " + str(message.topic) + "\n"
    formated_message = str(message.payload.decode("utf-8"))
    res = json.loads(formated_message)
    print(res)
    f = open("messages.log", "w")
    f.write(str(res['SensorData']['WaterTemperature']))
    f.close()


def subscribe_on_topic(topic=mqtt_topic):
    global subscribed
    if subscribed == False:
        client = mqtt.Client("subscriber7")
        client.on_message = on_message  # attach function to callback
        client.on_connect = on_connect  # attach function to callback
        print("connecting to broker: " + broker_address)
        client.connect(broker_address, port=default_port)  # connect to broker
        client.username_pw_set(username=mqtt_user, password=mqtt_password)
        client.loop_start()  # start the loop
        print("Subscribing to topic: " + mqtt_topic)
        client.subscribe(mqtt_topic)
        subscribed = True
