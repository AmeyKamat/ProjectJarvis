  
#!/usr/bin/env python
from circuits.net.events import write
from circuits import Component, handler
from circuits.web import Controller

from events.MessageReceivedEvent import MessageReceivedEvent
from context.Context import Context

import json
import jsonpickle

class WSGateway(Component):

	channel="wsserver"

	connections = {}

	def read(self, sock, message):
		#messageJson = json.loads(message)

		#if sock not in self.connections:
		#	self.connections[sock] = {}
		#	self.connections[sock]["type"] = messageJson["type"]
			
		print(message)
		self.fire(MessageReceivedEvent(Context(message)))

	def connect(self, sock, host, port):
		self.socket = sock

	def disconnect(self, sock):
		self.socket = None

	@handler("DialogReadyEvent")
	def handleDialogReadyEvent(self, context):
		print(jsonpickle.encode(context))
		self.fire(write(self.socket, jsonpickle.encode(context)))

class Root(Controller):

	tpl = "./webSocketInterface.html"

	def index(self):
		with open(self.tpl, 'r') as content_file:
			return content_file.read()

