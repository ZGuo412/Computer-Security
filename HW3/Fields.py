#ECE404 HW3
#Ziyu Guo 0029214148
#!/usr/bin/env python3
import os
import sys

def get_integer():
    key = None
    while True:
        if sys.version_info[0] == 3:
            key = input("\nEnter an integer which is less than 50 digits: ")
        else:
            print("python version should be 3")
            break
        key = key.strip()
        if len(key) < 50:
            key = int(key)
            return key
    return key

def determineFields():
    mod = get_integer()
    if (mod < 2):
        print('ring')
        return
    zmod = mod
    for num in range(1, zmod):
        mod = zmod
        x, x_old = 0, 1
        y, y_old = 1, 0
        while mod:
            q = num // mod
            num, mod = mod, num % mod
            x, x_old = x_old - q * x, x
            y, y_old = y_old - q * y, y
        if num != 1:
            print('ring')
            return
    print('field')
    return




if __name__ == '__main__':
    determineFields()