import json


def load_robot_data(response):
    data_formatted = response.content.replace(b"'", b'"')
    data_unnulled = data_formatted.replace(b"None", b"null")
    print(data_unnulled)
    return json.loads(data_unnulled)