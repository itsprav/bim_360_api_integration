import http.client
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

authorization_token = config.get('Parameters', 'AuthorizationToken')

file_name = config.get('Parameters', 'FileName')

containerId = config.get('Parameters', 'containerId')


def get_issue_types():
    conn = http.client.HTTPSConnection("developer.api.autodesk.com")
    payload = ''
    headers = {
        'Authorization': f"Bearer {authorization_token}"
    }
    conn.request("GET", f"/issues/v2/containers/{containerId}/issue-types?include=subtypes",
                 payload, headers)
    res = conn.getresponse()
    return json.loads(res.read().decode('utf-8'))


def get_issue_attribute_definitions():
    conn = http.client.HTTPSConnection("developer.api.autodesk.com")
    payload = ''
    headers = {
        'Authorization': f"Bearer {authorization_token}"
    }
    conn.request("GET", f"/issues/v2/containers/{containerId}/issue-attribute-definitions",
                 payload, headers)
    res = conn.getresponse()
    return json.loads(res.read().decode('utf-8'))


def update_project_issue(issue_id, payload):
    conn = http.client.HTTPSConnection("developer.api.autodesk.com")
    print(payload)
    headers = {
        'Authorization': f"Bearer {authorization_token}",
        'Content-Type': 'application/json'
    }
    conn.request("PATCH", f"/issues/v2/containers/{containerId}/issues/{issue_id}", payload,
                 headers)
    res = conn.getresponse()
    return json.loads(res.read().decode('utf-8')), res
