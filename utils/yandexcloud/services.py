from logging import Logger
from boto3 import Session

import utils.yandexcloud.user_management

# Define environment variables
access_key_id: str | None = None
secret_access_key: str | None = None
docapi_endpoint: str | None = None

# Define services
logger: Logger
boto_session: Session
docapi_database = None

# Initialize environment variables
def InitEnvVars(yc_access_key_id: str | None = None, yc_secret_access_key: str | None = None, yc_docapi_endpoint: str | None = None):
    if yc_access_key_id is None or yc_secret_access_key is None or yc_docapi_endpoint is None:
        raise ValueError("Yandex Cloud Access Key ID, Secret Access Key, and Docapi Endpoint must be provided")

    global access_key_id, secret_access_key, docapi_endpoint
    
    access_key_id = yc_access_key_id
    secret_access_key = yc_secret_access_key
    docapi_endpoint = yc_docapi_endpoint

# Setup logger
def SetupLogger(external_logger: Logger):
    global logger

    logger = external_logger
    utils.yandexcloud.user_management.logger = logger


# Service method for initializing boto session and docapi database
def InitServices():
    global boto_session, docapi_database

    if docapi_database is not None:
        return

    if access_key_id is None or secret_access_key is None:
        raise ValueError("Access Key ID or Secret Access Key from Yandex Cloud Service Account is not set")

    boto_session = Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    if docapi_endpoint is None:
        raise ValueError("Docapi Endpoint is not set")

    docapi_database = boto_session.resource(
        service_name='dynamodb',
        endpoint_url=docapi_endpoint,
        region_name='ru-central1',
    )

    utils.yandexcloud.user_management.user_settings_table = docapi_database.Table('user_settings')

    logger.info("Successfully initialized Yandex Cloud Services")