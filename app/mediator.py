# Module to mediate calls from the frontend and backend
# Will take JSON from frontend and call relevant query functions and return the result as JSON to frontend

# POST - Takes JSON as input
def create(json):
    # Can directly get values from keys
    number_of_chapters = json['chapters']
    # So just focus on parsing all json values from the book JSON and validating them
    # i.e. ISBN should be 13 numbers, etc.

    # Just demonstrating, can remove this
    return number_of_chapters


# GET - Takes JSON as input
def read(json):
    return str(json)


# PATCH - Takes JSON as input
def update(json):
    return str(json)


# DELETE - Takes JSON as input
def delete(json):
    return str(json)
