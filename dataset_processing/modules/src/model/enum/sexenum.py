
class Sex:
	MALE, FEMALE = ['M', 'F']

	@staticmethod
	def getGenderValue(gender):
		gender = gender.capitalize()[0]
		if (gender == 'M'):
			return Sex.MALE
		elif (gender == 'F'):
			return Sex.FEMALE
		else:
			raise ValueError("Provided value '%s' does not match either MALE or FEMALE" % (gender))
			return None