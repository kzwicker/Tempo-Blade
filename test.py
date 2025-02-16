import subprocess
import os
import sys

def main():
    print(check_file_exists(sys.argv[1]))

def check_file_exists(filename):
    return os.path.exists(filename)

main()