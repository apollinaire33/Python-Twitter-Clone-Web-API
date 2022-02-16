import boto3
import json

from django.conf import settings


class AmazonWebServices:
    def __init__(self, service_type):
        self._aws_client = boto3.client(
            service_type,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )


class SES(AmazonWebServices):
    def __init__(self):
        super().__init__('ses')

    def send_email(self, recipients, subject, body):
        charset = "UTF-8"
        return self._aws_client.send_email(
            Source=settings.AWS_SES_EMAIL_SOURCE,
            Destination={
                'ToAddresses': [recipients],
            },
            Message={
                "Subject": {
                    "Charset": charset,
                    "Data": subject,
                },
                "Body": {
                    "Html": {
                        "Charset": charset,
                        "Data": body,
                    }
                },
            },
        )

    def send_template_email(self, recipients, tempalte, template_data):
        return self._aws_client.send_templated_email(
            Source=settings.AWS_SES_EMAIL_SOURCE,
            Destination={
                'ToAddresses': [recipients],
            },
            Template=tempalte,
            TemplateData=json.dumps(template_data),
        )


class S3(AmazonWebServices):
    def __init__(self):
        super().__init__('s3')

    def get_presigned_url(self, key, time=3600):
        return self._aws_client.generate_presigned_url(
            ClientMethod='put_object',
            ExpiresIn=time,
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key}
        )

    def get_file(self, key, time=3600):
        return self._aws_client.generate_presigned_url(
            ClientMethod='get_object',
            ExpiresIn=time,
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key}
        )

    def delete_file(self, key):
        return self._aws_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
