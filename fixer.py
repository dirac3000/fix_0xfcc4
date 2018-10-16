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
    try:
        out = subprocess.check_output("rg -l _0xfcc4 " + os.getcwd() + "/www", shell=True)
    except subprocess.CalledProcessError:
        return []
    matches = [f.decode(sys.stdout.encoding) for f in out.strip().split(b'\n') if f != b""]
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
    try:
        out = subprocess.check_output("rg -l 'String.fromCharCode\\(118' " + os.getcwd() + "/www", shell=True)
    except subprocess.CalledProcessError:
        return []
    return [f.decode(sys.stdout.encoding) for f in out.strip().split(b'\n') if f != b""]

def fix_118(files):
    txt = None
    for fn in files:
        with open(fn, 'r', errors='ignore') as f:
            txt = f.read()
        txt1 = re.sub(r"<script language=javascript>eval\(String\.fromCharCode\(118.*</script>", "", txt, flags=re.M)
        txt2 = re.sub(r"eval\(String\.fromCharCode\(118.*\)\);", "", txt1, flags=re.M)
        with open(fn, 'w') as f:
            f.write(txt2)

def get_suspicious_eval(files):
    wplist = None
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files-wordpress-4.9.3.txt'), 'r') as f:
        wplist = f.readlines()
    #print(wplist[0].encoding)

    try:
        out = subprocess.check_output("rg -l 'eval\\s*\\(' " + os.getcwd() + "/www", shell=True)
    except subprocess.CalledProcessError:
        return []
    return [f.decode(sys.stdout.encoding) for f in out.strip().split(b'\n')
                if f != b"" and
                f.decode(sys.stdout.encoding).replace(os.getcwd() + "/www/", "") not in wplist]

def get_suspisious_php_code(files):
    try:
        out = subprocess.check_output("rg -l '<\\?php\\s\\s+\\$\\w+\\s=\\s\\d+;' " + os.getcwd() + "/www", shell=True)
    except subprocess.CalledProcessError:
        return []
    return [f.decode(sys.stdout.encoding) for f in out.strip().split(b'\n') if f != b""]

def fix_suspicious_php_code(files):
    txt = None
    for fn in files:
        with open(fn, 'r', errors='ignore') as f:
            txt = f.read()
        txt1 = re.sub(r"<\?php\s\s+\$\w+\s=\s\d+;.*\?>", "", txt, flags=re.M)
        with open(fn, 'w') as f:
            f.write(txt1)

def get_suspisious_php_include(files):
    try:
        out = subprocess.check_output("rg -l '@include \"' " + os.getcwd() + "/www", shell=True)
    except subprocess.CalledProcessError:
        return []
    return [f.decode(sys.stdout.encoding) for f in out.strip().split(b'\n') if f != b""]

def fix_suspicious_php_include(files):
    txt = None
    for fn in files:
        with open(fn, 'r', errors='ignore') as f:
            txt = f.read()
        txt1 = re.sub(r"@include\s\".*;", "", txt, flags=re.M)
        with open(fn, 'w') as f:
            f.write(txt1)

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

    matches = get_suspisious_php_code(files)
    print("Number of suspicious php code matches: {}".format(len(matches)))
    fix_suspicious_php_code(matches)
    matches = get_suspisious_php_code(files)
    print("Matches of suspicious php code now: {}".format(len(matches)))

    matches = get_suspisious_php_include(files)
    print("Number of suspicious php includes matches: {}".format(len(matches)))
    fix_suspicious_php_include(matches)
    matches = get_suspisious_php_include(files)
    print("Matches of suspicious php includes now: {}".format(len(matches)))

    matches = get_suspicious_eval(files)
    print("Matches of suspicious eval: {}".format(len(matches)))
    print("\nSuspicious eval matches, to edit or delete manually:\n\n{}".format("\n".join(matches)))
    print("\nTo finish, compare a reference wordpress with the one attacked to see if there are still bogus files.")


if __name__ == "__main__":
    main()
