import boto3
import os
import botocore 

BUCKET_NAME = 'ncar-archives-pre' # replace with your bucket name
DOWN_LOAD_DIR = '/home/ec2-user/environment/chksumtmp/'
PREFIX = ''

def delete_local_file (location):

    import os
    if os.path.exists(location):
      os.remove(location)
    else:
      print("The file does not exist")

def getfilefroms3(s3_client, bucket_name, object_name, down_load_dir):

    
    import ntpath
    base_name = ntpath.basename(object_name)
    location = down_load_dir + base_name

    try:
        s3_client.download_file(bucket_name, object_name, location)
#        s3r.Bucket(bucket_name).download_file(object_name, down_load_dir + base_name)
#        print("The bucket has been downloaded.")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    else:
        print ("The file -> {0} <-has downloaded succesfully".format(location))
    return location



s3_client = boto3.client('s3', region_name='us-west-2')
paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': BUCKET_NAME,
                        'Prefix': '',
                        'PaginationConfig': {'MaxItems':20, 'PageSize' : 1000}
    
}
i = 0
j = 0
k = 0
page_iterator = paginator.paginate(**operation_parameters)
for page in page_iterator:
    for object in page['Contents']:
        key = object['Key']
        
        if not key.endswith(os.sep):
            k = k + 1
            local_file_name = getfilefroms3(s3_client, BUCKET_NAME, key, DOWN_LOAD_DIR)
            delete_local_file(local_file_name)
#            filenames.append(key)
#            FilesNotFound = False
            
    
        else:
            print()
            print("Object Key {0} ends with a slash".format(key))
            print()
            j = j + 1
        
        
#        print(key)
        i = i + 1
    print("Objects so far = {0}" .format(i))
 
print()       
print("Total objects = {0}, Total objects ending with slashes = {1}, Total objects not ending with a slash = {2}" .format(i,j,k))