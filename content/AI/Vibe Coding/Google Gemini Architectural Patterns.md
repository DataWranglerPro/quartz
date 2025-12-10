Below you will find all the architectural patterns, strategies, and "first principles" for building applications with the Google GenAI SDK.

---

### 1. First Principles of the Architecture

The core philosophy across many Gemini apps is a **stateless logic with stateful context**.
*   **The Client:** You always instantiate a singleton `GoogleGenAI` client.
*   **The Model:** You don't "run" the model; you select a model variant (`flash` for speed/audio, `pro` for logic/code, `imagen` for visuals) and send it a state (context).
*   **The Modality:** The input is rarely just text. It is a mix of `text`, `inlineData` (images/files), and `functionDeclarations`.

### 2. Pattern A: The "Text-In, Text-Out" (Standard GenAI)
**Used in:** `codeToTutorial.txt`, `teacherSimulation.txt`

This is the simplest architecture. It follows a Request-Response cycle.

*   **Setup:**
    ```typescript
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    const model = ai.getGenerativeModel({ model: "gemini-2.5-pro" });
    ```
*   **Prompt Engineering Strategy:**
    *   **Role Definition:** Use `systemInstruction` to set the persona ("You are an expert...").
    *   **Context Injection:** If analyzing code (like in `codeToTutorial.txt`), you must manually serialize your file system into a string (e.g., `// FILE: path/to/file \n content`) and inject it into the prompt.
*   **Pattern:** `generateContent` is stateless. If you need a conversation, you use `startChat` which maintains a `history` array in memory on the client side.

### 3. Pattern B: Structured Deterministic Output (JSON Mode)
**Used in:** `githubRoadmap.txt`, `mindMap.txt`, `presenter.txt`

When you need the AI to drive a UI (render a mind map, a roadmap, or slides), you cannot rely on free text. You must enforce a schema.

*   **The Schema Strategy:**
    Instead of asking for JSON in the prompt, you define a `Schema` object using the SDK's `Type` enum.
*   **The Call:**
    ```typescript
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash', // Flash is usually sufficient and faster for JSON
        contents: prompt,
        config: {
            responseMimeType: 'application/json', // CRITICAL
            responseSchema: mySchemaObject // Defined using Type.OBJECT, Type.ARRAY, etc.
        },
    });
    ```
*   **Result:** The `response.text()` is guaranteed to be a valid JSON string matching your schema, which you immediately `JSON.parse()`.

### 4. Pattern C: The "Agentic" Loop (Function Calling/Tools)
**Used in:** `Excel.txt`, `genCodePro.txt`, `deliverance.txt`

This is how you bridge the AI to the real world (database, filesystem, spreadsheet state).

*   **The Strategy:**
    1.  **Define Tools:** Create `FunctionDeclaration` objects describing *what* the AI can do (e.g., `updateSheetData`, `saveFile`).
    2.  **Pass to Model:** Attach these to the `tools` config in `connect` or `generateContent`.
    3.  **The Loop (Automatic vs Manual):**
        *   **Standard API:** The model returns a `functionCall`. You execute it locally. You send the result back (User: "result is X"). The model continues.
        *   **Live API (Real-time):** The model sends a `toolCall` message via WebSocket. You execute it. You send a `toolResponse` message back.
*   **Key Insight:** In `Excel.txt`, the "System Instruction" tells the AI *how* to use the tools (e.g., "Always call getCurrentSheetData() first"). The AI relies on these tools to "see" the application state.

### 5. Pattern D: The Multimodal Live API (Real-time Audio/Video)
**Used in:** `deliverance.txt`, `javaTutor.txt`, `openDoors.txt`

This is the most complex architecture. It bypasses HTTP REST calls in favor of a persistent WebSocket connection.

*   **Connection Lifecycle:**
    1.  **Connect:** `ai.live.connect({ config: { responseModalities: [Modality.AUDIO] } })`.
    2.  **Handshake:** The SDK handles the WebSocket handshake.
*   **Audio Pipeline (The "Plumbing"):**
    *   **Input (Mic):** You need an `AudioContext` (16kHz). You capture the mic stream, convert it to PCM (Pulse Code Modulation), and send it via `session.sendRealtimeInput({ media: { data: base64PCM, mimeType: 'audio/pcm' } })`.
    *   **Output (Speaker):** The server sends PCM chunks (usually 24kHz). You must decode these chunks into an `AudioBuffer` and queue them in an `AudioContext` to play sequentially.
