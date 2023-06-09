import configparser

import pandas as pd

import api
import utils
import json


def get_filepath_to_process():
    config = configparser.ConfigParser()
    config.read('config.ini')
    file_name = config.get('Parameters', 'FileName')
    return file_name


def call_api():
    specific_df = read_desired_columns_from_input_file()
    issue_types_master_list = api.get_issue_types()
    issue_attribute_definitions = api.get_issue_attribute_definitions()
    print(issue_attribute_definitions)
    defect_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions, "Defect")
    issue_type_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions, "Issue Type")
    production_line_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions,
                                                                            "Production Line")
    station_number_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions,
                                                                           "Station Number")
    man_hours_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions,
                                                                      "Man Hours")
    what_attribute_id = utils.get_issue_attribute_definitions_id(issue_attribute_definitions,
                                                                 "What")
    # Station Number, Man Hours, What are not there in Excel
    status = []
    reason = []

    for index, row in specific_df.iterrows():
        issue_subtype_id = utils.get_subtype_id(issue_types_master_list, row["Subtype"])
        defect_option_id = utils.get_issue_attribute_definitions_option_id(issue_attribute_definitions, "Defect",
                                                                           row["Defect"])
        issue_type_option_id = utils.get_issue_attribute_definitions_option_id(issue_attribute_definitions,
                                                                               "Issue Type", row["Issue Type"])
        production_line_option_id = utils.get_issue_attribute_definitions_option_id(issue_attribute_definitions,
                                                                                    "Production Line",
                                                                                    row["Production Line"])
        station_number_option_id = utils.get_issue_attribute_definitions_option_id(issue_attribute_definitions,
                                                                                   "Station Number", "01")
        what_option_id = utils.get_issue_attribute_definitions_option_id(issue_attribute_definitions,
                                                                         "What", "Other")
        payload = json.dumps({
            "issueSubtypeId": f"{issue_subtype_id}",
            "customAttributes": [
                {
                    "attributeDefinitionId": f"{issue_type_attribute_id}",
                    "value": f"{issue_type_option_id}"
                },
                {
                    "attributeDefinitionId": f"{defect_attribute_id}",
                    "value": f"{defect_option_id}"
                },
                {
                    "attributeDefinitionId": f"{production_line_attribute_id}",
                    "value": f"{production_line_option_id}"
                },
                {
                    "attributeDefinitionId": f"{station_number_attribute_id}",
                    "value": f"{station_number_option_id}"
                },
                {
                    "attributeDefinitionId": f"{man_hours_attribute_id}",
                    "value": ""
                },
                {
                    "attributeDefinitionId": f"{what_attribute_id}",
                    "value": f"{what_option_id}"
                }
            ]
        })
        updated_issue, res = api.update_project_issue(row["issue_id"], payload)
        print(res)
        status.append(res.status)
        reason.append(res.reason)

    specific_df['Status'] = status
    specific_df['Comments'] = reason
    specific_df.to_csv('output.csv', index=False)


def read_desired_columns_from_input_file():
    file_path = get_filepath_to_process()
    input_df = pd.read_excel(file_path)
    desired_columns = ["issue_id", "Production Line", "Type", "Subtype", "Defect", "Issue Type"]
    specific_df = input_df[desired_columns]
    return specific_df


call_api()
