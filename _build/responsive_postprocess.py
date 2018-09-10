"""
Responsive Image Post-Processor

Parses all .html files in a given directory, and performs the following:
  - scans for all img tags
  - if the images meet certain criteria, a series of resized versions are 
    created in a subdirectory of their current location called 'responsive'
  - the relevant img tags are replaced with new img tags with srcset and
    sizes attributes to make the image responsive, linking to the correct
    variants
  - the new html file is written

"""
import os, shutil
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from wand.image import Image
import piexif
import tempfile
import re

PATH = os.path.abspath("../") # the path to scan for HTML files
DOCUMENT_ROOT = PATH          # the physical path that maps to / for absolute
                              # paths
                              
# sizes of variations to generate (None is fullsize)
# SIZES = (200, 400, 800, 1000, 1200, 1600, 1800, 2000, 2500, None)
SIZES = (None, 2500, 2000, 1800, 1600, 1200, 1000, 800, 400, 200)
# Assayed the design in various widths in responsive design mode
#
# CONTENT_WIDTHS = {
#     1280: 1214,
#     1024: 970.833,
#     414: 391.333,
#     375: 354.267,
#     320: 302,
#     1440: 1366,
#     384: 362.833,
#     360: 340,
#     412: 389.434,
#     960: 910,
#     1366: 1295.73,
#     640: 606,
#     800: 758,
#     786: 727.634,
#     736: 697.233,
#     667: 631.667,
#     568: 537.634,
#     732: 696.434,
#     600: 568,
#     533: 504
# }
#
# Average ratio is 1.058
CONTENT_WIDTH_RATIO = 1.06      # used for guessing the viewport slot size

CHANGE_WINDOW = timedelta(minutes=30)

def calculate_width(image_tag, variant_width):
    """
    Given a BeautifulSoup Tag object, return a value corresponding
    to the approximate size the image will render.
    
    It follows the following rules:
        - if the image tag has a width attribute, it will be extracted.
        - if the image tag has a style attribute, the width rule will be extracted.
        - the width will be returned verbatim, unless it's a relative size 
          (only percentages are supported). 
        - if the width is a relative size, a value is calculated using 
          CONTENT_WIDTH_RATIO, the width and the variant_width.
          
    If no width can be extracted, None is returned.
    
    TODO: test edge cases
    TODO: raise exception or otherwise notify when a malformed width is found.
    """
    width = None
    
    if image_tag.has_attr("width"):
        width = image_tag["width"]
    elif image_tag.has_attr("style"):
        matches = re.match("width:\s*([^;]*);", image["style"])
        if matches:
            width = matches.group(1)
    else:
        return width
        
    matches = re.match("(\d+)(em|%|px|vw|pt)?", width)
    
    try:
        if matches:
            width = int(matches.group(1))
            unit = matches.group(2)
            
            if unit is None or unit == "pt":
                # assume pixels
                return width
            elif unit == "%":
                return round(variant_width*(width/100))
            
        else:
            return None
    except ValueError:
        return None
    

