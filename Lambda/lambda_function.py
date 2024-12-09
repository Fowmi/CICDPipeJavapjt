import boto3
def get_volume_id_from_arn(volume_arn):
    # Ensure the ARN is valid and contains "volume/"
       return volume_arn.split(":")[5].split("/")[1] if "volume/" in volume_arn and len(volume_arn.split(":")) > 5 else ""

def lambda_handler(event, context):
    # Extract the volume ARN from the event
    volume_arn = event['resources'][0]
    # Get the volume ID from the ARN
    volume_id = get_volume_id_from_arn(volume_arn)
    
    if not volume_id:
        return {
            "statusCode": 400,
            "message": "Invalid ARN or volume ID not found."
        }
    
    # Initialize EC2 client
    # https://www.youtube.com/watch?v=DgavixR_w5Y&t=1190s
    ec2_client = boto3.client('ec2')
    try:
        # Modify the volume
        response = ec2_client.modify_volume(
            VolumeId=volume_id,
            VolumeType="gp3"
        )
        return {
            "statusCode": 200,
            "message": "Volume modified successfully",
            "response": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"Failed to modify volume: {str(e)}"
        }
