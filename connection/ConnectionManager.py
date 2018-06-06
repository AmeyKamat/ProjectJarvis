
class ConnectionManager(object):

	connections = {}

	reverse_lookup = {}

	devices = {}

	def __init__(self):
		super(ConnectionManager, self).__init__()
		

	def register(self, socket, json):
		deviceId = json["deviceId"]
		deviceType = json["deviceType"]

		self.connections[deviceId] = {}
		self.connections[deviceId]["deviceType"] = deviceType
		self.connections[deviceId]["socket"] = socket

		self.reverse_lookup[socket] = deviceId

		if self.devices[deviceId] == None:
			self.devices[deviceType] = [deviceId]
		else:
			self.devices[deviceType].append(deviceId)

	def deregister(self, socket):
		deviceId = reverse_lookup[socket]
		deviceType = self.connections[deviceId]["deviceType"]
		
		if deviceId in self.devices[deviceType]:
			self.devices[deviceType].remove(deviceId)

		if socket in self.reverse_lookup.keys():
			self.reverse_lookup.pop(socket)

		self.connections.pop(deviceId)
