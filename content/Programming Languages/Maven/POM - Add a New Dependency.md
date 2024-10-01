Here are the steps I take to add a new JAR dependency to my Maven project.  
  
# 𝐒𝐭𝐞𝐩 1:  
I open my applications pom.xml file  

# 𝐒𝐭𝐞𝐩 2:
I recommend to use the `properties` section to create a new tag that holds the version number of the JARs you are trying to add. This way, you can control version numbers in a centralized location.  

Here is an example: 
``` xml
<properties>  
	<opentelemetry.version>1.41.0</opentelemetry.version>  
</properties>  
```

# 𝐒𝐭𝐞𝐩 3:  
I then add the JARs to the section named `dependencies` and make sure to use the property created above.  
  
``` xml
<dependencies>  
	<dependency>  
		<groupId>io.opentelemetry</groupId>  
		<artifactId>opentelemetry-api<artifact-Id>  
		<version>${opentelemetry.version}</version>  
		<scope>compile</version>  
	</dependency>  
</dependencies>
```