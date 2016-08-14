# setup.py
from distutils.core import setup
import py2exe

'''
setup(console=["HydraulicsToolBox.py"],
				data_files=[("",["ico.jpg", "rect.jpg", "rect-small.jpg"])])'''

setup(windows=["tester.py"])