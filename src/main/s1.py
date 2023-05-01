import bluetooth

server = bluetooth.BlueToothSocket(bluetooth.RFCOMM)
server.bind("", bluetooth.PORT_ANY)
server.listen(1)

port = server.getSocketName()

try:
    bluetooth.advertise_service(server, "Rover",
                                service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                 profiles=[bluetooth.SERIAL_PORT_PROFILE],)
except bluetooth.BluetoothError as err:
    print("advertising: {}".format(err))

print("waiting for connectrion")
client_sock, client_info = server.accept()
print("accepted connection from {}".format(client_info))
server.setttimeout(2.0)
server.send("Rover here")
