#!/bin/python
import subprocess
import os
import sys

def main():
    print(get_subdirectories())

def get_subdirectories():
    return next(os.walk('.'))[1]

main()