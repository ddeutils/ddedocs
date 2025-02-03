# OpenID Connect

## Workload Identity Federation through a Service Account

1. (Optional) Create a Google Cloud Service Account. If you already have a
    Service Account, take note of the email address and skip this step.

    ```shell
    gcloud iam service-accounts create "my-service-account" \
      --project "${PROJECT_ID}"
    ```

2. Create a Workload Identity Pool:

    ```shell
    gcloud iam workload-identity-pools create "github" \
      --project="${PROJECT_ID}" \
      --location="global" \
      --display-name="GitHub Actions Pool"
    ```

3. Get the full ID of the Workload Identity Pool:

    ```shell
    gcloud iam workload-identity-pools describe "github" \
      --project="${PROJECT_ID}" \
      --location="global" \
      --format="value(name)"
    ```

    This value should be of the format:

    ```text
    projects/123456789/locations/global/workloadIdentityPools/github
    ```

4. Create a Workload Identity Provider in that pool:

    ```shell
    gcloud iam workload-identity-pools providers create-oidc "my-repo" \
      --project="${PROJECT_ID}" \
      --location="global" \
      --workload-identity-pool="github" \
      --display-name="My GitHub repo Provider" \
      --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
      --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'" \
      --issuer-uri="https://token.actions.githubusercontent.com"
    ```

    !!! warning

        Using "name" fields in Attribute Conditions or IAM Bindings like repository
        and repository_owner increase the chances of cybersquatting and typosquatting
        attacks. If you delete your GitHub repository or GitHub organization, someone
        could claim that same name and establish an identity.
        To protect against this situation, use the numeric *_id fields instead,
        which GitHub guarantees to be unique and never re-used.

        To get your numeric organization ID:

        ```shell
        ORG="my-org" # TODO: replace with your org
        curl -sfL -H "Accept: application/json" "https://api.github.com/orgs/${ORG}" | jq .id
        ```

        To get your numeric repository ID:

        ```shell
        REPO="my-org/my-repo" # TODO: replace with your full repo including the org
        curl -sfL -H "Accept: application/json" "https://api.github.com/repos/${REPO}" | jq .id
        ```

        These can be used in an Attribute Condition:

        ```text
        assertion.repository_owner_id == '1342004' && assertion.repository_id == '260064828'
        ```

        [Read more Security Considerations](https://github.com/google-github-actions/auth/blob/main/docs/SECURITY_CONSIDERATIONS.md)

5. Allow authentications from the Workload Identity Pool to your Google Cloud
   Service Account.

    ```shell
    gcloud iam service-accounts add-iam-policy-binding "my-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
      --project="${PROJECT_ID}" \
      --role="roles/iam.workloadIdentityUser" \
      --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"
    ```

    !!! note

        `${REPO}` is the full repo name including the parent GitHub organization,
        such as `my-org/my-repo`.

    !!! note

        `${WORKLOAD_IDENTITY_POOL_ID}` is the full pool id, such as
        `projects/123456789/locations/global/workloadIdentityPools/github`.

6. Extract the Workload Identity Provider resource name:

    ```shell
    gcloud iam workload-identity-pools providers describe "my-repo" \
      --project="${PROJECT_ID}" \
      --location="global" \
      --workload-identity-pool="github" \
      --format="value(name)"
    ```

    Use this value as the workload_identity_provider value in the GitHub Actions YAML:

    ```yaml
    - uses: 'google-github-actions/auth@v2'
      with:
        service_account: '...' # my-service-account@my-project.iam.gserviceaccount.com
        workload_identity_provider: '...' # "projects/123456789/locations/global/workloadIdentityPools/github/providers/my-repo"
    ```

7. As needed, grant the Google Cloud Service Account permissions to access
   Google Cloud resources. This step varies by use case.
   The following example shows granting access to a secret in Google Secret Manager.

    ```shell
    gcloud secrets add-iam-policy-binding "my-secret" \
      --project="${PROJECT_ID}" \
      --role="roles/secretmanager.secretAccessor" \
      --member="serviceAccount:my-service-account@${PROJECT_ID}.iam.gserviceaccount.com"
    ```

## References

- https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform
- https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
- [GitHub Action: Authenticate to Google Cloud](https://github.com/google-github-actions/auth?tab=readme-ov-file#workload-identity-federation-through-a-service-account)
- https://github.com/google-github-actions/auth/issues/77
