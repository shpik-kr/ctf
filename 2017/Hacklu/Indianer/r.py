_ = 0x6E
needle = [0 for i in range(35)]
for i in range(0,512,9):
  needle[i%35]=chr(((_ & 1)+i)%24+97)

print ''.join(needle)

