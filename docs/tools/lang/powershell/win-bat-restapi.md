# PowerShell: _RestAPI_

## WebRequest

Create Function to get the response code:

```shell
function Get-UrlStatusCode([string] $Url)
{ try
    { (Invoke-WebRequest -Uri $Url -UseBasicParsing -DisableKeepAlive).StatusCode }
  catch [Net.WebException]
	{ [int]$_.Exception.Response.StatusCode }
}
```

```shell
$r = Get-UrlStatusCode "http://localhost:8000/health"
if ($r -eq 200) {
	echo "The application can run normally."
} else {
	echo "Failed to request to health check endpoint."
}
```

## RestMethod

```shell
$Body = @{
    Cook = "Barbara"
    Meal = "Pizza"
}

$Header = @{
    "authorization" = "Bearer $token"
}

$Parameters = @{
    Method      = "POST"
    Uri         =  "https://4besday4.azurewebsites.net/api/AddMeal"
    Body        = ($Body | ConvertTo-Json)
    ContentType = "application/json"
    Headers     = $Header
}
Invoke-RestMethod @Parameters
```

!!! note

    ```shell
    $User = "GitHubUserName"
    $Token = "tokenhere"
    $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($User):$($Token)"))
    $Header = @{
        Authorization = "Basic $base64AuthInfo"
    }
    ```
