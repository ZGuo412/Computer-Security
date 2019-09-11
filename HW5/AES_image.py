#!/usr/bin/env python 3
#Homework Number:5
#Name:Ziyu Guo
#ECN Login:guo412
#Due Date:2/19

from BitVector import *
import time
AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption

def round_key(key_words):
    key_schedule = []
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        if word_index % 4 == 0: print("\n")
        key_schedule.append(keyword_in_ints)
        num_rounds = 14
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]).get_bitvector_in_hex()
    return round_keys

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))



def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_key_schedule_256(key_bv):
    byte_sub_table = subBytesTable
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal =
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words



def get_key_from_user(key_file):
    with open(key_file, 'r') as file:
        key = file.read()
    key_bv = BitVector( textstring = key )
    return key_bv

def en_sub(statearray):
    for a in range(0, 4):
        for b in range(0, 4):
            place = int(statearray[b][a])
            statearray[b][a] = BitVector(intVal=subBytesTable[place])  # same as the sub in DES
    return statearray

def en_shiftRow(statearray):
    for c in range(1, 4):
        temp = [''] * 4
        for d in range(0, 4):
            left_shift = (d + c) % 4
            temp[d] = statearray[c][left_shift]
        for e in range(0, 4):
            statearray[c][e] = temp[e]
    return statearray

def en_mix(statearray, two, three, n, modulus):
    for g in range(0, 4):
        first_row = statearray[0][g].gf_multiply_modular(two, modulus, n) ^ statearray[1][g].gf_multiply_modular(three, modulus, n) ^ statearray[2][g] ^ statearray[3][g]
        second_row = statearray[1][g].gf_multiply_modular(two, modulus, n) ^ statearray[2][g].gf_multiply_modular(three,modulus,n) ^ statearray[3][g] ^ statearray[0][g]
        third_row = statearray[2][g].gf_multiply_modular(two, modulus, n) ^ statearray[3][g].gf_multiply_modular(three,modulus, n) ^ statearray[0][g] ^ statearray[1][g]
        fourth_row = statearray[3][g].gf_multiply_modular(two, modulus, n) ^ statearray[0][g].gf_multiply_modular(three,modulus,n) ^ statearray[2][g] ^ statearray[1][g]
        statearray[0][g] = first_row
        statearray[1][g] = second_row
        statearray[2][g] = third_row
        statearray[3][g] = fourth_row
    return statearray
def aes(bitvec, key_words, two, three, modulus):
    f = open('temp.txt', 'wb')
    statearray = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            statearray[j][i] = bitvec[32 * i + 8 * j:32 * i + 8 * (j + 1)]  # initial statearray
    for m in range(4):
        for n in range(4):
            statearray[n][m] ^= key_words[m][
                                n * 8: 8 + n * 8]  # XOR the first four word in key_word with statearray
    # statearray ^= round_keys[0]
    for rounds in range(0, 14):
        # Substitute bytes
        statearray = en_sub(statearray)
        statearray = en_shiftRow(statearray)
        n = 8
        if (rounds != 13):
            statearray = en_mix(statearray, two, three, n, modulus)
        for o in range(0, 4):
            for p in range(0, 4):
                statearray[p][o] ^= key_words[(4 * (rounds)) + 4 + o][
                                    8 * p: 8 + 8 * p]  # + 4 because skip first 4 key words
    for r in range(4):
        for s in range(4):
            statearray[s][r].write_to_file(f)
def x931(v0, dt, key_file, totalNum):
    genTables()
    key_bv = get_key_from_user(key_file)  # get the key
    key_words = gen_key_schedule_256(key_bv)  # used to xor with input block
    modulus = BitVector(bitstring='100011011')  # AES modulus
    two = BitVector(bitstring='00000010')
    three = BitVector(bitstring='00000011')
    ran = list()
    num = 0
    while num < totalNum:
        bitvec = dt
        aes(bitvec, key_words, two, three, modulus)
        bv = BitVector(filename='temp.txt')
        ede1 = bv.read_bits_from_file(128)
        aes(ede1 ^ v0, key_words, two, three, modulus)
        bv = BitVector(filename='temp.txt')
        ede2 = bv.read_bits_from_file(128)
        aes(ede1 ^ ede2, key_words, two, three, modulus)
        bv = BitVector(filename='temp.txt')
        v0 = bv.read_bits_from_file(128)
        ran.append(int(ede2))
        num += 1
    return ran

def ctr_aes_image(iv, image_file, out_file, key_file):
    f = open(image_file, 'rb')
    head_length = 0
    for k in range(0, 3):
        head = f.readline()
        head_length += len(head)   #read head file and get the length
    f.close()
    bv = BitVector(filename=image_file)
    header = bv.read_bits_from_file(head_length * 8)
    FILEOUT = open(out_file, 'wb')
    header.write_to_file(FILEOUT)
    genTables()
    key_bv = get_key_from_user(key_file)  # get the key
    key_words = gen_key_schedule_256(key_bv)  # used to xor with input block
    ### len of key_words : 60. for each of it, 32 bit. Every time read four words with 32 bits.
    modulus = BitVector(bitstring='100011011')  # AES modulus
    two = BitVector(bitstring='00000010')
    three = BitVector(bitstring='00000011')
    while bv.more_to_read:    #only aes for the iv and xor with plaintext box
        bit = bv.read_bits_from_file(128)  # AES allows 128 bits block
        bit.pad_from_right(128 - len(bit))
        bitvec = BitVector(intVal = int(iv))
        statearray = [[0 for x in range(4)] for x in range(4)]
        for i in range(4):
            for j in range(4):
                statearray[j][i] = bitvec[32 * i + 8 * j:32 * i + 8 * (j + 1)]  # initial statearray
        for m in range(4):
            for n in range(4):
                statearray[n][m] ^= key_words[m][
                                    n * 8: 8 + n * 8]  # XOR the first four word in key_word with statearray
        # statearray ^= round_keys[0]
        for rounds in range(0, 14):
            # Substitute bytes
            statearray = en_sub(statearray)
            # Shift Row
            # first row doesn't change
            # second by one byte, third by two byte, last by three
            statearray = en_shiftRow(statearray)
            # MIX COLUMNS
            n = 8
            if (rounds != 13):
                statearray = en_mix(statearray, two, three, n, modulus)
            # AddRoundKey
            for o in range(0, 4):
                for p in range(0, 4):
                    statearray[p][o] ^= key_words[(4 * (rounds)) + 4 + o][
                                        8 * p: 8 + 8 * p]  # + 4 because skip first 4 key words
        temp = BitVector(size = 0)
        for r in range(4):
            for s in range(4):
                #f.write(statearray[s][r].get_bitvector_in_hex())  # need to change the mode to w
                ans = statearray[s][r]     #need to change the mode to wb
                temp +=ans
        ans = temp ^ bit
        ans.write_to_file(FILEOUT)
        iv = int(iv) + 1   #iv + 1 and change it to bitvector for next loop
        iv = BitVector(intVal = iv)
    f.close()
    return

if __name__ == '__main__':
    dt1 = int(time.time() * 1000000)
    dt1 = BitVector(intVal=dt1, size=64)
    dt2 = int(time.time() * 1000000)
    dt2 = BitVector(intVal=dt2, size=64)
    dt = dt1 + dt2
    key_file = 'key.txt'
    v0 = 'computersecurity'
    v0 = BitVector(textstring = v0)
    iv = x931(v0, dt, 'key.txt',1 )[0]
    iv = BitVector(intVal = iv)
    ctr_aes_image(iv, 'image.ppm', 'enc_image.ppm', 'key.txt')