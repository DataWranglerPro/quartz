This is the language that I mostly worked with when working with [[Jenkins]].

# Variables
``` groovy
// using their type
String x = "Hellow World"
Integer n = 19
boolean flag = true

// using the def keyword
def x = "Hellow World"
def n = 19
def flag = true
```

# How to Print
``` groovy
// print without adding a newline character
print("Hellow World")

// print followed by a newline character
println("Hellow World")

// formatting strings
printf("%s is %d years old", "David", 305)
```

# Conditional Statements
``` groovy
if ( ... ) {
	// do something
} else if ( ... ) {
	// do something
} else {
	// do something
}
```

# Loops
``` groovy
// loop n number of times
for (into i=0; i < 5; i++) {
	println(i)
}

// loop using array, method 1
def myList = ["a", "b", "c"]

for (i in myList) {
	println(i)
}

// loop using array, method 2
def myList = ["a", "b", "c"]

myList.each { item ->
	println(i)
}
```

# Functions
``` groovy
// no parameters
def myFunction() {
	// do something
}

// with a return
def myFunction() {
	return "Hello World"
}

// with parameters
def myFunction(int a, int b, String c) {
	return a + b
}
```

# Exception Handling
``` groovy
try {
	// do something
} catch (Exception e) {
	println("INFO: An error occurred: ${e.message}")
}
```

