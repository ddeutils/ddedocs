# Setup Unity Catalog

**Unity Catalog** is a data governance solution for Databricks, designed to provide
a unified approach across all of your Databricks workspaces.

!!! important

    **Azure Databricks** workspace should be **Premium** pricing tier.

---

## :material-sort-variant: Prerequisite

To enable the **Databricks Account Console** and establish your first **Account
Admin**, you will need to engage someone who has the **Microsoft Entra ID** (Azure Active Directory)
==**Global Administrator**== role

For security purposes, only someone with the **Global Administrator** role has
permission to assign the first account admin role. After completing these steps,
you can remove the **Global Administrator** role from the Azure Databricks account.

1.  Create **Resource Group**
2.  Create Premium Tier **Azure Databricks** Workspace
3.  Create **Azure DataLake Gen2 Storage Account** and Container
4.  Create **Access Connector** for **Azure Databricks**
5.  Grant **Storage Blob Data Contributor** to **Access Connector** for **Azure Databricks** on **Azure DataLake Gen2 Storage Account**
6.  Enable **Unity Catalog** by creating Metastore and assigning to Workspace

!!! note

    If you do not create new **Access Connector** and use default provisioning, it
    will not use any managed identity on this **Access Connector**. The default
    Accesss Connector name is `unity-catalog-access-connector`

---

## :material-arrow-down-right: Getting Started

- Go to **Azure Databricks Workspace** :octicons-arrow-right-24: Click on **Manage Account**
  :octicons-arrow-right-24: Login into **Account console**
- Click on the **Data** tab :octicons-arrow-right-24: Create **Metastores** tab
- Provide information to create metastore (1 metastore per Region):
    - Metastore Name and Region (The best practice is choose same region and resource group)
    - **Azure DataLake Storage Gen2** (Example: `https://<container-name>@<storage-account-name>.dfs.core.windows.net/<path>`)
    - **Access Connector ID** (Resource ID of your **Access Connector**)
- Assign the workspace map to this metastore :octicons-arrow-right-24: Click on **Enable** Unity Catalog

---

## :material-arrow-right-bottom: External Catalog

**Create storage credentials**:

- On your **Azure Databricks Workspace** :octicons-arrow-right-24: Go to **Data Explorer**
  :octicons-arrow-right-24: **External Data** :octicons-arrow-right-24: Select **Storage Credentials**
- Click Add and then select Add a storage credential :octicons-arrow-right-24: Select Service Principal
- Enter the Storage credential name of your choice :octicons-arrow-right-24: Provide
  your service principle information :octicons-arrow-right-24: Click **Create**

**Create external location**:

- In the **Data Explorer** :octicons-arrow-right-24: Select **External Locations**
  :octicons-arrow-right-24: Click **Add** an external location
- Enter the External location name and **Azure DataLake Storage Gen2** URL :octicons-arrow-right-24:
  Select the Storage credential you created :octicons-arrow-right-24: Click **Create**

---

## :material-playlist-plus: Read Mores

- [:material-youtube: Enabling Unity Catalog on Azure Databricks: A Step-by-Step Guide](https://www.youtube.com/watch?v=f6Acij4hPqA)
- [:material-microsoft: Set up and manage Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/get-started)
- [:material-microsoft: Azure Databricks administration introduction](https://learn.microsoft.com/en-us/azure/databricks/admin/)
- [:material-microsoft: Create a Unity Catalog metastore](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/create-metastore)
- [:material-microsoft: Use Azure managed identities in Unity Catalog to access storage](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/azure-managed-identities)
