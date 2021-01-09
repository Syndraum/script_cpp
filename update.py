import sys
from Cpp import Cpp
from os import listdir
from os.path import isfile, join

def main(argv):
	if (len(argv) == 0):
		files = [f[:-4] for f in listdir("./") if isfile(join("./", f)) and f[-4:] == ".cpp"]
		for f in files:
			Myclass = Cpp(f, False)
			Myclass.update()
	else:
		for arg in argv:
			Myclass = Cpp(arg)
			Myclass.update()

if __name__ == "__main__":
	main(sys.argv[1:])