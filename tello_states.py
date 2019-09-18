import threading
from threading import Thread
import socket
import time
import netifaces
import netaddr
from netaddr import IPNetwork
from collections import defaultdict
from stats import Stats
import binascii
from time import sleep
import curses


class Tello_States:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8890
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip_list = []
        self.tello_list = []
        self.log = defaultdict(list)

        self.COMMAND_TIME_OUT = 9.0

        self.last_response_index = {}
        self.str_cmd_index = {}