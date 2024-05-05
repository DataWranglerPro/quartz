Tornado is a [[Python]] Web Framework. When I was learning web development, this was my go to back-end library. Below are all the notes I have on my web learnings.

# Folder structure

**root folder**
- static
- templates
	- index.html
	- template.html
- app.py


# App.py
This is the python back-end code
``` python
# Webserver stuff
import tornado.ioloop
import tornado.web

# route to index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html') 

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


# Front-end code
The idea is to create a base html file named *template.html* and then build all other html files on top of the template. This made the html files much cleaner an easier to maintain.


### template.html
``` html
<!DOCTYPE html>
<head>
  <title>Tornado</title>
</head>
<body>


    {% block content %}
    {% end block %}

	
</body>
</html>
```

### index.html
``` html
{% extends "template.html" %}
{% block content %}

		<h2>Welcome to Tornado</h2>
		<br>
		<p>This is the index page</p>

{% end block %}
```


![[Pasted image 20240505085539.png]]