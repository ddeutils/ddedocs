# PowerShell: _Batch File_

As others have already said, parameters passed through the command line can be
accessed in batch files with the notation `%1` to `%9`. There are also two other
tokens that you can use:

- `%0` is the executable (batch file) name as specified in the command line.
- `%*` is all parameters specified in the command line -- this is very useful if
  you want to forward the parameters to another program.

There are also lots of important techniques to be aware of in addition to simply
how to access the parameters.

## Checking if a parameter was passed

This is done with constructs like `IF "%~1"==""`, which is `true` if and only if
no arguments were passed at all. Note the tilde character which causes any surrounding
quotes to be removed from the value of `%1`;
without a tilde you will get unexpected results if that value includes double quotes,
including the possibility of syntax errors.

## Handling more than 9 arguments

If you need to access more than 9 arguments you have to use the command `SHIFT`.
This command shifts the values of all arguments one place, so that `%0` takes the
value of `%1`, `%1` takes the value of `%2`, etc. `%9` takes the value of the tenth
argument (if one is present), which was not available through any variable before
calling `SHIFT` (enter command `SHIFT /?` for more options).

`SHIFT` is also useful when you want to easily process parameters without requiring
that they are presented in a specific order. For example, a script may recognize
the flags `-a` and `-b` in any order. A good way to parse the command line in such
cases is

```shell
:parse
    IF "%~1"=="" GOTO endparse
    IF "%~1"=="-a" REM do something
    IF "%~1"=="-b" REM do something else
    SHIFT
    GOTO parse

:endparse
    REM ready for action!
```

## Substitution of batch parameters

For parameters that represent file names the shell provides lots of functionality
related to working with files that is not accessible in any other way. This
functionality is accessed with constructs that begin with `%~`.

For example, to get the size of the file passed in as an argument use

```shell
ECHO %~z1
```

To get the path of the directory where the batch file was launched from you can
use

```shell
ECHO %~dp0
```

> **Note**: \
> You can view the full range of these capabilities by typing `CALL /?` in the
> command prompt.

## Full Example

```shell
@echo off
goto :init

:usage
    echo USAGE:
    echo   %__bat_filename% [flags] "release argument"
    echo.
    echo.  -h, --help           shows this help
    echo.  -p, --port value     specifies a port number value
    goto :eof

:missing_args
    call :usage
    echo.
    echo ****
    echo MISSING RELEASE ARGUMENT !!!
    goto :eof

:port
    echo Port does set from argument and port changes from 8000 to %__port% ...
    goto :eof

:version
    if "%~1"=="full" call :usage & goto :eof
    echo %__version%
    goto :eof

:init
    set "__name=%~n0"
    set "__port=8000"

    set "__bat_filepath=%~0"
    set "__bat_path=%~dp0"
    set "__bat_filename=%~nx0"

    set "__version=0.1.0"
    set "__release="

:parse
    if "%~1"==""                goto :validate

    if /i "%~1"=="-h"           call :usage "%~2" & goto :end
    if /i "%~1"=="--help"       call :usage "%~2" & goto :end

    if /i "%~1"=="-v"           call :version      & goto :end
    if /i "%~1"=="--version"    call :version full & goto :end

    if /i "%~1"=="-p"           set "__port=%~2" & shift & shift & call :port & goto :parse
    if /i "%~1"=="--port"       set "__port=%~2" & shift & shift & call :port & goto :parse

    if not defined __release    set "__release=%~1" & shift & goto :parse

    shift
    goto :parse

:validate
    if not defined __release call :missing_args & goto :end

:main
    echo INFO: Start running server with release "%__release%" ...
    call .\venv\Scripts\activate
    call uvicorn main:app --port %__port%

:end
    echo.
    echo End and Clean Up
    call :cleanup
    exit /B

:cleanup
    REM The cleanup function is only really necessary if you
    REM are _not_ using SETLOCAL.

    set "__name="
    set "__port="

    set "__bat_filepath="
    set "__bat_path="
    set "__bat_filename="

    set "__release="
    set "__version="

    goto :eof
```

> **Note**: \
> `setlocal` allows you to set environmental variables (that are usually global)
> only seen inside your batch file and automatically cleans them up when the
> `endlocal` call is executed or the batch file ends.
>
> The most frequent use of SETLOCAL is to turn on command extensions and allow
> delayed expansion of variables:
> `setlocal enableextensions enabledelayedexpansion`

## References

- https://stackoverflow.com/questions/14286457/using-parameters-in-batch-files-at-windows-command-line
- https://stackoverflow.com/questions/3973824/windows-bat-file-optional-argument-parsing
