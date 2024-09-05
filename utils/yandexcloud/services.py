from logging import Logger
from decimal import Decimal
from boto3 import Session

import utils.yandexcloud.conversation_management
import utils.yandexcloud.user_management
from utils.yandexcloud.db_table_columns import PartitionKey, Attribute

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
    utils.yandexcloud.conversation_management.logger = logger


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

# Service method for checking if a table exists
def DoesTableExist(table_name: str) -> bool:
    if docapi_database is None:
        InitServices()
    
    return table_name in map(lambda table: table.name, docapi_database.tables.all())

# Service method for creating a new table
def CreateNewTable(table_name: str):
    table = docapi_database.create_table(
        TableName=table_name,
        KeySchema=[PartitionKey(AttributeName='id', KeyType='HASH')],
        AttributeDefinitions=[
            Attribute(AttributeName='id', AttributeType='N'),
            Attribute(AttributeName='message_type', AttributeType='S'),
            Attribute(AttributeName='user_role', AttributeType='S'),
            Attribute(AttributeName='content', AttributeType='S'),
        ],
    )

    logger.info(f"Successfully created new table '{table_name}' in the database")

    return table

# Service method for deleting a table
def DeleteTable(table_name: str, table = None):
    if not DoesTableExist(table_name):
        return
    
    if table is None:
        table = docapi_database.Table(table_name)
    table.delete()

    logger.info(f"Successfully deleted table '{table_name}'")

# Service method for getting a table for the specified chat ID
def GetTable(chat_id: int | Decimal | str):
    table_name = str(chat_id)

    if DoesTableExist(table_name):
        return docapi_database.Table(table_name)
    
    return CreateNewTable(table_name)