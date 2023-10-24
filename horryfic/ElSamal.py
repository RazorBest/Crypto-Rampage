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


flag = open("flag.txt","rb").read()

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
		
		K = hashlib.sha256(long_to_bytes(key.x)).digest()
		
		cipher = AES.new(K,AES.MODE_ECB)
		
		ciphertext = cipher.encrypt(pad(flag,16))
		
		return x*y,ciphertext.hex()
	
		

print(ElSamal().encrypt())


