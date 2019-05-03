# \*CTF 2019

I had been attended as TenDollar.

I solved 3 Prob exclude MIC Check.

**mywebsql** : It's 1-day exploit problem on mywebsql. RCE was occured by backup service. We just save backup file contains `<?php var_dump(system($_GET[c]));?>` with .php extensions. Finally i get flag using IPC Programming to php because of /readfile.

**quiicksort** : This is implementation to Quick Sort. Simple Logic Error.

**girlfriend** :  It is running from glibc 2.29 like Ubuntu 19.04. So, i fill tcache list, then exploit using fastbin dup.

