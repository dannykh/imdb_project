import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from prep.vector_file_generation import run

if __name__ == "__main__":
    run()
