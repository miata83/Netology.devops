# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательные задания

1. Есть скрипт:
	```bash
	a=1
	b=2
	c=a+b
	d=$a+$b
	e=$(($a+$b))
	```
	* Какие значения переменным c,d,e будут присвоены?
	* Почему?

**Ответ:**
```
vagrant@vagrant:~$ echo $c
a+b                         #так как указали строки
vagrant@vagrant:~$ echo $d
1+2                         #вывод значений переменных, но арифметическая операция не выполняется, тк это строки
vagrant@vagrant:~$ echo $e
3                           #теперь работают скобки, дающие команду на выполнение арифметической операции
```

2. На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
	```bash
	while ((1==1)
	do
	curl https://localhost:4757
	if (($? != 0))
	then
	date >> curl.log
	fi
	done
	```
**Ответ:**
- нет закрывающей скобки в условии while
- уменьшить частоту проверок, введя условие timeout
- ввести условие успешности, else exit
```
while (( 1 == 1 ))
do
curl https://localhost:4757
if (($? != 0))
then
date >> curl.log
else exit
fi
sleep 5
done
```

3. Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.

**Ответ:**
```
vagrant@vagrant:~/bash$ cat hosts1.sh
#!/usr/bin/env bash
hosts=(192.168.0.1 173.194.222.113 87.250.250.24)
timeout=3
for i in {1..5}
do
        for h in ${hosts[@]}
        do
        curl -s --connect-timeout $timeout $h:80 >/dev/null
        echo "    check" $h status=$? >>hosts1.log
        done
done
vagrant@vagrant:~/bash$ bash hosts1.sh
vagrant@vagrant:~/bash$ cat hosts1.log

    check 192.168.0.1 status=0
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
    check 192.168.0.1 status=0
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
    check 192.168.0.1 status=0
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
    check 192.168.0.1 status=0
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
    check 192.168.0.1 status=0
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
```
    
4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается

**Ответ:**
```
vagrant@vagrant:~/bash$ cat hosts2.sh
#!/usr/bin/env bash
hosts=(192.168.0.1 173.194.222.113 87.250.250.24)
timeout=3
err=0

while (($err == 0))
do
for h in ${hosts[@]}
        do
                curl -Is --connect-timeout $timeout $h:80 >/dev/null
                err=$?
                if (($res != 0))
                then
                echo "    ERROR on " $h status=$res >>hosts2.log
                fi
        done
done
vagrant@vagrant:~/bash$ bash hosts2.sh
vagrant@vagrant:~/bash$ cat hosts2.log
    ERROR on  87.250.250.24 status=28
```    

