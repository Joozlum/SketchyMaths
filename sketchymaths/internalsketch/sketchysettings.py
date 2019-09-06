settings_json = '''
[
  {
    "type": "string",
    "title": "Evaluated Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Settings",
    "key": "text_color_main"
  },
  {
    "type": "string",
    "title": "Unevaluated Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Settings",
    "key": "text_color_faded"
  },
  {
    "type": "string",
    "title": "Variable Text Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Settings",
    "key": "text_color_variable"
  },
  {
    "type": "string",
    "title": "Arrow Color",
    "desc": "RGB values, in x, x, x format",
    "section": "Settings",
    "key": "arrow_color"
  },
  {
    "type": "numeric",
    "title": "Arrow Transparency",
    "desc": "How dark the arrows get drawn, between 0-1",
    "section": "Settings",
    "key": "arrow_transparency"
  },
  {
    "type": "string",
    "title": "Comment Color",
    "desc": "RGB values in x, x, x format",
    "section": "Settings",
    "key": "comment_color"
  },
  {
    "type": "string",
    "title": "Depth Limit Error Color",
    "desc": "RGB values in x, x, x, format.  If you see this color, you've either created an infinite loop, or have a massively complicated equation.",
    "section": "Settings",
    "key": "depth_limit_color"
    
  },
  {
    "type": "numeric",
    "title": "Depth Limit",
    "desc": "How deep can internal calculations go?  This prevents infinite loops, by limiting how many times an equation can call for the math of references.  It doesn't change any calculates, but rather, serves as crash protection against accidental self references",
    "section": "Settings",
    "key": "depth_limit"
  }
]
'''

settings_defaults = {'text_color_main': '1, 1, 1',
                     'text_color_faded': '.5, .5, .5',
                     'text_color_variable': '1, 0, 1',
                     'arrow_color': '0, 1, 0',
                     'arrow_transparency': 0.25,
                     'comment_color': '0, .8, 1',
                     'depth_limit_color': '1, 0, 0',
                     'depth_limit': 30}
