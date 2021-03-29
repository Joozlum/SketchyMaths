def load_text(text_to_load):
    app_directory = r'sketchymaths/sketchymathsapp'
    if text_to_load == 'guide':
        app_directory += r'/Guide.txt'
    elif text_to_load == 'methods':
        app_directory += r'/Methods.txt'
    else:
        return "Text not found!"
    with open(app_directory, 'r') as loaded_file:
        loaded_text = loaded_file.read()
    return loaded_text
