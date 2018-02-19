import socket

host = 'localhost'
port = 1234
buf = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

# print "Sending 'test1\\n'"
# clientsocket.send('test1\n')
# print "REPLY: " + clientsocket.recv(buf)

# print "Sending 'test2'"
# clientsocket.send('test2')
# print "REPLY: " + clientsocket.recv(buf)

# print "Sending 'abc'"
# clientsocket.send('abc')
# print "REPLY: " + clientsocket.recv(buf)

# print "Sending 'abc'"
# clientsocket.send('abc')
# print "REPLY: " + clientsocket.recv(buf)

# path = raw_input('JPG file [/tmp/fotka.jpg]:') or '/tmp/fotka.jpg'
# clientsocket.send('jpg_' + path)
# reply = clientsocket.recv(buf)
# print "___Binary data START___"
# print reply
# print "___Binary data END___"
# file = open('fotka.jpg', 'w')
# file.write(reply)
# file.close()
# print "New file 'fotka.jpg' was created."

# print "Sending 'bye'"
# clientsocket.send('bye\n')
# print "REPLY: " + clientsocket.recv(buf)

clientsocket.close()
