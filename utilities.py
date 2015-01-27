""" file:   utilities.py
    author: Jess Robertson
            CSIRO Mineral Resources Flagship
    date:   Tuesday 9 September, 2014
"""

import numpy
from IPython.display import HTML


def prefix(url):
    prefix = '' if url.startswith('http') else 'http://'
    return prefix + url


def simple_link(url, name=None):
    name = url if name is None else name
    url = prefix(url)
    return '<a href="%s" target="_blank">%s</a>' % (url, name)


def html_link(url, name=None):
    return HTML(simple_link(url, name))


def normalize(image, mask_value=1):
    """ Convert image to lie between 0 and 1
    """
    # Create a masked version of the image, masked values are 1
    mask_image = numpy.ma.MaskedArray(image, mask=(image == mask_value))

    # Constrain floats to lie between 0 and 1
    min_index = mask_image.min()
    max_index = mask_image.max()
    return (mask_image - min_index) / float(max_index - min_index)


def website(url, name=None, width=800, height=450):
    html = []
    if name:
        html.extend(['<div class="nb_link">',
                     simple_link(url, name),
                     '</div>'])

    html.append('<iframe src="%s"  width="%s" height="%s">' %
                (prefix(url), width, height))
    return HTML('\n'.join(html))


def embed_map(leafmap, path="map.html"):
    """ Embeds a linked iframe to a Leaflet map into the IPython notebook.

        Note: this method will not capture the source of the map into the
        notebook. This method should work for all maps (as long as they
        use relative urls).
    """
    leafmap.create_map(path=path)
    return HTML(('<iframe src="files/{path}" '
                 'style="width: 100%; height: 510px; border: none">'
                 '</iframe>').format(path=path))
