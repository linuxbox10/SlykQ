from Converter import Converter
from time import localtime, strftime
from Components.Element import cached


class SlykClockToText(Converter, object):
	DEFAULT = 0
	FORMAT = 1
	SLYK_AS_LENGTH = 2
	SLYK_FULL_DATE = 3

	# add: date, date as string, weekday, ...
	# (whatever you need!)

	def __init__(self, type):
		Converter.__init__(self, type)

		self.fix = ""
		if ';' in type:
			type, self.fix = type.split(';')

		if  type == "SlykAsLength":
			self.type = self.SLYK_AS_LENGTH
		elif type == "SlykFullDate":
			self.type = self.SLYK_FULL_DATE
		elif "Format" in type:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		# add/remove 1st space
		def fix_space(string):
			if "Proportional" in self.fix and t.tm_hour < 10:
				return " " + string
			if "NoSpace" in self.fix:
				return string.lstrip(' ')
			return string

		# handle durations
		if self.type == self.SLYK_AS_LENGTH:
			if time < 0:
				return ""	
			return "%dh %02dm" % (time / 3600, time / 60 % 60)			
		
		t = localtime(time)

		if self.type == self.DEFAULT:
			return fix_space(_("%2d:%02d") % (t.tm_hour, t.tm_min))
		elif self.type == self.SLYK_FULL_DATE:
			d = _("%A, %l.%M")
		elif self.type == self.FORMAT:
			d = self.fmt_string
		else:
			return "???"
			
		if int(strftime("%H", t)) >= 12:
			timetext = strftime(d, t) + _('pm')
		else:
			timetext = strftime(d, t) + _('am')
		
		return timetext

	text = property(getText)
	