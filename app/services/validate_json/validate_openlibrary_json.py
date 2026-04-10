import json

def validate_isbn_search(json_input):
    json_output = {}
    json_output['Author_First_Name_1'] = str(json_input.get('Author_1')).split(' ')[0]
    json_output['Author_Last_Name_1'] = str(json_input.get('Author_1')).split(' ')[-1]
    json_output['Author_1_OLID'] = str(json_input.get('Author_1_OLID')).split('/')[-1]

    if json_input.get('Author_2') is not None:
        json_output['Author_First_Name_2'] = str(json_input.get('Author_2')).split(' ')[0]
        json_output['Author_Last_Name_2'] = str(json_input.get('Author_2')).split(' ')[-1]
        json_output ['Author_2_OLID'] = str(json_input.get('Author_2_OLID')).split('/')[-1]

    json_output['Publisher_Name'] = json_input.get('Publisher')
    json_output['Publisher_OLID'] = json_input.get('Publisher_OLID')

    json_output['Publish_Year'] = json_input.get('Publish_Year')

    # If the OL data includes months or day, remove them
    if ' ' in json_input.get('Publish_Year'):
        json_output['Publish_Year'] = str(json_input.get('Publish_Year')).split(' ')[-1]
    else:
        json_output['Publish_Year'] = json_input.get('Publish_Year')

    json_output['Summary'] = json_input.get('Summary')
    json_output['Cover_Image_URL'] = json_input.get('Cover_Image_URL')

    return json_output