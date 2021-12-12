# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`
- отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```
- В ответе укажите полученный HTTP код, что он означает?   

**Ответ:** HTTP код - 301 Moved Permanently - По указанному адресу страница перемещена, новый адрес прописан в поле location: https://stackoverflow.com/questions
```
HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: de7a4548-a1b4-4730-8098-6892be0b0fe6
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Sun, 12 Dec 2021 11:16:13 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-hel1410024-HEL
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1639307773.034203,VS0,VE109
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=b97b9ced-171d-a44f-85bd-ceb400179d9b; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.
```

2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers` 
- укажите в ответе полученный HTTP код. **307 Internal Redirect**
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего? **46.20 ms, Content Download (31.72 ms)**
- приложите скриншот консоли браузера в ответ.
![image](https://user-images.githubusercontent.com/26379231/145710608-01e3b600-5abd-46fb-b4cb-674e2e5d3500.png)

3. Какой IP адрес у вас в интернете? **94.180.42.176**
![image](https://user-images.githubusercontent.com/26379231/145712350-92b67ee7-5de7-4b2a-9299-3fbed53650a2.png)


4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`

**Ответ:** JSC "ER-Telecom Holding" Novosibirsk branch, AS43478
```
vagrant@vagrant:~$ whois -h whois.radb.net 94.180.42.176
route:          94.180.40.0/22
origin:         AS43478
org:            ORG-CN31-RIPE
descr:          JSC "ER-Telecom Holding" Novosibirsk branch
descr:          Novosibirsk, Russia
notify:         ripe@ertelecom.ru
mnt-by:         RAID-MNT
created:        2010-10-22T12:31:05Z
last-modified:  2016-01-28T13:06:08Z
source:         RIPE
```

5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

**Ответ:**
```
agrant@vagrant:~$ traceroute -IA 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  _gateway (10.0.2.2) [*]  0.304 ms  0.318 ms  0.096 ms
 2  XiaoQiang (192.168.31.1) [*]  1.650 ms  2.242 ms  2.342 ms
 3  10.85.255.254 (10.85.255.254) [*]  4.332 ms  4.512 ms  4.504 ms
 4  lag-3-438.bgw01.nsk.ertelecom.ru (109.194.88.30) [AS34533/AS43478/AS41843]  4.306 ms  4.479 ms  4.571 ms
 5  72.14.215.165 (72.14.215.165) [AS15169]  43.665 ms  43.794 ms  43.954 ms
 6  72.14.215.166 (72.14.215.166) [AS15169]  44.286 ms  45.246 ms  45.236 ms
 7  142.251.53.69 (142.251.53.69) [AS15169]  48.650 ms  48.007 ms  48.925 ms
 8  108.170.250.113 (108.170.250.113) [AS15169]  50.404 ms  50.462 ms  50.684 ms
 9  142.251.49.158 (142.251.49.158) [AS15169]  60.351 ms  60.315 ms *
10  216.239.43.20 (216.239.43.20) [AS15169]  62.697 ms  63.097 ms  63.908 ms
11  216.239.47.173 (216.239.47.173) [AS15169]  64.498 ms  64.652 ms  56.433 ms
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * dns.google (8.8.8.8) [AS15169]  57.537 ms
```

6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?

**Ответ:** Участки с наибольшей задержкой **8. AS15169  108.170.250.113** и **9. AS15169  142.251.49.158** 
```
vagrant@vagrant:~$ mtr -zw 8.8.8.8
Start: 2021-12-12T12:11:16+0000
HOST: vagrant                                   Loss%   Snt   Last   Avg  Best  Wrst StDev
  1. AS???    _gateway                           0.0%    10    0.7   0.8   0.7   0.9   0.1
  2. AS???    XiaoQiang                          0.0%    10    3.2   3.5   2.9   4.3   0.4
  3. AS???    10.85.255.254                      0.0%    10    4.0   5.7   4.0  10.6   2.0
  4. AS43478  lag-3-438.bgw01.nsk.ertelecom.ru   0.0%    10    4.0   6.2   3.7  14.0   3.4
  5. AS15169  72.14.215.165                      0.0%    10   43.2  45.2  43.2  49.6   2.5
  6. AS15169  72.14.215.166                      0.0%    10   44.1  44.4  43.5  45.7   0.6
  7. AS15169  142.251.53.69                      0.0%    10   47.8  49.7  47.7  55.5   2.7
  8. AS15169  108.170.250.113                    0.0%    10   45.2  48.7  44.4  61.9   6.6
  9. AS15169  142.251.49.158                    40.0%    10   73.8  60.6  55.7  73.8   6.6
 10. AS15169  216.239.43.20                      0.0%    10   56.5  58.9  55.8  64.7   3.4
 11. AS15169  216.239.47.173                     0.0%    10   58.0  58.1  57.2  59.7   0.7
 12. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 13. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 14. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 15. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 16. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 17. AS???    ???                               100.0    10    0.0   0.0   0.0   0.0   0.0
 18. AS15169  dns.google                        90.0%    10   58.0  58.0  58.0  58.0   0.0
```

7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`   
**Ответ:**

```
dns.google.             10800   IN      NS      ns4.zdns.google.
dns.google.             10800   IN      NS      ns2.zdns.google.
dns.google.             10800   IN      NS      ns3.zdns.google.
dns.google.             10800   IN      NS      ns1.zdns.google.
```
```
dns.google.             900     IN      A       8.8.4.4
dns.google.             900     IN      A       8.8.8.8
```



8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`    
**Ответ:**
```
4.4.8.8.in-addr.arpa.   30      IN      PTR     dns.google.
8.8.8.8.in-addr.arpa.   30      IN      PTR     dns.google.
```

В качестве ответов на вопросы можно приложите лог выполнения команд в консоли или скриншот полученных результатов.
