import sys
from src.main import main

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
