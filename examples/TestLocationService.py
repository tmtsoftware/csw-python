from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType
import time

locationService = LocationService()

# List the registered connections
for i in locationService.list():
    print("Location: " + str(i))

connection = ConnectionInfo("myComp", ComponentType.Service.value, ConnectionType.HttpType.value)
reg = Registration(8080, connection, path = "myservice/test")
regResult = locationService.register(RegType.HttpRegistration, reg)
print("Registration result: " + str(regResult))
time.sleep(1)
unregResult = locationService.unregister(connection)
print("Unregister result: " + str(unregResult))

