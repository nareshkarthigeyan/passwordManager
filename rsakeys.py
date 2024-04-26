import json
import rsa

def generateKeys():
    (pubkey, privkey) = rsa.newkeys(512)
    keyData = {
        "public_key": pubkey.save_pkcs1().decode(),
        "private_key": privkey.save_pkcs1().decode()
    }

    with open("keys.json", 'w') as f:
        json.dump(keyData, f)


def fetchKeys():
    while True:
        try:
            with open("keys.json", "r") as f:
                keyData = json.load(f)
                pubkey = rsa.PublicKey.load_pkcs1(keyData['public_key'].encode())
                privkey = rsa.PrivateKey.load_pkcs1(keyData['private_key'].encode())
                return pubkey, privkey
        except FileNotFoundError:
            generateKeys()
        
    
(pubkey, privkey) = fetchKeys()

def encrypt(data, pubkey):
    return rsa.encrypt(data, pubkey)

def decrypt(data, privkey):
    try: 
        return rsa.decrypt(data, privkey)
    except rsa.pkcs1.DecryptionError:
        print("Decryption Error. Did you change the keys?")
        return
