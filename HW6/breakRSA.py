#!/usr/bin/env python3
import sys
import numpy as np
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
    e = 3
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
def get_d(p,q):
    e = 3
    totient = (p - 1) * (q - 1)
    bv_modulus = BitVector(intVal=totient)
    bv = BitVector(intVal=e)
    d = bv.multiplicative_inverse(bv_modulus)
    d = int(d)
    return d
def breakRSA(file1,file2):
    key1p, key1q = get_p_q()
    key2p, key2q = get_p_q()
    key3p, key3q = get_p_q()
    d1 = get_d(key1p, key1q)
    d2 = get_d(key2p, key2q)
    d3 = get_d(key3p, key3q)
    n1 = key1p * key1q
    n2 = key2p * key2q
    n3 = key3p * key3q
    N = n1 * n2 * n3
    rsa(n1, 'en1.txt',file1)
    rsa(n2, 'en2.txt',file1)
    rsa(n3, 'en3.txt',file1)
    bv1 = BitVector(filename = 'en1.txt')
    bv2 = BitVector(filename='en2.txt')
    bv3 = BitVector(filename='en3.txt')
    f = open(file2, 'wb')
    while bv1.more_to_read:
        bitvec1 = int(bv1.read_bits_from_file(256))
        bitvec2 = int(bv2.read_bits_from_file(256))
        bitvec3 = int(bv3.read_bits_from_file(256))
        #N is the products of n1,n2,n3. For each n, n is coprime to p,q. P, Q are prime numbers.
        M1 = n2 * n3
        M2 = n1 * n3
        M3 = n2 * n1
        t_M1 = BitVector(intVal=M1)
        t_M2 = BitVector(intVal=M2)
        t_M3 = BitVector(intVal=M3)
        t_n1 = BitVector(intVal=n1)
        t_n2 = BitVector(intVal=n2)
        t_n3 = BitVector(intVal=n3)
        c1 = M1 * int(t_M1.multiplicative_inverse(t_n1))
        c2 = M2 * int(t_M2.multiplicative_inverse(t_n2))
        c3 = M3 * int(t_M3.multiplicative_inverse(t_n3))
        breakrsa = (c1 * bitvec1 + bitvec2 * c2 + bitvec3 * c3) % N
        breakrsa = solve_pRoot(3, breakrsa)
        breakrsa = BitVector(intVal = breakrsa, size = 256)
        breakrsa[128:].write_to_file(f)



def rsa(n, file,file1):
    e = 3
    f = open(file, 'wb')
    # bv = BitVector(filename = sys.argv[2]) #message.txt
    bv = BitVector(filename=file1)
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file(128)
        bitvec.pad_from_right(128 - len(bitvec))
        bitvec.pad_from_left(128)
        bitvec = int(bitvec)
        encry = pow(bitvec, e, n)
        bitvec = BitVector(intVal=encry, size=256)
        bitvec.write_to_file(f)
    f.close()

def solve_pRoot(p, y):
    p = int(p);
    y = int(y);
    # Initial guess for xk
    try:
        xk = int(pow(y, 1.0 / p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = int(pow(2.0, (a + np.log2(float(y0))) / p));

    # Solve for x using Newton's Method
    err_k = int(pow(xk, p)) - y;
    while (abs(err_k) > 1):
        gk = p * int(pow(xk, p - 1));
        err_k = int(pow(xk, p)) - y;
        xk = int(-err_k / gk) + xk;
    return xk

if __name__ == '__main__':
    breakRSA(sys.argv[1], sys.argv[2])
