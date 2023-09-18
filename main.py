from PythonC.compiler import Compiler

import argparse

parser = argparse.ArgumentParser(
    prog='PyCpp',
    description='Compiles Python code into Cpp',
    epilog='Made for exploration and educational purposes'
)

parser.add_argument('target', nargs='?', default='inputMain.py')
parser.add_argument('root', nargs='?', default='files/input/test1')

args = parser.parse_args()

comp = Compiler(args.target, args.root)
comp.compile()

breakpoint()
