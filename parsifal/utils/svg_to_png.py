from django.conf import settings as djangoSettings
from cairosvg import svg2png

def svg_to_png(svg, review):

    f = open(djangoSettings.MEDIA_ROOT + '/forest_plot-'+ review.name +'.svg', "w+")
    f.write(svg)
    f.close()

    return svg2png(open(djangoSettings.MEDIA_ROOT + '/forest_plot-'+ review.name +'.svg', 'rb').read(), write_to=open(djangoSettings.MEDIA_ROOT + '/forest_plot-'+ review.name +'.png', 'wb'))
