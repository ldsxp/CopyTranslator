@echo off

::���ó�����ļ�������·������ѡ��

set Program=%~dp0CopyTranslator.exe

 

::���ÿ�ݷ�ʽ���ƣ���ѡ��

set LnkName=CopyTranslator

 

::���ó���Ĺ���·����һ��Ϊ������Ŀ¼�����������գ��ű������з���·��

set WorkDir=%~dp0

 

::���ÿ�ݷ�ʽ��ʾ��˵������ѡ��

set Desc=Foreign language assisted reading and translation solution

 

if not defined WorkDir call:GetWorkDir "%Program%"

(echo Set WshShell=CreateObject("WScript.Shell"^)

echo strDesKtop=WshShell.SpecialFolders("DesKtop"^)

echo Set oShellLink=WshShell.CreateShortcut(strDesKtop^&"\%LnkName%.lnk"^)

echo oShellLink.TargetPath="%Program%"

echo oShellLink.WorkingDirectory="%WorkDir%"

echo oShellLink.WindowStyle=1

echo oShellLink.Description="%Desc%"

echo oShellLink.Save)>makelnk.vbs

echo �����ݷ�ʽ�����ɹ���

makelnk.vbs

del /f /q makelnk.vbs

exit

goto :eof

:GetWorkDir

set WorkDir=%~dp1

set WorkDir=%WorkDir:~,-1%

goto :eof