from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import unchanged


class Quote(Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'credit': unchanged,
        'link': unchanged,
    }

    def _build_cite(self, credit, citation, link):
        parts = []

        if credit:
            parts.append(credit)

        if citation and link:
            parts.append(f'<a href="{link}">{citation}</a>')
        elif citation:
            parts.append(citation)
        elif link:
            parts.append(f'<a href="{link}">{link}</a>')

        if not parts:
            return None

        return '<cite>' + ', '.join(parts) + '</cite>'

    def run(self):
        self.assert_has_content()

        citation = self.arguments[0] if self.arguments else None
        credit = self.options.get('credit')
        link = self.options.get('link')

        aside_open = nodes.raw('', '<aside>', format='html')
        blockquote_open = nodes.raw('', '<blockquote class="pull-quote">', format='html')

        body = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, body)

        cite_html = self._build_cite(credit, citation, link)
        cite_node = nodes.raw('', cite_html, format='html') if cite_html else None

        blockquote_close = nodes.raw('', '</blockquote>', format='html')
        aside_close = nodes.raw('', '</aside>', format='html')

        result = [aside_open, blockquote_open] + list(body.children)
        if cite_node:
            result.append(cite_node)
        result += [blockquote_close, aside_close]

        return result


def register():
    directives.register_directive('quote', Quote)
