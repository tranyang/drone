from djitellopy import Tello
from time import sleep
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, World!"

# @app.route('/users/<name>', methods=['POST'])
# def create_user(name):

#     msg = f'user {name} created'
#     return (msg, 201)

me = Tello()
me.connect()
print(me.query_wifi_signal_noise_ratio())
print(me.get_battery())

me.takeoff()
# me.move_forward(20)
# sleep(2)
# me.move_left(20)
me.land()
