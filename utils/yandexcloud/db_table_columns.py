from typing import TypedDict, Literal


# Class for representing a DynamoDB table's partition key
class PartitionKey(TypedDict):
    AttributeName: str
    KeyType: Literal['HASH']


# Class for representing a DynamoDB table's attribute
class Attribute(TypedDict):
    AttributeName: str
    AttributeType: Literal['S', 'N', 'B']