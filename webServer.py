from socket import *
import atexit
import json


#content types
serverSocket = socket(AF_INET, SOCK_STREAM)
con=open("config.json")
config=json.load(con)
con.close()
type(config)
print(config)
ContentTypes = config["ContentTypes"]#loading content types from conig


@atexit.register
def exitOP():
    print("closing")
    serverSocket.detach()
    serverSocket.close()


#returns the file or the defult 404 file if cant find
def getFile(url):
    print(url)
    url=str(url)[3:-1]#remove quotes
    print(url)

    if(url==''):
        url="index.html"
    try:
        f=open(url,'rb')
    except FileNotFoundError:
        print("404")
        f=open(config["404page"],'rb')

    return f
# returns headers for the file
def getheaders(file):
    out='HTTP/1.0 200 OK\r\n'#normal

    if(file.name=="404.html"):#if 404
        out = 'HTTP/1.0 404 Not Found\r\n'

    path=file.name#gets file name
    try:
        print(path)
        # get file extention
        extention=path.split('.')[-1]
        # gets content type form config.json file and adds to out
        out+="Content-Type:"+ContentTypes[extention]+"\r\n\r\n"

    except:
        print("unknown file type in config")
    print(out)
    return out

def main():

    serverPort = config["port"]#port loads form config.json

    serverSocket.bind(('', serverPort))
    serverSocket.listen(config["requestN"])
    print('The	server	is	ready	to	receive	messages on :'+str(serverPort))
    try:
        while 1:
            try:
                connectionSocket, addr = serverSocket.accept()
                request = connectionSocket.recv(1024)
                file=getFile(request.split()[1])#load file
                headers=getheaders(file)
                l=file.read(1024)
                connectionSocket.send(headers.encode())
                while (l):
                    connectionSocket.send(l)
                    l = file.read(1024)

                connectionSocket.close()
            except ConnectionResetError:
                print("conection rest")
    except KeyboardInterrupt:
        serverSocket.close()




if __name__ == '__main__':
    main()