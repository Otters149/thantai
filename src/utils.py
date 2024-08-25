import hashlib
import jwt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes
import base64
import datetime

###
import configure

secret_key = "mhWv2B5q6i8Zd"
iss = "thantai"

def md5_get_hash(input: str):
    hash = hashlib.md5(input.encode('utf-8')).hexdigest()
    return hash

def rsa_decode(input: str):
    # return input
    msg = input
    msg = base64.b64decode(msg)
    sentinel = get_random_bytes(128)
    private_keyPEM = RSA.import_key(configure.rsa_private_key_pem)
    decyptor = PKCS1_v1_5.new(private_keyPEM)
    decrypted = decyptor.decrypt(msg, sentinel)
    return str(decrypted, 'utf-8')

def rsa_encode(input: str):
    # return input    
    msg = input
    public_keyPEM = RSA.import_key(configure.rsa_public_key_pem)
    encryptor = PKCS1_v1_5.new(public_keyPEM)
    encrypted = encryptor.encrypt(bytes(msg, encoding="UTF-8"))
    return str(base64.b64encode(encrypted))

def rsa_gen_keypem():
    key_pair = RSA.generate(1024)
    public_key = key_pair.publickey()
    public_keypem = public_key.exportKey()

    private_keypem = key_pair.exportKey()
    return public_keypem.decode('ascii'), private_keypem.decode('ascii')

def server_timestamp():
    return str(int(datetime.datetime.now().timestamp()))

def server_datetime():
    return str(datetime.datetime.now())

def jwt_gen(id, role, expired, payload):
    return jwt.encode({"iss": iss, "id": id, "role": role, "exp": expired, "payload": payload}, secret_key, algorithm="HS256")

def jwt_validate(token):
    try:
        data = jwt.decode(token, secret_key, issuer=iss, algorithms=["HS256"])
        return data, True
    except jwt.ExpiredSignatureError as e:
        return "JWT Expired", False
    except jwt.InvalidTokenError as e:
        return "JWT Invalid", False
    except Exception as e:
        return e, False   

def str_replace_uncommon_char(origin: str):
    preprocess = origin
    remove_template = ["\xa0", "'", '"', "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "\\", "?", ".", ",", "|", "{", "}", "[", "]" ";", ":"]
    for template in remove_template:
        preprocess = preprocess.replace(template, "")
    return preprocess     
