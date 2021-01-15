class Attribute:
	def __init__(self, m_type, m_name, m_pointer):
		self.type = m_type
		self.name = m_name
		self.pointer = m_pointer
		begin = 0
		if (self.name.find("_") == 0):
			begin = 1
		self.a_name = self.name[begin:]
		self.getter = "get" + self.a_name.capitalize() + "()"
		self.setter = "set" + self.a_name.capitalize() + "(" + self.type + " " + self.pointer + self.a_name + ")"
		self.get = -1
		self.set = -1

	def getHeader(self):
		if len(self.type) < 4:
			return "\n\t{att.type}\t\t{att.pointer}{att.getter} const;\n\tint\t\t{att.setter};".format(att=self)
		else:
			return "\n\t{att.type}\t{att.pointer}{att.getter} const;\n\tint\t\t{att.setter};".format(att=self)
