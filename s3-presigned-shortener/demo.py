#IMPORT THE CLASS REFERENCE
from shorterURL import shorter
#general parameters
LINK_EXPIRATION_HOURS = 1 # one hours
REGION="<REGION_OF_YOUR_BUCKET>"
USER_KEY="<YOUR_USER_IAM_KEY>"
USER_SECRET="<YOUR_USER_IAM_SECRET>"
SHORTER_DOMAIN="<YOUR_DOMAN>"
SHORTER_API_KEY="<YOUR_SHORTER_API_KEY>"

#create the instance
#the expiration is expresed in seconds
shortURL = shorter(REGION,USER_KEY,USER_SECRET,
            3600*LINK_EXPIRATION_HOURS, SHORTER_DOMAIN,
            SHORTER_API_KEY)

def linkGenerator(bucket,s3_object_key):
    #the s3 object key is the name of the file available in s3
    presigned_link=shortURL.getSignedURL(bucket,s3_object_key)
    response_link=shortURL.getShortUrl(presigned_link)
    return response_link


#sample of call
link = linkGenerator("<YOUR BUCKET NAME>","<YOUR OBJECT KEY >")
print("response is: ", link)