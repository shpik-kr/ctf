# [WEB] Hack Dat Kiwi CTF 2017 - Fractal

# Description

>   문제 페이지 닫힘

# Analysis

페이지에 접속해서 메뉴를 이동해보면 `page=home`과 같은 형태로 페이지가 이동되는 것을 알 수 있다.

그래서 LFI를 통해 소스를 읽어보고자 PHP Filter를 사용해보았다.

`php://filter/convert.base64-encode/resource=home`

필터는 작동하지 않았으나 home.php가 존재하는 것을 확인할 수 있으므로, include나 require을 통해 페이지를 로드하는 것이며, 필터링이 되어있는 것 같다.

shop에 가보면 flag를 살 수 있는데, 1개당 $100000.00이며, 가진 돈이 없어서 구입을 할 수가 없다.

다른 메뉴를 가보면 email을 입력하고 쿠폰을 받을 수 있으며, 그 쿠폰은 `10% + $5`를 할인해 준다.

쿠폰을 이용해서 저 flag를 사는 문제인 것 같다.

# Exploit

1. LFI

## 1. LFI

flag를 담은 상태에서 쿠폰을 발급받고 해당 쿠폰을 입력하면 URL의 형태가 `page=checkout&coupon=쿠폰번호`가 된다.
해당 URL에서 page를 index를 로딩하게 하기 위해 `page=index&coupon=쿠폰 번호`를 요청하면 수 많은 index페이지가 로드되면서 쿠폰이 중복 적용되고, 최종적으로 $0에 쿠폰을 구매할 수 있게 된다.

```html
Total price: $100005.00
Discounted price: $0.00
Your account balance: $0.00
Thank you for making a purchase through fractal shop! Here are your digital content:
Torn Flag: the torn flag is 97hveijfpsa13j4f
Flag: the flag is 07mR3Hdaiks20uMJ
```



**07mR3Hdaiks20uMJ**

