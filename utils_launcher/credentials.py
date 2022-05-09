"""Aqui van todas las credenciales que tienen que ver con el Endpoint"""
USERNAME = 'javier.rodriguez'
PASSWORD = 'secret123'

class endpoint:
    LOGIN = 'http://192.168.0.135:8000/api/v1/login'

    POST_SPEED = 'http://192.168.0.135:8000/api/v1/device-event/6'
    POST_PERSONS = 'http://192.168.0.135:8000/api/v1/device-event/1'
    
    GET_DEVICES = 'http://192.168.0.135:8000/api/v1/devices'
    GET_DEVICES_ZONES = 'http://192.168.0.135:8000/api/v1/device-zones/'

class id:
    SPEED = 6
    PERSONS = 1
