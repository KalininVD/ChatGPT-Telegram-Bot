# Import necessary modules, classes and functions
from decimal import Decimal
from boto3 import Session
from boto3.dynamodb.conditions import Key

# Define environment variables
ACCESS_KEY_ID: str | None = None
SECRET_ACCESS_KEY: str | None = None
DOCAPI_ENDPOINT: str | None = None

# Initialize environment variables
def InitEnvVars(vars: dict):
    global ACCESS_KEY_ID, SECRET_ACCESS_KEY, DOCAPI_ENDPOINT
    
    ACCESS_KEY_ID = vars.get('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = vars.get('SECRET_ACCESS_KEY')
    DOCAPI_ENDPOINT = vars.get('DOCAPI_ENDPOINT')

# Define service variables
boto_session = None
docapi_table = None

# Query to the database for finding user's information
def query_find(user_id: Decimal, user_name: str) -> dict | None:
    table = _get_docapi_table()

    response = table.get_item(
        Key = {
            'user_id': user_id,
            'user_name': user_name
        }
    )

    return response

# Query to the database for searching for users' information by the specified role
def query_search(user_role: str):
    table = _get_docapi_table()

    scan_kwargs = {
        'FilterExpression': Key('info.user_role').eq(user_role),
        'ProjectionExpression': "user_id, user_name, info.user_role, info.language, info.chat_model, info.remaining_budget"
    }

    users = []

    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        response = table.scan(**scan_kwargs)
        users += response.get('Items', [])

        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    return {'Items': users}

# Query to the database for inserting data about new user
def query_insert(user_id: Decimal, user_name: str, user_role: str, language: str, chat_model: str, remaining_budget: Decimal):
    table = _get_docapi_table()

    response = table.put_item(
        Item = {
            'user_id': user_id,
            'user_name': user_name,
            'info': {
                'user_role': user_role,
                'language': language,
                'chat_model': chat_model,
                'remaining_budget': remaining_budget
            }
        }
    )

    return response

# Query to the database for updating user's information
def query_update(user_id: Decimal, user_name: str, user_role: str, language: str, chat_model: str, remaining_budget: Decimal):
    table = _get_docapi_table()

    response = table.update_item(
        Key = {
            'user_id': user_id,
            'user_name': user_name
        },
        UpdateExpression = "set info.user_role = :r, info.language = :l, info.chat_model = :m, info.remaining_budget = :b",
        ExpressionAttributeValues = {
            ':r': user_role,
            ':l': language,
            ':m': chat_model,
            ':b': remaining_budget
        },
        ReturnValues = "UPDATED_NEW"
    )

    return response

# Query to the database for deleting user's information
def query_delete(user_id: Decimal, user_name: str):
    table = _get_docapi_table()
    
    response = table.delete_item(
        Key = {
            'user_id': user_id,
            'user_name': user_name
        }
    )

    return response

# Service method for initializing docapi table (table from YDB database)
def _get_docapi_table():
    global docapi_table
    if docapi_table is not None:
        return docapi_table

    docapi_table = _get_boto_session().resource(
        'dynamodb',
        endpoint_url=DOCAPI_ENDPOINT,
        region_name='ru-central1'
    ).Table('users')

    return docapi_table

# Service method for initializing boto session
def _get_boto_session() -> Session:
    global boto_session
    if boto_session is not None:
        return boto_session

    boto_session = Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )

    return boto_session