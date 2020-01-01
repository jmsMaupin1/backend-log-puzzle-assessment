#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    url_list = []
    host_name = filename.split('_')[1]
    with open(filename) as file:
        for line in file:
            match = re.search(r'\S+puzzle+\S+', line)
            if match:
                url_list.append("http://" + host_name + match.group())
    return sorted(list(set(url_list)), key=lambda url: url[-8:-4])


def create_dir(path):
    """Checks to see if a directory exists, if not creates it"""
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of directory %s failed" % path)
            return -1

    return 0


def write_html(image_tags):
    """Takes a string of image tags and inserts them into the body of an html page"""

    html_template = """
        <html>
            <body>
                {}
            </body>
        </html>
    """

    with open('index.html', 'w') as html:
        html.write(html_template.format(image_tags))


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    image_tag_template = "<img src={}>"
    image_path = dest_dir + "/img{}.jpg"
    image_tags = ""

    create_dir(dest_dir)

    for idx, url in enumerate(img_urls):
        final_path = image_path.format(idx)
        urllib.urlretrieve(url, final_path)
        image_tags += image_tag_template.format(final_path)

    write_html(image_tags)

    pass


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
