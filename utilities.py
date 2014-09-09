""" file:   utilities.py
    author: Jess Robertson
            CSIRO Mineral Resources Flagship
    date:   Tuesday 9 September, 2014
"""

import numpy


def normalize(image, mask_value=1):
    """ Convert image to lie between 0 and 1
    """
    # Create a masked version of the image, masked values are 1
    mask_image = numpy.ma.MaskedArray(image, mask=(image == mask_value))

    # Constrain floats to lie between 0 and 1
    min_index = mask_image.min()
    max_index = mask_image.max()
    return (mask_image - min_index) / float(max_index - min_index)
