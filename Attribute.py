class Attribute:
	def __init__(self, m_type, m_name, m_pointer, m_const):
		self.type = m_type
		self.name = m_name
		self.cap = m_name[0].upper() + m_name[1:]
		self.pointer = m_pointer
		self.const = m_const
		begin = 0
		if (self.name.find("_") == 0):
			begin = 1
		self.a_name = self.cap[begin:]
		self.getter = "get" + self.a_name + "(void)"
		self.setter = "set" + self.a_name + "(" + self.type + " " + self.pointer + self.a_name + ")"
		self.get = -1
		self.set = -1

	def getGetter(self):
		return "\n\t{att.type}\t{att.pointer}{att.getter} const;".format(att=self)

	def getSetter(self):
		return "\n\tint\t{att.setter};".format(att=self)

	def getHeader(self):
		buffer = self.getGetter()
		if not self.const:
			buffer += self.getSetter()
		return buffer
