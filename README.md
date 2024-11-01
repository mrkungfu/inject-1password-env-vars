# inject-1password-env-vars

Very basic. Gets env variables matching 1Password urls (`op://...`), pulls the secrets/variables all at once and then provides the shell commands which can be executed directly by a shell script. Couple examples shell scripts for Windows below.


# Q&A

## Why use this instead of `$ op run`?
A: Simple, you don't have to deal with any oddities that crop up running in a subshell (lack of ansii colors, weird window resizing) as well as having access to those secrets across commands without having to type `op run` each time. It's the simple things that matter in life. :)

## Might there be a better way?
A: Prolly! Let me know if so. :)


# Examples

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
