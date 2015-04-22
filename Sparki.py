import serial
import struct
import time

class Sparki:

	SERVO_CENTER = 0
	SERVO_LEFT = 90
	SERVO_RIGHT = -90
	
	STATUS_OK = struct.pack('!B',0)
	MOVE_FORWARD = struct.pack('!B',1)
	MOVE_BACKWARD = struct.pack('!B',2)
	MOVE_LEFT = struct.pack('!B',3)
	MOVE_RIGHT = struct.pack('!B',4)
	SERVO = struct.pack('!B',5)
	REQ_PING = struct.pack('!B',6)
	REQ_WHEELS = struct.pack('!B',7)
	MOVE_STOP = struct.pack('!B',8)
	REQ_LINESENS = struct.pack('!B',9)

	portName = None
	serialPort = None

	def __init__(self, comPort):
		# Error check if comPort is a string
		self.portName = comPort
		self.serialPort = serial.Serial()

	"""
	Returns a boolean as to connection status
	"""
	def connect(self):
		print "Trying to Connect"
		self.serialPort.port = self.portName
		self.serialPort.baudrate = 9600
		self.serialPort.parity = 'N'
		self.serialPort.writeTimeout = 0
		# Might want to set other settings as well, to be safe
		self.serialPort.open()
		# Can throw ValueErrors on failure
		if (self.serialPort.isOpen()):
			print "Connected"
			self.servo(self.SERVO_CENTER)
			return True
		else:
			return False
	
	def disconnect(self):
		print "Disconnecting..."
		self.serialPort.close()
		if (self.serialPort.isClosed()):
			print "Disconnected"
	
	def moveForward(self):
		# Should be open port
		self.serialPort.write(self.MOVE_FORWARD)
	
	def moveBackward(self):
		# Should be open port
		self.serialPort.write(self.MOVE_BACKWARD)
	
	def moveLeft(self):
		# Should be open port
		self.serialPort.write(self.MOVE_LEFT)
	
	def moveRight(self):
		# Should be open port
		self.serialPort.write(self.MOVE_RIGHT)
	
	def moveStop(self):
		# Should be open port
		self.serialPort.write(self.MOVE_STOP)
	
	def servo(self, angle):
		# Should be open port
		# Should check angle to be int
		if (angle < -90 or angle > 90):
			print "Invalid servo angle" #Should append angle
			return
		angle = -1*(angle) + 90
		self.serialPort.write(self.SERVO)
		self.serialPort.write(struct.pack('!B',angle))
	
	"""
	Returns an int of the ping value or -1
	"""
	def ping(self):
		# Should be open port
		distance = -1
		self.serialPort.write(self.REQ_PING)
		distance = int(self.readString())
		return distance
	
	"""
	Returns a list of ints for the travel of the two motors
	"""
	def totalTravel(self):
		# Should be open port
		values = [0,0]
		self.serialPort.write(self.REQ_WHEELS)
		retValues = self.readString().split()
		values[0] = int(retValues[0])
		values[1] = int(retValues[1])
		return values
	
	"""
	Returns a list of the line sensor data
	"""
	def lineSense(self):
		# Should be open port
		values = [0,0,0,0,0]
		self.serialPort.write(self.REQ_LINESENS)
		retValues = self.readString().split()
		values[0] = int(retValues[0])
		values[1] = int(retValues[1])
		values[2] = int(retValues[2])
		values[3] = int(retValues[3])
		values[4] = int(retValues[4])
		return values
	
	"""
	Reads return strings from Sparki that EOL with '*'
	Returns the string
	"""
	def readString(self):
		# Should be open port
		# Validate that conversion to string works
		output = ""
		last = ""
		while (True):
			last = str(self.serialPort.read(size=1))
			if (last == "*"):
				break
			output = output + last
		return output
	
	def delay(self, time):
		# Should validate time is int in milliseconds
		time.sleep(time/1000)