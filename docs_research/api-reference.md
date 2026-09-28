# Source: https://cactuscompute.com/docs/v1.6/api-reference

API Reference

# API Reference

Complete API reference for all Cactus SDKs

Complete class and type definitions for each SDK.

FlutterKotlinC++

## [Cactus](#cactus)

```auto
class Cactus {
  static Cactus create(String modelPath, {String? corpusDir});

  CompletionResult complete(
    String prompt,
    {CompletionOptions options, void Function(String, int)? onToken}
  );

  CompletionResult completeMessages(
    List<Message> messages,
    {CompletionOptions options, List<Map<String, dynamic>>? tools, void Function(String, int)? onToken}
  );

  TranscriptionResult transcribe(String audioPath, {String? prompt, TranscriptionOptions options});
  TranscriptionResult transcribePcm(Uint8List pcmData, {String? prompt, TranscriptionOptions options});

  List<double> embed(String text, {bool normalize = true});
  List<double> imageEmbed(String imagePath);
  List<double> audioEmbed(String audioPath);
  String ragQuery(String query, {int topK = 5});

  List<int> tokenize(String text);
  String scoreWindow(List<int> tokens, int start, int end, int context);
  StreamTranscriber createStreamTranscriber();

  void reset();
  void stop();
  void dispose();

  static String getLastError();
}
```

## [Message](#message)

```auto
class Message {
  static Message system(String content);
  static Message user(String content);
  static Message assistant(String content);
}
```

## [CompletionOptions](#completionoptions)

```auto
class CompletionOptions {
  final double temperature;
  final double topP;
  final int topK;
  final int maxTokens;
  final List<String> stopSequences;
  final double confidenceThreshold;

  static const defaultOptions;
}
```

## [CompletionResult](#completionresult)

```auto
class CompletionResult {
  final String text;
  final List<Map<String, dynamic>>? functionCalls;
  final int promptTokens;
  final int completionTokens;
  final double timeToFirstToken;
  final double totalTime;
  final double prefillTokensPerSecond;
  final double decodeTokensPerSecond;
  final double confidence;
  final bool needsCloudHandoff;
}
```

## [TranscriptionResult](#transcriptionresult)

```auto
class TranscriptionResult {
  final String text;
  final List<Map<String, dynamic>>? segments;
  final double totalTime;
}
```

## [StreamTranscriber](#streamtranscriber)

```auto
class StreamTranscriber {
  void insert(Uint8List pcmData);
  TranscriptionResult process({String? language});
  TranscriptionResult finalize();
  void dispose();
}
```

## [CactusIndex](#cactusindex)

```auto
class CactusIndex {
  static CactusIndex create(String indexDir, {required int embeddingDim});

  void add({
    required List<int> ids,
    required List<String> documents,
    required List<List<double>> embeddings,
    List<String>? metadatas
  });

  void delete(List<int> ids);
  List<IndexResult> query(List<double> embedding, {int topK = 5});
  void compact();
  void dispose();
}

class IndexResult {
  final int id;
  final double score;
}
```

## [Cactus](#cactus-1)

```auto
object Cactus {
    fun create(modelPath: String, corpusDir: String? = null): Cactus
}

fun complete(
    prompt: String,
    options: CompletionOptions = CompletionOptions()
): CompletionResult

fun complete(
    messages: List<Message>,
    options: CompletionOptions = CompletionOptions(),
    tools: List<Map<String, Any>>? = null,
    callback: TokenCallback? = null
): CompletionResult

fun transcribe(
    audioPath: String,
    prompt: String? = null,
    language: String? = null,
    translate: Boolean = false
): TranscriptionResult

fun transcribe(
    pcmData: ByteArray,
    prompt: String? = null,
    language: String? = null,
    translate: Boolean = false
): TranscriptionResult

fun embed(text: String, normalize: Boolean = true): FloatArray
fun imageEmbed(imagePath: String): FloatArray
fun audioEmbed(audioPath: String): FloatArray
fun ragQuery(query: String, topK: Int = 5): String
fun tokenize(text: String): IntArray
fun scoreWindow(tokens: IntArray, start: Int, end: Int, context: Int): String
fun createStreamTranscriber(): StreamTranscriber
fun reset()
fun stop()
fun close()
```

## [Message](#message-1)

```auto
data class Message(val role: String, val content: String) {
    companion object {
        fun system(content: String): Message
        fun user(content: String): Message
        fun assistant(content: String): Message
    }
}
```

## [CompletionOptions](#completionoptions-1)

```auto
data class CompletionOptions(
    val temperature: Float = 0.7f,
    val topP: Float = 0.9f,
    val topK: Int = 40,
    val maxTokens: Int = 512,
    val stopSequences: List<String> = emptyList(),
    val confidenceThreshold: Float = 0f
)
```

