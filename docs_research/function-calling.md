# Source: https://cactuscompute.com/docs/v1.6/function-calling

Function Calling

# Function Calling

Enable structured outputs and tool use with on-device language models

## [Defining Tools](#defining-tools)

Tools are defined as JSON schemas that describe available functions:

FlutterKotlinC++

```auto
final tools = [
  {
    'name': 'get_weather',
    'description': 'Get weather for a location',
    'parameters': {
      'type': 'object',
      'properties': {
        'location': {'type': 'string', 'description': 'City name'}
      },
      'required': ['location']
    }
  }
];
```

```auto
val tools = listOf(
    mapOf(
        "name" to "get_weather",
        "description" to "Get weather for a location",
        "parameters" to mapOf(
            "type" to "object",
            "properties" to mapOf(
                "location" to mapOf("type" to "string", "description" to "City name")
            ),
            "required" to listOf("location")
        )
    )
)
```

```auto
const char* tools = R"([
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
])";
```

## [Calling with Tools](#calling-with-tools)

Pass tools to the completion call and parse the structured response:

FlutterKotlinC++

```auto
final result = model.completeMessages(
  [Message.user("What's the weather in Paris?")],
  tools: tools,
);

if (result.functionCalls != null) {
  for (final call in result.functionCalls!) {
    print('Function: ${call['name']}');
    print('Arguments: ${call['arguments']}');
  }
}
```

```auto
val result = model.complete(
    messages = listOf(Message.user("What's the weather in Paris?")),
    tools = tools
)

result.functionCalls?.forEach { call ->
    println("Function: ${call["name"]}")
    println("Arguments: ${call["arguments"]}")
}
```

```auto
char response[4096];
cactus_complete(
    model, messages, response, sizeof(response),
    nullptr,  // use default options
    tools,    // pass tools JSON
    nullptr,
    nullptr
);
```

The response JSON includes parsed function calls:

```auto
{
    "success": true,
    "function_calls": [{
        "name": "get_weather",
        "arguments": {"location": "Paris"}
    }],
    "response": null,
    "confidence": 0.91
}
```

## [Tool Schema Reference](#tool-schema-reference)

```auto
interface Tool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, {
      type: string;          // 'string', 'number', 'boolean', 'array', 'object'
      description?: string;
    }>;
    required?: string[];
  };
}
```

## [Tips](#tips)

- **Keep descriptions clear** — The model uses tool descriptions to decide which function to call
- **Use required fields** — Mark parameters as required when they are always needed
- **Smaller models** may struggle with complex multi-tool scenarios; use larger models for reliability
- **Cloud handoff** — If the model confidence is low on a tool call, consider routing to a cloud API for better accuracy

[LLM

Text generation, vision, streaming, and model options with Cactus](/docs/v1.6/llm)[Transcription

Audio transcription with streaming support](/docs/v1.6/transcription)

### On this page

[Defining Tools](#defining-tools)[Calling with Tools](#calling-with-tools)[Tool Schema Reference](#tool-schema-reference)[Tips](#tips)
