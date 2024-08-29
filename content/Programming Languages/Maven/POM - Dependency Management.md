At work I manage a large POM file that has a gazillion jars. The problem I had was that 4 of those jars had the same dependency and I was getting a warning.

# SLF4J-API versions
- sqlcl was using v2.0.7
- HikariCP was using v1.7.36
- dbunit was using v1.7.25

This was causing Jenkins to throw the error/warning:
``` jenkins log
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder"
SLF4J: Defaulting to no-operation (NOP) logger implementation
```

# Solution
We can tell the POM file to always use the same version for all dependencies. This will make sure all jars use the same version and prevent any conflicts.

``` xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.6</version>
    </dependency>
  </dependencies>
</dependencyManagement>
```