## [CompletionResult](#completionresult-1)

```auto
data class CompletionResult(
    val text: String,
    val functionCalls: List<Map<String, Any>>?,
    val promptTokens: Int,
    val completionTokens: Int,
    val timeToFirstToken: Double,
    val totalTime: Double,
    val prefillTokensPerSecond: Double,
    val decodeTokensPerSecond: Double,
    val confidence: Double,
    val needsCloudHandoff: Boolean
)
```

## [TranscriptionResult](#transcriptionresult-1)

```auto
data class TranscriptionResult(
    val text: String,
    val segments: List<Map<String, Any>>?,
    val totalTime: Double
)
```

## [TokenCallback](#tokencallback)

```auto
fun interface TokenCallback {
    fun onToken(token: String, tokenId: Int)
}
```

## [StreamTranscriber](#streamtranscriber-1)

```auto
class StreamTranscriber : Closeable {
    fun insert(pcmData: ByteArray)
    fun process(language: String? = null): TranscriptionResult
    fun finalize(): TranscriptionResult
    override fun close()
}
```

## [CactusIndex](#cactusindex-1)

```auto
class CactusIndex : Closeable {
    companion object {
        fun create(indexDir: String, embeddingDim: Int): CactusIndex
    }

    fun add(
        ids: IntArray,
        documents: Array<String>,
        embeddings: Array<FloatArray>,
        metadatas: Array<String>? = null
    )

    fun delete(ids: IntArray)
    fun query(embedding: FloatArray, topK: Int = 5): List<IndexResult>
    fun compact()
    override fun close()
}

data class IndexResult(val id: Int, val score: Float)
```

## [Core Functions](#core-functions)

```auto
// Initialize a model
cactus_model_t cactus_init(
    const char* model_path,      // Path to weight folder
    const char* corpus_dir       // Optional: RAG corpus directory (or nullptr)
);

// Run completion
int cactus_complete(
    cactus_model_t model,        // Model handle from cactus_init
    const char* messages,        // Chat messages as JSON array
    char* response,              // Output buffer
    size_t response_size,        // Buffer size
    const char* options,         // Generation options JSON (or nullptr)
    const char* tools,           // Tool definitions JSON (or nullptr)
    void (*callback)(const char* token, int token_id, void* user_data),
    void* user_data              // User data passed to callback
);
```

## [Options JSON](#options-json)

```auto
{
    "max_tokens": 512,
    "stop_sequences": ["<|im_end|>"],
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40
}
```

## [Response JSON](#response-json)

```auto
{
    "success": true,
    "error": null,
    "cloud_handoff": false,
    "response": "The capital of France is Paris.",
    "function_calls": [],
    "confidence": 0.8193,
    "time_to_first_token_ms": 45.23,
    "total_time_ms": 163.67,
    "prefill_tps": 1621.89,
    "decode_tps": 168.42,
    "ram_usage_mb": 245.67,
    "prefill_tokens": 28,
    "decode_tokens": 50,
    "total_tokens": 78
}
```

## [Graph API](#graph-api)

```auto
class CactusGraph {
    Tensor input(std::vector<int> shape, Precision precision);
    Tensor matmul(Tensor a, Tensor b, bool transpose_b);
    Tensor transpose(Tensor t);

    void set_input(Tensor t, void* data, Precision precision);
    void execute();
    void* get_output(Tensor t);
    void hard_reset();
};
```

## [Precision Enum](#precision-enum)

```auto
enum class Precision {
    FP32,   // Full precision floating point
    FP16,   // Half precision
    INT8,   // 8-bit quantized
    INT4    // 4-bit quantized
};
```

See the [GitHub repository](https://github.com/cactus-compute/cactus) for the complete source code and additional usage examples.

[C++ Engine

Cactus Graph API, precision types, and native C++ engine internals](/docs/v1.6/cpp)

### On this page

[Cactus](#cactus)[Message](#message)[CompletionOptions](#completionoptions)[CompletionResult](#completionresult)[TranscriptionResult](#transcriptionresult)[StreamTranscriber](#streamtranscriber)[CactusIndex](#cactusindex)[Cactus](#cactus-1)[Message](#message-1)[CompletionOptions](#completionoptions-1)[CompletionResult](#completionresult-1)[TranscriptionResult](#transcriptionresult-1)[TokenCallback](#tokencallback)[StreamTranscriber](#streamtranscriber-1)[CactusIndex](#cactusindex-1)[Core Functions](#core-functions)[Options JSON](#options-json)[Response JSON](#response-json)[Graph API](#graph-api)[Precision Enum](#precision-enum)
