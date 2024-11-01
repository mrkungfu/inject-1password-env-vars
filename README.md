# inject-1password-env-vars

Very, very basic script - not even making this pip installable - to load secrets from 1Password's cli tool into your environment.

What it does:
- gets env variables matching 1Password urls (`op://...`)
- pulls the secrets/variables all at once to minimize requests via `op` cli
- outputs the shell commands which can be executed directly by a shell script to replace op urls with secrets

Couple examples shell scripts for Windows below.


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
@echo on
```
