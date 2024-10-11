@echo off
title Tool-Py2exe
color f4
mode con cols=100 lines=30
:根据.py一键生成.exe，注意是否安装了pyinstaller并添加进环境变量
:在add中导入pykakasi的数据库资源，请确认自己环境的实际目录！
@REM pyinstaller -F -w -i images/music.ico -n gaokao main.py --add-data "%LOCALAPPDATA%\\Programs\\Python\\Python39\\Lib\\site-packages\\pykakasi\\data\\*;.\\pykakasi\\data"
pyinstaller -F -w -i images/music.ico -n gaokao main.py
pause