"""Tools to style a talk."""

from IPython.display import HTML, display, YouTubeVideo

def prefix(url):
    prefix = '' if url.startswith('http') else 'http://'
    return prefix + url


def simple_link(url, name=None):
    name = url if name is None else name
    url = prefix(url)
    return '<a href="%s" target="_blank">%s</a>' % (url, name)


def html_link(url, name=None):
    return HTML(simple_link(url, name))


# Utility functions
def website(url, name=None, width=800, height=450):
    html = []
    if name:
        html.extend(['<div class="nb_link">',
                     simple_link(url, name),
                     '</div>'] )

    html.append('<iframe src="%s"  width="%s" height="%s">' % 
                (prefix(url), width, height))
    return HTML('\n'.join(html))


def embed_map(map, path="map.html"):
    """ Embeds a linked iframe to the map into the IPython notebook.
    
        Note: this method will not capture the source of the map into the notebook.
        This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))


def nbviewer(url, name=None, width=800, height=450):
    return website('nbviewer.ipython.org/url/' + url, name, width, height)

# Load and publish CSS
# style = HTML(open('style.css').read())

# display(style)
