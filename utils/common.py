import json


def load_robot_data(reponse):
    data_formatted = reponse.content.replace(b"'", b'"')

    return json.loads(data_formatted)