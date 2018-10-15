#!/usr/bin/env python3

"""
Fix Worpress infected site.
Tested with wordpress 4.9.3 infected.
"""


import glob
import mmap
import os
import subprocess
import re
import sys

def get_files():
    """ Return list of files"""
    return [f for f in glob.glob('./www/**', recursive=True) \
            if os.path.isfile(f) and \
            os.stat(f).st_size != 0 and
            not f.startswith('./www/.git')]

def get_0xfcc4(files):
    out = subprocess.run("ag -l _0xfcc4 " + os.getcwd() + "/www", shell=True, capture_output=True)
    matches = [f.decode(sys.stdout.encoding) for f in out.stdout.strip().split(b'\n') if f != b""]
    """
    In alternative you can run this, but in my mac it's slower :(
    for fn in files:
        with open(fn, 'rb', 0) as f, \
             mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b'_0xfcc4') != -1:
                matches.append(fn)
    """
    return matches

def fix_0xfcc4(files):
    txt = None
    for fn in files:
        with open(fn, 'r', errors='ignore') as f:
            txt = f.read()
        txt1 = re.sub(r"<script language=javascript>var _0xfcc4.*</script>", "", txt, flags=re.M)
        txt2 = re.sub(r"var _0xfcc4.*125\)\);", "", txt1, flags=re.M)
        with open(fn, 'w') as f:
            f.write(txt2)

def get_118(files):
    out = subprocess.run("ag -l 'String.fromCharCode\\(118' " + os.getcwd() + "/www", shell=True, capture_output=True)
    return [f.decode(sys.stdout.encoding) for f in out.stdout.strip().split(b'\n') if f != b""]

def fix_118(files):
    txt = None
    for fn in files:
        with open(fn, 'r', errors='ignore') as f:
            txt = f.read()
        txt1 = re.sub(r"<script language=javascript>eval\(String\.fromCharCode\(118.*</script>", "", txt, flags=re.M)
        txt2 = re.sub(r"eval\(String\.fromCharCode\(118.*\)\);", "", txt1, flags=re.M)
        with open(fn, 'w') as f:
            f.write(txt2)

def main():
    """Main entry function."""
    files = get_files()
    print("Number of files: {}".format(len(files)))

    matches = get_0xfcc4(files)
    print("Number of 0xfcc4 matches: {}".format(len(matches)))
    fix_0xfcc4(matches)
    matches = get_0xfcc4(files)
    print("Matches of 0xfcc4 now: {}".format(len(matches)))

    matches = get_118(files)
    print("Number of 118 matches: {}".format(len(matches)))
    fix_118(matches)
    matches = get_118(files)
    print("Matches of 118 now: {}".format(len(matches)))

if __name__ == "__main__":
    main()
