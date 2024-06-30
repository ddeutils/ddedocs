# Self Hosted with FastAPI

When we want to create a Rest API application like **Azure Function App** on
an on-premises server, it is simply to use the [FastAPI](https://fastapi.tiangolo.com/)
package, which is a lightweight Python ASGI web application, for this our purpose.

## :material-arrow-down-right: Getting Started

### Setup Application

Let’s start setting up your **FastAPI** application and a `.bat` script for run
this application with dynamic input arguments.

```python title="app/app.py"
from fastapi import FastAPI

def create_app() -> FastAPI:
    """Application Factory"""
    app = FastAPI()

    @app.get("/health/")
    async def health():
        return {"message": "Hello World"}

    return app
```

```python title="main.py"
import uvicorn
from app.app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```shell title="scripts/runserver.bat"
@echo off
goto :init

:usage
    echo USAGE:
    echo   %__bat_filename% [flags] "release argument"
    echo.
    echo.  -h, --help           shows this help
    echo.  -p, --port value     specifies a port number value
    echo.  --reload             enable auto-reload
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
    set "__reload="
    set "__release="

:parse
    if "%~1"==""                goto :validate

    if /i "%~1"=="-h"           call :usage "%~2" & goto :end
    if /i "%~1"=="--help"       call :usage "%~2" & goto :end

    if /i "%~1"=="-v"           call :version      & goto :end
    if /i "%~1"=="--version"    call :version full & goto :end

    if /i "%~1"=="-p"           set "__port=%~2" & shift & shift & call :port & goto :parse
    if /i "%~1"=="--port"       set "__port=%~2" & shift & shift & call :port & goto :parse

    if /i "%~1"=="--reload"     set "__reload=--reload" & shift & goto :parse

    if not defined __release    set "__release=%~1" & shift & goto :parse

    shift
    goto :parse

:validate
    if not defined __release call :missing_args & goto :end

:main
    echo INFO: Start running server with release "%__release%" ...
    call .\venv\Scripts\activate
    call uvicorn main:app --port %__port% %__reload%

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
    set "__reload="

    goto :eof
```

!!! note

    I use the `.bat` script because the on-premise server that I want to run is
    Windows OS.

### Deploy to Window Service

I use the [NSSM](https://nssm.cc/) software for wrap the `runserver.bat` script file and monitor
whether my app is able to run continuously on the Windows service.
So, I will [Download NSSM](https://nssm.cc/release/nssm-2.24.zip) and unzip the installed file to the current path.

!!! note

    We cannot use the **Docker** container in the target on-premises server
    because of the Windows Server version does not support, it be **Windows Server 2016**
    which does not support Linux container on VM and WSL.

First, we install my application on the **Windows service**, which can be seen
in the **Services** software.

```shell
.\nssm\win64\nssm.exe install "FastAPIService" "%cd%\runserver.bat"
```

Next, we can setup additional the logging component for `stdout` and `stderr`
in this application.

```shell
.\nssm\win64\nssm.exe set "FastAPIService" AppStdout "%cd%\logs\FastAPIService.log"
.\nssm\win64\nssm.exe set "FastAPIService" AppStderr "%cd%\logs\FastAPIService.log"
.\nssm\win64\nssm.exe set "FastAPIService" AppRotateFiles 1
.\nssm\win64\nssm.exe set "FastAPIService" AppRotateOnline 1
.\nssm\win64\nssm.exe set "FastAPIService" AppRotateSeconds 86400
.\nssm\win64\nssm.exe set "FastAPIService" AppRotateBytes 1048576
```

Finally, we start the application service by `sc.exe` command.

```shell
sc.exe start "FastAPIService"
```

!!! warning

    I cannot use the python package, `pywin32`, because I get the error message;

    ```text
    Error 1053: The service did not respond to the start or control request in a timely fashion
    ```

    when start this application service on locally.

### Setup Agent to On-Premises Server

We will create a CI/CD deployment pipeline with **Azure DevOps** that able to
deploy the application to target server. The purpose is running this application
on the Windows service in an on-premises server.

Firstly, the on-premises server does not connect to **Azure DevOps** because
It was not listed in the **Agent Pools** by **Self-Hosted** agent connection
type in my organization setting. So, we create a new agent pool name like
`MYSTDVM01` and follow the Azure document to list this new agent in the Agents menu.

!!! note

    More detail about the new Agent implementation, [How to install Self-hosted Windows agent for Azure DevOps](https://www.youtube.com/watch?v=xuKXO811O_w).

If you want to let everyone in your group of **Azure DevOps** can see and use this agent, you
should add owner permission to your group by
**Organization Setting** > **Agent Pools** > Your Agent Pool > **Security**.

Next, We create a folder `$(Agent.HomeDirectory)/app` for keeping source code without the DevOps pipeline
process before deploying my artifact to this agent.

Finally, we set up a Python interpreter for running the Python application in this agent.

- Download the required version of Python and install it on this agent

- Copy all the installed python files from `C:/Users/{user}/AppData/Local/Programs/Python/Python39`
  to `$(Agent.ToolsDirectory)/Python/3.9.13/x64/*`

- Create a complete file at `$(Agent.ToolsDirectory)/Python/3.9.13/x64.complete` for trigger **Azure DevOps**
  pipeline can use this package in the job

!!! note

    If your server set a proxy firwall rule, you can run self-hosted agent config by
    `./config.cmd --proxyurl http://proxy.domain.co.th --proxyusername "CEMENTH/{user}" --proxypassword "*******"`,
    it will save your password to `.proxycredentials` file for reuse this password for proxy mode configuration.

### Deploy to On-Premises Server

For the **CI pipeline**, I test code and package dependencies on the artifact server.

```yaml
jobs:
  - job: Phase_1
    displayName: Build and Test
    pool:
      vmImage: windows-latest
    variables:
      python.version: "3.9, 3.10"
    steps:
      - checkout: self
        clean: true
        fetchDepth: 1
      - task: UsePythonVersion@0
        displayName: Use Python $(python.version)
        inputs:
          versionSpec: $(python.version)
      - task: CmdLine@2
        displayName: Install dependencies
        inputs:
          script: python -m pip install --upgrade pip && pip install -r requirements.txt
          workingDirectory: fastapi
          failOnStderr: true
      - task: CmdLine@2
        displayName: pytest
        inputs:
          script: pip install pytest && pytest tests --doctest-modules --junitxml=junit/test-results.xml
          workingDirectory: fastapi
          failOnStderr: true
      - task: PublishTestResults@2
        displayName: Publish Test Results **/test-results.xml
        inputs:
          testResultsFiles: "**/test-results.xml"
          failTaskOnFailedTests: true
          testRunTitle: Python $(python.version)
  - job: Phase_2
    displayName: Publish
    dependsOn: Phase_1
    pool:
      vmImage: windows-latest
    steps:
      - checkout: self
        clean: true
        fetchDepth: 1
      - task: UsePythonVersion@0
        displayName: Use Python 3.9.13
        inputs:
          versionSpec: 3.9.13
      - task: CmdLine@2
        displayName: Create virtual environment
        inputs:
          script: python -m pip install --upgrade pip && python -m venv venv
          workingDirectory: fastapi
      - task: CmdLine@2
        displayName: Install dependencies
        inputs:
          script: .\venv\Scripts\activate && pip install -r requirements.txt --no-cache
          workingDirectory: fastapi
      - task: CmdLine@2
        displayName: Pack dependency files to wheel format
        inputs:
          script: .\venv\Scripts\activate && pip wheel -w wheels -r .\requirements.txt && echo "Create wheel files successful."
          workingDirectory: fastapi
      - task: PublishBuildArtifacts@1
        displayName: "Publish Artifact: drop"
        inputs:
          PathtoPublish: fastapi
```

!!! note

    For the Python dependencies in the requirement.txt file, I use wheel to download
    these dependencies from PyPI and save them to `\wheels` path by
    `pip wheel -w wheels -r .\requirements.txt`

For the **CD pipeline**, I deploy the application to the Windows service and the test service.

```yaml
jobs:
- job: Phase_1
  displayName: Deploy job
  pool:
    vmImage: Self-hosted agent
  variables:
    python.version: '3.9, 3.10'
  variables:
    application_name: 'FastAPIServiceDev'
    application_port: '8001'
    application_folder: 'dev/app_dmz'
    health_route: 'health/'
  steps:
  - powershell: |
      echo "User that this job uses to run:"
      whoami
      $service = Get-Service -Name "$(application_name)" -ErrorAction SilentlyContinue
      if ($service -eq $null)
      {
          echo "Service does not exists."
      } else {
          echo "Service does exists ..."
          sc.exe stop "$(application_name)"
          nssm.exe remove "$(application_name)" confirm
          echo "Success stop and remove service."
      }
      Start-Sleep -Seconds 20
    displayName: 'Remove existing Windows Service'
  - task: CopyFiles@2
    displayName: 'Copy Files to App Folder'
    inputs:
      SourceFolder: '$(System.DefaultWorkingDirectory)/_DATA360-DMZ/drop'
      Contents: |
        **
        !.git/**/*
        !.gitignore
        !.gitattributes
        !venv/**
      TargetFolder: '$(Agent.HomeDirectory)/app/$(application_folder)'
      CleanTargetFolder: true
  - task: UsePythonVersion@0
    displayName: 'Use Python 3.9.13'
    inputs:
      versionSpec: 3.9.13
      disableDownloadFromRegistry: true
  steps:
  - powershell: |
      echo "Start run setup ..."
      .\scripts\setup.bat
      $service = Get-Service -Name "$(application_name)" -ErrorAction SilentlyContinue
      if ($service -eq $null)
      {
          echo "Service does not exists"
          nssm.exe install "$(application_name)" "$(pwd)\scripts\runserver.bat" "--port $(application_port) develop"
          nssm.exe set "$(application_name)" AppDirectory "$(pwd)"
          echo "Set AppStdout to $(pwd)\logs\$(application_name).log"
          nssm.exe set "$(application_name)" AppStdout "$(pwd)\logs\$(application_name).log"
          echo "Set AppStderr to $(pwd)\logs\$(application_name).log"
          nssm.exe set "$(application_name)" AppStderr "$(pwd)\logs\$(application_name).log"
          nssm.exe set "$(application_name)" AppRotateFiles 1
          nssm.exe set "$(application_name)" AppRotateOnline 1
          nssm.exe set "$(application_name)" AppRotateSeconds 86400
          nssm.exe set "$(application_name)" AppRotateBytes 1048576
      } else {
          echo "Service does exists."
      }
      nssm.exe status "$(application_name)"
      sc.exe start "$(application_name)"
    workingDirectory: '$(Agent.HomeDirectory)\app\$(application_folder)\'
    displayName: 'Setup and Install Windows service'
- job: Phase_1
  displayName: Deploy job
  pool:
    vmImage: Self-hosted agent
  variables:
    application_port: '8001'
    health_route: 'health/'
  steps:
  - powershell: |
      $r = curl.exe "http://localhost:$(application_port)/$(health_route)" --silent
      if (($r -ne '{"detail":"Not Found"}') -or ($r)) {
        echo "SUCCESS: The application can run normally."
        exit 0;
      } else {
        echo "ERROR: Failed to request to health check endpoint."
        exit 1;
      }
    displayName: 'RestAPI to Health Check'
```

!!! warning

    We should install **NSSM** on that on-premises server before running this
    CI/CD pipeline. If you get a permission issue of your agent job when executing
    the **NSSM** file, you can add the self-host agent user, `NetworkService`,
    to the **Admin** group in that server.

### Setup Environments

We will set up environments for the **CD pipelines** by the port of application
such as `8001` for development and `8000` for production because we want to partition
that server for two environments.
