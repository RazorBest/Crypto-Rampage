#!/usr/bin/env python3
import secrets
import os

flag = os.environ.get("FLAG", "flagbot{test_flag}")
SHIFT = 39
P = 128-SHIFT
MESSAGE_SIZE = len(flag)

class Lines:
    def __init__(self):
        self.sk = [secrets.randbelow(P) for _ in range(MESSAGE_SIZE**2)]

    def encrypt(self,message):
        message_list = [ ord(l)-(SHIFT-1) for l in message]
        assert(len(message_list)**2==len(self.sk))
        ct_list = [sum([message_list[i]*self.sk[j+len(message_list)*i] for i in range (len(message_list))])%P for j in range (len(message_list))]
        ct= "".join([chr(c+(SHIFT-1)) for c in ct_list])
        return(ct)
    
if __name__ == "__main__":
    L = Lines()
    print("Welcome to my new encryption machine. It can encrypt " + str(MESSAGE_SIZE) + " character text messages")
    for i in range (MESSAGE_SIZE):
        message = input(str(MESSAGE_SIZE) + " character message to encrypt:\n")
        try:
            print(L.encrypt(message))
        except: 
            print("Bad message")
    print("My flag is: " + L.encrypt(flag))


    
