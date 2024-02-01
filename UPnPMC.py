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

def port_function(action, port, protocols, device):

	# display information about the IGD and the internet connection
	print('local ip address :', device.lanaddr)
	for protocol in protocols:
		if action == 'open':
			open_port(device, int(port), protocol)
		elif action == 'close':
			close_port(device, int(port), protocol)



if __name__ == '__main__':
	arguments = len(sys.argv) - 1
	if arguments < 1:
		print("Error: Wrong number of arguments, use -h for help")
		exit()
	# Arguments specification
	# 1: type of action to perform (open or close) -c or -o
	# 2: ports to open in the format of port1,port2,port3
	# 3: -p protocol to open (TCP or UDP) (optional) default is both. -p TCP,UDP or -p UDP,TCP or -p TCP or -p UDP or -p tcp,udp or -p udp,tcp or -p tcp or -p udp
	# 4: -d duration to keep port open for (optional) default is 0 (forever)
	# 8: -h help
	#parse arguments
	args = sys.argv
	#check if help is requested
	if '-h' in args:
		print("This program is used to open ports on your router using UPnP.")
		print("Usage: python3 UPnPMC.py [action] [ports] [protocols]")
		print("Arguments:")
		print("\taction: -o open ports, -c close ports")
		print("\tports: port1,port2,port3")
		print("\tprotocols: TCP, UDP, or TCP,UDP")
		print("\t-h help")
		exit()
	#check if action is specified
	if '-o' in args:
		action = 'open'
	elif '-c' in args:
		action = 'close'
	else:
		print("Error: No action specified")
		exit()
	actionShortcut = '-o' if action == 'open' else '-c'
	#check if ports are specified by checking if there are numbers in the first argument after -o or -c
	if any(char.isdigit() for char in args[args.index(actionShortcut) + 1]):
		ports = args[args.index(actionShortcut) + 1].split(',')
		#check if ports are valid
		for port in ports:
			if not port.isdigit():
				print("Error: Invalid port number")
				exit()
	else:
		print("Error: No ports specified")
		exit()
	#check if protocols are specified
	if '-p' in args:
		protocols = args[args.index('-p') + 1].split(',')
		#check if protocols are valid and uppercase
		if len(protocols) > 2:
			print("Error: Too many protocols specified")
			exit()
		for protocol in protocols:
			if protocol.upper() != 'TCP' and protocol.upper() != 'UDP':
				print("Error: Invalid protocol")
				exit()
		#set protocols to uppercase
		protocols = [protocol.upper() for protocol in protocols]
	else:
		protocols = ['TCP', 'UDP']

	#print out arguments
	print("Action: {}".format(action))
	print("Ports: {}".format(ports))
	print("Protocols: {}".format(protocols))

	#For each port spawn a thread to open or close the port
	device = miniupnpc.UPnP()
	device.discoverdelay = 100
	try:
		print("Discovering UPnP devices...")
		devices = device.discover()
		print(devices, 'device(s) detected')
		#open for all devices
		for i in range(devices):
			device.selectigd()
			for port in ports:
				port_function(action, port, protocols, device)
	except Exception as e:
		print(e)
	
	print()
	#close app
	exit()



		# device.discoverdelay = 200
		# try:
		# 	print("Discovering UPnP devices...")
		# 	devices = device.discover()
		# 	print(devices, 'device(s) detected')
		# 	#open for all devices
		# 	for i in range(devices):
		# 		device.selectigd()
		# 		# display information about the IGD and the internet connection
		# 		print('local ip address :', device.lanaddr)
		# 		open_port(device, port, 'TCP')
		# 		open_port(device, port, 'UDP')
		# 		#if the user wants to keep the port open enters third argument of 1, check if argument exists
		# 	if len(sys.argv) > 2 and sys.argv[2] == '1':
		# 		print("Press CTRL + C to exit")
		# 		while True:
		# 			pass
		# except Exception as e:
		# 	print(e)

