# Курсовая работа по итогам модуля "DevOps и системное администрирование"

Курсовая работа необходима для проверки практических навыков, полученных в ходе прохождения курса "DevOps и системное администрирование".

Мы создадим и настроим виртуальное рабочее место. Позже вы сможете использовать эту систему для выполнения домашних заданий по курсу

## Задание

1. Создайте виртуальную машину Linux.
2. Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.
3. Установите hashicorp vault ([инструкция по ссылке](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started#install-vault)).
4. Cоздайте центр сертификации по инструкции ([ссылка](https://learn.hashicorp.com/tutorials/vault/pki-engine?in=vault/secrets-management)) и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).
5. Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.
6. Установите nginx.
7. По инструкции ([ссылка](https://nginx.org/en/docs/http/configuring_https_servers.html)) настройте nginx на https, используя ранее подготовленный сертификат:
  - можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
  - можно использовать и другой html файл, сделанный вами;
8. Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.
9. Создайте скрипт, который будет генерировать новый сертификат в vault:
  - генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
  - перезапускаем nginx для применения нового сертификата.
10. Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.

## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

**В качестве виртуальной машины используется сервер Ubuntu 20.04 на Amazon Web Services**

**- Процесс установки и настройки ufw**

```
ubuntu@ip-172-31-5-116:~$ sudo apt install ufw
Reading package lists... Done
Building dependency tree
Reading state information... Done
ufw is already the newest version (0.36-6ubuntu1).
0 upgraded, 0 newly installed, 0 to remove and 12 not upgraded.

ubuntu@ip-172-31-5-116:~$ sudo ufw default deny incoming
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)

ubuntu@ip-172-31-5-116:~$ sudo ufw default allow outgoing
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)

ubuntu@ip-172-31-5-116:~$ sudo ufw allow ssh
ubuntu@ip-172-31-5-116:~$ sudo ufw allow 443
ubuntu@ip-172-31-5-116:~$ sudo ufw allow from 127.0.0.1

ubuntu@ip-172-31-5-116:~$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup

ubuntu@ip-172-31-5-116:~$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
443                        ALLOW       Anywhere
22                         ALLOW       Anywhere
Anywhere                   ALLOW       127.0.0.1
22/tcp (v6)                ALLOW       Anywhere (v6)
443 (v6)                   ALLOW       Anywhere (v6)
22 (v6)                    ALLOW       Anywhere (v6)

```
**- Процесс установки и выпуска сертификата с помощью hashicorp vault**

```
ubuntu@ip-172-31-5-116:~$ curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK
ubuntu@ip-172-31-5-116:~$ sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
Hit:1 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal InRelease
Get:2 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:3 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal-backports InRelease [108 kB]
Hit:4 https://apt.releases.hashicorp.com focal InRelease
Get:5 http://security.ubuntu.com/ubuntu focal-security InRelease [114 kB]
Fetched 336 kB in 1s (610 kB/s)
Reading package lists... Done
ubuntu@ip-172-31-5-116:~$ sudo apt-get update && sudo apt-get install vault
Hit:1 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal InRelease
Hit:2 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal-updates InRelease
Hit:3 http://eu-central-1.ec2.archive.ubuntu.com/ubuntu focal-backports InRelease
Hit:4 https://apt.releases.hashicorp.com focal InRelease
Hit:5 http://security.ubuntu.com/ubuntu focal-security InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree
Reading state information... Done
vault is already the newest version (1.9.2).
0 upgraded, 0 newly installed, 0 to remove and 12 not upgraded.
ubuntu@ip-172-31-5-116:~$ vault
Usage: vault <command> [args]

Common commands:
    read        Read data and retrieves secrets
    write       Write data, configuration, and secrets
    delete      Delete secrets and configuration
    list        List data or secrets
    login       Authenticate locally
    agent       Start a Vault agent
    server      Start a Vault server
    status      Print seal and HA status
    unwrap      Unwrap a wrapped secret

Other commands:
    audit          Interact with audit devices
    auth           Interact with auth methods
    debug          Runs the debug command
    kv             Interact with Vault's Key-Value storage
    lease          Interact with leases
    monitor        Stream log messages from a Vault server
    namespace      Interact with namespaces
    operator       Perform operator-specific tasks
    path-help      Retrieve API help for paths
    plugin         Interact with Vault plugins and catalog
    policy         Interact with policies
    print          Prints runtime configurations
    secrets        Interact with secrets engines
    ssh            Initiate an SSH session
    token          Interact with tokens
ubuntu@ip-172-31-5-116:~$vault server -dev -dev-root-token-id=root
ubuntu@ip-172-31-5-116:~$ export VAULT_ADDR=http://127.0.0.1:8200
ubuntu@ip-172-31-5-116:~$ export VAULT_TOKEN=root

ubuntu@ip-172-31-5-116:~$ tee admin-policy.hcl <<EOF
> # Enable secrets engine
> path "sys/mounts/*" {
>   capabilities = [ "create", "read", "update", "delete", "list" ]
> }
>
> # List enabled secrets engine
> path "sys/mounts" {
>   capabilities = [ "read", "list" ]
> }
>
> # Work with pki secrets engine
> path "pki*" {
>   capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
> }
> EOF
# Enable secrets engine
path "sys/mounts/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# List enabled secrets engine
path "sys/mounts" {
  capabilities = [ "read", "list" ]
}

# Work with pki secrets engine
path "pki*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}
ubuntu@ip-172-31-5-116:~$


ubuntu@ip-172-31-5-116:~$ vault policy write admin admin-policy.hcl
Success! Uploaded policy: admin
```

**#Generate root CA**
```
ubuntu@ip-172-31-5-116:~$ vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
ubuntu@ip-172-31-5-116:~$ vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
ubuntu@ip-172-31-5-116:~$ vault write -field=certificate pki/root/generate/internal \
>      common_name="ec2-3-71-99-4.eu-central-1.compute.amazonaws.com" \
>      ttl=87600h > CA_cert.crt

ubuntu@ip-172-31-5-116:~$ vault write pki/config/urls \
>      issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
>      crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls
```
**#Generate intermediate CA**
```
ubuntu@ip-172-31-5-116:~$ vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
ubuntu@ip-172-31-5-116:~$ vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
ubuntu@ip-172-31-5-116:~$ vault write -format=json pki_int/intermediate/generate/internal \
>      common_name="ec2-3-71-99-4.eu-central-1.compute.amazonaws.com Intermediate Authority" \
>      | jq -r '.data.csr' > pki_intermediate.csr
ubuntu@ip-172-31-5-116:~$ vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
>      format=pem_bundle ttl="43800h" \
>      | jq -r '.data.certificate' > intermediate.cert.pem
ubuntu@ip-172-31-5-116:~$ vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
```
**#Create a role**
```
ubuntu@ip-172-31-5-116:~$ vault write pki_int/roles/example-dot-com \
>      allowed_domains="ec2-3-71-99-4.eu-central-1.compute.amazonaws.com" \
>      allow_subdomains=true \
>      max_ttl="720h"
Success! Data written to: pki_int/roles/example-dot-com
```
**#Request certificates**
```
vault write pki_int/issue/example-dot-com \
     common_name="test.ec2-3-71-99-4.eu-central-1.compute.amazonaws.com" \
     ttl="720h" > test.ec2-3-71-99-4.eu-central-1.compute.amazonaws.com.crt
     
ubuntu@ip-172-31-5-116:~$ cat test.aws.com.crt | jq -r .data.certificate > test.aws.com.crt
ubuntu@ip-172-31-5-116:~$ cat test.aws.com.crt | jq -r .data.private_key > test.aws.com.crt.key
```
**Установка корневого сертификата созданного центра сертификации в доверенные в хостовой системе**
```
ubuntu@ip-172-31-5-116:~$ sudo cp CA_cert.crt /usr/local/share/ca-certificates/
ubuntu@ip-172-31-5-116:~$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
ubuntu@ip-172-31-5-116:
``

- Процесс установки и настройки сервера nginx

```
ubuntu@ip-172-31-5-116:~$ sudo apt install nginx
ubuntu@ip-172-31-5-116:~$ sudo ufw app list
Available applications:
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
  OpenSSH
ubuntu@ip-172-31-5-116:~$ sudo ufw allow 'Nginx Full'
ubuntu@ip-172-31-5-116:~$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset:>
     Active: active (running) since Sun 2022-01-30 16:05:04 UTC; 6min ago
       Docs: man:nginx(8)
   Main PID: 24119 (nginx)
      Tasks: 2 (limit: 1147)
     Memory: 5.8M
     CGroup: /system.slice/nginx.service
             ├─24119 nginx: master process /usr/sbin/nginx -g daemon on; master>
             └─24120 nginx: worker process
```            
После установки nginx копируем файлы сертификата и ключа и указываем путь до них в файле настроек конфигурации сервера:             
```
ubuntu@ip-172-31-5-116:~$ sudo mkdir /etc/nginx/ssl
ubuntu@ip-172-31-5-116:~$ sudo cp test.aws.com.crt /etc/nginx/ssl
ubuntu@ip-172-31-5-116:~$ sudo cp test.aws.com.crt.key /etc/nginx/ssl
```

- Страница сервера nginx в браузере хоста не содержит предупреждений 
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Как сдавать курсовую работу

Курсовую работу выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. 
Ссылка на инструкцию [Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop).
