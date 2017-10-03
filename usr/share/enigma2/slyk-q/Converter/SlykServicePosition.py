from Converter import Converter
from Poll import Poll
from enigma import iPlayableService
from Components.Element import cached, ElementError
from Components.config import config

class SlykServicePosition(Poll, Converter, object):
	TYPE_LENGTH = 0
	TYPE_POSITION = 1
	TYPE_REMAINING = 2
	TYPE_REMAINING2 = 3
	TYPE_GAUGE = 4
	TYPE_REMAINING = 5
	TYPE_POSITION = 6
	TYPE_MOVIEREMAINING = 7
	
	
	
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)

		args = type.split(',')
		type = args.pop(0)

		if type == "Remaining":
			self.type = self.TYPE_REMAINING
		elif type == "Remaining2":
			self.type = self.TYPE_REMAINING2
		elif type == "Position":
			self.type = self.TYPE_POSITION
		elif type == "MovieRemaining":
			self.type = self.TYPE_MOVIEREMAINING
				
		self.poll_interval = 500
		self.poll_enabled = True

	def getSeek(self):
		s = self.source.service
		return s and s.seek()

	@cached
	def getPosition(self):
		seek = self.getSeek()
		if seek is None:
			return None
		pos = seek.getPlayPosition()
		if pos[0]:
			return 0
		return pos[1]

	@cached
	def getLength(self):
		seek = self.getSeek()
		if seek is None:
			return None
		length = seek.getLength()
		if length[0]:
			return 0
		return length[1]

	@cached
	def getCutlist(self):
		service = self.source.service
		cue = service and service.cueSheet()
		return cue and cue.getCutList()

	@cached
	def getText(self):
		seek = self.getSeek()
		if seek is None:
			return ""

		
		if self.type == self.TYPE_REMAINING or self.type == self.TYPE_REMAINING:
			s = self.position / 90000
			e = (self.length / 90000) - s
			sign_n = ""
			if (e/60) > 0:
				sign_n = "-"
			return sign_n + ngettext("%d Min", "%d Mins", (e/60)) % (e/60)
				
		if self.type == self.TYPE_REMAINING2 or self.type == self.TYPE_REMAINING2:
			s = self.position / 90000
			e = (self.length / 90000) - s
			sign_n = ""
			if (e%60) > 0:
				sign_n = "-"
			
			
			if (e/60) < 1:
				return sign_n + ("%d Secs") % (e%60)
			else:
			    return sign_n + ngettext("%d Min", "%d Mins", (e/60)) % (e/60)
			
		if self.type == self.TYPE_POSITION or self.type == self.TYPE_POSITION:
			p = self.position / 90000
			sign_p = "+"
			return sign_p + ngettext("%d Min", "%d Mins", (p/60)) % (p/60)
			
		if self.type == self.TYPE_MOVIEREMAINING or self.type == self.TYPE_MOVIEREMAINING:
			s = self.position / 90000
			e = (self.length / 90000) - s
			return ngettext("%d Min", "%d Mins", (e/60)) % (e/60)

		l = self.length
	
		if l < 0:
			return ""


	# range/value are for the Progress renderer
	range = 10000

	@cached
	def getValue(self):
		pos = self.position
		len = self.length
		if pos is None or len is None or len <= 0:
			return None
		return pos * 10000 / len

	position = property(getPosition)
	length = property(getLength)
	cutlist = property(getCutlist)
	text = property(getText)
	value = property(getValue)

	def changed(self, what):
		cutlist_refresh = what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evCuesheetChanged,)
		time_refresh = what[0] == self.CHANGED_POLL or what[0] == self.CHANGED_SPECIFIC and what[1] in (iPlayableService.evCuesheetChanged,)

		if cutlist_refresh:
			if self.type == self.TYPE_GAUGE:
				self.downstream_elements.cutlist_changed()

		if time_refresh:
			self.downstream_elements.changed(what)