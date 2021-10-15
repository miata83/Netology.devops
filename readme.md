netology-devops \
Домашнее задание к занятию «2.4. Инструменты Git» 
1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.
Полный хэш: aefead2207ef7e2aa5dc81a34aedf0cad4c32545 \
Комментарий: Update CHANGELOG.md

2. Какому тегу соответствует коммит 85024d3? \
tag: v0.12.23

3. Сколько родителей у коммита b8d720? Напишите их хеши. \
много родителей, хэш первого: 56cd7859e05c36c06b56d013b55a252d0bb7e158

4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24. \
225466bc3e5f35baa5d07197bbc079345b77525e Cleanup after v0.12.23 release \
dd01a35078f040ca984cdd349f18d0b67e486c35 Update CHANGELOG.md \
4b6d06cc5dcb78af637bbb19c198faff37a066ed Update CHANGELOG.md \
d5f9411f5108260320064349b757f55c09bc4b80 command: Fix bug when using terraform login on Windows \
06275647e2b53d97d4f0a19a0fec11f6d69820b5 Update CHANGELOG.md \
5c619ca1baf2e21a155fcdb4c264cc9e24a2a353  website: Remove links to the getting started guide's old location

    Since these links were in the soon-to-be-deprecated 0.11 language section, I
    think we can just remove them without needing to find an equivalent link. \
6ae64e247b332925b872447e9ce869657281c2bf registry: Fix panic when server is unreachable

    Non-HTTP errors previously resulted in a panic due to dereferencing the
    resp pointer while it was nil, as part of rendering the error message.
    This commit changes the error message formatting to cope with a nil
    response, and extends test coverage.

    Fixes #24384 \
3f235065b9347a758efadc92295b540ee0a5e26e  Update CHANGELOG.md \
b14b74c4939dcab573326f4e3ee2a62e23e12f89 [Website] vmc provider links 


6. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы). \
 5e06e39fcc86bb622b962c87da84213d3331ddf8

7. Найдите все коммиты в которых была изменена функция globalPluginDirs. \
35a058fb3ddfae9cfee0b3893822c9a95b920f4c \
c0b17610965450a89598da491ce9b6b5cbd6393f \
8364383c359a6b738a436d1b7745ccdce178df47 

8. Кто автор функции synchronizedWriters? \
Author: Martin Atkins <mart@degeneration.co.uk>


