#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    cli.py
    ~~~~~

    lmb command line interface toolchain

    examples uses:

    ```
    $ lmb detect faces.jpg
    10 10 128 128
    $ lmb detect face.jpg | lmb draw -i faces.jpg > faces_rect.jpg
    $ cat faces_rect.jpg | lmb edge > faces_rect_edge.jpg
    $ lmb gallery *.jpg > gallery.html
    ```

    :created: 2013-02-21 23:59:15 -0800
    :copyright: (c) 2013, Lambda Labs, Inc.
    :license: BSD. See LICENSE.
"""
import sys
from sys import stdout
import draw as lmb_draw
import detect as lmb_detect
from utils import fname, module_name, pretty_now, tuple_rect, is_rect


def detect(*images):
    """Detect faces in images, output rects.

    Outputs serialized shapes

    :param images: a list of images to detect
    """
    def write_out(image, featname, recttup):
        stdout.write('%s %s %s %s %s %s\n' % ((image, featname) + recttup))

    for image in images:
        img = lmb_detect.img_url(image)
        for face in img.faces:
            r = face['rect']
            write_out(image, 'face', tuple_rect(r))
            for fkey, fval in face.iteritems():
                if is_rect(fval):
                    write_out(image, fkey, tuple_rect(fval))


def draw(image, ftype, x, y, w, h):
    """Draw shapes on an image (default rectangles)

    :param image: an image path
    :param x: rect x origin
    :param y: rect y origin
    :param w: rect w size
    :param h: rect h size
    """
    shape = (x, y, w, h)
    img = lmb_detect.img_url(image)
    out = lmb_draw.draw_rect(img, shape)
    sys.stdout.write('%s\n' % out)
    return out


def edge(image):
    """Perform edge detection on an image

    :param image: an image path
    """
    pass


def gallery(*images):
    """Create an HTML gallery for the images provided.

    :param images: a list of image URLs or paths
    """
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>%s</title>
</head>
<body>
<h1>%s</h1>
%s
<hr />
<img src="http://lambdal.com/images/lambda-labs-logo-25x25.png" /> Created with the <a href="http://github.com/lambdal/lmb">Lambda Labs API</a>
</body>
</html>
"""
    title = 'Image Gallery Generated by %s on %s' % (module_name, pretty_now())
    mid = ''
    for image in images:
        mid += '\t<img src="%s" alt="%s" />\n' % (image, fname(image))
    result = template % (title, title, mid)
    stdout.write(result)
    return result


if __name__ == '__main__':
    command = sys.argv[1]
    args = sys.argv[2:]
    cmd = locals()[command]
    if (args):
        cmd(*args)
    else:
        for line in sys.stdin.readlines():
            cmd(*line.strip().split(' '))
