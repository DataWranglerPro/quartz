Here is an example on how we can pass parameters to out html pages directly from Python. This was one of the features of Tornado that I fell in love with.

With very little code, we can get a web application running. In my experience this has been excellent for simple web apps, they are very stable, and very easy to maintain.

Even thought I used to run www.hedaro.com using Tornado, I do not really recommend you use it for your personal website. I would use Tornado for dashboards or for some sort of back-end tool.  

## Folder structure

![[Pasted image 20240505141750.png]]
**root folder**
- static
- templates
	- index.html
	- template.html
- app.py


## App.py

Notice that I pass two parameters to the index.html page.

``` python
# Webserver stuff
import tornado.ioloop
import tornado.web

# route to index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html',
                    page_title = 'This is Amazing!!!',
                    page_heading = 'Welcome to Tornado'
        ) 

# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler)
],debug=True) 

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
![[Pasted image 20240506094353.png]]
![[Pasted image 20240506094315.png]]
