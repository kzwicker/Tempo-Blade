import os
def main():
    print(next(os.walk("."))[2])
main()