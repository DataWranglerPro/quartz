This is the lesson that I am the most excited to show you. This is the lesson that opens up a lot of opportunities if you understand the concepts and the code. 

I will show you how to route using Tornado.
- How to handle http://localhost:7777/about?
	- What is the code to navigate to the about html page?

I will show you how to move data from the back-end to the front-end
- How to create a pandas DataFrame and show that data:
	- As a json object (great for api scenarios)
	- as a table (great for a basic html page)

The folder structure is very similar as all the previous lessons. I do have some additional python files in the root. These files could probably moved to a new folder under the static folder, but I kept them here for now.
## Folder structure

![[Pasted image 20240509070142.png]]
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
	- SampleLayout1.html
	- welcome.html
- app.py
- HtmlTblExample.py
- JsonExample.py


## HtmlTblExample.py

Here I simply create some fake data and return an html object. We will use this function to show an html table to the user.

Note that I am passing [[bootstrap]] class names to the html table.

``` python
import pandas as pd

def html():

    # Create a simple df
    df = pd.DataFrame(data=[1,2,3,4,5], columns=['Revenue'])

    # Add columns
    df['bii'] = 'foo'
    df['Test'] = df['Revenue']*125
    df['Test1'] = df['Revenue']*125
    df['Test2'] = df['Revenue']*125
    df['Test3'] = df['Revenue']*125
    df['Test4'] = df['Revenue']*125

    return df.to_html(index=False, classes="table table-hover table-striped")
```

## JsonExample.py

Here I create some fake data and simply return a json object. JSON is a very common format you will encounter in the wild, so I added it here. We will display this json string on a web page very soon.

``` python
import pandas as pd

def to_json(): 

    # Create a simple df
    df = pd.DataFrame(data=[1,2,3,4,5], columns=['Revenue'])

    # Add a column
    df['bii'] = 'foo'

    return df.to_json()
```


## App.py

Take a close look at all the new code as it has been placed here so you can see how to:

- Call functions
	- Look how I imported the extra two python scripts and then used them throughout the code
- Display html content
	- Look how the **tbl** variable is passed to Tornado. See how the index.html page looks for the **tbl** variable and displays it.
- Routing
	- Look at the section that has r"/data2" and see how you can handle different kinds of http requests on your web application. 

``` python
# Webserver stuff
import tornado.ioloop
import tornado.web

# User created scripts
from JsonExample import to_json
from HtmlTblExample import html

# Utility libraries
import os.path

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    page_title = 'This is Amazing!!!',
                    company_name = 'Business Intelligence',
                    tbl = html()
        ) 

class welcome(tornado.web.RequestHandler):
    def get(self):
        self.render('welcome.html',
                    page_title = 'This is Amazing!!!',
                    company_name = 'Business Intelligence'
        )

class data(tornado.web.RequestHandler):
    def get(self):
        self.write(to_json())

class data2(tornado.web.RequestHandler):
    def get(self):
        self.write(html())
        
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

# r"/" == root website address
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/welcome", welcome),
    (r"/data", data),
    (r"/data2", data2)
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

Nothing new or exciting on the template file.

``` html
<!DOCTYPE html>
<head>
  <title>{{ escape(page_title) }}</title>
  <link href="{{ static_url('css/bootstrap.min.css') }}" rel="stylesheet">
  <script src="{{ static_url('js/bootstrap.bundle.min.js') }}"></script>
</head>
<body>

    <div class="container">
    {% block content %}
    {% end block %}
    </div>

</body>
</html>
```

# index.html

Notice how I had to add the raw keyword to display the html table correctly. Also note that you will be experimenting with a lot of bootstrap and html code. This is probably my least favorite thing about front-end coding. You have to try many many variations to get the final result you are looking for.

``` html
{% extends "template.html" %}
{% block content %}

    <div class="container">
    	<br/>
        <br/>
        <br/>
        <h2>Welcome to Tornado</h2>
		<br/>

		  <div class="row">
			<div class="col-2">
				{% raw tbl %}
			</div>
		  </div>	

		
	</div>	

{% end block %}
	
// {% autoescape None %} if you put this at the top, it will affect everything
// {% raw *expression* %} does not escape the expression
```

## welcome.html

Very basic web page.

``` html
{% extends "template.html" %}
{% block content %}
    <div class="container">
		<h2>Welcome to Tornado</h2>
		<br>
		<p>This is the welcome page</p>
	</div>
{% end block %}
```


## SampleLayout1.html

Here is a challenge for you. See if you can get this html page to render. You have to make some changes to the app.py file. 

``` html
{% extends "template.html" %}
{% block content %}
    <div class="container">
    	<br/>
        <br/>
        <br/>
        <h2>Welcome to Tornado</h2>
		<br/>
            
		<!--Place two tables side by side-->
		<div class="row">
			<div class="col-6">{% raw tbl %}</div>
			<div class="col-4">{% raw tbl %}</div>
		</div>

		<!--Add a little space between the tables-->
		<br/>
		<br/>
		<br/>

		<!--Place two tables side by side-->
		<div class="row">
			<div class="col-6">{% raw tbl %}</div>
			<div class="col-4">{% raw tbl %}</div>
		</div>

	</div>

{% end block %}
	
// {% autoescape None %} if you put this at the top, it will affect everything
// {% raw *expression* %} does not escape the expression
```

# Run the application

![[Pasted image 20240509081037.png]]

![[Pasted image 20240509081107.png]]

![[Pasted image 20240509081136.png]]

![[Pasted image 20240509081206.png]]

![[Pasted image 20240509081233.png]]

Here is how the SampleLayout1.html looks like. Yes, the picture is cutoff at the bottom. Hopefully you were able to get this page to render. It is a very small code change.

![[Pasted image 20240509081333.png]]