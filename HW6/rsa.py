#!/usr/bin/env python3
#Homework Number:6
#Name:Ziyu Guo
#ECN Login:guo412
#Due Date:2/26

import sys
import random
from BitVector import *
class PrimeGenerator( object ):                                              #(A1)

    def __init__( self, **kwargs ):                                          #(A2)
        bits = debug = None                                                  #(A3)
        if 'bits' in kwargs  :     bits = kwargs.pop('bits')                 #(A4)
        if 'debug' in kwargs :     debug = kwargs.pop('debug')               #(A5)
        self.bits            =     bits                                      #(A6)
        self.debug           =     debug                                     #(A7)
        self._largest        =     (1 << bits) - 1                           #(A8)

    def set_initial_candidate(self):                                         #(B1)
        candidate = random.getrandbits( self.bits )                          #(B2)
        if candidate & 1 == 0: candidate += 1                                #(B3)
        candidate |= (1 << self.bits-1)                                      #(B4)
        candidate |= (2 << self.bits-3)                                      #(B5)
        self.candidate = candidate                                           #(B6)

    def set_probes(self):                                                    #(C1)
        self.probes = [2,3,5,7,11,13,17]                                     #(C2)

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):                                      #(D1)
        'returns the probability if candidate is prime with high probability'
        p = self.candidate                                                   #(D2)
        if p == 1: return 0                                                  #(D3)
        if p in self.probes:                                                 #(D4)
            self.probability_of_prime = 1                                    #(D5)
            return 1                                                         #(D6)
        if any([p % a == 0 for a in self.probes]): return 0                  #(D7)
        k, q = 0, self.candidate-1                                           #(D8)
        while not q&1:                                                       #(D9)
            q >>= 1                                                          #(D10)
            k += 1                                                           #(D11)
        if self.debug: print("q = %d  k = %d" % (q,k))                       #(D12)
        for a in self.probes:                                                #(D13)
            a_raised_to_q = pow(a, q, p)                                     #(D14)
            if a_raised_to_q == 1 or a_raised_to_q == p-1: continue          #(D15)
            a_raised_to_jq = a_raised_to_q                                   #(D16)
            primeflag = 0                                                    #(D17)
            for j in range(k-1):                                             #(D18)
                a_raised_to_jq = pow(a_raised_to_jq, 2, p)                   #(D19)
                if a_raised_to_jq == p-1:                                    #(D20)
                    primeflag = 1                                            #(D21)
                    break                                                    #(D22)
            if not primeflag: return 0                                       #(D23)
        self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))          #(D24)
        return self.probability_of_prime                                     #(D25)

    def findPrime(self):                                                     #(E1)
        self.set_initial_candidate()                                         #(E2)
        if self.debug:  print("    candidate is: %d" % self.candidate)       #(E3)
        self.set_probes()                                                    #(E4)
        if self.debug:  print("    The probes are: %s" % str(self.probes))   #(E5)
        max_reached = 0                                                      #(E6)
        while 1:                                                             #(E7)
            if self.test_candidate_for_prime():                              #(E8)
                if self.debug:                                               #(E9)
                    print("Prime number: %d with probability %f\n" %
                          (self.candidate, self.probability_of_prime) )      #(E10)
                break                                                        #(E11)
            else:                                                            #(E12)
                if max_reached:                                              #(E13)
                    self.candidate -= 2                                      #(E14)
                elif self.candidate >= self._largest - 2:                    #(E15)
                    max_reached = 1                                          #(E16)
                    self.candidate -= 2                                      #(E17)
                else:                                                        #(E18)
                    self.candidate += 2                                      #(E19)
                if self.debug:                                               #(E20)
                    print("    candidate is: %d" % self.candidate)           #(E21)
        return self.candidate                                                #(E22)

####################################  main  ######################################
#if __name__ == '__main__':

#    if len( sys.argv ) != 2:                                                 #(M1)
#        sys.exit( "Call syntax:  PrimeGenerator.py  width_of_bit_field" )    #(M2)
#   num_of_bits_desired = int(sys.argv[1])                                   #(M3)
#   generator = PrimeGenerator( bits = num_of_bits_desired )                 #(M4)
#   prime = generator.findPrime()                                            #(M5)
#   print("Prime returned: %d" % prime)                                      #(M6)

