"""
Looks for all the images in a directory, if they are wider or taller than 
SIZE_THRESHOLD, 7 copies will be made in a sub-folder named 'responsive'. 

Given ./my-image.png (4032x3024):

- ./responsive/my-image-full-4032w.jpg (full size)
- ./responsive/my-image-80-3225w.jpg (80% of full size)
- ./responsive/my-image-60-2420w.jpg (60% of full size)
- ./responsive/my-image-40-1613w.jpg (40% of full size)
- ./responsive/my-image-20-806w.jpg (20% of full size)
- ./responsive/my-image-thumbnail.jpg (400px wide)
- ./responsive/my-image-square.jpg (400px wide square, seam carving)

Each image will have its exif data wiped, and replaced with a copyright notice.

The script runs in two passes, first it collects all of the potential images, 
and sees what sizes aready exist, then it processes each one.

Set DRY_RUN to True to simply print out the actions that would happen.

TODO
====
* edit exif data on images to strip anything weird and add in copyright info.
* repackage into a self-contained repo and egg
* add command-line options via argparse instead of globals 
* add buildout to (try to) build ImageMagick from source
* add thumbnail that is cropped
* format logs to be a bit more informative (timestamps)
* use multiprocessing to parallelize scanning for images and generating 
  thumbnails
* progress bar
* try smart cropping for square thumbnails: https://github.com/epixelic/python-smart-crop
* keep a record of some sort of what images were already processed so we don't 
  have to rescan every time
* remember last time we ran, have a mode where we only process files with a mod time since then.
* work with SVGs (image/svg+xml) and other vector formats
* handle transparency in source files

NOTES
=====
To get Wand working with liquid rescale, I had to install imagemagick via 
macports using the "variants" feature:

$ sudo port install imagemagick +lqr

"""

import os, shutil
from wand.image import Image
from wand.color import Color
from collections import namedtuple
import logging
import mimetypes
import math
import pprint

logging.basicConfig(level=logging.DEBUG)

# TODO: replace with argparse cli options
SIZE_THRESHOLD = 800
DRY_RUN = False
PATH = "./content/images"
DEST_SUBDIR = "responsive" 
THUMBNAIL_WIDTH = 400
OVERWRITE = False

TYPES = ['image/gif', 'image/jpeg', 'image/png'] 

queue = []

ImageInfo = namedtuple(
    "ImageInfo", 
    ["path",         # the full filesystem path to this image 
     "width",        # the image width in pixels
     "height",       # the image height in pixels
     "mimetype",     # the mimetype of the image
     "make_full",    # (size, path to full sized version), None if it already exists.
     "make_80",      # (size, path to 80% sized version), None if it already exists.
     "make_60",      # (size, path to 60% sized version), None if it already exists.
     "make_40",      # (size, path to 40% sized version), None if it already exists.
     "make_20",      # (size, path to 20% sized version), None if it already exists.
     "make_thumb",   # (size, path to thumbnail version), None if it already exists.
     "make_square"]) # (size, path to square thumbnail version), None if it already exists.

class NotAnImage(Exception):
    """
    Exception to simplify some logic - raised when scan_image() runs across a
    file it doesn't think is an image to process.
    """
    
class TooSmall(NotAnImage):
    """
    Raised when an image is too small to bother resizing it.
    """
    
class ImageExists(Exception):
    """
    Raised if an image that is to be written already exists, and you don't want
    it to be clobbered.
    """

def variations(width):
    """
    Given a width, return a dictionary containing each variation name 
    and the width of that variation.
    """
    result = {
        'thumbnail': THUMBNAIL_WIDTH,
        # 'square': 400,
        f'full-{width}w': width
    }
    
    if width < SIZE_THRESHOLD:
        if width > THUMBNAIL_WIDTH:
            return result
        
        logging.debug(f"below {SIZE_THRESHOLD} pixels wide/high")
        raise TooSmall()
    
    #for scale in [20, 40, 60, 80]:
    for scale in [40,]:
        scaled = round(width*(scale/100))
        result[f"{scale}-{scaled}w"] = scaled
    
    return result

def link_to_simpler_name(path, overwrite=False):
    """
    Create a symlink that removes the width specific information from the given
    path.
    
    So my-image-40-1446w.jpg will have a symlink called my-image-40.jpg 
    pointing to it.
    
    if overwrite is True, the symlink will be removed and recreated if it exists.
    
    If overwrite is False, if the symlink exists, ImageExists will be raised.
    """
    prefix, suffix = os.path.splitext(path)
    
    prefix = "-".join(prefix.split("-")[:-1])
    
    link_path = f"{prefix}{suffix}" 
    
    logging.debug(f"Attempting to create symlink from {link_path} to {path}")
    
    if os.path.exists(link_path):
        if overwrite:
            logging.debug(f"Removing existing symlink {link_path}")
            os.remove(link_path)
        else:
            logging.debug(f"Symlink {link_path} already exists")
            raise ImageExists()
            
    if not DRY_RUN:
        os.symlink(path, link_path)
    else:
        logging.info("DRY RUN: skipping creation of symlink {link_path}")
    

