import re

from docutils import nodes, utils
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives.images import Image, Figure

import pelican.settings as pys

def process_image_nodes(node):
    """
    Process a single image node - return a raw HTML node in its place
    
    If the node is not an image node, returns the node as-is.
    
    If the node has children, calls process_image_node recursively on each child.
    """
    if node.children:
        children = node.children
        node.children = []
        
        for n in children:
            node += process_image_nodes(n)
        output = node
    else:
        if node.tagname == "image":
            node.attributes["srcset"] = "boo!"
            node.attributes["sized"] = "ya ya ya I am lorde ya ya ya"
            # output = nodes.raw('', "<strong>BOO</strong>", format='html')
        
        output = node
        
    return output
    

class ResponsiveImage(Image):
    """ 
    Works similarly to the image:: directive, except that the image will be 
    resized to several resoultions and the end result will be a "reactive" image,
    where only the appropriately sized version will be loaded.
    """
    def run(self):
        parsed = Image.run(self)
        
        output = []
        
        for n in parsed:
            output.append(process_image_nodes(n))
        
        return output
        

def register():
    directives.register_directive('responsiveimage', ResponsiveImage)