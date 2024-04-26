import json
import sys
import rsakeys
import base64
import os.path

def assign_task(command, additional=""):
    if command == "help":
        help()
    elif command == "add":
        add(additional)
    elif command == "show":
        show()
    elif command == "remove":
        remove()
    return

def add(accountName=""):
    (pubkey, privkey) = rsakeys.fetchKeys()
    if accountName == "":
        accountName = input("Enter The Account Name: ")

    if accountName in accounts:
        message = input("Password for this account is already entered. Overrite? This cannot be undone. [Y]/[N]? ")
        if message.upper() == "Y":
            password = input("Enter Password: ").encode("utf-8")
            encyrptedPW = rsakeys.encrypt(password, pubkey)
            accounts[accountName] = base64.b64encode(encyrptedPW).decode("utf-8")
            with open("accountinfo.json", "w") as f:
                json.dump(accounts, f)
    # print(accounts)

    return

def show():
    print(accounts)
    return

def help():
    pass

def remove():
    pass


n = len(sys.argv)

arguments = ("help", "add", "show", "remove")

if os.path.isfile("accountinfo.json"):
        # Read existing data from the JSON file
        with open("accountinfo.json", "r") as f:
            accounts = json.load(f)
else:
    accounts = {}

if n < 2:
    print("Usage: appname.py command. Use appname.py help for more info.")
elif sys.argv[1] not in arguments:
    print("No use for the command {", sys.argv[1], "} found. Try using appname.py help.")

if n == 2:
    assign_task(sys.argv[1])
elif n == 3:
    assign_task(sys.argv[1], sys.argv[2])

