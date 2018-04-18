from circuits import Debugger
from circuits.web.dispatchers import WebSocketsDispatcher
from circuits.web import Logger, Server, Static

from components.SementicAnalyserComponent import SementicAnalyserComponent 
from components.ContextBuilderComponent import ContextBuilderComponent
from gateways.WSGateway import WSGateway

IP_ADDR = "0.0.0.0"
PORT = 8000

BOOTSTRAP_MODULES = {
	"appComponents": [
		SementicAnalyserComponent(),
		ContextBuilderComponent()
	],
	"gateways": [
		WSGateway()
	],
	"dispatchers": [
		WebSocketsDispatcher("/websocket")
	],
	"circuitComponents": [
		Debugger(),
		Static(),
		Logger(),
	]
}


def bootstrapAppComponents(app, appComponents):
	for appComponent in appComponents:
		appComponent.register(app)

def bootstrapGateways(app, gateways):
	for gateway in gateways:
		gateway.register(app)

def bootstrapDispatchers(app, dispatchers):
	for dispatcher in dispatchers:
		dispatcher.register(app)

def bootstrapCircuitComponents(app, circuitComponents):
	for circuitComponent in circuitComponents:
		circuitComponent.register(app)



app = Server(("0.0.0.0", 8000))
bootstrapAppComponents(app, BOOTSTRAP_MODULES["appComponents"])
bootstrapGateways(app, BOOTSTRAP_MODULES["gateways"])
bootstrapDispatchers(app, BOOTSTRAP_MODULES["dispatchers"])
bootstrapCircuitComponents(app, BOOTSTRAP_MODULES["circuitComponents"])
app.run()