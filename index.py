# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
import subprocess, ipaddress, json, time
from wakeonlan import send_magic_packet
from subprocess import Popen, PIPE
import nmap
nm = nmap.PortScanner()

application = Flask(__name__)

hostList = []

class Hosts:
    def __init__(self, name, type, ipv4, mac, state, reason):
        self.name = name
        self.type = type
        self.ipv4 = ipv4
        self.mac = mac
        self.state = state
        self.reason = reason
        self.enabled = None

    def update(self, name, ip, mac):
        print("")
        self.name = name
        self.ipv4 = ip
        self.mac = mac

# use nmap and the local file to update the list of configured and available hosts on the network
def updateComputers():
    scanForHosts()

    readComputerFileList()



# scan the network for hosts and add them to the global object
def scanForHosts():

    global hostList

    # TODO: support different IP address format
    nm.scan(hosts='192.168.1.0/24', arguments='-sn', sudo=True)

    for x in nm.all_hosts():
        # print(x, nm[x])

        temp = nm[x]

        # hostList.append(Hosts(nm[x]))
        hostList.append(Hosts(nm[x].get('hostnames',{})[0].get('name'), nm[x].get('hostnames',{})[0].get('type'), nm[x].get('addresses',{}).get('ipv4'), nm[x].get('addresses',{}).get('mac'), nm[x].get('status',{}).get('state'), nm[x].get('status',{}).get('reason')))

# return the host object based on a given IP address
def getComputer(ip = None, mac = None):

    # if neither ip address or mac address are passed in, then return nothing
    if not ip and not mac:
        return None

    global hostList

    for host in hostList:

        if ip and mac:
            # TODO: should this be an and or an or? what to do if there is one computer with the requested mac, and one with the requested IP?
            # probably use an or as a mismatch will mean the wake wont work
            if host.ipv4 == ip or host.mac == mac:
                return host

        if ip:
            if host.ipv4 == ip:
                return host
        
        if mac:
            if host.mac == mac:
                return host
    
    return None



# read in JSON data from the file of the defined configured computers
def readComputerFileList():

    global hostList

    try:
        # TODO: support different file location
        with open("./data/computers.json",'r') as computersFile:
            data = json.load(computersFile)
            print(data)

            # return data

            for computer in data:

                # TODO: how to handle cases where entries are missing certain values. Are these passed in as None?
                hostList.append( Hosts(computer['name'], computer['type'], computer['ipv4'], computer['mac'], computer['state'], computer['reason']))

    except IOError as e:
      print("Error: File does not appear to exist. ", e)
      return None

def saveComputersList():
    print("")

# format the computer information to be in a format that's readable for the page template
def formatComputers():
    global hostList

    computers = []

    for host in hostList:

        # TODO: filter only enabled computers
        temp = {}
        temp['name'] = host.name
        temp['ip'] = host.ipv4
        temp['mac'] = host.mac
        temp['enabled'] = host.enabled
        temp['state'] = host.state

        computers.append(temp)

    return computers

# read in JSON data of the currently configured computers
# def getComputerList():

#     try:
#         with open("./data/computers.json",'r') as computersFile:
#             data = json.load(computersFile)
#             print(data)

#             return data

#     except IOError:
#       print("Error: File does not appear to exist.")
#       return None

# add the submitted computer information to the file of configured computers
def submitFormData(newComputerFormData):

    global hostList

    # if there is already a computer with this information, then either do nothing or update it
    if getComputer(newComputerFormData["computerIPFormField"], newComputerFormData["computerMACFormField"]):
        print("there is already a computer with this IP or MAC...") 
    
        getComputer(newComputerFormData["computerIPFormField"], newComputerFormData["computerMACFormField"]).update(newComputerFormData["computerNameFormField"], newComputerFormData["computerIPFormField"], newComputerFormData["computerMACFormField"])
    else:
        hostList.append(Hosts(newComputerFormData["computerNameFormField"], newComputerFormData["computerIPFormField"], newComputerFormData["computerMACFormField"]))

    saveComputersList()

def deleteComputer(newComputerFormData):

    global hostList

    hostList.remove(getComputer(newComputerFormData["computerIPFormField"], newComputerFormData["computerMACFormField"]))

def wakeComputer(newComputerFormData):
    print("waking computer at ", newComputerFormData["computerMACFormField"])

    # print("sending command: `wakeonlan ", newComputerFormData["computerMACFormField"], "`")

    try:
        send_magic_packet(newComputerFormData["computerMACFormField"])
        time.sleep(3)
    except:
        print("Unexpected error:", sys.exc_info()[0])

def pingComputer(host):
    # ip = "192.168.1.140"
    # ip = host.ipv4
    toping = Popen(['ping', '-c', '1', host.ipv4], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive = toping.returncode

    if hostalive == 0:
        print (host.ipv4, "is reachable")
        data = json.dumps({"ipaddress": host.ipv4, "isAlive": "true"})

    else:
        print(host.ipv4, "is unreachable")
        data = json.dumps({"ipaddress": host.ipv4, "isAlive": "false"})

    resp = Response(response=data, status=200, mimetype="application/json")
    return resp
    # return result

# makes functions contained here available to all templates
@application.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)

    def pingComp(ipAddress):
        # ip = "192.168.1.140"
        ip = str(ipAddress)
        toping = Popen(['ping', '-c', '1', ip], stdout=PIPE)
        output = toping.communicate()[0]
        hostalive = toping.returncode
        if hostalive == 0:
            # print (ip, "is reachable")
            return "true"
        else:
            # print(ip, "is unreachable")
            return "false"
        # return result

    return dict(format_price=format_price, pingComputer = pingComp)

#  return a list of the hosts on the network
@application.route("/hosts")
def hostsRoute():

    return formatComputers()

#  return whether the computer with the requested IP address is awake or not
@app.route("/ping")
def ping():

    ipAddress = request.args.get('ipAddress')
    if ipAddress:
        temp = getComputer(ip = ipAddress)

        return pingComputer(getComputer(ip = ipAddress))

    else:
        return None

@app.route("/", methods=['GET', 'POST'])
def index():

    updateComputers()

    # selectedProject = request.args.get('project')
    
    #TODO: add in validation from here https://pythonspot.com/flask-web-forms/ or here https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    #form = ReusableForm(request.form)

    #print form.errors
    if request.method == 'POST':
        if request.form["form_id"] == "newComputerForm":
            submitFormData(request.form)
            # print(request.form["computerNameFormField"])
        if request.form["form_id"] == "deleteComputer":
            deleteComputer(request.form)

        if request.form["form_id"] == "wakeComputer":
            wakeComputer(request.form)

    # Return the index template and a formatted list of computers when the page is initially loaded/not called using a POST request
    return render_template('index.html', computers = formatComputers())
 
if __name__ == "__main__":
    app.run(port=5000, threaded=True, host=('0.0.0.0'))