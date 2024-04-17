For any windows task, PowerShell is usually the go to language. You probably already have it installed, it's usually fast enough for scripting tasks, and it has a lot of built-in functionality for us Windows folks. I have used it at work to automate tasks, to create tools to install software, and manage user's environment variables.

# Variables
In PS, we do not need to declare the variables before using them. We also do not need to give the variables a type.

``` powershell
$a = 1
$b = "Hello World"
$c = $True
$d = Get-Date
```

# How to Print
``` powershell
Write-Output Hello World!

$name = "David"
Write-Output "My name is $($name)"
```

# Conditional Statements
These are typical if/else code blocks

``` powershell
$number = 5
if($number -gt 10) {
	Write-Output "The number is greater than 10."
} elseif ($number -eq 10) {
	Write-Output "The number is equal to 10."
} else {
	Write-Output "The number is less than 10."
}
```

- -gt, greater than
- -ge, greater than or equal to
- -lt, less than
- -le, less than or equal to
- -eq, equal to
- -ne, not equal to

# Loops
Here is how to do some common loops in PS.

``` powershell
# loop n number of times
for ($i=1; $i -le 5; $i++) {
	Write-Output "Iteration $i"
}

# loop using an array
$MODULES = "a", "b", "c"

foreach($MODULE in $MODULES){
	Write-Host $MODULE
}
```

# Functions
Here are a few ways to declare functions in PS

``` powershell
# functions with no parameters
def myFunction() {
	# function code
}

# function with a return
def myFunction() {
	return "Hellow World"
}

# function with parameters
def myFunction($CONFIG) {
	return $CONFIG"
}
```

# Exception Handling
``` powershell
try {
	# do something
} catch {
	Write-Output "An error occurred: $_"
}
```


