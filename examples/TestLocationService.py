from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType

# Demonstrate usage of the Python Location Service API

locationService = LocationService()

# List all registered connections
print("\nAll Locations:")
for i in locationService.list():
    print("    " + str(i))

# List the registered HCDs
print("\nHCDs:")
for i in locationService.list(ComponentType.HCD):
    print("    " + str(i))

# List the registered http connections
print("\nConnections on 192.168.178.78")
for i in locationService.list("192.168.178.78"):
    print("    " + str(i))

# List the registered http connections
print("\nHTTP connections:")
for i in locationService.list(ConnectionType.HttpType):
    print("    " + str(i))

# Register a connection
connection = ConnectionInfo("myComp", ComponentType.Service.value, ConnectionType.HttpType.value)
reg = Registration(8080, connection, path="myservice/test")
regResult = locationService.register(RegType.HttpRegistration, reg)
print("\nRegistration result: " + str(regResult))

# Find a connection
location1 = locationService.find("myComp", ComponentType.Service, ConnectionType.HttpType)
print("location1 = " + str(location1))

# Resolve a connection (waiting if needed)
location2 = locationService.resolve("myComp", ComponentType.Service, ConnectionType.HttpType)
print("location2 = " + str(location2))

# Unregister
unregResult = locationService.unregister(connection)
print("\nUnregister result: " + str(unregResult))
