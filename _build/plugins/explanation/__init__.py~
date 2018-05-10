from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


class ExplanationNode(nodes.Labeled, nodes.container):
    pass

class Explanation(Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'forms': directives.unchanged, 
        'language': directives.unchanged
    }
    has_content = True
    
    # def run(self):
    #     self.assert_has_content()
    #     
    #     node = nodes.raw('', '<div class="explanation">Explanation <button>Show</button>
    
    def clojure_form_links(self):
        """
        Return a list of link nodes in clojuredocs for each passed clojure form.
        """
        forms = self.options.get("forms", None)
        out = []
        if forms:
            forms = forms.split()
            
            for form in forms:
                out.append("* HEY `{} <{}>`__\n".format(form, "http://somewhere"))
            
            print(out)
            
            links = nodes.block_quote("\n".join(out))
            
            return links
        else:
            return nodes.container()
        
    
    def run(self):
        # Raise an error if the directive does not have contents.
        
        
        # main node
        self.assert_has_content()
        
        text = "`google <http://www.google.com>`__\n"
        text += '\n'.join(self.content)
        
        # add explanation header
        print(self.arguments)
        try:
            title = self.arguments[0]
        except IndexError:
            title = "Explanation"
            
        header = nodes.title(text=title)
        
        body = nodes.container(text)
        
        links = self.clojure_form_links()
        
        node = nodes.section()
        node['classes'] = ["explanation"]
        
        node += header
        node += links
        node += body
        
        self.state.nested_parse(self.content, self.content_offset, links)
        self.state.nested_parse(self.content, self.content_offset, body)
        
        
        
        return [node]



def register():
    directives.register_directive('explanation', Explanation)