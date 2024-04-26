import json
import pprint
import sys
import time
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
        show(additional)
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
    (pubkey, _) = rsakeys.fetchKeys()
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

def show(name=""):
    (_, pubkey) = rsakeys.fetchKeys()
    showAccounts = {}
    for k,v in accounts.items():
        account, password = k, rsakeys.decrypt(base64.b64decode(v), pubkey).decode("utf-8")
        showAccounts[account] = password
    
    if name == "all":
        pprint.pprint(showAccounts)
    else:
        if not name:
            accountName = input("Enter Account: ")
        else:
            accountName = name

        if accountName not in showAccounts:
            message = input("Account not found. Add a new account with that name? [Y]/[N]? ")
            if message.upper() == "Y":
                add(name)
                return
        else:
            print(accountName, showAccounts[accountName])

    for i in range(5, 0, -1):
        print(f"clearing screen in {i} seconds.", end="\r")
        time.sleep(1)
    if os.name == 'nt':
        _ = os.system('cls')
    # For UNIX-like systems (Linux, macOS)
    else:
        _ = os.system('clear')
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

