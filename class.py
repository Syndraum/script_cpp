import sys

class CppClass:
	name=""

	def __init__(self, name):
		self.name = name
		self.filename = self.name + ".cpp"
		self.headerName = self.name + ".hpp"
	
	def is_file_exist(self, filename):
		try:
			f = open(filename)
			f.close()
		except OSError:
			return False
		else:
			print("file " + filename + " already exist")
			return True
	
	def is_exist(self):
		return self.is_file_exist(self.filename) or self.is_file_exist(self.headerName)
	
	def createFiles(self):
		if self.is_exist():
			return 0
		f = open(self.filename, "w")
		f.write(self.getFileBuff())
		h = open(self.headerName, "w")
		h.write(self.getHeaderBuff())
		f.close
		h.close

	def getFileBuff(self):
		return "#include \"" + self.headerName + "\"\n\n" + self.name + "::" + self.name + "()\n{\n\t\n}\n\n" + self.name + "::~" + self.name + "()\n{\n\t\n}\n"

	def getHeaderBuff(self):
		nameUpper = self.name.upper()
		return "#ifndef " + nameUpper + "\n#define " + nameUpper + "\n\nclass " + self.name + "\n{\n\tpublic:\n\n\t" + self.name + "();\n\t~" + self.name + "();\n};\n\n#endif\n"

def main(argv):
	if (len(argv) == 0):
		print("Need name of one class")
		return 1
	for arg in argv:
		Myclass = CppClass(arg)
		Myclass.createFiles()

if __name__ == "__main__":
	main(sys.argv[1:])