def get_p_q():
    e = 65537
    e = BitVector(intVal=e)
    size = 128
    generator1 = PrimeGenerator(bits = size)
    generator2 = PrimeGenerator(bits = size)
    prime1 = generator1.findPrime()
    prime2 = generator2.findPrime()
    while(prime1 == prime2):
        generator1 = PrimeGenerator(bits = size)
        prime1 = generator1.findPrime()
    a = BitVector(intVal= prime1)
    b = BitVector(intVal = prime2)
    while(str(a)[0:2] != '11' or  str(b)[0:2] != '11'):
        generator1 = PrimeGenerator(bits=size)
        generator2 = PrimeGenerator(bits=size)
        prime1 = generator1.findPrime()
        prime2 = generator2.findPrime()
        a = BitVector(intVal=prime1)
        b = BitVector(intVal=prime2)
    gcd1 = BitVector(intVal= int(a) - 1)
    gcd2 = BitVector(intVal=int(b) - 1)
    bv1 = gcd1.gcd(e)
    bv2 = gcd2.gcd(e)
    while(int(bv1) != 1 or int(bv2) != 1):
        generator1 = PrimeGenerator(bits=size)
        generator2 = PrimeGenerator(bits=size)
        prime1 = generator1.findPrime()
        prime2 = generator2.findPrime()
        a = BitVector(intVal=prime1)
        b = BitVector(intVal=prime2)
        gcd1 = BitVector(intVal=int(a) - 1)
        gcd2 = BitVector(intVal=int(b) - 1)
        bv1 = gcd1.gcd(e)
        bv2 = gcd2.gcd(e)
    return prime1, prime2

def rsa(command, file1, file2):
    e = 65537
   # if sys.argv[1] is '-e':
    if command is 'e':
        en(e,file1,file2)
    else:
        de(e,file1,file2)

def de(e,file1,file2):
    f = open('p.txt', 'r')
    p = int(f.read())
    f.close()
    f = open('q.txt', 'r')
    q = int(f.read())
    f.close()
    totient = (p - 1) * (q - 1)
    bv_modulus = BitVector(intVal=totient)
    bv = BitVector(intVal=e)
    d = bv.multiplicative_inverse(bv_modulus)
    d = int(d)
    n = p * q
    f1 = open(file1, 'r')
    hex = f1.read()
    f1.close()
    f1 = open('temp.txt', 'wb')
    text = BitVector(hexstring=hex)
    text.write_to_file(f1)
    f1.close()
    f = open(file2, 'wb')
    bv = BitVector(filename = 'temp.txt')
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file(256)
        bitvec = int(bitvec)
        Vp = pow(bitvec, d, p)
        Vq = pow(bitvec, d, q)
        t_p = BitVector(intVal= p)
        t_q = BitVector(intVal= q)
        Xp = q * int(t_q.multiplicative_inverse(t_p))
        Xq = p * int(t_p.multiplicative_inverse(t_q))
        decry = (Vp * int(Xp) + Vq * int(Xq)) % n
        decry = BitVector(intVal=decry, size = 256)
        decry[128:].write_to_file(f)
def en(e,file1,file2):
    p, q = get_p_q()
    totient = (p - 1) * (q - 1)
    bv_modulus = BitVector(intVal=totient)
    bv = BitVector(intVal=e)
    d = bv.multiplicative_inverse(bv_modulus)
    d = int(d)
    n = p * q
    f = open('p.txt', 'w')
    f.write(str(p))
    f.close()
    f = open('q.txt', 'w')
    f.write(str(q))
    f.close()
    #f = open(sys.argv[3], 'w')  #encrypted.txt
    f = open(file2, 'w')
    #bv = BitVector(filename = sys.argv[2]) #message.txt
    bv = BitVector(filename = file1)
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file(128)
        bitvec.pad_from_right(128 - len(bitvec))
        bitvec.pad_from_left(128)
        bitvec = int(bitvec)
        encry = pow(bitvec, e, n)
        bitvec = BitVector(intVal=encry, size = 256)
        f.write(bitvec.get_hex_string_from_bitvector())
    f.close()

if __name__ == '__main__':
    if sys.argv[1] == '-e':
        rsa('e', sys.argv[2], sys.argv[3])
    else:
        rsa('d', sys.argv[2], sys.argv[3])