def make_variant(source, width=None, force=False):
    """
    Create a jpeg variant of the image at path, with the given width.
    
    Puts the variant in a subdirectory of the image called responsive.
    
    The image will be named with the width in its name.
    
    So for an image located at /var/www/site1/images/big_photo.png, given the
    width of 500, this function will generate a 500 pixel wide version at
    
    /var/www/site1/images/responsive/big_photo-500px.jpg
    
    Return value: the newly created path.
    
    If you pass None for the width, the new image is placed in the fullsize 
    subdirectory, the width is not added to the name. 
    """
    directory, image_name = os.path.split(source)
    
    name, ext = os.path.splitext(image_name)
    
    if width is not None:
        dest = os.path.join(directory, "responsive")
        variant_path = os.path.join(dest, f"{name}-{width}.jpg")
    else:
        dest = os.path.join(directory, "fullsize")
        variant_path = os.path.join(dest, f"{name}.jpg")
    
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    if os.path.exists(variant_path) and not force:
        print("Already exists, force=False")
        return variant_path
    
    with Image(filename=source) as image:
        if width and image.width < width:
            return None
        
        # preserve orientation but otherwise remove all exif data after resize
        # TODO: is this standard across all image types?
        orientation = image.metadata.get("exif:Orientation")
        mime = image.mimetype
        
        with image.clone() as variant:
            image.auto_orient()
            if width is not None:
                variant.transform(resize=f'{width}x{width}>')
            
            variant.format = "jpg"
            variant.save(filename=variant_path)
            
    year = datetime.today().year
    exif = {'0th': {33432: f"(c){year} Josh Johnson. All Rights Reserved.\0"}}
    if orientation and mime != "image/png":
        exif['0th'][274] = orientation
        
    piexif.remove(variant_path)
    piexif.insert(piexif.dump(exif), variant_path)
            
    return variant_path 
    
for path in os.scandir(PATH):
    path = os.path.abspath(path)
    
    base, ext = os.path.splitext(path)
    
    if ext == ".html":
        with open(path) as fp:
            soup = BeautifulSoup(fp, 'lxml')
            images = soup.select("section img")
            
            for image in images:
                if image.get("srcset"):
                    print("WARNING: IMAGE ALREADY PROCESSED?")
                    continue
                
                # TODO: catch off-site image links
                # TODO: detect if the image already is wrapped in an A tag
                src_path = image["src"]
                parent = os.path.dirname(path)
                is_absolute = os.path.isabs(src_path)
                
                if image["src"].startswith("/"):
                    parent = DOCUMENT_ROOT
                    src_path = src_path[1:]
                
                image_path = os.path.normpath(os.path.join(parent, src_path))
                
                variants = {}
                
                last_modified = datetime.fromtimestamp(os.path.getmtime(image_path))
                if datetime.now() - last_modified <= CHANGE_WINDOW:
                    force = True
                else:
                    force = False
                
                for size in SIZES:
                    variants[size] = make_variant(image_path, size, force=force)
                
                fullsize_link = os.path.relpath(variants[None], DOCUMENT_ROOT)
                
                if is_absolute:
                    fullsize_link = os.path.join("/", fullsize_link)
                
                a_tag = soup.new_tag("a", href=fullsize_link)
                
                srcset = []
                sizes = []
                
                for size, variant_path in variants.items():
                    if size is None or variant_path is None:
                        continue
                    
                    src = os.path.relpath(variant_path, DOCUMENT_ROOT)
                    
                    if is_absolute:
                        src = os.path.join("/", src)
                    
                    srcset.append(f"{src} {size}w")
                    
                    slot_width = calculate_width(image, size)
                    if slot_width is not None:
                        screen_width = size*CONTENT_WIDTH_RATIO
                        sizes.append(f"(min-width: {screen_width}px) {slot_width}px")  
                    
                
                image["src"] = fullsize_link
                image["srcset"]= ",".join(srcset)
                image["sizes"] = ",".join(sizes)
                
                print(fullsize_link)
                print("-----------------------")
                print("SRCSET:")
                [print(f"\t{x}") for x in srcset]
                print("SIZES:")
                [print(f"\t{x}") for x in sizes]
                print("")
                
                image.wrap(a_tag)
                
            # wrap code blocks in a div so overflow will
            # work properly
            code_blocks = soup.select(".highlighttable")
            for block in code_blocks:
                if "highlight-wrapper" in block.parent.get("class", []):
                    print("ALREADY VISITED CODE BLOCK")
                    continue
                
                div = soup.new_tag("div")
                div["class"] = "highlight-wrapper"
                block.wrap(div)
                
        
        temp_path = f"{base}.new{ext}"
        
        shutil.copy(path, temp_path)
        with open(temp_path, "wb") as new_html:
            new_html.write(soup.encode(formatter="html"))
            
        shutil.move(temp_path, path)
