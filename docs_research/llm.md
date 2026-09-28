# Source: https://cactuscompute.com/docs/v1.6/llm

LLM

# LLM

Text generation, vision, streaming, and model options with Cactus

## [Basic Completion](#basic-completion)

FlutterKotlinC++

```auto
import 'cactus.dart';

final model = Cactus.create('/path/to/model.gguf');
final result = model.complete('What is the capital of France?');
print(result.text);
model.dispose();
```

```auto
import com.cactus.*

val model = Cactus.create("/path/to/model")
val result = model.complete("What is the capital of France?")
println(result.text)
model.close()
```

```auto
#include <cactus.h>

cactus_model_t model = cactus_init("path/to/weight/folder", nullptr);

const char* messages = R"([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
])";

const char* options = R"({
    "max_tokens": 50,
    "stop_sequences": ["<|im_end|>"]
})";

char response[4096];
int result = cactus_complete(
    model, messages, response, sizeof(response),
    options, nullptr, nullptr, nullptr
);
```

**Response Format:**

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

## [Chat Messages](#chat-messages)

FlutterKotlin

```auto
final model = Cactus.create(modelPath);
final result = model.completeMessages([
  Message.system('You are a helpful assistant.'),
  Message.user('What is 2 + 2?'),
]);
print(result.text);
model.dispose();
```

```auto
Cactus.create(modelPath).use { model ->
    val result = model.complete(
        messages = listOf(
            Message.system("You are a helpful assistant."),
            Message.user("What is 2 + 2?")
        )
    )
    println(result.text)
}
```

## [Completion Options](#completion-options)

FlutterKotlin

```auto
final options = CompletionOptions(
  temperature: 0.7,
  topP: 0.9,
  topK: 40,
  maxTokens: 256,
  stopSequences: ['\n\n'],
);

final result = model.complete('Write a haiku:', options: options);
```

```auto
val options = CompletionOptions(
    temperature = 0.7f,
    topP = 0.9f,
    topK = 40,
    maxTokens = 256,
    stopSequences = listOf("\n\n")
)

val result = model.complete("Write a haiku:", options)
```

## [Streaming](#streaming)

FlutterKotlinC++

```auto
final result = model.complete(
  'Tell me a story',
  callback: (token, tokenId) {
    print(token);
  },
);
```

```auto
val result = model.complete(
    messages = listOf(Message.user("Tell me a story")),
    callback = TokenCallback { token, tokenId ->
        print(token)
    }
)
```

```auto
void token_callback(const char* token, int token_id, void* user_data) {
    printf("%s", token);
    fflush(stdout);
}

cactus_complete(
    model, messages, response, sizeof(response),
    nullptr, nullptr,
    token_callback,  // streaming callback
    nullptr          // user data
);
```

## [Cloud Handoff](#cloud-handoff)

When the model lacks confidence, the response signals a cloud handoff:

FlutterKotlinC++

The `CompletionResult` includes `needsCloudHandoff` and `confidence` fields. Check these to decide whether to route to a cloud API.

The `CompletionResult` includes `needsCloudHandoff` and `confidence` fields. Check these to decide whether to route to a cloud API.

```auto
{
    "success": true,
    "cloud_handoff": true,
    "response": null,
    "confidence": 0.42
}
```

Your application should route to a cloud API when `cloud_handoff` is `true`.

## [Performance Tips](#performance-tips)

- **Model Selection** - Use smaller models (`lfm2-350m`) for faster inference on mobile
- **Quantization** - `int4` uses less memory, `int8` is more accurate
- **NPU Acceleration** - Available on Apple devices for vision and transcription models
- **Memory** - Always call `dispose()` / `close()` when done to free resources
- **Reuse model handles** across requests (don't reinitialize)

[Quickstart

Install Cactus and run your first on-device AI model](/docs/v1.6/quickstart)[Function Calling

Enable structured outputs and tool use with on-device language models](/docs/v1.6/function-calling)

### On this page

[Basic Completion](#basic-completion)[Chat Messages](#chat-messages)[Completion Options](#completion-options)[Streaming](#streaming)[Cloud Handoff](#cloud-handoff)[Performance Tips](#performance-tips)
