import os
 # Environment Variables to Handle Local and Production
app_name = os.getenv('appName')
environment = os.getenv('environment')
baseurl = os.getenv('baseurl')
dynamo_project_table_name = os.getenv('dynamotablename')
dynamo_subproject_table_name=os.getenv('dynamosubprojecttable')

Project_keySchema_body = [
            {
                'AttributeName': 'projectid',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'email',
                'KeyType': 'RANGE'
            }
        ]
Project_attributeDefinitions_body = [
            {
                'AttributeName': 'projectid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }

        ]

Subproject_keySchema_body = [
            {
                'AttributeName': 'projectid',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'subprojectid',
                'KeyType': 'RANGE'
            }
        ]
Subproject_attributeDefinitions_body = [
            {
                'AttributeName': 'projectid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'subprojectid',
                'AttributeType': 'S'
            }

        ]