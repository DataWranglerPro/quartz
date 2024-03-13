[[Jenkins]] is a [[CI CD]] (Continuous Integration and Continuous Delivery) tool I have used at work. The team that I was a part of was a subset of QA (Quality Assurance) and the team used Jenkins for test automation. 

I was the primary developer responsible for maintaining [[Jenkins]], which involved:
- Creating and maintaining all pipelines
- Maintaining all [[Groovy]] code that mainly resided in the shared library
- Monitoring the [[Jenkins]] service for outages and providing user support with issues as they came up

There was a separate team that installed [[Jenkins]] which I believed was run inside [[Kubernetes]]. This made it a challenge to manage the [[Jenkins]] plugins, mange any container images, and troubleshoot issues that required us to shell into the pod. For these kinds of activities, the trick was to maintain a good working relationship with the other team and ask for assistance as needed.

# Jenkinsfile
This is the file that contains the code that drives all the pipelines. In general, all of the pipelines I managed were in [[gitlab]] and the only important file in the repo was the [[jenkinsfile]]. This file was written in [[Groovy]] and you can say this was a good example of infrastructure as code.

> [!NOTE] Pro Tip
> Even though the code written in the [[jenkinsfile]] is mainly [[Groovy]], you will also find in this file [[Jenkins]] plugins that have their own syntax. This is important to note as I myself and other people I have worked with confuse [[Groovy]] code with code that references [[Jenkins]] plugins. 

Where do I find out what plugins I have available in my [[Jenkins]] environment?
- {https://YOUR_JENKINS_URL}/pipeline-syntax

What is the basic structure of a [[jenkinsfile]]?
The stages block defines the individual stages of a pipeline, and each stage contains a steps block that defines the steps to be executed in that stage.

``` groovy
pipeline {
	agent (where to execute, Jenkins agent)
	stages {
		stage("build") {
			steps {}
		}
	}
}
```

# Test/Development Process
At a high level, all development was done in [[Eclipse]] using a common branch for all the pipelines and the shared library. I had access to a Development folder in Jenkins where I had copies of all the production pipelines. I had the ability to point to my git branches in this development area and do all my development and testing here.

I usually had a branch for the pipeline, the shared library, and an application I was attempting to run tests against. At times you may be able to get away with a simple replay and some editing of the [[jenkinsfile]].

# Shared Library
There was a separate [[gitlab]] repository that was referred to as the shared library. This repo contained most of the [[Groovy]] code for [[Jenkins]] and at the top of every pipeline, we imported this library.

``` groovy
@Library('MY_SHARED_LIB@TAG_NAME') _
```

This repo had to be organized in a very specific manner and I learned this the hard way.
- **resources**
	- contains any non [[Groovy]] file
	- I maintained the [[Kubernetes]] pod configuration file here
- **src/a/b/c**
	- Any folder structure was allowed here
	- We maintained testing code, reporting code, etc
	- [[Groovy]] code has to be declared using a class
		- You will need to use the import syntax to access any of these files/functions in the [[jenkinsfile]]
- **vars**
	- **DO NOT** create sub folders here, this folder is meant to be flat
	- [[Groovy]] code can be as simple as a file with a bunch of functions
		- All of these functions will be available in the [[jenkinsfile]] without any extra code except the @Library syntax 

