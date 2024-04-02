Helper function to get HTTP status code and content payload. 


In my example I was calling a rest api that returned a JSON string.
- https://github.com/GoogleChromeLabs/chrome-for-testing#json-api-endpoints

``` java
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

private static HTTPGetResult getStatusContent(String url){
	// declare variables
	int statusCode = 0;
	String statusResult = "";
	String jsonContent = "";

	try {
		// create http client object
		CloseableHttpClient httpclient = HttpClients.createDefault();

		// query url
		HttpGet httpGet = new HttpGet(url);
		CloseableHttpResponse response = httpclient.execute(httpGet);

		// get HTTP status code
		statusCode = response.getstatusLine().getstatusCode();

		// get the content
		HttpEntity entity = response.getEntity();
		if (entity != null) {
			jsonContent = EntityUtils.toString(entity);
		}
	} catch (Exception e) {
		statusResult = e.getMessage();
	} finally {
		if (httpclient != null) {
			httpclient.close();
		}
	}
	return new HTTPGetResult(statusCode, jsonContent);
}

public static class HTTPGetResult {
	private final int statusCode;
	private final String content;

	public HTTPGetResult(int statusCode, String content) {
		this.statusCode = statusCode;
		this.content = content;
	}

	public int getstatusCode() {
		return statusCode;
	}

	public String getContent() {
		return content;
	}
}
```