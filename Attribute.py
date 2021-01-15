class Attribute:
	def __init__(self, m_type, m_name, m_pointer, m_const):
		self.type = m_type
		self.name = m_name
		self.pointer = m_pointer
		self.const = m_const
		begin = 0
		if (self.name.find("_") == 0):
			begin = 1
		self.a_name = self.name[begin:]
		self.getter = "get" + self.a_name.capitalize() + "()"
		self.setter = "set" + self.a_name.capitalize() + "(" + self.type + " " + self.pointer + self.a_name + ")"
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
		# if len(self.type) < 4:
		# 	return "\n\t{att.type}\t\t{att.pointer}{att.getter} const;\n\tint\t\t{att.setter};".format(att=self)
		# else:
		# 	return "\n\t{att.type}\t{att.pointer}{att.getter} const;\n\tint\t\t{att.setter};".format(att=self)
