from optparse import OptionParser
if __name__=="__main__":
	Parser = OptionParser()
	Parser.add_option("-r", "--read", dest="readfilename")
	(options, args) = Parser.parse_args()
	sReadFileName=options.readfilename
	hFread = open(sReadFileName,'r')
	sDatabase = hFread.readlines()
	hFread.close()
	fMaxSimilarity = 0.000000
	lList = []
	nMaxRow = 0
	i = 0
	while i < len(sDatabase):
		print sDatabase[i][0:6]
		if sDatabase[i][0:6] == "result":
			print i
			fTmp = float(sDatabase[i][8:])
			print fTmp
			lList.append(fTmp)
			if fTmp > fMaxSimilarity:
				fMaxSimilarity = fTmp
				nMaxRow = i
		i = i + 1
	lList.sort()
	print "MaxSimilarity: ",fMaxSimilarity
	print "Row ",nMaxRow
	print lList[-10:]
	print sum(lList)/len(lList)
