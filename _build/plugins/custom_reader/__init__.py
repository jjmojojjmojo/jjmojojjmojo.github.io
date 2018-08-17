from pelican import signals
from pelican.readers import RstReader
from pelican.readers import PelicanHTMLTranslator
import docutils, re
from docutils import nodes, utils, writers, languages, io
from wand.image import Image as MagickImage


def make_responsive_images(source):
    """
    Make a series of variations of a given image to provide
    responsive image sizes.
    
    Returns a list of tuples of image-path, image size
    """


class CustomHTMLTranslator(PelicanHTMLTranslator):
    """
    Any special HTML output goes here.
    """
    
    def visit_image(self, node):
        """
        Overloading to provide responsive images.
        """
        atts = {}
        uri = node['uri']
        atts['src'] = uri
        
        import ipdb; ipdb.set_trace();
        
        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']
            
        style = []
        
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        
        for att_name in 'width', 'height':
            if att_name in atts:
                if re.match(r'^[0-9.]+$', atts[att_name]):
                    # Interpret unitless values as pixels.
                    atts[att_name] += 'px'
                style.append('%s: %s;' % (att_name, atts[att_name]))
                del atts[att_name]
        if style:
            atts['style'] = ' '.join(style)
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
            
        atts["srcset"] = "boo"
        atts["sizes"] = "boo2"
        
        self.body.append(self.emptytag(node, 'img', suffix, **atts))
        

class CustomRSTReader(RstReader):
    enabled = True
    file_extensions = ['rst']
    
    def __init__(self, *args, **kwargs):
        RstReader.__init__(self, *args, **kwargs)
    
    def _get_publisher(self, source_path):
        """
        Have to override this method, and reimplement all of it, 
        because there's no way to hook in a custom translator
        """
        extra_params = {'initial_header_level': '2',
                        'syntax_highlight': 'short',
                        'input_encoding': 'utf-8',
                        'exit_status_level': 2,
                        'embed_stylesheet': False}
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = docutils.core.Publisher(
            source_class=self.FileInput,
            destination_class=docutils.io.StringOutput)
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = CustomHTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish(enable_exit_status=True)
        return pub
        
    def read(self, filename):
        content, metadata = RstReader.read(self, filename)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['rst'] = CustomRSTReader

# This is how pelican works.
def register():
    signals.readers_init.connect(add_reader)