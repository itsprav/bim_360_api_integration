import re


def get_subtype_id(issue_types, issue_type_name):
    if 'results' in issue_types:
        for result in issue_types['results']:
            if 'subtypes' in result:
                for subtype in result['subtypes']:
                    if subtype['title'] == issue_type_name and subtype['isActive']:
                        return subtype['id']
    return None


def get_issue_attribute_definitions_option_id(issue_attribute_definitions, title, option_val):
    results = issue_attribute_definitions.get('results', [])
    for result in results:
        if result.get('title') == title:
            options = result.get('metadata', {}).get('list', {}).get('options', [])
            for option in options:
                if option.get('value') == option_val:
                    return option.get('id')
    return None


def get_issue_attribute_definitions_id(issue_attribute_definitions, title):
    results = issue_attribute_definitions.get('results', [])
    for result in results:
        if result.get('title') == title:
            return result.get('id')
    return None


def get_subtype_ids(issue_types, issue_type_names):
    subtype_ids = []
    if 'results' in issue_types:
        for result in issue_types['results']:
            if 'subtypes' in result:
                for subtype in result['subtypes']:
                    for issue_type_name in issue_type_names:
                        if subtype['title'] == issue_type_name:
                            subtype_ids.append(subtype['id'])

    if len(subtype_ids) != 0:
        print("------------subtypes Found----------")
        return subtype_ids
    else:
        print("--------------No subtype Found-------------")
        return None


# Get project_id from link by regex
def get_project_id(issue_link):
    pattern = r"projects/(\w+)/issues#preview=(\w+)"
    match = re.search(pattern, issue_link)
    if match:
        project_id = match.group(1)

        # if we want to get issue_id then uncomment next line
        # issue_id = match.group(2)

        return project_id
    else:
        return None
