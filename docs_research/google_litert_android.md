# Source: https://developers.google.com/edge/litert/android

- [Home](https://developers.google.com/)
- [Products](https://developers.google.com/products)
- [Google AI Edge](https://developers.google.com/edge)
- [LiteRT](https://developers.google.com/edge/litert)

Send feedback

# LiteRT for Android Stay organized with collections Save and categorize content based on your preferences.

The following LiteRT runtime APIs are available for Android development:

- **`CompiledModel`** API: The modern standard for **high-performance**
  inference, streamlining hardware acceleration across CPU/GPU/NPU. Learn more
  about [why to choose the CompiledModel API](https://developers.google.com/edge/litert/inference).
- **`Interpreter`** API: the basic inference API, maintained for backward
  compatibility.

## Get Started with `CompiledModel` API

- **For classical ML models**, see the following demo apps.

  - [Image segmentation Kotlin App](https://github.com/google-ai-edge/litert-samples/tree/main/samples/litert/image_segmentation): CPU/GPU/NPU inference.
  - [Image segmentation C++ App](https://github.com/google-ai-edge/litert-samples/tree/main/samples/litert/image_segmentation/c%2B%2B_segmentation): CPU/GPU/NPU inference with
    **async** execution.
- **For GenAI models**, see the following demo apps:

  - [EmbeddingGemma semantic similarity C++ App](https://github.com/google-ai-edge/litert-samples/tree/main/samples/litert/semantic_similarity/build_from_source):
    CPU/GPU/NPU inference.

## Supported Android Versions and APIs

| LiteRT Version | Status | Supported API | Min SDK Level | Min NDK version (if used) | Release Date |
| --- | --- | --- | --- | --- | --- |
| **`v2.2.0`** | ✅ Latest | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-08-14 |
| **`v2.1.6`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-07-07 |
| **`v2.1.5`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-05-15 |
| **`v2.1.4`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-04-10 |
| **`v2.1.3`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-03-16 |
| **`v2.1.1`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2026-01-27 |
| **`v2.1.0`** | ⚠️ Legacy | `CompiledModel`   `Interpreter`(CPU only) | `23` (Android 6 Marshmallow) | `r26a` | 2025-12-19 |
| **`v2.0.3`** | ⚠️ Legacy | `CompiledModel` | `26` (Android 8 Oreo) | `r26a` | 2025-11-08 |
| **`v1.4.2`** | ✅ Latest | `Interpreter` | `21` (Android 5 Lollipop) | `r26a` | 2026-03-16 |
| **`v1.4.1`** | ⚠️ Legacy | `Interpreter` | `21` (Android 5 Lollipop) | `r26a` | 2025-11-07 |
| **`v1.4.0`** | ⚠️ Legacy | `Interpreter` | `26` (Android 8 Oreo) | `r26a` | 2025-06-25 |
| **`v1.3.0`** | ⚠️ Legacy | `Interpreter` | `21` (Android 5 Lollipop) | `r26a` | 2025-05-19 |
| **`v1.2.0`** | ⚠️ Legacy | `Interpreter` | `21` (Android 5 Lollipop) | `r26a` | 2025-03-13 |

**Important:** *Keep your dependencies up to date to ensure compatibility with
the latest features and security updates.*

## Quickstart with `CompiledModel` API

Add the LiteRT Maven package to your Android project:

```auto
dependencies {
  ...
  implementation `com.google.ai.edge.litert:litert:2.1.0`
}
```

Integrate your `.tflite` model with the `CompiledModel` API. The following code
snippet shows the basic implementation in Kotlin and C++.

### Kotlin

```auto
// Load model and initialize runtime
val compiledModel = CompiledModel.create(
    "/path/to/mymodel.tflite",
    CompiledModel.Options(Accelerator.CPU))

// Preallocate input/output buffers
val inputBuffers = compiledModel.createInputBuffers()
val outputBuffers = compiledModel.createOutputBuffers()

// Fill the input buffer
inputBuffers.get(0).writeFloat(input0)
inputBuffers.get(1).writeFloat(input1)

// Invoke
compiledModel.run(inputBuffers, outputBuffers)

// Read the output
val output = outputBuffers.get(0).readFloat()
```

### C++

```auto
// Load model and initialize runtime
LITERT_ASSIGN_OR_RETURN(auto env, GetEnvironment());
LITERT_ASSIGN_OR_RETURN(auto options, GetOptions());
LITERT_ASSIGN_OR_RETURN(
    auto compiled_model,
    CompiledModel::Create(env, "/path/to/mymodel.tflite", options));

// Preallocate input/output buffers
LITERT_ASSIGN_OR_RETURN(auto input_buffers,compiled_model.CreateInputBuffers(signature_index));
LITERT_ASSIGN_OR_RETURN(auto output_buffers,compiled_model.CreateOutputBuffers(signature_index));

// Fill the input buffer
LITERT_ABORT_IF_ERROR(input_buffers[0].Write(input0));
LITERT_ABORT_IF_ERROR(input_buffers[1].Write(input1));

// Invoke
LITERT_ABORT_IF_ERROR(compiled_model.Run(signature_index, input_buffers, output_buffers));

// Read the output
LITERT_ABORT_IF_ERROR(output_buffers[0].Read(output0));
```

Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-09-15 UTC.

Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-09-15 UTC."],[],[]]
