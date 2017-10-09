# [FUN] Kaspersky 2017 - Old School

# Description
Hey! Do you like playing? Are you old school?

Have fun!

Concat answer to KLCTF prefix

# Analysis
문제에서 nes파일이 하나 주어졌다.

해당파일을 nes에뮬레이터 Fceux(http://www.fceux.com/web/home.html)를 이용하여 실행하면 ms.pacman이라는 고전게임이 실행된다.

실행을 하면 메뉴 하단에 C4N U R34D 8TN LIN35라는 문구가 적혀있다.

뭔진 몰라도 8번째 라인을 읽으라는 것 같다.

정상적으로 플레이할 시, 스테이지 2에서 Decimal값이 나오는데, 해당 Decimal이 벽으로 취급되는지 이동이 되지 않아 정상적인 플레이가 불가능했다.

우선 해당게임에 대한 정보를 수집하였고 다음의 페이지를 발견했다.
(https://tcrf.net/Ms.\_Pac-Man\_(NES,\_Namco))

~~여담으로 게임 원본의 스테이지가 총 7개여서 8번째 스테이지 읽으라는건 줄 알았는데 알고보니 9개였다.~~

해당 페이지에서 다음과 같은 정보를 얻을 수 있었다.
> If you'd prefer to modify the ROM instead, change the pointer at $896A (0x97A in the ROM file) to the appropriate address.
> 

# Exploit
1. Binary Patch

## 1. Binary Patch
위에서 얻은 정보를 바탕으로 nes 문제 파일의 0x97A의 부분을 보자.
```
0x97A : D491 78AB 3BAD F8AE 698E B4B0 81B2 48B4 
0x98A : 19B6
```
0x97A부터 0x98B까지 2바이트 씩 맵 데이터의 대한 주소를 차례대로 가지고 있다.
1. $91D4
2. $AB78
3. $AD3B
4. $F8AE
5. $8E69
6. $B0B4
7. $B281
8. $B448

해당 주소는 nes파일이 로드되었을때 메모리에 매핑되는 주소 값이다.

스테이지 1의 주소에 다른 스테이지의 주소로 덮어씌우면 첫번째 스테이지가 우리가 덮어씌운 주소를 기준으로 맵을 로딩한다.

스테이지 2부터의 Decimal값들을 모아 String으로 변경하면 다음과 같은 문구를 얻을 수 있다.

2. 87,69,76,67,79,77,69           (WELCOME)
3. 89,79,85,87,73,76,76           (YOUWILL)
4. 70,73,78,68,84,72,69           (FINDTHE)
5. 70,76,65,71,65,84              (FLAGAT)
6. 84,72,69,76,69,86,69,76        (THELEVEL)
7. 69,73,71,72,84                 (EIGHT)
8. 47,110,88,78,117,86,120,121,57 (/nXNuVxy9)

you will find the flag at the level eight이며 스테이지 8에서는 /nXNuVxy9의 값을 얻을 수 있었다.

해당 값을 플래그로 인증하였으나 안되서 뭔가했었는데, 문제 nes를 보면 HI-SCORE대신 ON-PASTE, 1UP대신 BIN이 들어가있다.(여기서 영감을 받아야 하는건가보다.)

pastebin페이지 뒤에 이어 붙이면 된다.
~~???????????뭐죠~~

https://pastebin.com/nXNuVxy9 에 들어가면 `S0xGQ1RGe1czXzRMTF9MMFYzX1IzVFIwfQ==`의 값을 얻을 수 있으며 이를 base64decode하면 플래그를 얻을 수 있다.

**KLFCTF{W3_4LL_L0V3_R3TR0}**
