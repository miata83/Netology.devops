# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.   
  **Ответ:** Использование дыр в разряженном файле как способ сжатия и экономии места на диске.   
  
2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?   
  **Ответ:** Hardlink - это по сути один и тот же файл, с одним и тем же INode, в отличие от symlink. Права и владелец - одни и те же.
3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.   
    **Ответ:**
    ```
    vagrant@vagrant:~$ lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    sda                    8:0    0   64G  0 disk
    ├─sda1                 8:1    0  512M  0 part /boot/efi
    ├─sda2                 8:2    0    1K  0 part
    └─sda5                 8:5    0 63.5G  0 part
    ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
    └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
    sdb                    8:16   0  2.5G  0 disk
    sdc                    8:32   0  2.5G  0 disk
    ```
1. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.   
    **Ответ:**   
    ```
    vagrant@vagrant:~$ sudo fdisk -l /dev/sdb
    Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x26c0f764

    Device     Boot   Start     End Sectors  Size Id Type
    /dev/sdb1          2048 4196351 4194304    2G 83 Linux
    /dev/sdb2       4196352 5220351 1024000  500M 83 Linux
    ```
1. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.   
    **Ответ:**   
    ```
    vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb| sudo sfdisk /dev/sdc
    Checking that no-one is using this disk right now ... OK

    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes

    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Created a new DOS disklabel with disk identifier 0x26c0f764.
    /dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
    /dev/sdc2: Created a new partition 2 of type 'Linux' and of size 500 MiB.
    /dev/sdc3: Done.

    New situation:
    Disklabel type: dos
    Disk identifier: 0x26c0f764

    Device     Boot   Start     End Sectors  Size Id Type
    /dev/sdc1          2048 4196351 4194304    2G 83 Linux
    /dev/sdc2       4196352 5220351 1024000  500M 83 Linux

    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.
    vagrant@vagrant:~$
    ```
1. Соберите `mdadm` RAID1 на паре разделов 2 Гб.   
    **Ответ:**
    ```
    vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md0 -l 1 -n 2 /dev/sd{b1,c1}
    mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
    mdadm: size set to 2094080K
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md0 started.
    vagrant@vagrant:~$
    ```

1. Соберите `mdadm` RAID0 на второй паре маленьких разделов.   
    **Ответ:**
    ```
    vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md1 -l 0 -n 2 /dev/sd{b2,c2}
    mdadm: chunk size defaults to 512K
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.
    vagrant@vagrant:~$
    ```
1. Создайте 2 независимых PV на получившихся md-устройствах.   
    **Ответ:**   
    ```
    vagrant@vagrant:~$ sudo pvcreate /dev/md0 /dev/md1
    Physical volume "/dev/md0" successfully created.
    Physical volume "/dev/md1" successfully created.
    ```  

1. Создайте общую volume-group на этих двух PV.   
    **Ответ:**   
    ```
    vagrant@vagrant:~$ sudo vgcreate vg-1 /dev/md0 /dev/md1
    Volume group "vg-1" successfully created
    ```

1. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.   
    **Ответ:** 
    ```
    vagrant@vagrant:~$ sudo lvcreate -L 100M vg-1 /dev/md1
    Logical volume "lvol0" created.
    vagrant@vagrant:~$ sudo lvs
    LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
    lvol0  vg-1      -wi-a----- 100.00m
    root   vgvagrant -wi-ao---- <62.54g
    swap_1 vgvagrant -wi-ao---- 980.00m
    vagrant@vagrant:~$
    ```
    
1. Создайте `mkfs.ext4` ФС на получившемся LV.   
    **Ответ:** 
    ```
    vagrant@vagrant:~$ mkfs.ext4 /dev/vg-1/lvol0
    mke2fs 1.45.5 (07-Jan-2020)
    Could not open /dev/vg-1/lvol0: Permission denied
    vagrant@vagrant:~$ sudo mkfs.ext4 /dev/vg-1/lvol0
    mke2fs 1.45.5 (07-Jan-2020)
    Creating filesystem with 25600 4k blocks and 25600 inodes

    Allocating group tables: done
    Writing inode tables: done
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done
    ```
1. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.   
    **Ответ:** 
    ```
    vagrant@vagrant:~$ mkdir /tmp/new
    vagrant@vagrant:~$ sudo mount /dev/vg-1/lvol0 /tmp/new
    ```

1. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.   
    **Ответ:** 
    ```
    vagrant@vagrant:~$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
    --2021-11-17 12:32:01--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
    Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
    Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 22501269 (21M) [application/octet-stream]
    Saving to: ‘/tmp/new/test.gz’

    /tmp/new/test.gz              100%[=================================================>]  21.46M  8.47MB/s    in 2.5s

    2021-11-17 12:32:04 (8.47 MB/s) - ‘/tmp/new/test.gz’ saved [22501269/22501269]

    vagrant@vagrant:~$ ls /tmp/new
    lost+found  test.gz
    vagrant@vagrant:~$ ls -l /tmp/new
    total 21992
    drwx------ 2 root root    16384 Nov 17 12:27 lost+found
    -rw-r--r-- 1 root root 22501269 Nov 17 11:17 test.gz
    ```
1. Прикрепите вывод `lsblk`.   
    **Ответ: Тут не понял почему md1 с raid0 создались с размером 996М, при создании md1 размер не указывался** 
    ```
    vagrant@vagrant:~$ lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                    8:0    0   64G  0 disk
    ├─sda1                 8:1    0  512M  0 part  /boot/efi
    ├─sda2                 8:2    0    1K  0 part
    └─sda5                 8:5    0 63.5G  0 part
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
    sdb                    8:16   0  2.5G  0 disk
    ├─sdb1                 8:17   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    └─sdb2                 8:18   0  500M  0 part
      └─md1                9:1    0  996M  0 raid0
        └─vg--1-lvol0    253:2    0  100M  0 lvm   /tmp/new
    sdc                    8:32   0  2.5G  0 disk
    ├─sdc1                 8:33   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    └─sdc2                 8:34   0  500M  0 part
      └─md1                9:1    0  996M  0 raid0
        └─vg--1-lvol0    253:2    0  100M  0 lvm   /tmp/new
    vagrant@vagrant:~$
    ```
1. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
    **Ответ:**    
    ```
    vagrant@vagrant:~$ gzip -t /tmp/new/test.gz
    vagrant@vagrant:~$ echo $?
    0
    ```
1. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.   
    **Ответ:** 
       
    ```
    vagrant@vagrant:~$ sudo pvmove /dev/md1 /dev/md0
      /dev/md1: Moved: 24.00%
      /dev/md1: Moved: 100.00%
    vagrant@vagrant:~$ lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                    8:0    0   64G  0 disk
    ├─sda1                 8:1    0  512M  0 part  /boot/efi
    ├─sda2                 8:2    0    1K  0 part
    └─sda5                 8:5    0 63.5G  0 part
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
    sdb                    8:16   0  2.5G  0 disk
    ├─sdb1                 8:17   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    │   └─vg--1-lvol0    253:2    0  100M  0 lvm   /tmp/new
    └─sdb2                 8:18   0  500M  0 part
      └─md1                9:1    0  996M  0 raid0
    sdc                    8:32   0  2.5G  0 disk
    ├─sdc1                 8:33   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    │   └─vg--1-lvol0    253:2    0  100M  0 lvm   /tmp/new
    └─sdc2                 8:34   0  500M  0 part
      └─md1                9:1    0  996M  0 raid0
    vagrant@vagrant:~$
    ```

1. Сделайте `--fail` на устройство в вашем RAID1 md.   
    **Ответ:**   
    ```
    vagrant@vagrant:~$ sudo mdadm /dev/md0 --fail /dev/sdb1
    mdadm: set /dev/sdb1 faulty in /dev/md0
    ```

1. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.   
    **Ответ:** 
    ```
    vagrant@vagrant:~$ dmesg | grep raid1
    [ 8883.390227] md/raid1:md0: not clean -- starting background reconstruction
    [ 8883.390230] md/raid1:md0: active with 2 out of 2 mirrors
    [12350.035326] md/raid1:md0: Disk failure on sdb1, disabling device.
                   md/raid1:md0: Operation continuing on 1 devices.
    vagrant@vagrant:~$
    ```

1. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
    **Ответ:**    
    ```
    vagrant@vagrant:~$ gzip -t /tmp/new/test.gz && echo $?
    0
    ```
1. Погасите тестовый хост, `vagrant destroy`.   
    **Ответ:** 
    ```
    C:\Users\miata\vagrant>vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
    ==> default: Forcing shutdown of VM...
    ==> default: Destroying VM and associated drives...

    C:\Users\miata\vagrant>
    ```
