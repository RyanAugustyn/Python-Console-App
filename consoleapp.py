import requests, json

#functions 

#functions for entire list
def get_all():
    response = requests.get('http://127.0.0.1:5000/api/trees')
    tree_dicts = response.json()
    print(tree_dicts)
    return tree_dicts, 200

def post():
    name = input("Please enter a tree name\n")
    type = input("please enter a type of tree\n")
    tree_dict = {'name' : name, 'type' : type}
    response = requests.post('http://127.0.0.1:5000/api/trees', json=tree_dict)
    print(f'Added {tree_dict} to database')
    return response, 201

#functions for individual entries
def get(tree_id): 
    response = requests.get(f'http://127.0.0.1:5000/api/trees/{tree_id}')
    tree_dict = response.json()
    print(tree_dict)
    return tree_dict

def put(tree_id):
    response = requests.get(f'http://127.0.0.1:5000/api/trees/{tree_id}')
    response_dict = response.json()
    name = input("Please enter a new tree name, or 'none' to keep the same\n")
    type = input("please enter a new type of tree, or 'none' to keep the same\n")
    if name == 'none': 
        name = response_dict.get('name')
    if type == 'none':
        type = response_dict.get('type')
    tree_dict = {'name' : name, 'type' : type}
    response = requests.put(f'http://127.0.0.1:5000/api/trees/{tree_id}', json=tree_dict)
    print(f'Updated at id {tree_id} with {response}')
    return response, 201

def delete(tree_id):
    requests.delete(f'http://127.0.0.1:5000/api/trees/{tree_id}')
    print(f'Tree at id #{tree_id} has been deleted\n')
    return '', 204


def run_program():
    choice = 0 
    while choice != 6:
        choice = int(input("""Please choose from the following options: 
    1 to retrieve everything from the database
    2 to get a particular entry by id
    3 to post a new tree
    4 to update an existing tree
    5 to delete an existing three
    6 to exit\n"""))
        if choice == 1:
            get_all()
        if choice == 2:
            tree_choice = int(input("Which tree ID would you like to retrieve?\n"))
            get(tree_choice)
        if choice == 3:
            post()
        if choice == 4:
            tree_choice = int(input("Which tree ID would you like to modify?\n"))
            put(tree_choice)
        if choice == 5:
            tree_choice = int(input("Which tree ID would you like to delete?\n"))
            delete(tree_choice)
        if choice == 6:
            print("Exiting program...")
            choice = 6


###START PROGRAM###

run_program()
