# Terraform: Manage Secret

One of the most common questions we get about using Terraform to manage infrastructure
as code (IaC) is how to handle secrets such as passwords, API keys, and other sensitive
data.

For example, here’s a snippet of Terraform code that can be used to deploy MySQL
using Amazon RDS:

```terraform
resource "aws_db_instance" "example" {
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "example"

  # How should you manage the credentials for the master user?
  username             = "???"
  password             = "???"
}
```

## Technique: Environment Variables

```terraform
resource "aws_db_instance" "example" {
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "example"

  # Set the secrets from variables
  username             = var.username
  password             = var.password
}
```

## References

- [GruntWork: A Comprehensive Guide to Manage Secrets in Terraform](https://blog.gruntwork.io/a-comprehensive-guide-to-managing-secrets-in-your-terraform-code-1d586955ace1)
