At my current job, [[java]] is the most widely used programming language in the automation team. I am definitely not an expert, but over this past year I have seen and written enough [[java]] to have a working knowledge of the language.

# Variables
In [[java]], variables are declared by specifying the data type, followed by the variable name.

``` java
String x = "Hello World";
int n = 19;
boolean flag = true;

// get the current date
import java.time.LocalDate;
LocalDate currentDate = LocalDate.now();

// here are other data structures we use in the team
import org.json.JSONObject;
import java.util.HashMap;
Map<String, JSONObject> uMap = new HashMap<>();
JSONObject jsonObject = new JSONObject();

import java.io.File;
File myDir - new File(someStringLocation);

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
List<Map<String, String>> data = new ArrayList<>();

String[] emptyArray = new String[0];
```

# How to Print
The team makes use of the logger library as shown below.

``` java
import org.apache.logging.log4j.Logger;

public class myClass {
	// declare this at the top of your class
	final static Logger logger = LogManager.getLogger(myClass.class);
	
	// you can now print to console
	logger.debug("Hello World!"); 
}
```

# Conditional Statements
These are the typical if/else code blocks.

``` java
if ( ... ) {
	// do something
} else if ( ... ) {
	// do something
} else {
	// do something
}
```

# Loops
Here are some common loops in [[java]].

``` java
// loop n number of times
for (int i = 0; i < 5; i++) {
	// do something
}

// loop using an array
import java.util.ArrayList;

// declare array variable
ArrayList<String> values = new ArrayList<>();

// add data to array
values.add("a");
values.add("b");
values.add("c");

// loop through array
for (String value : values) {
	logger.debug("value is: " + value);
}

// while loop
String myVar = "test";
while (myVar != null) {
	// do something

	// set myVar to null
	myVar = null;
}
```

# Functions
Here are a few ways to declare functions in [[java]]. You need to declare your functions/methods inside a class.

``` java
// function with no parameters
static void myMethod() {
	// function code
}

/*
Notes:
	- static indicates that the method belongs to the class and not an object
	- void specifies that the method does not return a value
	- you call this method via, myMethod();
*/

// function with a return and parameters
static int add(int num1, int num2) {
	return num1 + num2;
}

/*
Notes:
	- Notice we to declare the function with the data type you plan to return (integer was chosen for this example)
*/

// function with exception handling
static void myMethod() throws JSONException, IOException {
	// function code
}

/*
Notes:
	- Java is always bugging me about exception handling. This is normally done when you declare your functions. It will let the users of the function know which exceptions can be thrown by the method they are calling.
*/
```

# Exception Handling
``` java
try {
	// do something
} catch (IOException e) {
	// handle the exception
	logger.error(e.getMessage());
}
```

# Tips
- Make sure to name the .java file the same name as the class name inside the file.
	- This practice is essential because it helps in identifying the entry point of the program.
- Your classes will also need a "package" line at the top telling [[java]] where the file is located
	- i.e. package src.myClass.utils;
- Every class needs a main method/function.
- If you have a code repository like [[gitlab]], before searching the web or asking [[chatGPT]], look through the repositories as there is a high probability that the code you are looking for has already been written.


