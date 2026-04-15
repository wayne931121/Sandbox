chcp 65001

:O

gcc sandbox.c -o sandbox

pause

.\sandbox.exe "\"C:\Windows\System32\cmd.exe\" /v /k \"chcp 65001 ^& .\main.bat ^& echo 你好OK\""

pause

goto O