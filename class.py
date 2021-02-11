import argparse
import sys
from Cpp import Cpp

def main(argv, prefix):
	if (len(argv) == 0):
		print("Need name of one class")
		return 1
	for arg in argv:
		Myclass = Cpp(arg,prefix)
		if prefix == "int":
			Myclass.createInterface()
		else:
			Myclass.createFiles()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="create cpp class", prog="cppclass")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--prefix", action="store_true", help="prefix filename with 'Class'")
	group.add_argument("-s", "--suffix", action="store_true", help="suffix filename with '.class'")
	group.add_argument("-I", "--interface", action="store_true", help="create interface")
	parser.add_argument("className", nargs='+', help="name of your class ")
	args = parser.parse_args()
	if args.prefix == True:
		main(args.className, "pre")
	elif (args.suffix == True):
		main(args.className, "suf")
	elif (args.interface == True):
		main(args.className, "int")
	else:
		main(args.className, None)
