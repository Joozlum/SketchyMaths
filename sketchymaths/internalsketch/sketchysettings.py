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
    "type": "bool",
    "title": "Draw Arrows",
    "desc": "Draw arrows to connect equations.",
    "section": "Behavior",
    "key": "bool_draw_arrows"
  },
  {
    "type": "numeric",
    "title": "Arrow Refresh Rate",
    "desc": "Time, in ms, to refresh arrows.",
    "section": "Behavior",
    "key": "arrow_refresh_rate"
  },
  {
    "type": "numeric",
    "title": "Floating-Point Accuracy",
    "desc": "How many decimal places to display.  Only affects display, does not change values used for calculation.",
    "section": "Behavior",
    "key": "decimal_places"
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
    'arrow_color': '0, 1, 0',
    'arrow_transparency': 0.5,
    'comment_color': '0, .8, 1',
}
behavior_settings_defaults = {
    'load_type': False,
    'decimal_places': 2,
    'bool_draw_arrows': 1,
    'arrow_refresh_rate': 200,
    'auto_save_interval': 10,
    'auto_save_number': 25
}
