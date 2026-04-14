from app.services.Mediator.mediator_create import mediator_create
from app.services.Mediator.mediator_delete import mediator_delete
from app.services.Mediator.mediator_read import mediator_read
from app.services.Mediator.mediator_update import mediator_update

SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

# POST - Takes JSON as input
def create(json_input, create_type):
   return mediator_create(json_input, create_type)

# GET - Takes JSON as input
def read(json_input=None, read_type='book-all', filter_json=None):
    return mediator_read(json_input, read_type, filter_json)


# PATCH - Takes JSON as input
def update(json_input, update_type):
    return mediator_update(json_input, update_type)


# DELETE - Takes JSON as input
def delete(json_input, delete_type):
    return mediator_delete(json_input, delete_type)



if __name__ == '__main__':
    #main()
    pass