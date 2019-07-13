# Google CTF 2019 Quals

## pastetastic
- XSS Auditor Abusing
- DOM Clobbering
- Same Origin Policy
- postMessage

Origin verification logic does not exist when postMessage send data with `error`. 
So, we used that for loading our wanted.

# BVN
- Blind XXE
- Local DTD

Try to xxe using local dtd, then we got a flag.

# gphotos
- XXE
- SVG
- ImageMasick

ImageMasick consists of default settings.
Therefore i can use dangerouse funtions.

# Malvertising
- Javascript
- Obfuscator
- Brute Force

Try to deobfuscator javascript, then you can get a flag.
