import json
import pprint
import random
import sys
import time
import rsakeys
import base64
import os.path
import getpass
from tabulate import tabulate

def refreshkeys():
    tempAccounts = {}
    (pubkey, privkey) = rsakeys.fetchKeys()
    for k,v in accounts.items():
        account, password = k, rsakeys.decrypt(base64.b64decode(v), privkey).decode("utf-8")
        tempAccounts[account] = password

    rsakeys.generateKeys()
    (pubkey, privkey) = rsakeys.fetchKeys()

    try:
        for account, password in tempAccounts.items():
            encyrptedPW = rsakeys.encrypt(password.encode("utf-8"), pubkey)
            tempAccounts[account] = base64.b64encode(encyrptedPW).decode("utf-8")

        with open("accountinfo.json", "w") as f:
            json.dump(tempAccounts, f)
    except Exception as e:
        print("An error occurred while writing to the file:", e)
        

def assign_task(command, additional="", additional2=""):
    if command == "help":
        help()
    elif command == "add":
        add(additional, additional2)
    elif command == "show":
        show(additional)
        refreshkeys()
    elif command == "remove":
        remove()
    elif command == "refresh":
        refreshkeys()
    elif command == "keys":
        (pub, priv) = rsakeys.fetchKeys()
        print(pub, priv)

    return

def add(accountName="", password=""):
    (pubkey, privkey) = rsakeys.fetchKeys()
    if not accountName:
        accountName = input("Enter The Account Name: ")

    if accounts.get(accountName) is not None:
        message = input("Password for this account is already entered. Overrite? This cannot be undone. [Y]/[N]? ")
        if message.upper() == "N":
            return
        
    if not password:        
        password = getpass.getpass(f"Enter Password for {accountName}: ").encode("utf-8")
    else:
        password = password.encode("utf-8")

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
    (pubkey, privkey) = rsakeys.fetchKeys()
    showAccounts = {}
    for k,v in accounts.items():
        try:
            account, password = k, rsakeys.decrypt(base64.b64decode(v), privkey).decode("utf-8")
            showAccounts[account] = password
        except Exception as e:
            print("An error occured. Error:", e, "Have you changed the keys?")
            return
    
    if name == "all":
        # pprint.pprint(showAccounts)
        table_data = [(key, value) for key, value in showAccounts.items()]
        table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
        print(table)
        print(" ")

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
            table_data = [(accountName, showAccounts[accountName])]
            table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
            print(table)
            print(" ")

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
    help_message = """
Passman - Password Manager

Usage:
    passman command

Commands:
    add          Add a new account
    show         Show account information
    refresh      Refresh account information
    help         Show this help message

Examples:
    passman add Google                # Add a new account named "Google"
    passman add Facebook password     # Add a new account named "Facebook" with password "password"
    passman show all                       # Show all accounts
    passman show Google               # Show account information for "Google"
    passman refresh                     # Refresh account information

For more information, visit: https://github.com/nareshkarthigeyan/passwordManager

Note:
    - Passwords are encrypted at all times.
    - Passwords will disappear from the screen after 5 seconds.
"""
    print(help_message)
    return

def remove():
    pass


n = len(sys.argv)

arguments = ("help", "add", "show", "remove", "keys", "refresh")

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
elif n == 4:
    assign_task(sys.argv[1], sys.argv[2], sys.argv[3])

