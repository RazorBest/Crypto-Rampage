import random
from Crypto.Util.number import *
from Crypto.PublicKey import ECC
from fastecdsa.curve import Curve
from fastecdsa.point import Point
from fastecdsa.curve import P256
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
import hashlib
from operator import xor


OUTPUT_FILE = "output.txt"
flag = b"CYDEX{dsadsadsadsadsadsa}"#open("flag.txt","rb").read()

class ElSamal:

    def __init__(self):
        self.order = P256.q
        self.generator = P256.G
    
    def generate_key(self):
        x = random.randint(1, self.order-1)
        y = xor(x, self.order + 26854634375482082607969097059425148432393575017737131280054341130926)

        Q = x * self.generator
        P = y * self.generator 
        return (x,y,Q,P)
    
    def encrypt(self):
        x,y,P,Q = self.generate_key()
        key = x * P

        self.x = x
        
        K = hashlib.sha256(long_to_bytes(key.x)).digest()
        
        cipher = AES.new(K,AES.MODE_ECB)
        
        ciphertext = cipher.encrypt(pad(flag,16))
        
        return x*y,ciphertext.hex()
    
        
knowns = None
with open(OUTPUT_FILE) as file:
   data = file.read()
   known1, known2 = data.split(",")
   known1 = int(known1[1:])
   known2 = known2[2:-3]
   knowns = (known1, known2)

es = ElSamal()
#xy, _ = es.encrypt()
xy = knowns[0]

C = P256.q + 26854634375482082607969097059425148432393575017737131280054341130926
x = 0
mod = 16
# Bruteforce x in blocks of 4 bits, starting with the least significant
for i in range(512):
    new_poss = []
    for j in range(mod):
        x2 = (j*mod**i) + x
        if (x2 * xor(x2, C)) % (mod**(i+1)) == xy % (mod**(i+1)):
            # Stop the search at the first solution
            # We didn't check to see if there are more solutions
            # The first one turned out to be the good one
            x = x2
            break

key = x * (x * es.generator)
K = hashlib.sha256(long_to_bytes(key.x)).digest()
cipher = AES.new(K,AES.MODE_ECB)
msg = cipher.decrypt(bytes.fromhex(knowns[1]))
print(msg)
