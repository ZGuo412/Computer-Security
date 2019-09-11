#!/usr/bin/env python3.7
#ECE 404 Homework 1
#Ziyu Guo 
#This code is based on DecryptForFun and I did a little change to finish the homework
import sys
from BitVector import *                                                     #(A)

if len(sys.argv) is not 3:                                                  #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

PassPhrase = "Hopes and dreams of a million years"                          #(C)

BLOCKSIZE = 16                                                              #(D)
numbytes = BLOCKSIZE // 8                                                   #(E)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
for i in range(0,len(PassPhrase) // numbytes):                              #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
    bv_iv ^= BitVector( textstring = textstr )                              #(I)

# Create a bitvector from the ciphertext hex string:
FILEIN = open(sys.argv[1])                                                  #(J)
encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)

# check key:
for j in range(0, 2**16):
    key_bv = BitVector(intVal = j, size = 16)                        #(S)

# Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector( size = 0 )                                    #(T)

# Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv                                            #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                                  #(b)

# Extract plaintext from the decrypted bitvector:    
    outputtext = msg_decrypted_bv.get_text_from_bitvector()                     #(c)
    if "Cormac McCarthy" in outputtext:
        f = open('key.txt','w+')
        f.write(str(j))
        f.close()
        break
# Write plaintext to the output file:
FILEOUT = open(sys.argv[2], 'w')                                            #(d)
FILEOUT.write(outputtext)                                                   #(e)
FILEOUT.close()                                                             #(f)


###    You go back home and everything you wished was different is still the same and everything you wished was the same is different.
###
###-Cormac McCarthy, Cities of the Plain
###
###     key: 26998