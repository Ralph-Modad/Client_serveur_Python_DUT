import datetime
import os
import math
import shutil
import socket, platform, psutil,cpuinfo,re,uuid
import time
#####################################################################################################################################################################
#Partie socket 
HEADER = 64 #longueur
PORT = 5000 #port attribué
FORMAT = 'utf-8'#format de codage
DISCONNECT_MESSAGE = "!DISCONNECT"#message de deconnection envoyé au serv pour couper la connection
SERVER = input("enter the ip add of the server") #demande utilisateur de entrer une addresse ip serv
ADDR = (SERVER, PORT)#regroupement de addr et Port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#création de la socket
client.connect(ADDR)#connection client



######################################################################################################################################################################
#fonction pour convertire les bytes
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

######################################################################################################################################################################
#Récpération des infos du proc #dans cpuinfo pour le test
cpu_info = open('/proc/cpuinfo',"r")#ouverture du fichier contenant les infos cpu
info = cpu_info.readlines()#lecture des lignes dans le fichier 
cpu = info[4]#chosie quel infos 
cpuname = re.findall(":([^\]]+)CPU", cpu) #CPU name regex coupe le nom du cpu juste
cpuspeed = re.findall("\@([^\]]+)GHz", cpu) #CPU speed et la juste la vitesse 
cpu_info.close()

#recupération de la température sensors pour tester
temp=open("/sys/class/thermal/thermal_zone1/temp","r")
temperature = temp.readline()
t= int(temperature) /1000 #température du cpu obtenu 
temp.close()

total, used, free = shutil.disk_usage("/")
total=(total // (2**30)) #Mémoire total
used=(used // (2**30))#Mémoire utilisé
free=(free // (2**30)) #Mémoire Libre

#ram totale 
ram=open("/proc/meminfo","r")
lire=ram.readline()
regexram=re.findall("([0-9])",lire)
ram.close()

#ram Utilisé
ramused=open("/proc/meminfo","r")
lire=ramused.readlines()
contenu=lire[6]
regexusedram=re.findall("[0-9]",contenu)
regexusedram1=regexusedram[0]+regexusedram[1]+regexusedram[2]+regexusedram[3]+regexusedram[4]+regexusedram[5]+regexusedram[6]
kbtobyu=int(regexusedram1)*1000
kbtobyu=convert_size(kbtobyu)
ramused.close()

#Ram disponible
ramfree=open("/proc/meminfo","r")
lire=ramfree.readlines()
contenu=lire[2]
regexfreeram=re.findall("[0-9]",contenu)
regexfreeram1=regexfreeram[0]+regexfreeram[1]+regexfreeram[2]+regexfreeram[3]+regexfreeram[4]+regexfreeram[5]+regexfreeram[6]
kbtoby=int(regexfreeram1)*1000
kbtoby=convert_size(kbtoby)
ramfree.close()


#Ram disponible #pour tester free -k ou /proc/meminfo et valeur
ramused=open("/proc/meminfo","r")
lire=ramused.readlines()
contenu=lire[2]
regexfreeram=re.findall("[0-9]",contenu)
regexfreeram1=regexfreeram[0]+regexfreeram[1]+regexfreeram[2]+regexfreeram[3]+regexfreeram[4]+regexfreeram[5]
regexfreeram2=int(regexfreeram1)/1000
print(regexfreeram2)
n=round(regexfreeram2,2)
ramfree.close()

#charge sur le cpu
load=psutil.cpu_percent()


#Nom d'exploitation
uname = platform.uname()
hostname = uname.system
local_ip = socket.gethostbyname(socket.gethostname())



#######################################################################################################################################################

#message envoyé sous forme de String au quel on ajoute les valeurs obtenu envoies sous forme de string plus simple a lire et décodé coté serv

message = """
    <tr>
    <td>""" +str(local_ip)+"""</td>
    <td>""" +str(hostname)+  """</td>
	<td>""" +str(total)+"""</td>
	<td>"""+str(free)+ """</td>
	<td>""" +str(regexram[0])+"""</td>
	<td>""" +str(kbtobyu)+"""</td>
	<td>"""+str(kbtoby) + """</td>
	<td>"""+str(cpuname[0])+  """</td>
	<td>""" +str(cpuspeed[0])+"""</td>
	<td>"""+str(load)+ """</td>
	<td>"""+str(t)+"""</td>
	</tr>
    """

#Fonction qui envoies les données 
def send(msg):
    message = msg.encode(FORMAT) #encodage du msg en utf-8
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) # waiting bits verification de la taille du message
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
send(message)#appel a  la fonction send qui envoie le msg en html et qui sera écris dans le fichier html coté serveur puis afficher 













