[[Jenkins]] has a plugin to send emails, below is a simple example on how you would call it. 

``` groovy
emailtext mimeType: 'text/html', body: "", subject: "", to: "", from: "${env.SOME_FOM_EMAIL_VARIABLE}"
```

It is important to note that the "body" needs to be formatted in HTML so it will appear just like you expect it when you open your email. 

I was saving a bunch of text into a variable and using it to log into the console and also using it for the email body. This got me into trouble when my emails where looking ugly and I realized that "/n" does not translate into a new line in an email message.

Here are some HTML code snippets that will work with the plugin:
``` html
<!-- how to add a line break, yes you can stack these <br/><br/> -->
<br/> 

<!-- how to create a list -->
<ul><li>list1</li><li>list2</li></ul>

<!-- how to bold text -->
<strong</strong>
```