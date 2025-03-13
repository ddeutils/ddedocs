# Customer Profile

## Profile

| Field Name      |  Alias   | Data Type | PK | Description                                            |
|-----------------|:--------:|-----------|----|--------------------------------------------------------|
| `customer_id`   | cust_id  | STRING    | Y  | Unique identifier for the customer                     |
| `first_name`    |  fname   | STRING    |    | Customer's first name                                  |
| `last_name`     |  lname   | STRING    |    | Customer's last name                                   |
| `email`         |  email   | STRING    |    | Customer's email address                               |
| `phone_number`  |  phone   | STRING    |    | Customer's phone number                                |
| `dob`           |   dob    | DATE      |    | Date of birth                                          |
| `gender`        |  gender  | STRING    |    | Customer's gender (e.g., "M", "F", "Other")            |
| `address`       | address  | STRING    |    | Full address (e.g., street, city, state, zip)          |
| `register_date` | register | DATE      |    | Date the customer signed up                            |
| `email_opt_in`  |          | BOOLEAN   |    | Whether the customer opted in for email communications |
| `sms_opt_in`    |          | BOOLEAN   |    | Whether the customer opted in for SMS communications   |


## Family

| Field Name      |  Alias   | Data Type | PK | Description                                          |
|-----------------|:--------:|-----------|----|------------------------------------------------------|
| `family_id`     |  fam_id  | STRING    | Y  | Unique identifier for the family                     |
| `family_name`   | fam_name | STRING    |    | Family's name (e.g. last name of customer)           |
| `customer_id`   | cust_id  | STRING    |    | Identifier for the customer that stay on this family |
