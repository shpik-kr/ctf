# Harekaze CTF 2019

I'm attended by "Yokosuka Hackers", and got a 1st place :).

"Yokosuka Hacerks" is Korean and Japanese joint team.. (Twitterから始まるCTF)

## Writeup

### Harekaze Note

It's heap exploitation problem in glibc2.29 environment.

Nowdays, there are many problems of this type.

Tcache check **double free** in tcache slot at glibc2.29.

But, Fastbin is still available for fastbin-dup.

So, I used fastbin-dup and overwrite **\_\_malloc\_hook** to oneshot gadget.

Finally, i got a flag.

Full exploit => note.py

