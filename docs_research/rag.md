# Source: https://cactuscompute.com/docs/v1.6/rag

RAG & Embedding

# RAG & Embedding

Embeddings, vector search, and retrieval-augmented generation

## [Embeddings](#embeddings)

Generate text, image, and audio embeddings on-device.

FlutterKotlin

```auto
// Text embeddings
final embedding = model.embed('Hello, world!');

// Image embeddings
final imageEmbedding = model.imageEmbed('/path/to/image.jpg');

// Audio embeddings
final audioEmbedding = model.audioEmbed('/path/to/audio.wav');
```

```auto
// Text embeddings
val embedding = model.embed("Hello, world!")

// Image embeddings
val imageEmbedding = model.imageEmbed("/path/to/image.jpg")

// Audio embeddings
val audioEmbedding = model.audioEmbed("/path/to/audio.wav")
```

## [Auto-RAG](#auto-rag)

Pass a corpus directory at model initialization for automatic retrieval-augmented generation.

FlutterKotlinC++

```auto
final model = Cactus.create(
  '/path/to/model.gguf',
  corpusDir: '/path/to/documents',
);

final result = model.complete('What does the documentation say about X?');
```

```auto
val model = Cactus.create(
    modelPath = "/path/to/model",
    corpusDir = "/path/to/documents"
)

val result = model.complete("What does the documentation say about X?")
```

```auto
cactus_model_t model = cactus_init(
    "path/to/weight/folder",
    "path/to/rag/documents", // auto-RAG corpus directory
);

char response[4096];
cactus_complete(model, messages, response, sizeof(response),
    nullptr, nullptr, nullptr, nullptr);
```

## [Vector Index](#vector-index)

Build and query an on-device vector index for similarity search.

FlutterKotlin

```auto
final index = CactusIndex.create('/path/to/index', embeddingDim: 384);

index.add(
  ids: [1, 2],
  documents: ['Document 1', 'Document 2'],
  embeddings: [
    model.embed('Document 1'),
    model.embed('Document 2'),
  ],
);

final results = index.query(model.embed('search query'), topK: 5);
for (final r in results) {
  print('ID: ${r.id}, Score: ${r.score}');
}

index.dispose();
```

```auto
CactusIndex.create("/path/to/index", embeddingDim = 384).use { index ->
    val embeddings = arrayOf(model.embed("doc1"), model.embed("doc2"))

    index.add(
        ids = intArrayOf(1, 2),
        documents = arrayOf("Document 1", "Document 2"),
        embeddings = embeddings
    )

    val results = index.query(model.embed("search query"), topK = 5)
    results.forEach { println("ID: ${it.id}, Score: ${it.score}") }
}
```

## [Tokenization](#tokenization)

FlutterKotlin

```auto
final tokens = model.tokenize('Hello, world!');
final scores = model.scoreWindow(tokens, 0, tokens.length, 512);
```

```auto
val tokens = model.tokenize("Hello, world!")
val scores = model.scoreWindow(tokens, start = 0, end = tokens.size, context = 512)
```

[Transcription

Audio transcription with streaming support](/docs/v1.6/transcription)[CLI Reference

Command-line interface for Cactus LLM completion, transcription, and function calling](/docs/v1.6/cli)

### On this page

[Embeddings](#embeddings)[Auto-RAG](#auto-rag)[Vector Index](#vector-index)[Tokenization](#tokenization)
