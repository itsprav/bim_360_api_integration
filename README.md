# bim_360_api_integration
BIM 360 API Integration  

# Update Project Issue using BIM 360 API

This project include python code to connect to BIM 360 API's to update project issues based on issue_id and project_id reading issue data from Excel.

# How to run ? 

## Prerequisites
* Python 3
* Update config.ini with correct file path (Excel having Issue Data), Authorization token and containerId  

## How to run the program ? 
* Install dependencies using `pip install -r requirements.txt` 
* Run the program using `python main.py`

## Required columns in input file

* Issue Link
* issue_id
* Production Line
* Type
* Subtype
* Defect
* Issue Type
