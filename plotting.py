""" file: plotting.py
"""

from pysiss.vocabulary.namespaces import NamespaceRegistry, shorten_namespace
import simplejson


def load_style_file(filename):
    """ Load a JSON-encoded style file
    """
    with open(filename, 'rb') as fhandle:
        style_data = simplejson.load(fhandle)

        # Expand styles using defaults
        styles = {}
        default_style = style_data['default']
        for lith in style_data.keys():
            # We only want to update the keys that aren't there already
            styles[lith] = default_style.copy()
            styles[lith].update(style_data[lith])
        return styles

# Load lithology and age styles
LITH_STYLES = load_style_file('lithology_styles.json')
AGE_STYLES = load_style_file('age_styles.json')


def style_by_lithology(feature):
    """ Return the style for a given feature based on lithology
    """
    lithology = feature.metadata.xpath(
        './/gsml:RockMaterial/gsml:lithology/@xlink:href',
        namespaces=NamespaceRegistry())
    if lithology:
        try:
            params = LITH_STYLES[shorten_namespace(lithology[0])]
        except KeyError:
            params = LITH_STYLES['default']
    else:
        params = LITH_STYLES['default']
    return params


def style_by_age(feature):
    """ Return the style for a given feature based on age
    """
    age_elem = feature.metadata.xpath(
        './/gsml:preferredAge//gsml:value',
        namespaces=NamespaceRegistry())
    if len(age_elem):
        try:
            params = AGE_STYLES[shorten_namespace(age_elem[0].text)]
        except KeyError:
            params = AGE_STYLES['default']
    else:
        params = AGE_STYLES['default']
    return params


def plot_contacts(axes, contacts):
    """ Plot a bunch of contact data
    """
    for contact in contacts:
        # Work out what sort of contact we're plotting
        descr = contact.metadata.find('.//gml:description',
                                      namespaces=NamespaceRegistry())

        descr = descr.text.lower()
        if descr == 'geological boundary':
            props = dict(color='black', dashes=(7, 1), linewidth=0.5)
        elif descr == 'fault':
            # We'll just skip these ones
            props = dict(color='blue', linewidth=0)
        elif descr == 'dyke or vein':
            props = dict(color='red', linewidth=3)
        elif descr == 'marker bed/band':
            props = dict(color='gray', linewidth=1)

        # Plot the line
        xs, ys = contact.shape.xy
        axes.plot(xs, ys, zorder=1, **props)

    # Fix up the axes to show the data
    axes.set_xlim(119.52, 120.90)
    axes.set_ylim(-20.5, -21.6)
    axes.set_aspect('equal')


def plot_faults(axes, faults):
    """ Plot a bunch of fault data
    """
    for fault in faults:
        # If fault is concealed, plot it with dashes
        description = fault.metadata.find('.//gml:description',
                                          namespaces=NamespaceRegistry())
        if ('concealed' in description.text):
            param = dict(color='black', linewidth=2, dashes=(5, 5))
        else:
            param = dict(color='black', linewidth=2)

        xs, ys = fault.shape.xy
        axes.plot(xs, ys, zorder=2, **param)

    # Fix up the axes to show the data
    axes.set_xlim(119.52, 120.90)
    axes.set_ylim(-21.6, -20.5)
    axes.set_aspect('equal')
