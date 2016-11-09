
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class MyRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
                #mistune.escape(code.strip())
        #lexer = get_lexer_by_name(lang, stripall=True)
        lexer = get_lexer_by_name(lang)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


def render(source):
    renderer = MyRenderer()
    md = mistune.Markdown(renderer=renderer)
    return md.render(source)
