import os
import sys

# Add parent directory to path so Vercel can find the voidlens package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voidlens.api import app
