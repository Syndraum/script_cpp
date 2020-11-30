import sys
from Cpp import Cpp

def main(argv):
	if (len(argv) == 0):
		print("Need name of one class")
		return 1
	for arg in argv:
		Myclass = Cpp(arg)
		Myclass.update()

if __name__ == "__main__":
	main(sys.argv[1:])