I am not really a front-end type of guy. I have a hard time making things look pretty, so I try to outsource this as much as I can. My go-to front-end framework that takes care of making things look good is called [[bootstrap]]. 

Below is how I add all the relevant bootstrap artifacts and how to reference them in Tornado.
## Folder structure

![[Pasted image 20240505141750.png]]
**root folder**
- static
	- js
		- bootstrap.bundle.min.js
		- bootstrap.bundle.min.js.map
	- css
		- bootstrap.min.css
		- bootstrap.min.css.map
- templates
	- index.html
	- template.html
- app.py


## App.py

Not much has changed with the app.py file aside from an extra parameter passed to index.html. Most of the new stuff is on the front-end code.

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
                    page_heading = 'Welcome to Tornado',
                    company_name = 'Business Intelligence'
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

- Navigation bar - I copy pasted directly from website and made a few teaks to it.
	- https://getbootstrap.com/docs/5.3/components/navbar/
- Also take note on how I referenced the css/js bootstrap files

``` html
<!DOCTYPE html>
<head>
  <!-- Add css and javascript files -->
  <title>{{ page_title }}</title>
  <link href="{{ static_url('css/bootstrap.min.css') }}" rel="stylesheet">
  <script src="{{ static_url('js/bootstrap.bundle.min.js') }}"></script>
</head>
<body>

<!-- add menu bar -->
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
      <a class="navbar-brand" href="#">{{ company_name }}</a>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">About</a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>

    <!-- Add contents from index.html -->
    <div class="container">
    {% block content %}
    {% end block %}
    </div>
	
</body>
</html>
```

# index.html
``` html
{% extends "template.html" %}
{% block content %}

		<br>
		<br>
		<br>
		<br>
		<h2><center>{{ page_heading }}</center></h2>
		<br>
		<p><center>This is the index page</center></p>

{% end block %}
```

# Run the application
![[Pasted image 20240508105145.png]]
![[Pasted image 20240508105214.png]]
