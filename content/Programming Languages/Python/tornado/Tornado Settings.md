Here we set a variabler named settings and this will allow us to tell Tornado where we save our HTML/Javascript/CSS files. We have been going from a very basic app.py file to more advanced versions of it through the lessons below.

- [[Basic Tornado Application]]
- [[Passing Parameters]]

## Folder structure

![[Pasted image 20240505141750.png]]
**root folder**
- static
- templates
	- index.html
	- template.html
- app.py


## App.py

We no longer need to tell the MainHandler where the html files live and in future lessons it will be easier to have Tornado find out Javascript/css files.

Here are some examples of what we can add in the settings dictionary:

- **debug**: A boolean indicating whether the application is in debug mode.
- **cookie_secret**: A secret key used for signing cookies.
- **xsrf_cookies**: A boolean indicating whether to use XSRF protection for cookies.
- **login_url**: The URL to redirect to for login.
- **default_handler_class**: The default handler class for 404 and 500 errors.
- **ui_modules**: A dictionary of UI modules to be used in templates.
- **autoescape**: A boolean indicating whether to automatically escape HTML in templates.
- **autoreload**: A boolean indicating whether to automatically reload the application when changes are detected.
- **compiled_template_cache**: A boolean indicating whether to cache compiled templates.
- **static_hash_cache**: A boolean indicating whether to cache static file hashes.
- **serve_traceback**: A boolean indicating whether to serve tracebacks in error responses.

``` python
# Webserver stuff
import tornado.ioloop
import tornado.web

# Utility libraries
import os.path

# route to index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    page_title = 'This is Amazing!!!',
                    page_heading = 'Welcome to Tornado'
        ) 

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler)
],**settings) 

# Start the server at port n
if __name__ == "__main__":
    PortNumber = str(7777)
    print(r'Server Running at http://localhost:' + PortNumber + r'/')
    print(r'To close press ctrl + c')
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()
```

# template.html

- **{{ variable_name }}** - notice how the double curly braces is how we are able to pass parameters from python to the html page.

``` html
<!DOCTYPE html>
<head>
  <title>{{ page_title }}</title>

</head>
<body>

    {% block content %}
    {% end block %}

</body>
</html>
```

# index.html
``` html
{% extends "template.html" %}
{% block content %}

		<h2>{{ page_heading }}</h2>
		<br>
		<p>This is the index page</p>

{% end block %}
```

# Run the application
![[Pasted image 20240507122311.png]]
![[Pasted image 20240506094315.png]]
