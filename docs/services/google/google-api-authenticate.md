# Google: API Authentication

## Getting Started

### 1) Create Credential

* Go to **APIs & Services** :octicons-arrow-right-24: On **Enabled APIs & Services**
  :octicons-arrow-right-24: Click **ENABLE APIS AND SERVICES**
* Find your API that want to authorize :octicons-arrow-right-24: Click **ENABLE**
* On **Credentials** :octicons-arrow-right-24: Click **CREATE CREDENTIALS** and
  select **OAuth client ID**
* Drop down and select **Web Application** :octicons-arrow-right-24: Pass a credential
  name like `app-bigquery-server`
* On **Authorized redirect URIs** :octicons-arrow-right-24: Pass `http://localhost:8080`
  :octicons-arrow-right-24: Click **ADD URI** and then **CREATE**
* Copy **Client ID** and **Client Secret ID** from this creation process

### 2) Client Authenticate

* Get Authorization Code

    ```console
    GET /o/oauth2/v2/auth HTTP/1.1
    Host: accounts.google.com
    Content-Type: application/x-www-form-urlencoded

    client_id={client-id}&
    redirect_uri={redirect-uri}&
    response_type=code&
    scope={scope}&
    access_type=offline&
    include_granted_scopes=true&
    prompt=consent
    ```

* Request Access and Refresh tokens

    ```console
    POST /token HTTP/1.1
    Host: oauth2.googleapis.com
    Content-Type: application/x-www-form-urlencoded

    code={authorization-code}&
    client_id={client-id}.apps.googleusercontent.com&
    client_secret={client_secret}&
    redirect_uri=https://oauth2-login.appclient.com/code&
    grant_type=authorization_code

    ```

    !!! abstract

        **When does a refresh token expire?**:

        Refresh tokens do not expire, unless there are few special conditions :

        * The user has removed your Google application.
        * The refresh token has not been used for six months.
        * The user changed password and the refresh token contained Gmail scopes.
          This means that the refresh token will be invalidated only when he had previously
          given the permisions for managing his Gmail, and then later changed his password.
          For the rest of Google services like Youtube, Calendar etc, a changed password
          will not invalidate the refresh token.
        * The application generated a new refresh token for the user for more than 50 times.

* Re-generate Access Token

    ```console
    POST /token HTTP/1.1
    Host: oauth2.googleapis.com
    Content-Type: application/x-www-form-urlencoded

    client_id={client-id}.apps.googleusercontent.com&
    client_secret={client_secret}&
    refresh_token={refresh-token}&
    grant_type=refresh_token
    ```

## Playground

https://developers.google.com/oauthplayground/

## References

* [GoogleDeveloper: Identity - OAuth2 Web Server](https://developers.google.com/identity/protocols/oauth2/web-server#userconsentprompt)
* https://medium.com/automationmaster/getting-google-oauth-access-token-using-google-apis-18b2ba11a11a
* https://stackoverflow.com/questions/67451025/how-to-get-google-authorization-code-using-postman