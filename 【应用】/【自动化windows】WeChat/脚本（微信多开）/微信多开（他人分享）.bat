@echo off
title ΢�Ŷ࿪����
color 3c
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Tencent\WeChat" /v InstallPath 2^>nul') do (set "wechat=%%b")
if not defined wechat echo;û���ҵ�΢��&pause&exit
set /p "num=����Ҫ��΢�ŵ�����:"
taskkill /f /t /im  WeChat.exe

cd /d "%wechat%"
for /L %%i in (1,1,%num%) do start /b "" "%wechat%\WeChat.exe" ""
exit