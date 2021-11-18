1. *На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter:*
* поместите его в автозагрузку,
* предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
* удостоверьтесь, что с помощью `systemctl` процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.   

**Ответ:**  
**Добавил EnvironmentFile в файл .service, возможно он и несет в себе доп опции для службы.**    
`sudo cp ~/node_exporter-1.2.2.linux-amd64/node_exporter /usr/local/bin`
`vagrant@vagrant:~$ sudo vim /etc/systemd/system/node_exporter.service`
```
[Unit]
Description=Node Exporter
After=network-online.target

[Service]
EnvironmentFile=/etc/default/node_exporter
ExecStart=/usr/local/bin/node_exporter $OPTIONS
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```
vagrant@vagrant:~$ sudo systemctl daemon-reload
vagrant@vagrant:~$ sudo systemctl start node_exporter
vagrant@vagrant:~$ sudo systemctl enable node_exporter
vagrant@vagrant:~$ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2021-11-18 05:26:32 UTC; 13s ago
   Main PID: 13425 (node_exporter)
      Tasks: 4 (limit: 1071)
     Memory: 2.3M
     CGroup: /system.slice/node_exporter.service
             └─13425 /usr/local/bin/node_exporter

Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.237Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.238Z caller=node_exporter.go:115 collec>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.238Z caller=node_exporter.go:199 msg="L>
Nov 18 05:26:32 vagrant node_exporter[13425]: level=info ts=2021-11-18T05:26:32.238Z caller=tls_config.go:191 msg="TLS >
vagrant@vagrant:~$
```



2. *Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.*

**Ответ:**   
Оказывается надо было пробросить порт 9100 на хост...   
CPU:   
    node_cpu_seconds_total{cpu="0",mode="idle"} 2238.49   
    node_cpu_seconds_total{cpu="0",mode="system"} 16.72   
    node_cpu_seconds_total{cpu="0",mode="user"} 6.86   
    process_cpu_seconds_total   
    
Memory:   
    node_memory_MemAvailable_bytes    
    node_memory_MemFree_bytes   
    
Disk:   
    node_disk_io_time_seconds_total{device="sda"}    
    node_disk_read_bytes_total{device="sda"}    
    node_disk_read_time_seconds_total{device="sda"}    
    node_disk_write_time_seconds_total{device="sda"}   
    
Network:   
    node_network_receive_errs_total{device="eth0"}    
    node_network_receive_bytes_total{device="eth0"}    
    node_network_transmit_bytes_total{device="eth0"}   
    node_network_transmit_errs_total{device="eth0"}   
    
3. *Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:*
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    *После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.*    
    
**Ответ:**   
```
vagrant@vagrant:~$ sudo lsof -i :19999
COMMAND PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
netdata 708 netdata    4u  IPv4  23866      0t0  TCP *:19999 (LISTEN)
```
![image](https://user-images.githubusercontent.com/26379231/142141725-783a2e0b-ccac-4a50-b2c4-1bb999127288.png)


4. *Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?*

**Ответ:**   
Можно:
`vagrant@vagrant:~$ dmesg | grep vbox`   
`vagrant@vagrant:~$ dmesg | grep virtual`

5. *Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?*

**Ответ:**
Это системное ограничение на количество открытых дескрипторов    
```
vagrant@vagrant:~$ sysctl fs.nr_open   
fs.nr_open = 1048576
```
Мягкий лимит на количество открытых файлов:   
```
vagrant@vagrant:~$ ulimit -Sn
1024
```
Жесткий лимит, который нельзя превысить:   
```
vagrant@vagrant:~$ ulimit -Hn
1048576
```
Значение мягкого лимита можно увеличить до жесткого. После завершения сессии, лимиты станут по умолчанию   

6. *Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.*

**Ответ:**   
```
root@vagrant:~# sleep 1h
^Z
[1]+  Stopped                 sleep 1h
root@vagrant:~# ps
    PID TTY          TIME CMD
   1938 pts/2    00:00:00 bash
   1946 pts/2    00:00:00 sleep
   1947 pts/2    00:00:00 ps
root@vagrant:~# ps aux
...
root        1938  0.0  0.4   9836  4060 pts/2    Ss   07:04   0:00 /bin/bash
root        1946  0.0  0.0   8076   592 pts/2    T    07:04   0:00 sleep 1h
root        1952  0.0  0.3  11492  3296 pts/2    R+   07:05   0:00 ps aux
```
```
root@vagrant:/# nsenter --target 1946 --pid --mount
root@vagrant:~# ps aux
...
root        1946  0.0  0.0   8076   592 pts/2    T    07:04   0:00 sleep 1h
root        1960  0.0  0.0   8996   636 pts/0    S    07:07   0:00 nsenter --target 1946 --pid --mount
root        1961  0.0  0.4   9836  4028 pts/0    S    07:07   0:00 -bash
root        1970  0.0  0.3  11492  3288 pts/0    R+   07:07   0:00 ps aux
```

7. *Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?*

**Ответ**  
`:(){ :|:& };:` функция, изветная как fork bomb. `:()` - функция с именем `:`. Плодит саму себя и убирает процесс в фон, перегружая процессор.
`cgroup` - механизм управления, отвечающий за ресурсы процессора, памяти и устройств, помогает стабилизировать систему.   
`[ 6986.387583] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope`   
Можно уменьшить параметр Max user processes (сейчас по умолчанию у меня 3571 процесс макс):      
```
vagrant@vagrant:~$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 3571
max locked memory       (kbytes, -l) 65536
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 3571
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```


