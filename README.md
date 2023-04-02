# copy_paste_assignment

Goal: Implement a demo of following scenario: When a file uploaded to AWS s3 storage copy it to an Azure storage account.

Solution:

On AWS:
1. Create an s3 storage
2. Define role with permissios to access s3 Storage. IAM -> Roles -> Create new role -> Attach to the role following policies: AmazonS3FullAccess, CloudWatchFullAccess, AWSLambda_FullAccess
3. Create a lambda function. Assign to it the role you created in previous step. 
4. As a trigger for lambda use s3 storage created in step 1. Trigger by create events. (Event types: s3:ObjectCreated:*).
5. Write a code for lambda based on lambda_function.py and Deploy it.

On Azure:
1. Create storage account and create container for it.
2. Create Function App based on HTTP trigger.
3. Write a function based on azure_function_init.py. I used an external IDE and wrote a function app code using VS code.
4. On function app configuration add a connection string to consume the blob storage Name: df_storage_conn_str1, Type: Custom. Use the connction string from storage account page. 
  Save the function.
5. Copy function URL from Azure function (https://copy-paste-df.azurewebsites.net/api/HttpTriggerDf1) and use it in AWS lambda_function.py.

On AWS s3 storage upload a file. Logs of aws lambda func are available on CloudWatch. 
After a while verify the file appears on Azure blob storage. I tested to upload txt files and images of up to 10MB size. 

Dor Feldman
