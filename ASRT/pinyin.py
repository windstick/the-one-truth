import sys, time
d=dict()
d[('a', 1)], d[('a', 2)], d[('a', 3)], d[('a', 4)], d[('a', 5)] = 'ā', 'á', 'ǎ', 'à', 'a'
d[('o', 1)], d[('o', 2)], d[('o', 3)], d[('o', 4)], d[('o', 5)] = 'ō', 'ó', 'ǒ', 'ò', 'o'
d[('e', 1)], d[('e', 2)], d[('e', 3)], d[('e', 4)], d[('e', 5)] = 'ē', 'é', 'ě', 'è', 'e'
d[('i', 1)], d[('i', 2)], d[('i', 3)], d[('i', 4)], d[('i', 5)] = 'ī', 'í', 'ǐ', 'ì', 'i'
d[('u', 1)], d[('u', 2)], d[('u', 3)], d[('u', 4)], d[('u', 5)] = 'ū', 'ú', 'ǔ', 'ù', 'u'
d[('v', 1)], d[('v', 2)], d[('v', 3)], d[('v', 4)], d[('v', 5)] = 'ǖ', 'ǘ', 'ǚ', 'ǜ', 'v'

def process_pin_yin(pin_yin):
	ans = []
	for word in pin_yin:
		tune = int(word[-1])
		if word.find('a') != -1:
			loc = word.find('a')
			word = word[0: loc] + d[('a', tune)] + word[loc + 1: -1]
		elif word.find('o') != -1:
			loc = word.find('o')
			word = word[0: loc] + d[('o', tune)] + word[loc + 1: -1]
		elif word.find('e') != -1:
			loc = word.find('e')
			word = word[0: loc] + d[('e', tune)] + word[loc + 1: -1]
		elif word.find('i') != -1:
			loc = word.find('i')
			word = word[0: loc] + d[('i', tune)] + word[loc + 1: -1]
		elif word.find('u') != -1:
			loc = word.find('u')
			word = word[0: loc] + d[('u', tune)] + word[loc + 1: -1]
		elif word.find('v') != -1:
			loc = word.find('v')
			word = word[0: loc] + d[('v', tune)] + word[loc + 1: -1]
		ans.append(word)
	return ans
