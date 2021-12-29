# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательная задача 1

Есть скрипт:
```bash
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```

Какие значения переменным c,d,e будут присвоены? Почему?

| Переменная  | Значение | Обоснование |
| ------------- | ------------- | ------------- |
| `c`  | a+b  | так как указали не переменные, а строки |
| `d`  | 1+2  | вывод значений переменных, но арифметическая операция не выполняется, тк это строки |
| `e`  | 3  | теперь работают скобки, дающие команду на выполнение арифметической операции |


## Обязательная задача 2
На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным (после чего скрипт должен завершиться). В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
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
### Ваш скрипт:
```bash
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
## Обязательная задача 3
Необходимо написать скрипт, который проверяет доступность трёх IP: `192.168.0.1`, `173.194.222.113`, `87.250.250.242` по `80` порту и записывает результат в файл `log`. Проверять доступность необходимо пять раз для каждого узла.

### Ваш скрипт:
```bash
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
vagrant@vagrant:~/bash$    
```

## Обязательная задача 4
Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается.

### Ваш скрипт:
```bash
vagrant@vagrant:~/bash$ cat hosts2.sh
#!/usr/bin/env bash
hosts=(192.168.0.1 173.194.222.113 87.250.250.24)
timeout=3
err=0

while (($err == 0))
do
for h in ${hosts[@]}
        do
                curl -s --connect-timeout $timeout $h:80 >/dev/null
                err=$?
                if (($err != 0))
                then
                echo "    ERROR on " $h status=$err >>hosts2.log
                fi
        done
done
vagrant@vagrant:~/bash$ bash hosts2.sh
vagrant@vagrant:~/bash$ cat hosts2.log
    ERROR on  87.250.250.24 status=28
vagrant@vagrant:~/bash$
```
