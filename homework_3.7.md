# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?
**Ответ:**
Linux:
```
vagrant@vagrant:~$ ip -br address
vagrant@vagrant:~$ ip -br link
```
Windows: ```ipconfig -all```


2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?
**Ответ:**
LLDP protocol
пакет lldpd
```vagrant@vagrant:~$ ip -c neighbour```


3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.   

**Ответ:**
VLAN
```sudo apt-get install vlan```
Настраиваются VLANы в файле /etc/network/interfaces
```
auto vlan1400
iface vlan1400 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        vlan_raw_device eth0
```        

4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.    

**Ответ:**
LAG
balance-rr, balance-xor, balance-tlb, balance-alb
```
sudo apt-get install ifenslave
sudo stop networking
sudo modprobe bonding
sudo vi /etc/network/interfaces
                auto eth0
                iface eth0 inet manual
                    bond-master bond0
                   
                auto eth1
                iface eth1 inet manual
                    bond-master bond0

                auto bond0
                iface bond0 inet static
                    address 192.168.1.10
                    gateway 192.168.1.1
                    netmask 255.255.255.0
                    bond-mode balance-tlb
                    bond-miimon 100
                    bond-slaves none
sudo start networking
```

5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.    

**Ответ:**
8 адресов в /29 сети     
32 подсети /29 в сети /24     
10.10.10.0-10.10.10.8; 10.10.10.9-10.10.10.16; 10.10.10.17-10.10.10.24 ...   

6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

**Ответ:** Можно взять любую из диапазона 100.64.0.0 — 100.127.255.255/10, например 100.64.0.0/26

7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?

**Ответ:**
Как проверить ARP таблицу в Linux, Windows? ```arp -a```
Как очистить ARP кеш полностью? ```sudo ip neigh flush all```
Как из ARP таблицы удалить только один нужный IP? ```arp -d 192.168.0.100```


