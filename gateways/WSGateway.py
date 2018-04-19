  
#!/usr/bin/env python
from circuits.net.events import write
from circuits import Component, handler
from circuits.web import Controller

from events.MessageReceivedEvent import MessageReceivedEvent

import json

class WSGateway(Component):

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
		self.fireEvent(write(self.socket, message))
