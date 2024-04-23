Here are some JSON helper functions that have served me well for some of my [[java]] projects.

``` java
/**
 * Generic JSON writer
 * 
 * @param filePath - file path of the new JSON file
 * @param key - string identifier for a piece of data
 * @param value - data associated with a specific key
 * @throws JSONException
 * @throws IOException
 */
public static JSONObject generateJsonObject(String filePath, String key, Object value) throws JSONException, IOException {
	JSONObject jsonObject = new JSONObject();
	// create file if it does not exist
	if (!exists(filePath)) {
		// add data to json object
		jsonObject.put(key, value);

		// save json object to disk
		saveJsonObject(jsonObject, filePath);
	} else {
		// read existing file
		JSONObject existingJsonObject.put(key, value);

		// save json object to disk
		saveJsonObject(existingJsonObject, filePath);		
	}

	return jsonObject;
}

/**
 * Does the file path exist
 * 
 * @param filePath - file path of a file
 */
public static boolean exists(String filePath) {
	File file = new File(filePath);
	return file.exists();
}

/**
 * Generic JSON reader
 * 
 * @param filePath - file path of JSON file
 * @throws JSONException
 * @throws IOException
 */
public static JSONObject readJsonObject(String filePath) throws JSONException, IOException {
	JSONObject jsonObject = null;
	
	// read JSON as string
	String jsonString = new       
	String(Files.readAllBytes(Paths.get(filePath).normalize()), "UTF-8");

	// parse into a JSON object
	jsonObject = new JSONObject(jsonString);
	
	return jsonObject;
}

/**
 * Basic JSON writer
 * 
 * @param jsonObject - JSON object
 * @param filePath - file path of JSON file
 * @throws JSONException
 * @throws IOException
 */
public static JSONObject generateJsonObject2(JSONObject jsonObject, String filePath) throws JSONException, IOException {
	FileWriter fileWriter = null;

	try {
		// open a FileWriter(filePath)
		fileWriter = new FileWriter(filePath);

		// write to file
		FileWriter.write(jsonObject.toString(4));

		// flush the buffer to ensure the data is written
		fileWriter.flush();

		// close the writer
		fileWriter.close();
	} catch (IOException e) {
		logger.error(e);
	} finally {
		// close the file
		if (fileWriter != null) {
			try {
				fileWriter.close();
			} catch (IOException e) {
				logger.error(e);
			}
		}
	}
}
```

