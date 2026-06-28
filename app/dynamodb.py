import boto3
import logging
import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DynamoDB resource.
# AWS credentials will be loaded automatically from the environment or EC2 IAM Role.
# In local development, you should configure AWS CLI or set standard AWS environment variables.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_url_cache(short_code: str):
    """
    Retrieves the original URL from the url-cache DynamoDB table.
    """
    table = dynamodb.Table('url-cache')
    try:
        response = table.get_item(Key={'short_code': short_code})
        if 'Item' in response:
            logger.info(f"DynamoDB Cache Hit for short code: {short_code}")
            return response['Item']['original_url']
        logger.info(f"DynamoDB Cache Miss for short code: {short_code}")
        return None
    except ClientError as e:
        logger.error(f"Error fetching from DynamoDB url-cache: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching from DynamoDB url-cache: {e}")
        return None

def save_url_cache(short_code: str, original_url: str) -> bool:
    """
    Caches the short_code and original_url in the url-cache DynamoDB table.
    """
    table = dynamodb.Table('url-cache')
    try:
        table.put_item(
            Item={
                'short_code': short_code,
                'original_url': original_url,
                'created_at': datetime.utcnow().isoformat()
            }
        )
        logger.info(f"Cached short code {short_code} in DynamoDB successfully.")
        return True
    except ClientError as e:
        logger.error(f"Error putting item into DynamoDB url-cache: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error putting item into DynamoDB url-cache: {e}")
        return False

def record_click_analytics(short_code: str, ip_address: str, user_agent: str) -> bool:
    """
    Saves click information into the click-analytics DynamoDB table.
    Uses expires_at attribute for TTL (auto-deletes after 90 days).
    """
    table = dynamodb.Table('click-analytics')
    try:
        now = datetime.utcnow()
        # Calculate TTL (90 days from now in Unix epoch seconds)
        expires_at = int(time.time() + (90 * 24 * 60 * 60))
        
        table.put_item(
            Item={
                'short_code': short_code,
                'clicked_at': now.isoformat(),
                'ip_address': ip_address or 'Unknown',
                'user_agent': user_agent or 'Unknown',
                'expires_at': expires_at
            }
        )
        logger.info(f"Recorded click analytics for {short_code} in DynamoDB click-analytics.")
        return True
    except ClientError as e:
        logger.error(f"Error writing to DynamoDB click-analytics: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error writing to DynamoDB click-analytics: {e}")
        return False
