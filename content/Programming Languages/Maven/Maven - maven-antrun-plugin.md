After a major release to one of our pom.xml files, we started receiving messages that people's maven tests were failing.

**Example error:**
``` sh
2024-05-20 19:13:44 ERROR JunitTest:111 - Exception occurred!
java.lang.ClassNotFoundException: folder1.folder2.myScript
```

So on the previous version of our pom.xml, there were no issues. 

**Troubleshoot:**
The first thing I want to do is simply, replicate the issue. After having to fix a bunch of random bugs in the code, I finally was able to replicate he issue above.
- Fixed missing files
- Removed code added to pom.xml by tester

I also ran the code using the old pom.xml version and them compared both results. This is where I noticed the ant build section was not working. I expect text to appear after Executing Tasks, but nothing was happening.

``` sh
[INFO] --- maven-antrun-plugin:1.3:run (antrun-compile) @ myApp ---
[INFO] Executing tasks
[INFO] Executing tasks
```

The maven-antrun-plugin is used to run Apache Ant tasks from within a Maven build. Since the tasks were not being executed, the groovy files never made it to /target/classes and the maven test failed.

# root issue
We changed the configuration of the antrun plugin and even though I asked why this was changed and got a vague answer, we still committed those changes. I guess this is a lessons learned moment here.

Below is a proper configuration file. Instead of using tags named "tasks", we changed them to "target".

``` xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-antrun-plugin</artifactId>
  <version>1.3</version>
  <executions>
    <execution>
      <phase>process-resources</phase>
      <goals>
        <goal>run</goal>
      </goals>
      <configuration>
        <tasks>
          <!-- Define your Ant tasks here -->
          <echo message="Running Ant tasks from Maven!" />
        </tasks>
      </configuration>
    </execution>
  </executions>
</plugin>

```

Rolling back the changes to use the "tasks" tags fixed the issue. yay!
