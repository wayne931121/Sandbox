# Sandbox
Sandbox for Windows !

# How does this work?

This will open a new CLI, Only Access Low Setintegritylevel Files
- Read: All Files Access.
- Write: Only Low Setintegritylevel Files Can Be Writed.

# How to Run?

```bat
rem setintegritylevel.bat only need to run in the first time.
.\setintegritylevel.bat
rem this exe is windows x64 file, however you can compile it by yourself!
.\windows.exe
```

# How to Compile?

```bat
rem you need gcc installed first.
.\compile.bat
```

# How to Change Main Script?

- Edit main.bat
- Edit config.bat
- Edit windows.c

# 2. Using Sandbox.exe
if you don't want to use windows.exe.
```text
.\sandbox.exe "\"C:\Windows\System32\cmd.exe\" /v /k \"chcp 65001 ^& .\main.bat ^& echo 你好OK\""
```
