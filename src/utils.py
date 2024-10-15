import hashlib
import jwt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes
import base64
import datetime
import unicodedata
import os, signal
###
import configure
from src.enums import RESPONSE_CODE

#region General utils
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđ₫ďĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdddIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def str_remove_accents(s):
    input_str = ''.join(c for c in unicodedata.normalize('NFKC', s)
                  if unicodedata.category(c) != 'Mn')
    s = ""
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s
#endregion

###

#region Web utils
secret_key = "mhWv2B5q6i8Zd"
iss = "thantai"

def format_id(id) -> str:
    return "{0:04}".format(id)

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

def jwt_gen(id, role, expired, subscribe_expired, payload):
    return jwt.encode({"iss": iss, 
                       "id": id, 
                       "role": role, 
                       "exp": expired, 
                       "subs_exp": subscribe_expired, 
                       "payload": payload}, 
                       secret_key, algorithm="HS256")

def jwt_validate(token: str) -> tuple[str | dict[str, any], bool, int]:
    try:
        data = jwt.decode(token, secret_key, issuer=iss, algorithms=["HS256"])
        return data, True, RESPONSE_CODE.OK
    except jwt.ExpiredSignatureError as e:
        return "JWT Expired", False, RESPONSE_CODE.UNAUTHORIZED
    except jwt.InvalidTokenError as e:
        return "JWT Invalid", False, RESPONSE_CODE.BAD_REQUEST
    except Exception as e:
        return e, False, RESPONSE_CODE.INTERNAL_SERVER_ERROR

def str_replace_uncommon_char(origin: str):
    preprocess = origin
    remove_template = ["\xa0", "'", '"', "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "\\", "?", ".", ",", "|", "{", "}", "[", "]" ";", ":"]
    for template in remove_template:
        preprocess = preprocess.replace(template, "")
    return preprocess   

def kill_server():
    os.kill(os.getpid(), signal.SIGINT)  
#endregion

###

#region Modules utils
#endregion