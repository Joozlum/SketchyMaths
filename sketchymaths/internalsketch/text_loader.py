from os import getcwd

def load_text(text_to_load):
    path = getcwd().split('\\')
    path_length = len(path)
    root_directory_for_app = None
    for x in range(path_length):
        if 'sketchymaths' in path[x].lower():
            root_directory_for_app = path[0:x+1]

    root_directory_for_app.append('sketchymaths')
    root_directory_for_app.append('internalsketch')

    if text_to_load == 'guide':
        root_directory_for_app.append('Guide.txt')
    elif text_to_load == 'methods':
        root_directory_for_app.append('Methods.txt')
    else:
        return "Text not found!"

    with open('\\'.join(root_directory_for_app), 'r') as loaded_file:
        loaded_text = loaded_file.read()

    return loaded_text
