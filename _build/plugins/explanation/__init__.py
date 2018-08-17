from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition


class ExplanationNode(nodes.Labeled, nodes.container):
    pass

class Explanation(BaseAdmonition):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    
    def _run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        
        node = nodes.container(text)
        
        try:
            title = self.arguments[0]
        except IndexError:
            title = "Explanation"
        
        textnodes, messages = self.state.inline_text(text, self.lineno)
        node += nodes.title(title, '', *textnodes)
        node += messages
        
        # admonition_node = self.node_class(rawsource=text)
        node['classes'] = ["explanation"]
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]
    
    def run(self):
        # Raise an error if the directive does not have contents.
        
        
        # main node
        self.assert_has_content()
        
        text = '\n'.join(self.content)
        
        # add explanation header
        try:
            title = self.arguments[0]
        except IndexError:
            title = "Explanation"
            
        header = nodes.title(text=title)
        
        body = nodes.container(text)
        
        node = nodes.section()
        node['classes'] = ["explanation"]
        
        node += header
        node += body
        
        self.state.nested_parse(self.content, self.content_offset, node)
        
        return [node]



def register():
    directives.register_directive('explanation', Explanation)