
# Background
At my job, when we run jobs in Jenkins, we end up saving the files we generated during the run in a third party repository. This is so the persons who are interested in seeing the results can go to this third party location and retrieve the results. In general, we never delete these files.

As you might expect, there are times where this 3rd party service is not available (down for maintenance, down for technical reasons, etc). In these situations, when the Jenkins job completes, the files that normally get saved are lost forever. Some people are not really happy about this situation, so it's up to me to come up with a solution.

# Solution
Since the 3rd party repository is 99% working without any issues, I only need to find a way to keep a copy of the files somewhere while I wait until the service is back up. A very easy way to accomplish this is to use the [[Jenkins]] plugin named **archiveArtifacts**.

![[Pasted image 20240502084621.png]]
- **archiveArtifacts** - Allows you to save as many files as needed to the results of the job itself. This means the files get saved in Jenkins and are available in the section named Build Artifacts as shown in the picture above.

Here is the simple groovy code:
``` groovy
archiveArtifacts "${filePathofFile}"
```

# Persistence?
Also note that depending on how you have configured your pipeline, these files may be deleted after some time. There is a pipeline setting named "Discard old builds" that if activated will delete this run from Jenkins after a certain number of days. This also means you will loose all the files you have archived. So be mindful of this and double check your settings.

