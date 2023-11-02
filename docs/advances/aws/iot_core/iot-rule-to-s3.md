# AWS IoT Core: _Rule_

## Set up AWS IoT

1.  Set up AWS IoT Core

    * Go to **AWS IoT Core** :octicons-arrow-right-24: Manage :octicons-arrow-right-24: Thing types :octicons-arrow-right-24: Click `Create thing type`

    * On Thing groups :octicons-arrow-right-24: Click `Create thing group`

    * On Security :octicons-arrow-right-24: Policies :octicons-arrow-right-24: Click `Create policy`

      * Create Connect Policy

        ```json linenums="1"
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "iot:Connect"
              ],
              "Resource": [
                "arn:aws:iot:<region>:<aws_account_id>:client/${iot:Connection.Thing.ThingName}"
              ]
            }
          ]
        }
        ```

## References

- https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-tutorial.html
- https://www.cloudthat.com/resources/blog/step-by-step-guide-to-register-a-new-iot-device-in-aws-cloud?utm_source=blog-website&utm-medium=text-link&utm_campaign=%2Fstep-by-step-guide-to-register-a-new-iot-device-in-aws-cloud%2F
- https://www.cloudthat.com/resources/blog/step-by-step-guide-to-store-aws-iot-data-into-s3-bucket
- https://fanchenbao.medium.com/integrate-iot-device-with-aws-iot-using-python-part-i-upload-data-to-mqtt-topic-3f2b30ec6a6
- https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/cost-effectively-ingest-iot-data-directly-into-amazon-s3-using-aws-iot-greengrass.html#cost-effectively-ingest-iot-data-directly-into-amazon-s3-using-aws-iot-greengrass-best-practices

- https://docs.aws.amazon.com/solutions/latest/constructs/aws-iot-s3.html
- https://github.com/awslabs/aws-solutions-constructs/tree/main/source/patterns/@aws-solutions-constructs/aws-iot-s3

- https://www.youtube.com/watch?v=SN4_2ua6_Ko
- https://www.youtube.com/watch?v=kGqbqYMjAIE
