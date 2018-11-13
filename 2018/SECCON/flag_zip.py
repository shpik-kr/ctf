import os

qq = 1540560000


from zipfile import ZipFile
import os
for i in range(0,100000):
	try:
		with ZipFile('flag.zip') as zf:
		    zf.extractall(pwd=str(qq+i))
		os.system('cat flag.txt')
		print '-------'
	except:
		 continue
