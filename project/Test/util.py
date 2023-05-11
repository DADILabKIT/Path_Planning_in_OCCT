# OS
# for import
import os
import sys

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR_PATH = os.path.join(FILE_PATH, '..')

sys.path.append(PROJECT_DIR_PATH)
