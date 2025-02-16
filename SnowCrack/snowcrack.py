# snowcrack.py
#   Binary search based dictionary cracking utility
# By: Luke Jones

from bisect import bisect_left
import os
import sys
import time
import datetime
import binascii
import hashlib

######
def crackMulti(inhash, file, directory):
    """crackMulti manages cracking using multi-part dictionaries which are tracked
    via the base file name.
    -
    inhash: hash to crack
    file: base dictionary file (.sgn)"""

    print("\nSearching...")
    t = time.time()
    found = False

    files = [directory+f for f in next(os.walk(directory))[2]]
             #if (file[:-9] in f) and f[-6:] == ".psdct"]
    
    for f in files:
        with open(f, 'r') as table:
            print(table.name)
            lines = table.readlines()
            heads = [l[:4] for l in lines]
            
            head = inhash[:4]
            tail = inhash[4:]
            pos = bisect_left(heads, head)
            
            try:
                line = lines[pos]
                hashes,passes = line.split("÷")
                hashes = hashes.split("|")[1:]
                passes = passes.split("¬")
                m = hashes.index(tail)
                pas = passes[m]

                if not pos == 0:
                    print("Success! Password is:", pas)
                    print("\nRuntime: {}".format(_toTime(time.time()-t)))
                    
                    table.close()
                    found = True
                    break
            
            except ValueError:
                pass

    if not found:
        print("Password not found.")
        
    input("\nPress enter to exit...")
    print("")

######
def crackSingle(inhash,file,directory):
    """crackSingle manages cracking using a single file.
    -
    inhash: hash to crack
    file: dictionary file (.sdct)"""
        
    print("\nSearching...")
    t = time.time()
    table = open(directory+file, 'r')
    lines = table.readlines()
    heads = [l[:5] for l in lines]
    
    table.close()

    head = inhash[:4]
    tail = inhash[4:]
    pos = bisect_left(heads, head)

    try:
        line = lines[pos]
        hashes,passes = line.split("÷")
        hashes = hashes.split("|")[1:]
        passes = passes.split("¬")
        m = hashes.index(tail)
        pas = passes[m]
        
    except ValueError:
        print("Password not found!")
        return
        
    print("Success! Password is:", pas)
    print("\nRuntime: {}".format(_toTime(time.time()-t)))

######
def _toTime(raw):
    # Converts time in seconds to appropriate format

    t = raw
    
    if t < 60:
        return str(round(t,2))+" seconds"
    elif t < 3600:
        return str(round(t/60,2))+" minutes"
    else:
        return str(round((t/60)/60,2))+ " hours"

######
def _digestFile(file):
    # Converts file input into proper format to stop case sensitivity

    di = None

    if file.count("\\") != 0:
        di = file.rfind("\\")+1
    elif file.count("/") != 0:
        di = file.rfind("/")+1
    else:
        directory = sys.path[0]+"\\"

    if di != None:
        directory = file[:di]
        
    fname = file[di:-4]
    end = ".sgn"
    rfname = ""
    norm = False
    
    if ("alph" in fname or "Alph" in fname):
        rfname += "Alph"
    if ("caps" in fname or "Caps" in fname):
        rfname += "Caps"
    if ("nums" in fname or "Nums" in fname):
        rfname += "Nums"
    if ("chal" in fname or "Chal" in fname):
        rfname += "Chal"
    if rfname != "":
        rfname += " "+fname[len(rfname)+1:]+end
        fname = rfname
    else:
        fname += end
        
    return fname, directory

######  
def main():
    # Dictionary file is given by user. Script runs through dictionary using
    # a binary search to locate hash, retreives password.

    print("SnowCrack dictionary cracker.\n\n")
    
    hlist = ["ntlm","md4","md5","whirlpool","sha1","sha224","sha256","sha384","sha512"]
    inhash = input("Hash: ")

    print("\nValid hash types:\n0-NTLM 1-MD4 2-MD5 3-Whirlpool 4-SHA1 5-SHA2(224) 6-SHA2(256) 7-SHA2(384) 8-SHA2(512)\n")
    
    while True:
        try:
            hashtype = hlist[int(input("Hash type (number): "))]
            break
        except ValueError:
            print("Invalid input!")

    # If the hash is longer than 32 characters, hashes are stored in md5 format
    if not hashtype in ["ntlm", "md4", "md5"]:
        inhash = hashlib.md5(inhash.encode("ascii")).digest()
        inhash = str(binascii.hexlify(inhash))[2:-1]
    
    while True:
        file = input("Dictionary file: ")

        if os.path.isfile(file):
            break
        else:
            print("Dictionary not found!\n")

    fname, directory = _digestFile(file)
    
    for f in next(os.walk(directory))[2]:
        if f.startswith(fname.split(".")[0]+" ~"):
            crackMulti(inhash, fname, directory)
            return
        
    crackSingle(inhash, fname, directory)

    input("\nPress enter to exit...")
    print("")


if __name__ == "__main__":
    main()