def make_thumbnail(source, dest, width, square=False, overwrite=False):
    """
    Make a thumbnail version of the image at source, saved to the destination
    path. Width specifies how wide to make the thumbnail. The aspect ratio will
    be respected, unless square is set to True.
    
    If overwrite is True, the image will be deleted before it's regenerated, if 
    it already exists.
    
    Returns True if the image was created sucessfully. False if not.
    """
    logging.debug(f"Generating {dest}, {width}w, square? {square}") 
    try:
        if os.path.exists(dest):
            if overwrite:
                os.remove(dest)
            else:
                logging.debug(f"{dest} already exists, and overwrite is False")
                raise ImageExists()
        
        with Image(filename=source) as image:
            with image.clone() as thumbnail:
                if not square:
                    thumbnail.transform(resize=f'{width}x{width}>')
                else:
                    thumbnail.liquid_rescale(width, width)
                
                thumbnail.format = "jpg"
                thumbnail.save(filename=dest)
        logging.debug(f"{dest} generated successfully.")
        
        return True
            
    except Exception as e:
        logging.error(e)
        return False

def scan_image(path):
    """
    Given a path, decide if it's an image we care about.
    
    If it's not, return None.
    
    If there's an error, return False.
    
    Otherwise, return important information about it, as an ImageInfo object.
    """
    path = os.path.abspath(os.path.expanduser(path))
    logging.info(f"Processing {path}") 
    
    info = {'path': path}
    
    dest = os.path.join(os.path.dirname(path), DEST_SUBDIR)
    
    try:
        if os.path.isfile(path):
            logging.debug(f"{path} is a file")
            
            mime = mimetypes.guess_type(path)[0]
            
            info['mime'] = mime
            
            logging.debug(f"{path} is of type {mime}")
            
            prefix, suffix = os.path.splitext(os.path.basename(path))
            
            if mime in TYPES:
                with Image(filename=path) as image:
                    info['width'] = image.width
                    info['height'] = image.height
                    
                    if image.width < SIZE_THRESHOLD and image.height < SIZE_THRESHOLD:
                        if image.width > THUMBNAIL_WIDTH:
                            pass
                        else:
                            logging.debug(f"{path} is below {SIZE_THRESHOLD} pixels wide/high")
                            raise TooSmall()
                    
                    for name, width in variations(image.width).items():
                        variant = f"{prefix}-{name}.jpg"
                        variant_dest = os.path.join(dest, variant)
                        logging.debug(f"Processing {variant_dest}")
                        
                        # if not os.path.exists(variant_dest):
                        info[f"make_{name}"] = (width, variant_dest)
                        #else:
                        #    info[f"make_{name}"] = None
                        
                    
                return info
            else:
                logging.debug(f"{mime} is not a recognized image type.")
                raise NotAnImage()
        else:
            raise NotAnImage()
    except NotAnImage:
        return None
    except Exception as e:
        logging.error(e)
        return False

logging.info(f"Scanning {PATH} for images...")

images = 0
thumbnails = 0

for entry in os.scandir(PATH):
    result = scan_image(entry)
    if result:
        queue.append(result)
        images += 1
        
        for key, value in result.items():
            if "make" in key:
                if value is not None:
                    thumbnails += 1
        
        
dest_path = os.path.join(os.path.abspath(os.path.expanduser(PATH)), DEST_SUBDIR)

logging.info(f"Found {images} images to process. Will create {thumbnails} total images in {dest_path}")

logging.debug(f"Checking if {dest_path} exists")
if not os.path.exists(dest_path):
    logging.debug(f"{dest_path} does not exist")
    if not DRY_RUN:
        os.mkdir(dest_path)
    else:
        logging.debug(f"DRY RUN: {dest_path} not created") 

links_to_make = []

for result in queue:
    logging.debug(f"Processing thumbnails for {result['path']}")
    for key, value in result.items():
        if "make" in key:
            logging.debug(f"Action: {key}")
            if value is not None:
                width, path = value
                
                square = "square" in key
                
                logging.debug(f"Generating variation {path}, width {width}, square={square}")
                
                if DRY_RUN:
                    logging.debug(f"DRY RUN: skipping creation of {path}")
                else:
                    make_thumbnail(result['path'], path, width, square=square, overwrite=OVERWRITE)
                    
                links_to_make.append(path)
                
                
for path in links_to_make:
    try:
        link_to_simpler_name(path, overwrite=OVERWRITE)
    except ImageExists:
        pass
                
                