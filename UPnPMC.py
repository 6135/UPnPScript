import miniupnpc
import sys

def open_port(device, port, protocol):
	if protocol == 'TCP':
		res = device.addportmapping(port, 'TCP', device.lanaddr, port, 'Upnp port mapping ' + str(port) + " " + str(protocol), '')
		if res == 0:
			print("Error: Could not open port {} for TCP traffic".format(port))
		else:
			print("Port {} is now open for TCP traffic".format(port))
	elif protocol == 'UDP':
		res = device.addportmapping(port, 'UDP', device.lanaddr, port, 'Upnp port mapping ' + str(port) + " " + str(protocol), '')
		if res == 0:
			print("Error: Could not open port {} for UDP traffic".format(port))
		else:
			print("Port {} is now open for UDP traffic".format(port))
	else:
		print("Error: Invalid protocol")

def close_port(device, port, protocol):
	if protocol == 'TCP':
		res = device.deleteportmapping(port, 'TCP')
		if res == 0:
			print("Error: Could not close port {} for TCP traffic".format(port))
		else:
			print("Port {} is now closed for TCP traffic".format(port))
	elif protocol == 'UDP':
		res = device.deleteportmapping(port, 'UDP')
		if res == 0:
			print("Error: Could not close port {} for UDP traffic".format(port))
		else:
			print("Port {} is now closed for UDP traffic".format(port))
	else:
		print("Error: Invalid protocol")

if __name__ == '__main__':
	port = int(sys.argv[1])
	device = miniupnpc.UPnP()
	devices = 0
	try:

		device.discoverdelay = 200
		try:
			print("Discovering UPnP devices...")
			devices = device.discover()
			print(devices, 'device(s) detected')
			#open for all devices
			for i in range(devices):
				device.selectigd()
				# display information about the IGD and the internet connection
				print('local ip address :', device.lanaddr)
				open_port(device, port, 'TCP')
				open_port(device, port, 'UDP')
				#if the user wants to keep the port open enters third argument of 1, check if argument exists
			if len(sys.argv) > 2 and sys.argv[2] == '1':
				print("Press CTRL + C to exit")
				while True:
					pass
		except Exception as e:
			print(e)
	except KeyboardInterrupt:
		for i in range(devices):
			device.selectigd()
			close_port(device, port, 'TCP')
			close_port(device, port, 'UDP')

