import json
import uuid
import datetime
import boto3


def lambda_handler(event, context):
    body = json.loads(event['body'])
    job_name = body['job_name']
    job_creator = body['job_creator']
    client_id = body['client_id']
    description = body['description']
    # Generate a unique job id
    job_id = str(uuid.uuid4())
    # Create a job ticket as Python dictionary
    job_ticket = {
        'job_id': job_id,
        'job_name': job_name,
        'job_creator': job_creator,
        'client_id': client_id,
        'description': description,
        'status': 'pending',
        'created_at': str(datetime.datetime.now()),
        'updated_at': str(datetime.datetime.now())
    }
    # Convert the job ticket to JSON
    job_ticket_json = json.dumps(job_ticket)
    # Save the job ticket in S3
    s3_client = boto3.client('s3')
    filename = f'job-tickets/{job_id}.json'
    s3_client.put_object(Body=job_ticket_json,
                         Bucket='jobtickets', Key=filename)
    # Generate a presigned URL for the job ticket
    presign_url = s3_client.generate_presigned_url('get_object', Params={
                                                   'Bucket': 'jobtickets', 'Key': filename}, ExpiresIn=3600)
    # Return the job ticket and URL to the client
    return {
        'statusCode': 200,
        'body': json.dumps(f'Job ticket created successfully. The new job ID is: {job_id}'),
        'headers': {'Content-Type': 'application/json'}
    }
