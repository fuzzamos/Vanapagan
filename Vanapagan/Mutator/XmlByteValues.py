import shutil
import os
import MutatorBase


class XmlByteValues(MutatorBase.MutatorBase):
	byteValues = ["&#x00;", "&#xFF;", "&#xFE;", "&#xFF;&#xFF;", "&#xFF;&#xFE;", "&#xFE;&#xFF;", "&#xFF;&#xFF;&#xFF;&#xFF;", "&#xFF;&#xFF;&#xFF;&#xFE;", "&#xFE;&#xFF;&#xFF;&#xFF;", "&#x7F;", "&#x7E;", "&#x7F;&#xFF;", "&#x7F;&#xFE;", "&#xFF;&#x7F;", "&#xFE;&#x7F;", "&#x7F;&#xFF;&#xFF;&#xFF;", "&#x7F;&#xFF;&#xFF;&#xFE;", "&#xFF;&#xFF;&#xFF;&#x7F;", "&#xFE;&#xFF;&#xFF;&#x7F;"]
	rate = 20000
	min = 2
	max = 100
	skip = 0

	def mutate(self, src, dest):
		ret_signature = []
		ret_text = ""
		try:
			if src!=dest:
				shutil.copy2(src, dest)
			size = os.path.getsize( dest )		
			count = int(round(size / self.rate))
			if int(count) < self.min:
				count = self.min
			if self.max > 0 and int(count) > self.max:
				count = self.max
		
			f=open(dest, "r+b")
			for x in xrange(int(count)):
				while True:
					newVal = self.byteValues[self.myRand(0, len(self.byteValues)-1)]
					pos = self.myRand(self.skip, size-len(newVal))
					
					if not self.isInXmlValue(f, pos, len(newVal)):
						continue
					
					for y in xrange(len(newVal)):
						f.seek(pos+y)
						oldVal = f.read(1)
						f.seek(pos+y)
						f.write(newVal[y])
						ret_signature.append("%08X%02X%02X" % (pos+y, ord(oldVal), ord(newVal[y])))
						ret_text += "Mutating byte at 0x%X (%d) from 0x%02X to 0x%02X\n" % (pos, pos, ord(oldVal), ord(newVal[y]))
					break
			f.close()
		except:
			raise #Just for now
			return None
		return "|".join(ret_signature) + "\n" + ret_text