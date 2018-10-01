import os 
from chalice import Chalice, Response, BadRequestError, NotFoundError
from chalicelib import config, dynamoHelper
import json, uuid
from datetime import datetime
from bson.json_util import dumps


app = Chalice(app_name='Andromeda Project Service')
dynamo_project_table_name = config.dynamo_project_table_name
dynamo_subproject_table_name = config.dynamo_subproject_table_name

dynamoHelper.create_project_table(dynamo_project_table_name, config.Project_keySchema_body, config.Project_attributeDefinitions_body)
dynamoHelper.create_subproject_table(dynamo_subproject_table_name, config.Subproject_keySchema_body, config.Subproject_attributeDefinitions_body)


@app.route('/')
def rootroute():
    return {'response': 'Andromeda Project Service'}

@app.route('/project', methods=['POST'])
def createproject():
    data = app.current_request.json_body
    projectid = str(uuid.uuid4().hex)
    projectname = data['projectname'] if "projectname" in data else None
    description = data['description'] if "description" in data else None
    striker = data['striker'] if "striker" in data else None
    giturl = data['giturl'] if "giturl" in data else None
    created = datetime.now().replace(microsecond=0).isoformat() 

    if not projectname or projectname is None:
        raise BadRequestError("No Project Name Inputted")

    if not description or description is None:
        raise BadRequestError("No Project Description Inputted")

    if not striker or striker is None:
        raise BadRequestError('No Striker Inputted')

    if not giturl or giturl is None:
        raise BadRequestError('No Git URL Inputted')

    project = {'projectid': projectid, 'projectname': projectname, 'description':description, 'email':striker, 'giturl':giturl, 'created':created}
    res = dynamoHelper.add_doc(dynamo_project_table_name, project)
    return Response(
        body={ 'response':'Successfully saved', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}/subproject', methods=['POST'])
def createsubproject(projectid):
    i = app.current_request.json_body
    subprojectid = str(uuid.uuid4().hex)
    subname = i['name'] if "name" in i else None
    description = i['description'] if "description" in i else None
    striker = i['striker'] if "striker" in i else None
    giturl = i['giturl'] if "giturl" in i else None
    created = datetime.now().replace(microsecond=0).isoformat()

    if not projectid or projectid is None:
        raise BadRequestError("Please supply project ID")
    if not striker or striker is None:
        raise BadRequestError("Please supply striker email")
    if not subname or subname is None:
        raise BadRequestError('No Sub-Project Name Inputted')
    if not description or description is None:
        raise BadRequestError('No Description Inputted')
    if not giturl or giturl is None:
        raise BadRequestError('No Git URL Inputted')
        
    subproject = {"projectid":projectid, "subprojectid":subprojectid, "name":subname, "email": striker, "description":description,"giturl":giturl, "created-on":created}
    res = dynamoHelper.add_doc(dynamo_subproject_table_name, subproject)
    return Response(
        body={ 'response':'SubProject Created for %s' % projectid, 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )
    
@app.route('/project')
def getprojects():
    res = dynamoHelper.get_doc(dynamo_project_table_name)
    return Response(
        body={ 'response':'Successfully returned all projects', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}')
def findproject(projectid):
    param = projectid
    res = dynamoHelper.get_single_doc(dynamo_project_table_name, param)
    return Response(
        body={ 'response':'Successfully returned response', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}/subproject')
def findsubproject(projectid):
    res = dynamoHelper.get_all_sub_doc(dynamo_subproject_table_name, projectid)
    return Response(
        body={ 'response':'Successfully returned response', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )


@app.route('/project/{projectid}/subproject/{subprojectid}')
def findsubproject(projectid, subprojectid):
    res = dynamoHelper.get_single_sub_doc(dynamo_subproject_table_name, projectid, subprojectid)
    return Response(
        body={ 'response':'Successfully returned response', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}/subproject/{subprojectid}/{email}', methods=['DELETE'])
def deletesubproject(subprojectid, email):
    if not subprojectid or subprojectid is None:
        raise BadRequestError("Please supply Project ID")
    if not email or email is None:
        raise BadRequestError("Please supply Email of striker")
    res = dynamoHelper.delete_doc(dynamo_subproject_table_name, subprojectid, email)
    return Response(
        body={ 'response':'Successfully returned response', 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}/{email}', methods=['DELETE'])
def deleteproject(projectid, email):
    if not projectid or projectid is None:
        raise BadRequestError("Please supply Project ID")
    if not email or email is None:
        raise BadRequestError("Please supply Email of striker")
    res = dynamoHelper.delete_doc(dynamo_project_table_name, projectid, email)
    return Response(
        body={ 'response':'Successfully deleted project with id %s' % projectid, 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/project/{projectid}/{email}', methods=['PATCH'])
def updateproject(projectid, email):
    i = app.current_request.json_body
    projectname = i['projectname'] if "projectname" in i else None
    description = i['description'] if "description" in i else None
    striker = i['striker'] if "striker" in i else None
    giturl = i['giturl'] if "giturl" in i else None
    updated = datetime.now().replace(microsecond=0).isoformat()

    if projectid is None:
        raise BadRequestError('No Project ID Specified')
    if email is None:
        raise BadRequestError('No Project Email Specified')
    Key={
        'projectid': projectid,
        'email': striker
    }
    project = {'projectid': projectid, 'projectname': projectname, 'description':description, 'updatedBy':email, 'giturl':giturl, 'updated':updated}
    res = dynamoHelper.update_doc(dynamo_project_table_name, Key, project)
    return Response(
        body={ 'response':'Successfully updated project with id: %s' % projectid, 'message':res },
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )