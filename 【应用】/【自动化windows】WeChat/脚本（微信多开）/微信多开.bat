@REM 使中文显示
@REM 重复启动多个微信【使用前需要把所有微信全部退出】
@REM @echo off
chcp 65001 > nul

taskkill /F /IM wechat.exe

@REM 实际最多开出来四个
@REM @REM %%i 是一个循环变量，它从1开始，以1为步长，直到10。每次循环都会执行 start
@REM for /L %%i in (1,1,10) do (
@REM     start C:\WeChat\WeChat.exe
@REM )

start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe
start C:\WeChat\WeChat.exe

exit
