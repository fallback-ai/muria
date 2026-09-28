# Source: https://cactuscompute.com/docs/v1.6/transcription

Transcription

# Transcription

Audio transcription with streaming support

## [Basic Transcription](#basic-transcription)

FlutterKotlinCLI

From FileFrom PCM Data

```auto
final result = model.transcribe('/path/to/audio.wav');
print(result.text);
```

```auto
// 16kHz mono PCM
final pcmData = Uint8List.fromList([...]);
final result = model.transcribePcm(pcmData);
print(result.text);
```

From FileFrom PCM Data

```auto
val result = model.transcribe("/path/to/audio.wav")
println(result.text)
```

```auto
val pcmData: ByteArray = ... // 16kHz mono PCM
val result = model.transcribe(pcmData)
println(result.text)
```

```auto
# Transcribe an audio file
cactus transcribe openai/whisper-small --file recording.mp3

# Live microphone transcription
cactus transcribe UsefulSensors/moonshine-base
```

## [Streaming Transcription](#streaming-transcription)

Real-time transcription with incremental results.

FlutterKotlin

```auto
final stream = model.createStreamTranscriber();
stream.insert(audioChunk1);
stream.insert(audioChunk2);

final partial = stream.process();
print('Partial: ${partial.text}');

final finalResult = stream.finalize();
print('Final: ${finalResult.text}');

stream.dispose();
```

```auto
model.createStreamTranscriber().use { stream ->
    stream.insert(audioChunk1)
    stream.insert(audioChunk2)

    val partial = stream.process()
    println("Partial: ${partial.text}")

    val final = stream.finalize()
    println("Final: ${final.text}")
}
```

## [Supported Models](#supported-models)

- **Whisper Small/Medium** - OpenAI Whisper with Apple NPU support
- **Moonshine-Base** - Lightweight transcription model

## [Performance Tips](#performance-tips)

- **NPU Acceleration** - Whisper models support Apple NPU for significantly faster transcription
- **Model Selection** - Whisper Small is faster, Whisper Medium is more accurate
- **Streaming** - Use streaming transcription for real-time applications
- **Memory** - Always call `dispose()` / `close()` when done to free resources

[Function Calling

Enable structured outputs and tool use with on-device language models](/docs/v1.6/function-calling)[RAG & Embedding

Embeddings, vector search, and retrieval-augmented generation](/docs/v1.6/rag)

### On this page

[Basic Transcription](#basic-transcription)[Streaming Transcription](#streaming-transcription)[Supported Models](#supported-models)[Performance Tips](#performance-tips)
