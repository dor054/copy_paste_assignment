import json
import urllib
import urllib3
import boto3

def lambda_handler(event, context):
    # This lambda is triggered by create file event on a binded S3 storage. 
    # It sends a POST request to an external API (Azure trigger in our case) with source URL and filename
    
    print (f"Event occured: {event}")
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    filename = urllib.parse.unquote_plus(filename, encoding='utf-8')
    s3 = boto3.client('s3')

    # source file URL expires after 10 minutes
    url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket,
                                                'Key': filename},
                                        ExpiresIn=600)
                                        
    print (f"Bucket: {bucket}\nFilename: {filename}")
    print(url)
    
    body = {"filename":filename, "url":url}
    body_str=json.dumps(body)
    print(body_str)
    azure_trigger_url = "https://copy-paste-df.azurewebsites.net/api/HttpTriggerDf1"
    http = urllib3.PoolManager()
    response = http.request('POST', azure_trigger_url, body=body_str)
    print(f"Azure trigger response: {response.read()}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Copying file {filename} from S3 storage has been triggered successfully!')
    }
