VALID_ACTIONS = ["ADD", "VIEW", "DELETE","EDIT" ,"TOGGLE", "HELP", "EXIT","FILTER COMPLETED", "FILTER NOT COMPLETED"]
# ====== COMPLETED =============== # 


def filter_completed(todolist):
    filtered = (list(filter(lambda item:item["completed"], todolist["list"])))    
    return filtered

def display_filter_complete(todolist):
    check_empty_todolist(todolist)
    check_no_completed_items(todolist)           
    return display_list(filter_completed(todolist))

def check_empty_todolist(todolist):
    if len(todolist["list"])==0: print("No Todo items")


def check_completed_items(todolist):
    if (len(filter_completed(todolist)) == len(todolist["list"]) and len(todolist["list"])>0):
        print("All items have been completed")

def check_no_completed_items(todolist):
    if (len(filter_not_completed(todolist)) == 0) and len(todolist["list"])>0:
        print("No completed items")

def filter_not_completed(todolist):
    filtered = (list(filter(lambda item:item["completed"]==False, todolist["list"])))    
    return filtered

def display_filter_not_complete(todolist):
    check_empty_todolist(todolist)
    check_completed_items(todolist)           
    return display_list(filter_not_completed(todolist))    

   

def display_item(item):
    checkbox = "[x]" if item["completed"] else "[  ]"
    print(f"- {checkbox} {item['id']}: {item['task']}")


def display_list(todo_list):
    if not todo_list:        
        return

    display_item(todo_list[0])
    return display_list(todo_list[1:])


def create_item(task, id):
    return {"id": id+1, "task": task, "completed": False}


def append_to_todolist(todo_list, item):
    return {"list": todo_list["list"] + [item], "id": todo_list["id"] + 1}


def find_with_id(item_list, item_id):
    return next(item for item in item_list if item["id"] == item_id)


def remove_with_id(item_list, item_id):
    found_item = find_with_id(item_list, item_id)
    return [item for item in item_list if item["id"] != found_item["id"]]


def toggle_item(item, found_item):
    return {**item, "completed": not item["completed"]} if item["id"] == found_item["id"] else item


def toggle_list(item_list, item_id):
    found_item = find_with_id(item_list, item_id)
    return [toggle_item(item, found_item) for item in item_list]


def is_input_empty(id):
    task = input(f"[{id}] Edit Tasks: ") 
    if (task is None) or (task == "") or (task.isspace()):
        return is_input_empty(id)
    else:
        return task

def edit_item(item, found_item,new_activity):
    return {**item, "task": new_activity} if item["id"] == found_item["id"] else item

def edit_list(item_list, item_id,new_activty):
    found_item = find_with_id(item_list, item_id)
    return [edit_item(item, found_item,new_activty) for item in item_list]

def handle_edit(todo_list):
    item_id = int(input("Input ID: "))
    new_activity = is_input_empty(item_id)
    new_todo_list = {**todo_list,
                     "list": edit_list(todo_list["list"], item_id,new_activity)}
    display_list(new_todo_list["list"])
    return new_todo_list

def handle_toggle(todo_list):
    item_id = int(input("Input ID: "))
    new_todo_list = {**todo_list,
                     "list": toggle_list(todo_list["list"], item_id)}
    display_list(new_todo_list["list"])
    return new_todo_list

def handle_completed(todo_list):
    display_filter_complete(todo_list)
    return todo_list

def handle_not_completed(todo_list):
    display_filter_not_complete(todo_list)
    return todo_list


def handle_delete(todo_list):
    item_id = int(input("Item ID: "))
    new_todo_list = {**todo_list,
                     "list": remove_with_id(todo_list["list"], item_id)}
    display_list(new_todo_list["list"])
    return new_todo_list

def handle_add(todo_list):
    item = input("New Todo Item: ")
    item = create_item(item, todo_list["id"])
    new_todo_list = append_to_todolist(todo_list, item)
    display_list(new_todo_list["list"])

    return new_todo_list

def handle_view(todo_list):
    display_list(todo_list["list"])
    return todo_list


def get_action():
    
    action = input("What would you like to do? - ")

    if action.upper() not in VALID_ACTIONS:
        raise ValueError(f"Action '{action}' is invalid.")

    return action


def perform_action(action, todo_list):
    if action.upper() not in VALID_ACTIONS:
        raise ValueError(f"Action '{action}' is invalid.")
    
    if action.upper() in ["EDIT","TOGGLE","DELETE","VIEW"] and len(todo_list["list"])==0:
        raise ValueError("No todo items")



    action_handlers = {"ADD": handle_add, "VIEW": handle_view,
                        "EDIT":handle_edit, "DELETE": handle_delete,"TOGGLE": handle_toggle, 
                       "FILTER COMPLETED":handle_completed,
                       "FILTER NOT COMPLETED":handle_not_completed
                       }
    handle_action = action_handlers.get(action.upper(), lambda x: x)

    return handle_action(todo_list)


def activate_todolist(todo_list):
    try:
        action = get_action()

        if action.upper() == "EXIT":
            return 0

        todo_list = perform_action(action, todo_list)
        return activate_todolist(todo_list)
    except ValueError as value_error:
        print(value_error)
        return activate_todolist(todo_list)


def main():
    todo_list = {"list": [], "id": 0}
    activate_todolist(todo_list)

    return 0


if __name__ == '__main__':
    main()
