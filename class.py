import argparse
import sys
from Cpp import Cpp

def main(argv, prefix):
	if (len(argv) == 0):
		print("Need name of one class")
		return 1
	for arg in argv:
		Myclass = Cpp(arg,prefix)
		Myclass.createFiles()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="create cpp class", prog="class")
	parser.add_argument("-p", "--prefix", action="store_true", help="prefix filename with 'Class'")
	parser.add_argument("-s", "--suffix", action="store_true", help="suffix filename with '.class'")
	parser.add_argument("className", nargs='+', help="name of your class ")
	args = parser.parse_args()
	main(args.className, args.prefix)