*   **Handling Interruptions:**
    *   In `javaTutor.txt`, if the user speaks, the server sends an `interrupted: true` flag. You **must** immediately clear your client-side audio playback queue, or the AI will keep talking over the user.
*   **State Management:**
    *   Unlike REST, this is stateful. The server keeps the context until you call `session.close()`.

### 6. Pattern E: Media Generation (Images, Video, TTS)
**Used in:** `socialStudio.txt`, `elsa.txt`, `languagetutor.txt`

*   **Image Gen:** Uses `gemini-2.5-flash-image` (or Imagen 3). Returns raw base64 data.
*   **Video Gen:** Uses `veo` (experimental). This is an asynchronous operation. You submit a job (`generateVideos`) and poll for completion (`getVideosOperation`) because video rendering takes time.
*   **TTS (Text-to-Speech):**
    *   **REST Approach (`languagetutor.txt`):** You send text, get a blob back, play it. Good for static content.
    *   **Live Approach (`openDoors.txt`):** You stream audio chunks. Good for conversation.

---

### Summary of Models & When to Use Them

Based on your code, here is the selection strategy:

| Capability                 | Model to Use                            | Why?                                                                           |
| :------------------------- | :-------------------------------------- | :----------------------------------------------------------------------------- |
| **Complex Logic / Coding** | `gemini-2.5-pro` or `gemini-3-pro`      | Highest reasoning capability; better at following complex system instructions. |
| **Real-time Audio**        | `gemini-2.5-flash-native-audio-preview` | Low latency; specialized for speech-to-speech.                                 |
| **JSON / Simple Tasks**    | `gemini-2.5-flash`                      | Fastest, cheapest, follows schemas well.                                       |
| **Image Creation**         | `gemini-2.5-flash-image`                | Specialized for visual output.                                                 |
| **Video Creation**         | `veo-3.1-fast-generate-preview`         | The only model capable of temporal video generation.                           |

---

### Missing Patterns & "Tricks" (Not in your 13 files)

You have a very comprehensive set of examples, but here are advanced patterns missing that would take these apps to production level:

**1. Context Caching (The Cost Saver)**
*   **Scenario:** In `genCodePro.txt` or `teacherSimulation.txt`, if you are feeding a massive codebase or a textbook into the context every single time, it's slow and expensive.
*   **The Trick:** Use the **Context Caching API**. You upload the heavy context (files/books) once, get a cache key, and pass that key to the model. This drastically reduces Latency and Cost (Input tokens are cheaper when cached).

**2. Embeddings & RAG (Retrieval Augmented Generation)**
*   **Scenario:** In `codeToTutorial.txt`, if the project has 1,000 files, you cannot fit them all in the prompt string.
*   **The Trick:** Use `ai.models.embedContent`. Convert your files into vector numbers. Store them. When the user asks a question, find the relevant file snippets via vector search, and *only* inject those snippets into the Gemini prompt.

**3. "Thinking" Model Configuration**
*   **Scenario:** In `teacherSimulation.txt`, you used `thinkingBudget`, but this is a specific feature for models like `gemini-2.0-flash-thinking`.
*   **The Trick:** Explicitly using the **Thinking Model** allows the AI to output a hidden "thought process" block before the final answer. This dramatically improves performance on math, puzzles, or complex logic (like "deliverance" discernment) by allowing the model to "scratchpad" its ideas before speaking.

**4. Safety Settings Configuration**
*   **Scenario:** In `codeToTutorial.txt`, you catch a generic `SAFETY` error.
*   **The Trick:** You can granularly control this in the `config`.
    ```typescript
    safetySettings: [
        { category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold: HarmBlockThreshold.BLOCK_NONE }
    ]
    ```
    This is often necessary for creative writing or "villain" roleplay apps where standard safety filters might trigger false positives.

**5. Token Counting**
*   **Scenario:** Before sending a request in `githubRoadmap.txt`, you don't know if it fits context.
*   **The Trick:** Use `model.countTokens(prompt)`. This allows you to fail gracefully or truncate data *before* spending money on the API call.