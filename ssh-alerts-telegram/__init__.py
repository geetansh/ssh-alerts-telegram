# importing the requests library 
import os, json, urllib3
from requests import get
import requests
import sys, getopt
from  environs import Env

env = Env()
env_path = os.environ['HOME'] + "/.server_gaze_alerts"

def write_env():
    
    try: input = raw_input
    except NameError: pass
    uid = (input("Enter your UID: "))
    server_id = (input("Enter your server_id: "))

    with open(env_path + "/.env", "w") as fobj:
        fobj.write("uid=" + uid + "\n")
        fobj.write("server_id=" + server_id + "\n" )
    #return uid,server_id

def add_to_source():
    if (os.geteuid()==0):
        #Open the file
        fobj = open("/etc/profile")
        text = fobj.read().strip().split()
        
        #Conditions
        while True:
            s = "ssh-alerts-telegram"
            if s in text: #string in present in the text file
                break
            else: #string is absent in the text file
                os.system('echo "python -m ssh-alerts-telegram 2>> /dev/null" >> /etc/profile')
                break
        fobj.close()

    else:
        
        #check if file exist or not
        if (os.path.exists(os.environ['HOME'] + "/.bash_profile")):
        
            #Open the file
            fobj = open(os.environ['HOME'] + "/.bash_profile")
            text = fobj.read().strip().split()
            #Conditions
            while True:
                s = "ssh-alerts-telegram"
                if s in text: #string in present in the text file
                    break
                else: #string is absent in the text file
                    os.system('echo "python -m ssh-alerts-telegram 2>> /dev/null" >> $HOME/.bash_profile')
                    break
            fobj.close()
        
        else:
            
            #Open the file
            fobj = open(os.environ['HOME'] + "/.bash_profile", "w+")
            text = fobj.read().strip().split()

            #Conditions
            while True:
                s = "ssh-alerts-telegram"
                if s in text: #string in present in the text file
                    break
                else: #string is absent in the text file
                    os.system('echo "python -m ssh-alerts-telegram 2>> /dev/null" >> $HOME/.bash_profile')
                    break
            fobj.close()


def read_env():
    env.read_env(env_path + "/.env",recurse=False)

    #import variables
    # variable check if statement not working 
    #need to fix
    if not (env("uid")):
        print (".env file is corrupt")
    else:
        read_env.uid = env("uid")
    
    if not (env("server_id")):
        print (".env file is corrupt")
    else:
        read_env.server_id = env("server_id")
        
def send_alert(uid,server_id):
    #get ssh IP into variable
    get_ip = os.environ['SSH_CONNECTION']
    get_ip = get_ip.split()
    get_ip = str(get_ip[0])
    #get_ip = "8.8.8.8"
    server_ip = get('https://api.ipify.org').text
    
    ip_info = get('https://www.iplocate.io/api/lookup/' + get_ip)
    current_user = (os.environ['USER'])

    #send data as post msg to another api
    ip_info = ip_info.json()
    r = requests.post('http://alerts.servergaze.com:8080/sendalert/', data = {'uid': uid ,'server_id': server_id , 'username': current_user , 'server_ip': server_ip  ,'ip_info': json.dumps(ip_info)})
    
    return r


#check if folder exist
if not (os.path.exists(env_path)):
    #Dir Not Exist
    #so file also not exist
    #create dir and write env file
    os.mkdir(env_path)
    write_env()
    read_env()
    add_to_source()
    send_alert(read_env.uid,read_env.server_id)

else:
    #dir 
    #check ifexist files exist or not
    if not (os.path.exists(env_path + "/.env")):
        #file does not exist
        #create file
        write_env()
        read_env()
        add_to_source()
        send_alert(read_env.uid,read_env.server_id)

    else:
        #file exist
        #read file
        read_env()
        add_to_source()
        send_alert(read_env.uid,read_env.server_id)
