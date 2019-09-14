appearance_settings_json = '''
[
  {
    "type": "string",
    "title": "To Set Colors:",
    "desc": "Colors are displayed from RGB values.  To set them, enter a value as %red, %green, %blue.  Percents are decimal values (between 0 and 1).",
    "section": "Appearance",
    "key": "color_example",
    "disabled": "True"
  },
  {
    "type": "string",
    "title": "Evaluated Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Appearance",
    "key": "text_color_main"
  },
  {
    "type": "string",
    "title": "Unevaluated Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Appearance",
    "key": "text_color_faded"
  },
  {
    "type": "string",
    "title": "Variable Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Appearance",
    "key": "text_color_variable"
  },
  {
    "type": "string",
    "title": "Arrow Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Appearance",
    "key": "arrow_color"
  },
  {
    "type": "numeric",
    "title": "Arrow Transparency",
    "desc": "How dark the arrows get drawn, between 0-1",
    "section": "Appearance",
    "key": "arrow_transparency"
  },
  {
    "type": "string",
    "title": "Comment Color",
    "desc": "RGB values in x, x, x format",
    "section": "Appearance",
    "key": "comment_color"
  },
  {
    "type": "string",
    "title": "Depth Limit Error Color",
    "desc": "RGB values in x, x, x, format.  If you see this color, you've either created an infinite loop, or have a massively complicated equation.",
    "section": "Appearance",
    "key": "depth_limit_color"
    
  }
]
'''
behavior_settings_json = '''
[
  {
    "type": "bool",
    "title": "Load Type",
    "desc": "If ON, loading will try to fit save to current window.  If OFF, loading will take same view as when saved.",
    "section": "Behavior",
    "key": "load_type" 
  },
  {
    "type": "numeric",
    "title": "Depth Limit",
    "desc": "How deep can internal calculations go?  This prevents infinite loops, by limiting how many times an equation can call for the math of references.  It doesn't change any calculates, but rather, serves as crash protection against accidental self references",
    "section": "Behavior",
    "key": "depth_limit"
  },
  {
    "type": "numeric",
    "title": "Auto-Saves to keep",
    "desc": "Number of auto-saves to keep before throwing out the oldest.",
    "section": "Behavior",
    "key": "auto_save_number"
  },
  {
    "type": "numeric",
    "title": "Time Between Auto-Saves",
    "desc": "Time, in minutes, between each auto-save.",
    "section": "Behavior",
    "key": "auto_save_interval"
  }
]
'''

appearance_settings_defaults = {
    'color_example': '',
    'text_color_main': '1, 1, 1',
    'text_color_faded': '.5, .5, .5',
    'text_color_variable': '1, 0, 1',
    'arrow_color': '0, 1, 0',
    'arrow_transparency': 0.25,
    'comment_color': '0, .8, 1',
    'auto_save_interval': 10,
    'auto_save_number': 25,
    'depth_limit_color': '1, 0, 0',
    'depth_limit': 30,
    'load_type': False
}
behavior_settings_defaults = {
    'load_type': False,
    'depth_limit': 30,
    'auto_save_interval': 10,
    'auto_save_number': 25
}
