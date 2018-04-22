  
#!/usr/bin/env python
from circuits.net.events import write
from circuits import Component, handler
from circuits.web import Controller

from events.MessageReceivedEvent import MessageReceivedEvent

import json

class WSGateway(Component):

	channel="wsserver"

	socket = None

	def read(self, sock, message):
		#self.fireEvent(write(sock, "Received: " + message))
		self.fire(MessageReceivedEvent(message))

	def connect(self, sock, host, port):
		self.socket = sock

	def disconnect(self, sock):
		self.socket = None

	@handler("DialogReadyEvent")
	def handleDialogReadyEvent(self, message):
		self.fire(write(self.socket, message))

class Root(Controller):

	tpl = "./webSocketInterface.html"

	def index(self):
		with open(self.tpl, 'r') as content_file:
			return content_file.read()

