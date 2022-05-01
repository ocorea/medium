#Created by  Orlin Corea ocorea@truess.net
import requests
import boto3
from botocore.client import Config

class shorter:
    #Creation of the S3 BOTO Client
    def __init__(self, region:str, iam_key:str, iam_secret:str, expiration:int, domain:str, api_key:str):
        self.iam_key=iam_key
        self.iam_secret = iam_secret
        self.region = region
        self.api_key = api_key
        self.domain = domain
        self.expiration = expiration  # in seconds       
        self.s3_client = boto3.client('s3', region_name = self.region,
        aws_access_key_id=self.iam_key, aws_secret_access_key=self.iam_secret)

    def getSignedURL(self, bucket:str, s3_object_key:str)->str:
        try:
            response = self.s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': s3_object_key},
            ExpiresIn=self.expiration)
            return response
        except Exception as e:
            print('error: ',e)
            return None


    
    def getShortUrl(self,url:str)->str:
        try:
            #call api dynamic link
            headers={"Content-Type": "application/json"}
            payload={
                "dynamicLinkInfo": {"domainUriPrefix": self.domain, "link": url}}
            resp=requests.post("https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=" + self.api_key,
            headers=headers, json=payload        
            )        
            if (resp.status_code==200):            
                return resp.json()['shortLink']
            else:
                return url
        except Exception as e:
            print('error: ',e)
            return None


        