1. *Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. Вам нужно найти тот единственный, который относится именно к cd.*    

**Ответ:** Непосредственно к ```cd``` относится ```chdir("/tmp")```

2. *Попробуйте использовать команду ```file``` на объекты разных типов на файловой системе. Например:*
```
vagrant@netology1:~$ file /dev/tty
/dev/tty: character special (5/0)
vagrant@netology1:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@netology1:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64
```
*Используя ```strace``` выясните, где находится база данных ```file``` на основании которой она делает свои догадки.*    

**Ответ:** ```openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3```   
Из ```man file```:
```
 /usr/share/misc/magic.mgc  Default compiled list of magic.
 /usr/share/misc/magic      Directory containing default magic files.
```

3. *Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).*   

**Ответ:** 
```
vagrant@vagrant:~/test_vagrant$ python3 -c "import time;f=open('do_not_delete_me','r');time.sleep(600);" &
[1] 1849
vagrant@vagrant:~/test_vagrant$ lsof | grep do_not_delete_me
python3   1849                       vagrant    3r      REG              253,0       14     131094 /home/vagrant/test_vagrant/do_not_delete_me
vagrant@vagrant:~/test_vagrant$ lsof -p 1849 | grep do_not_delete_me
python3 1849 vagrant    3r   REG  253,0       14 131094 /home/vagrant/test_vagrant/do_not_delete_me
vagrant@vagrant:~/test_vagrant$ cat do_not_delete_me
valuable data
vagrant@vagrant:~/test_vagrant$ rm do_not_delete_me
vagrant@vagrant:~/test_vagrant$ cat do_not_delete_me
cat: do_not_delete_me: No such file or directory
vagrant@vagrant:~/test_vagrant$ lsof -p 1849 | grep do_not_delete_me
python3 1849 vagrant    3r   REG  253,0       14 131094 /home/vagrant/test_vagrant/do_not_delete_me (deleted)
vagrant@vagrant:~/test_vagrant$ : > /proc/1849/fd/3
vagrant@vagrant:~/test_vagrant$ lsof -p 1849 | grep do_not_delete_me
python3 1849 vagrant    3r   REG  253,0        0 131094 /home/vagrant/test_vagrant/do_not_delete_me (deleted)
vagrant@vagrant:~/test_vagrant$
```
размер обнулился с 14 до 0

4. *Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?*

**Ответ:** Зомби процессы высвобождают свои ресурсы, остается только запись в таблице процессов.   

5. *В iovisor BCC есть утилита opensnoop:*
```
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
```
*На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.*

**Ответ:**
```
vagrant@vagrant:~$ sudo -i
root@vagrant:~# /usr/sbin/opensnoop-bpfcc
PID    COMM               FD ERR PATH
1      systemd            12   0 /proc/591/cgroup
1      systemd            12   0 /proc/373/cgroup
822    vminfo              4   0 /var/run/utmp
568    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
568    dbus-daemon        18   0 /usr/share/dbus-1/system-services
568    dbus-daemon        -1   2 /lib/dbus-1/system-services
568    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
822    vminfo              4   0 /var/run/utmp
```

6. *Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.*

**Ответ:**
```
vagrant@vagrant:~$ type uname
uname is hashed (/usr/bin/uname)
```
как из командной строки открыть второй раздел мануала uname(2)?

```
Part of the utsname information is also accessible via
       /proc/sys/kernel/{ostype, hostname, osrelease, version,
       domainname}.
```

7. *Чем отличается последовательность команд через ; и через && в bash? Например:*
```
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```
*Есть ли смысл использовать в bash &&, если применить set -e?*    

**Ответ:**
```&&``` логический оператор ```;``` это простая последовательность.   
Во втором случае ```(test -d /tmp/some_dir && echo Hi)``` ```echo``` сработает при успешном выполнении ```test```

```set -e``` - Exit immediately if a command exits with a non-zero status. Применение && бессмысленно, т.к. по сути выполняет то же самое.   

8. *Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?*

**Ответ:**
-e [Exit immediately if a command exits with a non-zero status]   
-u [Treat unset variables as an error when substituting]
-x [Print commands and their arguments as they are executed]   
-o pipefail [the return value of a pipeline is the status of the last command to exit with a non-zero status, or zero if no command exited with a non-zero status]   

Повышает детализацию выполнения сценария при логгировании (вывод команд и их аргументов), завершение сценария при наличии ошибки на любом этапе.

9.  *Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).*

**Ответ:**    
```
vagrant@vagrant:~$ ps -o stat
STAT
Ss
R+
vagrant@vagrant:~$
```
Ss Процесс ожидания завершения события    
R+ Запущенные или запускаемые (или в процессе запуска)

Дополнительные символы - дополнительные характеристики или условия

