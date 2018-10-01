import boto3, json, sys
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from chalicelib import logging

logger = logging.setup_custom_logger()
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
boto_key = boto3.dynamodb.conditions.Key 
boto_attr = boto3.dynamodb.conditions.Attr

def create_project_table(table_name, keySchema_body, attributeDefinitions_body):
    # Create the DynamoDB table.
    logger.info("--------CREATING TABLE------------")
    try:
        table = dynamodb.create_table(
            TableName= table_name,
            KeySchema= keySchema_body,
            AttributeDefinitions= attributeDefinitions_body,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        logger.info("table", table_name)
        table.meta.client.get_waiter('project table_exists').wait(TableName=table_name)
        #print out some data about the table.
        logger.info("table item count:",table.item_count)
        logger.info("Table status:", table.table_status)
    
    except Exception as e:
        logger.error(e)
        pass

def create_subproject_table(table_name, keySchema_body, attributeDefinitions_body):
    # Create the DynamoDB table.
    logger.info("--------CREATING SUBPROJECT TABLE------------")
    try:
        table = dynamodb.create_table(
            TableName= table_name,
            KeySchema= keySchema_body,
            AttributeDefinitions= attributeDefinitions_body,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        logger.info("table", table_name)
        table.meta.client.get_waiter('subproject table_exists').wait(TableName=table_name)
        #print out some data about the table.
        logger.info("table item count:",table.item_count)
        logger.info("Table status:", table.table_status)
    
    except Exception as e:
        logger.error(e)
        pass


def delete_table(table_name):
    logger.info("--------DELETING TABLE------------")
    table = dynamodb.Table(table_name)
    table.delete()
    logger.info("TABLE DELETED")
    return "TABLE DELETED"
        
def add_doc(table_name, data):
    logger.info("--------CREATING ITEM------------")
    table = dynamodb.Table(table_name)
    logger.info("Adding", data, "to", table_name)
    try:
        table.put_item(
            TableName=table_name,
            Item=data
        )
        logger.info("Added")
        return data
    except Exception as e:
        logger.error("error occured", e)
        return e

def get_doc(table_name):
    logger.info("--------QUERYING ALL ITEM------------")
    table = dynamodb.Table(table_name)
    logger.info("querying all data")
    try:
        response = table.scan()
        logger.info("response is", response)
        if 'Items' in response:
            return response['Items']
        else:
            return response
    except Exception as e:
        logger.error("an error occured", e)
        return e

def get_single_doc(table_name, param):
    logger.info("--------QUERYING SINGLE RECORD------------") 
    table = dynamodb.Table(table_name)
    try:
        response = table.query(KeyConditionExpression=Key('projectid').eq(param))
        logger.info('--', response)
        if 'Items' in response:
            item = response['Items']
            return item
        else:
            return "No Item found for id"
    except Exception as e:
        logger.error("error", e)
        return e

def get_all_sub_doc(table_name, projectid):
    table = dynamodb.Table(table_name)
    logger.info("-------------QUERYING ALL SUBPROJECT------------")
    try:
        response = table.query(KeyConditionExpression=Key('projectid').eq(projectid))
        logger.info('--', response)
        if 'Items' in response:
            item = response['Items']
            return item
        else:
            return "No Item found for id"
    except Exception as e:
        logger.error("error", e)
        return e    

def get_single_sub_doc(table_name, projectid, subprojectid):
    logger.info("--------QUERYING SINGLE SUBPROJECT RECORD------------") 
    table = dynamodb.Table(table_name)     
    logger.info("-------------QUERYING BY SUBPROJECTID------------")
    try:
        response = table.query(KeyConditionExpression=Key('projectid').eq(projectid) & Key('subprojectid').eq(subprojectid))
        logger.info('--', response)
        if 'Items' in response:
            item = response['Items']
            return item
        else:
            return "No Item found for id"
    except Exception as e:
        logger.error("error", e)
        return e
        

def update_doc(table_name, key_id, data):
    logger.info("--------UPDATING ITEM RECORD------------", data)
    table = dynamodb.Table(table_name)
    try:
        table.update_item(
            Key= key_id,
            UpdateExpression='SET projectname = :projectname, updatedBy =:email, description =:description, giturl =:giturl',
            ExpressionAttributeValues={
                ':projectname': data["projectname"],
                ':email': data["updatedBy"],
                ':description': data["description"],
                ':giturl': data["giturl"]
            },
            ReturnValues = "ALL_NEW"
        )
        logger.info("UPDATED")
        # Then get back updated value
        response = table.query(KeyConditionExpression=Key('projectid').eq(key_id["projectid"]))
        if 'Items' in response:
            item = response['Items']
            return item
        else:
            return response
    except Exception as e:
        logger.error(e)
        return e   

def delete_doc(table_name, key_id, striker):
    logger.info("--------DELETING ITEM------------")
    table = dynamodb.Table(table_name)
    try:
        response = table.query(KeyConditionExpression=Key('projectid').eq(key_id))
        if 'Items' in response and response["Count"] != 0:
            logger.info("Project exists....deleting project")
            data = response["Items"]
            email = data[0]["email"]
            table.delete_item(
                Key={
                    'projectid': key_id,
                    'email': email
                }
            )
            logger.info("DELETED by", striker)
            return ("DELETED! action performed by", striker)
        return "UNABLE TO DELETE! This item does not exist"
    except Exception as e:
        logger.error(e)
        return e