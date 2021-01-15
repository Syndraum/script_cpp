from Attribute import Attribute

class Cpp:
	def __init__(self, name, format=None):
		self.name = name
		if (format == "pre"):
			self.prefix = "Class"
			self.filename = self.prefix + self.name.capitalize() + ".cpp"
			self.headerName = self.prefix + self.name.capitalize() + ".hpp"
		elif (format == "suf"):
			self.filename = self.name + ".class.cpp"
			self.headerName = self.name + ".class.hpp"
		else:
			self.filename = self.name + ".cpp"
			self.headerName = self.name + ".hpp"
		self.attributes = []
		self.setters = []
		self.getters = []
		self.insertLine = -1
	
	def is_file_exist(self, filename):
		try:
			f = open(filename)
			f.close()
		except OSError:
			return False
		else:
			return True
	
	def file_already_exist(self, filename):
		if self.is_file_exist(filename):
			print("file " + filename + " already exist")
			return True
		return False

	def file_not_exist(self, filename):
		if not self.is_file_exist(filename):
			print("file " + filename + " not exist")
			return True
		return False

	def is_exist(self):
		if self.is_file_exist(self.filename):
			print("file " + self.filename + " already exist")
			return True
		if self.is_file_exist(self.headerName):
			print("file " + self.headerName + " already exist")
			return True
		return False
	
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
		return "#include \"" + self.headerName + "\"\n\n" + self.name + "::" + self.name + "(void){}\n\n"+ self.name + "::" + self.name + "("+self.name+" const & src)\n{\n\t*this = src;\n}\n\n" + self.name + "::~" + self.name + "(void)\n{\n\t\n}\n\n"+self.name+" &\t"+self.name+"::operator=("+self.name+" const & rhs)\n{\n\t*this = rhs;\n}\n"

	def getHeaderBuff(self):
		nameUpper = self.name.upper()
		return "#ifndef " + nameUpper + "\n# define " + nameUpper + "\n\nclass " + self.name + "\n{\npublic:\n\n\t" + self.name + "(void);\n\t" + self.name + "(" + self.name + " const & src);\n\t~" + self.name + "(void);\n\t"+self.name+" &\toperator=("+self.name+" const &rhs);\n\nprivate:\n\n};\n\n#endif\n"

	def	setNewAttribute(self, line):
		args = line.split()
		i = 0
		if (args[i] == "static"):
			i += 1
		m_type = args[i]
		i += 1 
		m_name = args[i]
		m_pointer = ""
		if args[i].find("*") == 0:
			m_pointer = "*"
			m_name = args[i][1::]
		if args[i].find(";") == len(args[i]) - 1:
			m_name = m_name[:-1]
		self.attributes.append(Attribute(m_type, m_name, m_pointer))

	def	update(self):
		if self.file_not_exist(self.filename) or self.file_not_exist(self.headerName):
			return 1
		ret = self.parsing()
		if  ret > 0:
			return ret
		f = open(self.filename, "a")
		buff=""
		for att in self.attributes:
			if att.a_name not in self.setters and att.a_name not in self.getters:
				f.write(self.getClassGetter(att))
				f.write(self.getClassSetter(att))
				buff += att.getHeader()
		f.close()
		if buff != "":
			buff += '\n'
		h = open(self.headerName, "r+")
		tmp = h.readlines()
		h.seek(0)
		h.truncate()
		tmp.insert(self.insertLine, buff)
		h.writelines(tmp)
		h.close()
		return 0

	def parsing(self):
		private = True
		self.insertLine = -1
		actualLine = 0
		h = open(self.headerName, "r")
		buffer=""
		find = -1
		while find == -1:
			buffer = h.readline()
			find = buffer.find("class")
			actualLine += 1
		res = buffer.split()
		self.name = res[1]
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
					setter=line.find("set")
					getter=line.find("get")
					if setter != -1:
						self.setters.append(line[setter+3:line.find("(", setter)].lower())
					if getter != -1:
						self.getters.append(line[getter+3:line.find("(", getter)].lower())
				if line.find(self.name) != -1:
					self.insertLine = actualLine
		if self.insertLine == -1:
			print("Error: no public menber found in " + self.headerName)
			return 1
		if len(self.attributes) == 0:
			print("No attribute found in " + self.headerName)
			return 1
		h.close()
		return 0

	def getClassGetter(self, att):
		if (len(att.type) < 4):
			return "\n{att.type}\t\t{att.pointer}{self.name}::{att.getter} const\n{{\n\treturn this->{att.name};\n}}\n".format(att=att, self=self)
		else:
			return "\n{att.type}\t{att.pointer}{self.name}::{att.getter} const\n{{\n\treturn this->{att.name};\n}}\n".format(att=att, self=self)

	def getClassSetter(self, att):
		return "\nint\t\t{self.name}::{att.setter}\n{{\n\tthis->{att.name} = {att.a_name};\n\treturn 0;\n}}\n".format(att=att, self=self)
