At work we had a recent release to our shared pom.xml and users started to report issues. Below is one of those bug reports.

> Hi David! After switching to the new pom.xml, I am receiving the error below.

``` java
error: exception InterruptedException is never thrown in body of corresponding try statement
```
So what I did is start to look through the code and look at the changes to the new pom.xml file. 

The error above is just saying that whatever we have in the try block does not have the potential to throw a InterruptedException. This means something must have changed in the try block that is causing this issue since the user reported it used to work.

# Main.java

The issue is that the Helper.printMessage() method does not throw any Exceptions. Since main is trying to catch an Exception that will never get thrown, the compiler throws an error.

``` java
import com.example.Helper;

public class Main {
    public static void main(String[] args) {
        try {
	        // Call the method from Helper class
	        Helper.printMessage();
        } catch (InterruptedException e) {
            System.out.println("Caught InterruptedException: " + e.getMessage());
        }
    }
}
```

# Helper.java
``` java
public class Helper {
    public static void printMessage() {
        System.out.println("Hello from Helper class!");
    }
}
```


Now what I ended up finding out was that the Helper class used to throw the "InterruptedException" but it lo longer. This is going to require anyone who was calling the printMessage method remove any exception handling.