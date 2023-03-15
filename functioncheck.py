import sys
import os

IDR_API_LEXUS = os.getenv("IDR_API_LEXUS")
IDR_API_HSSD = os.getenv("IDR_API_HSSD")
IDR_API_MHC = os.getenv("IDR_API_MHC")
IDR_API_L4 = os.getenv("IDR_API_L4")
FS_API = os.getenv("FS_API")


def functionCheck():
    print("Performing Function Check")
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10+ Needed")
    if str(IDR_API_LEXUS) == "None":
        sys.exit("IDR_API_LEXUS key missing")
    if str(IDR_API_HSSD) == "None":
        sys.exit("IDR_API_HSSD key missing")
    if str(IDR_API_MHC) == "None":
        sys.exit("IDR_API_MHC key missing")
    if str(IDR_API_L4) == "None":
        sys.exit("IDR_API_L4 key missing")
    if str(FS_API) == "None":
        sys.exit("FS_API key missing")
    print("Function Check Succeeded")


if __name__ == "__main__":
    functionCheck()
