
def get_palette_EK():
    colors1=['#003326','#05283d','#ff9d6a','#599956']
    colors2=['#295247','#2c495a','#fdaf89','#7cae79']
    colors3=['#88b2eb','#ffcb21','#e85c03']
    
    colors=['#295247','#7cae79','#ffcb21','#e85c03','#88b2eb','#2c495a','#fdaf89']
    
    return sns.color_palette(colors)
    
def get_style_EK():
    axes={'axes.facecolor': 'white',
     'axes.edgecolor': 'black',
     'axes.grid': False,
     'axes.axisbelow': 'line',
     'axes.labelcolor': 'black',
     'figure.facecolor': 'white',
     'grid.color': '#b0b0b0',
     'grid.linestyle': '-',
     'text.color': 'black',
     'xtick.color': 'black',
     'ytick.color': 'black',
     'xtick.direction': 'out',
     'ytick.direction': 'out',
     'lines.solid_capstyle': 'projecting',
     'patch.edgecolor': 'black',
     'patch.force_edgecolor': False,
     'image.cmap': 'viridis',
     'font.family': ['sans-serif'],
     'font.sans-serif': ['IBM Plex Sans',
      'DejaVu Sans',
      'Bitstream Vera Sans',
      'Computer Modern Sans Serif',
      'Lucida Grande',
      'Verdana',
      'Geneva',
      'Lucid',
      'Arial',
      'Helvetica',
      'Avant Garde',
      'sans-serif'],
     'xtick.bottom': True,
     'xtick.top': False,
     'ytick.left': True,
     'ytick.right': False,
     'axes.spines.left': False,
     'axes.spines.bottom': True,
     'axes.spines.right': False,
     'axes.spines.top': False}
     
    return axes