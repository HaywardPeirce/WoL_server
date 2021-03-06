# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
import subprocess, ipaddress, json, time
from wakeonlan import send_magic_packet
from subprocess import Popen, PIPE
application = Flask(__name__)

# read in JSON data of the currently configured computers
def getComputerList():

    try:
        with open("../data/computers.json",'r') as computersFile:
            data = json.load(computersFile)
            # print(data)

            return data

    except IOError:
      print("Error: File does not appear to exist.")
      return None

def submitFormData(computersFileData, newComputerFormData):

    # if there is no existing computer data
    if computersFileData == None:

        # computersFileData = [
        # {"name":"JOHN-DESKTOP",
        #         "ip":"192.168.1.43",
        #              "mac":"00-14-22-01-23-45"
        # }]

        computersFileData = [
            {"name": newComputerFormData["computerNameFormField"],
             "ip": newComputerFormData["computerIPFormField"],
             "mac": newComputerFormData["computerMACFormField"]
             }]



    # if there is already computer data
    else:

        # check if the current entry is already a saved entry

        isNewEntry = True

        for comp in computersFileData:

            # if there is already a configured entry with this MAC address, then just update the name and IP
            if comp["mac"] == newComputerFormData["computerMACFormField"]:
                isNewEntry = False

                comp["name"] = newComputerFormData["computerNameFormField"]
                comp["ip"] = newComputerFormData["computerIPFormField"]

        # if it really is a new entry, append the new entry to the exising JSON object
        if isNewEntry:
            computersFileData.append(
                {
                    "name": newComputerFormData["computerNameFormField"],
                    "ip": newComputerFormData["computerIPFormField"],
                    "mac": newComputerFormData["computerMACFormField"]
                }
            )

        print(computersFileData)

    try:
        with open("../data/computers.json", 'w+') as computersFile:
            json.dump(computersFileData, computersFile)
            # print(data)

    except IOError:
      print("Error: Cannot write computers to file.")

def deleteComputer(computersFileData, newComputerFormData):

    for comp in computersFileData:

        # if this is the computer that is marked to be deleted, remove it from the list
        if comp["mac"] == newComputerFormData["computerMACFormField"]:
            computersFileData.remove(comp)

    print(computersFileData)

    try:
        with open("../data/computers.json", 'w') as computersFile:
            json.dump(computersFileData, computersFile)
            # print(data)

    except IOError:
      print("Error: File does not appear to exist.")

def wakeComputer(computersFileData, newComputerFormData):
    print("waking computer at ", newComputerFormData["computerMACFormField"])

    # print("sending command: `wakeonlan ", newComputerFormData["computerMACFormField"], "`")

    try:
        send_magic_packet(newComputerFormData["computerMACFormField"])
        time.sleep(3)
    except:
        print("Unexpected error:", sys.exc_info()[0])

def pingComputer(ipAddress):
    # ip = "192.168.1.140"
    ip = str(ipAddress)
    toping = Popen(['ping', '-c', '1', ip], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive = toping.returncode

    if hostalive == 0:
        print (ip, "is reachable")
        data = json.dumps({"ipaddress": ip, "isAlive": "true"})

    else:
        print(ip, "is unreachable")
        data = json.dumps({"ipaddress": ip, "isAlive": "false"})

    resp = Response(response=data, status=200, mimetype="application/json")
    return resp
    # return result

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

#  return whether the computer with the requested IP address is awake or not
@application.route("/ping")
def ping():

    ipAddress = request.args.get('ipAddress')

    if ipAddress:
        return pingComputer(ipAddress)

    else:
        return None

@application.route("/", methods=['GET', 'POST'])
def index():

    # selectedProject = request.args.get('project')
    
    #TODO: add in validation from here https://pythonspot.com/flask-web-forms/ or here https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    #form = ReusableForm(request.form)

    # read in JSON data of the currently configured computers
    # computers = getComputerList()

    #print form.errors
    if request.method == 'POST':
        if request.form["form_id"] == "newComputerForm":
            submitFormData(getComputerList(), request.form)
            # print(request.form["computerNameFormField"])
        if request.form["form_id"] == "deleteComputer":
            deleteComputer(getComputerList(), request.form)

        if request.form["form_id"] == "wakeComputer":
            wakeComputer(getComputerList(), request.form)

    return render_template('index.html', computers = getComputerList())
 
if __name__ == "__main__":
    application.run(port=5000, threaded=True, host=('0.0.0.0'))