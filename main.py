import json
import sys
import rsakeys
import base64
import os.path
import getpass

def assign_task(command, additional=""):
    if command == "help":
        help()
    elif command == "add":
        add(additional)
    elif command == "show":
        show()
    elif command == "remove":
        remove()
    elif command == "genkeys":
        if os.path.isfile("keys.json"):
            message = input("Keys have already been generated before. Overriding it will make the already stored passwords irrecoverable. Confirm? [Y]/[N]? ")
            if message.upper() == "Y":
                rsakeys.generateKeys()
    elif command == "keys":
        (pub, priv) = rsakeys.fetchKeys()
        print(pub, priv)

    return

def add(accountName=""):
    (pubkey, privkey) = rsakeys.fetchKeys()
    if accountName == "":
        accountName = input("Enter The Account Name: ")

    if accounts.get(accountName) is not None:
        message = input("Password for this account is already entered. Overrite? This cannot be undone. [Y]/[N]? ")
        if message.upper() == "N":
            return
        
    password = getpass.getpass("Enter Password: ").encode("utf-8")
    encyrptedPW = rsakeys.encrypt(password, pubkey)
    accounts[accountName] = base64.b64encode(encyrptedPW).decode("utf-8")
    try:
        with open("accountinfo.json", "w") as f:
            json.dump(accounts, f)
    except Exception as e:
        print("An error occurred while writing to the file:", e)
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

arguments = ("help", "add", "show", "remove", "keys", "genkeys")

if os.path.isfile("accountinfo.json"):
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

