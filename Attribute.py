class Attribute:
	def __init__(self, m_type, m_name, m_const):
		self.type = ' '.join(m_type)
		self.name = m_name
		self.const = m_const
		begin = 0
		if (self.name.find("_") == 0):
			begin = 1
		self.a_name = m_name[begin].upper() + m_name[begin + 1:]
		self.getter = "get" + self.a_name + "(void)"
		self.setter = "set" + self.a_name + "(" + self.type + " " + self.a_name + ")"
		self.get = -1
		self.set = -1

	def getGetter(self, max_tab):
		tab = '\t' * (max_tab - (len(self.type) // 4))
		return "\n\t{att.type}{tab}{att.getter} const;".format(att=self,tab=tab)

	def getSetter(self, max_tab):
		tab = '\t' * max_tab
		return "\n\tint{tab}{att.setter};".format(att=self,tab=tab)

	def getHeader(self, max_tab):
		buffer = self.getGetter(max_tab)
		if not self.const:
			buffer += self.getSetter(max_tab)
		return buffer
