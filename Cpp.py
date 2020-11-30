from Attribute import Attribute

class Cpp:
	def __init__(self, name):
		self.name = name
		self.filename = self.name + ".cpp"
		self.headerName = self.name + ".hpp"
		self.attributes = []
		self.insertLine = -1
	
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
		f.close
		h = open(self.headerName, "w")
		h.write(self.getHeaderBuff())
		h.close

	def getFileBuff(self):
		return "#include \"" + self.headerName + "\"\n\n" + self.name + "::" + self.name + "()\n{\n\t\n}\n\n" + self.name + "::~" + self.name + "()\n{\n\t\n}\n"

	def getHeaderBuff(self):
		nameUpper = self.name.upper()
		return "#ifndef " + nameUpper + "\n#define " + nameUpper + "\n\nclass " + self.name + "\n{\n\tpublic:\n\n\t" + self.name + "();\n\t~" + self.name + "();\n};\n\n#endif\n"

	def	setNewAttribute(self, line):
		args = line.split()
		m_type = args[0]
		m_name = args[1]
		m_pointer = ""
		if args[1].find("*") == 0:
			m_pointer = "*"
			m_name = args[1][1::]
		if args[1].find(";") == len(args[1]) - 1:
			m_name = m_name[:-1]
		self.attributes.append(Attribute(m_type, m_name, m_pointer))

	def	update(self):
		ret = self.parsing()
		if  ret > 0:
			return ret
		f = open(self.filename, "a")
		buff=""
		for att in self.attributes:
			# f.write(self.getClassGetter(att))
			# f.write(self.getClassSetter(att))
			buff += att.getHeader()
		f.close()
		buff += '\n'
		h = open(self.headerName, "r+")
		tmp = h.readlines()
		h.seek(0)
		h.truncate()
		tmp.insert(self.insertLine, buff)
		h.writelines(tmp)
		h.close()

	def parsing(self):
		private = True
		self.insertLine = -1
		actualLine = 0
		h = open(self.headerName, "r")
		while h.readline().find("class") == -1:
			actualLine += 1
		h.readline()
		actualLine += 1
		for line in h:
			actualLine += 1
			if line.find("};") != -1:
				break
			if private:
				if line.find("public") != -1:
					private = False
					if self.insertLine == -1:
						self.insertLine = actualLine
				elif not line == "\n" and line.find("(") == -1:
					self.setNewAttribute(line)
			elif not private:
				if line.find("private") != -1:
					private = True
				else:
					if line.find("set") != -1:
						print("set")
					if line.find("get") != -1:
						print("get")
				if line.find(self.name) != -1:
					self.insertLine = actualLine
		if self.insertLine == -1:
			print("Error: no public menber found in " + self.headerName)
			return 1
		if len(self.attributes) == 0:
			print("No attribute found in " + self.headerName)
			return 1
		self.insertLine += 1
		h.close()
		return 0

	def getClassGetter(self, att):
		return "\n{att.type}\t{att.pointer}{self.name}::{att.getter}\n{{\n\treturn this->{att.name};\n}}\n".format(att=att, self=self)

	def getClassSetter(self, att):
		return "\nvoid\t{self.name}::{att.setter}\n{{\n\tthis->{att.name} = {att.name};\n}}\n".format(att=att, self=self)
