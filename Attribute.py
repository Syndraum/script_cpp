class Attribute:
	def __init__(self, m_type, m_name, m_pointer):
		self.type = m_type
		self.name = m_name
		self.pointer = m_pointer
		self.getter = "get" + self.name.capitalize() + "()"
		self.setter = "set" + self.name.capitalize() + "(" + self.type + " " + self.pointer + self.name + ")"
		self.get = -1
		self.set = -1

	def getHeader(self):
		if len(self.type) < 4:
			return "\n\t{att.type}\t\t{att.pointer}{att.getter};\n\tvoid\t{att.setter};".format(att=self)
		else:
			return "\n\t{att.type}\t{att.pointer}{att.getter};\n\tvoid\t{att.setter};".format(att=self)
