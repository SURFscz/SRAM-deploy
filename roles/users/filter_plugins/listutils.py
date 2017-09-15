# small filters to manupulate lists
class FilterModule(object):

	# given a flat list (or tuple, or set), return a deduplicated list, i.e.,
	# a list in which each unique item in the src list only occurs once
	@staticmethod
	def _uniq(src):
		return list(set(src))

	# given a list of list (e.g., [[a,b,c],[c,d,e],[e,f,g]]) return a flat
	# list [a,b,c,c,d,e,e,f,g]
	@staticmethod
	def _flatten(src):
		return [ item for sublist in src for item in sublist ]

	def filters(self):
		return {
			'uniq':    self._uniq,
			'flatten': self._flatten,
		}

