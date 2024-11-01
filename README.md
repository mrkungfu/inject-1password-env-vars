# inject-1password-env-vars

Very basic. Gets env variables matching 1Password urls (op://), pulls them all at once and then provides the command line commands which can then be executed directly by a shell script. Couple examples shell scripts for Windows below.

Powershell:

```pwsh
python '<path_to_script>\inject_secrets.py' --shell powershell | Invoke-Expression
```

As a .bat script (via a file):

```winbatch
@echo off
for /f "delims=" %%i in ('python "<path_to_script>\inject_secrets.py"') do (%%i)

setlocal

set "tmpFile=out.test.tmp"

FOR /F "tokens=1,2 delims==" %%G IN ('SET ^| findstr "op://"') DO (
    op read "%%H" > "%tmpFile%"
    FOR /F %%A IN (%tmpFile%) DO (
        echo Updating %%G
        set %%G=%%A
    )
    if exist "%tmpFile%" del "%tmpFile%"
)

endlocal
@echo on
```
