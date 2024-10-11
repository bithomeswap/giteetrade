@echo off
title 微信多开工具
color 3c
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Tencent\WeChat" /v InstallPath 2^>nul') do (set "wechat=%%b")
if not defined wechat echo;没有找到微信&pause&exit
set /p "num=输入要开微信的数量:"
taskkill /f /t /im  WeChat.exe

cd /d "%wechat%"
for /L %%i in (1,1,%num%) do start /b "" "%wechat%\WeChat.exe" ""
exit