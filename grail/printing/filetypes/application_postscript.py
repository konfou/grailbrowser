__version__ = '$Revision: 1.7 $'

from ...sgml import HTMLParser
import sys

from ...grailbase.utils import conv_mimetype
from .. import epstools
from ...sgml.utils import *


def embed_application_postscript(parser, attrs):
    """<OBJECT> handler for Encapsulated PostScript."""
    data = extract_keyword('data', attrs)
    if not data or not parser.settings.imageflag:
        return None
    type, typeopts = conv_mimetype(
        extract_keyword('type', attrs, conv=conv_normstring))
    if "level" in typeopts:
        try:
            level = int(typeopts["level"])
        except ValueError:
            return None
        if level > parser.settings.postscript_level:
            return None
    # this is Encapsulated PostScript; use it.
    image = None
    imageurl = parser.context.get_baseurl(data)
    if imageurl in parser._image_cache:
        image = parser._image_cache[imageurl]
    else:
        try:
            image = load_eps_object(parser, imageurl)
        except BaseException as err:
            sys.stderr.write("Exception loading EPS object: {}\n".format(
                             type(err).__name__))
            image = None
        if image:
            parser._image_cache[imageurl] = image
    if image:
        width = extract_keyword('width', attrs, conv=conv_integer)
        height = extract_keyword('height', attrs, conv=conv_integer)
        parser.print_image(image, width, height)
        return HTMLParser.Embedding()


def load_eps_object(parser, imageurl):
    # load EPS data from an application/postscript resource
    try:
        image = parser._image_loader(imageurl)
    except:
        return None
    if not image:
        return None
    lines = image.decode('latin-1').split('\n')
    try:
        lines.remove('showpage')
    except ValueError:
        pass             # o.k. if not found
    bbox = epstools.load_bounding_box(lines)
    return epstools.EPSImage('\n'.join(lines), bbox)
