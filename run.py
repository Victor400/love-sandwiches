# run.py

import sys

def check_venv():
    # Check if we are inside a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("The virtual environment is active.")
    else:
        print("The virtual environment is not active.")

if __name__ == "__main__":
    check_venv()
