"""
Simple web server for static content - uses WebOb. 

Run this under a WSGI server like waitress, gunicorn or whatever.

TODO: integrate the webserver into this so it's a self-contained unit
"""

from webob import Request, Response
from webob.static import FileApp
import os

class DirectoryListingApp:
    """
    Similar to webob.static.DirectoryApp, but it displays a listing, ala Apache,
    when the index file isn't found.
    """
    def __init__(self, path, index_page="index.html", **fileapp_kw):
        self.path = os.path.abspath(path)
        
        if not self.path.endswith(os.path.sep):
            self.path += os.path.sep
        
        if not os.path.isdir(self.path):
            raise IOError("Path does not exist or is not directory: %r" % self.path)
        
        self.index_page = index_page
        self.fileapp_kw = fileapp_kw
        
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        path = os.path.join(self.path, request.path_info.lstrip('/'))
        
        
        if os.path.isdir(path):
            response = self.index(request, path)
        else:
            response = FileApp(path, **self.fileapp_kw)
            
        return response(environ, start_response)
            
    def index(self, request, path):
        index_path = os.path.join(path, self.index_page)
        
        if os.path.exists(index_path):
            return FileApp(index_path, **self.fileapp_kw)
        
        folders = []
        files = []
        
        for entry in os.scandir(path):
            relpath = os.path.relpath(entry.path, self.path)
            display_path = os.path.relpath(entry.path, path)
            
            link = f'<p><a href="{relpath}">{display_path}</a></p>'
            
            if entry.is_dir():
                folders.append(link)
            elif entry.is_file():
                files.append(link)
                
        folders.sort()
        files.sort()
                
        display_path = os.path.relpath(path, self.path)
        
        output = f"""
        <html>
        <head>
            <title>/{display_path}'s Contents</title>
        <body>
        <a href="../">Up ^</a>
        <hr />
            <h1>Directory Listing <em>/{display_path}</em></h1>
            {"".join(folders)}
            {"".join(files)}
        </body>
        </html>
        """
        
        return Response(body=output)

dev = DirectoryListingApp("./output")
preview = DirectoryListingApp("../")