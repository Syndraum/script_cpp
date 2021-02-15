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
		elif (format == "int" and name.find("I") != 0):
			self.name = "I" + name[0].upper() + name[1:]
			self.headerName = self.name + ".hpp"
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

	def createInterface(self):
		if self.is_file_exist(self.headerName):
			print("file " + self.headerName + " already exist")
			return True
		h = open(self.headerName, "w")
		h.write(self.getInterfaceBuff())
		h.close

	def	getInterfaceBuff(self):
		nameUpper = self.name.upper()
		return "#ifndef " + nameUpper + "\n# define " + nameUpper + "\n\nclass " + self.name + "\n{\npublic:\n\n};\n\n#endif\n"

	def getFileBuff(self):
		return "#include \"" + self.headerName + "\"\n\n" + self.name + "::" + self.name + "(void){}\n\n"+ self.name + "::" + self.name + "("+self.name+" const & src)\n{\n\t*this = src;\n}\n\n" + self.name + "::~" + self.name + "(void)\n{\n\t\n}\n\n"+self.name+" &\t"+self.name+"::operator=("+self.name+" const & rhs)\n{\n\treturn *this;\n}\n"

	def getHeaderBuff(self):
		nameUpper = self.name.upper()
		return "#ifndef " + nameUpper + "\n# define " + nameUpper + "\n\nclass " + self.name + "\n{\npublic:\n\n\t" + self.name + "(void);\n\t" + self.name + "(" + self.name + " const & src);\n\t~" + self.name + "(void);\n\t"+self.name+" &\toperator=("+self.name+" const &rhs);\n\nprivate:\n\n};\n\n#endif\n"

	def	setNewAttribute(self, line):
		args = line.split()
		m_type = args[:-1]
		m_name = args[-1]
		if m_name.find("*") == 0:
			ct = m_name.count('*')
			m_type.append(m_name[0:ct])
			m_name = m_name[ct::]
		if m_name.find(";") == len(m_name) - 1:
			m_name = m_name[:-1]
		if m_type[0] == "static":
			m_type = m_type[1::]
		m_const = "const" in m_type
		self.attributes.append(Attribute(m_type, m_name, m_const))

	def	update(self):
		if self.file_not_exist(self.filename) or self.file_not_exist(self.headerName):
			return 1
		ret = self.parsing()
		if  ret > 0:
			return ret
		max_len=0
		for att in self.attributes:
			if (len(att.type) > max_len):
				max_len=len(att.type)
		max_len = max_len
		max_tab = ((max_len) // 4) + 1
		f = open(self.filename, "a")
		buff=""
		for att in self.attributes:
			if att.a_name.lower() not in self.setters and att.a_name.lower() not in self.getters:
				f.write(self.getClassGetter(att, max_tab))
				if not att.const:
					f.write(self.getClassSetter(att, max_tab))
				buff += att.getHeader(max_tab)
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
				if line.find("public:") != -1:
					private = False
					if self.insertLine == -1:
						self.insertLine = actualLine
				elif not line == "\n" and line.find("(") == -1 and line.find("protected:") == -1:
					self.setNewAttribute(line)
			elif not private:
				if line.find("private:") != -1 or line.find("protected:") != -1:
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

	def getClassGetter(self, att, max_tab):
		tab = '\t' * (max_tab - (len(att.type) // 4))
		return "\n{att.type}{tab}{self.name}::{att.getter} const\n{{\n\treturn this->{att.name};\n}}\n".format(att=att, self=self, tab=tab)

	def getClassSetter(self, att, max_tab):
		tab = '\t' * max_tab
		return "\nint{tab}{self.name}::{att.setter}\n{{\n\tthis->{att.name} = {att.a_name};\n\treturn 0;\n}}\n".format(att=att, self=self, tab=tab)
