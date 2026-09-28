# Source: https://cactuscompute.com/docs/v1.6/quickstart

Quickstart

# Quickstart

Install Cactus and run your first on-device AI model

## [Installation](#installation)

FlutterKotlinCLIC++

Clone and set up the Cactus repository:

```auto
git clone https://github.com/cactus-compute/cactus && cd cactus && git checkout v1.6.0 && source ./setup
```

Build the Flutter bindings:

```auto
cactus build --flutter
```

Output files:

| File | Platform |
| --- | --- |
| `libcactus.so` | Android (arm64-v8a) |
| `cactus-ios.xcframework` | iOS |
| `cactus-macos.xcframework` | macOS |
| `cactus.dart` | Dart FFI bindings |

Clone and set up the Cactus repository:

```auto
git clone https://github.com/cactus-compute/cactus && cd cactus && git checkout v1.6.0 && source ./setup
```

Build the Android bindings:

```auto
cactus build --android
```

Build output: `android/build/lib/libcactus.so`

macOSLinux

```auto
git clone https://github.com/cactus-compute/cactus && cd cactus && source ./setup
```

```auto
sudo apt-get install python3 python3-venv python3-pip cmake build-essential libcurl4-openssl-dev
git clone https://github.com/cactus-compute/cactus && cd cactus && source ./setup
```

Include the Cactus header in your project:

```auto
#include <cactus.h>
```

Build instructions are available in the [Cactus repository](https://github.com/cactus-compute/cactus).

## [Platform Integration](#platform-integration)

FlutterKotlin

### [Android](#android)

Copy `libcactus.so` to `android/app/src/main/jniLibs/arm64-v8a/`

Copy `cactus.dart` to your `lib/` folder

### [iOS](#ios)

Copy `cactus-ios.xcframework` to your `ios/` folder

Open `ios/Runner.xcworkspace` in Xcode

Drag the xcframework into the project

In Runner target > General > "Frameworks, Libraries, and Embedded Content", set to "Embed & Sign"

Copy `cactus.dart` to your `lib/` folder

### [macOS](#macos)

Copy `cactus-macos.xcframework` to your `macos/` folder

Open `macos/Runner.xcworkspace` in Xcode

Drag the xcframework into the project

In Runner target > General > "Frameworks, Libraries, and Embedded Content", set to "Embed & Sign"

Copy `cactus.dart` to your `lib/` folder

Android OnlyKotlin Multiplatform

1. Copy `libcactus.so` to `app/src/main/jniLibs/arm64-v8a/`
2. Copy `Cactus.kt` to `app/src/main/java/com/cactus/`

Source files:

| File | Copy to |
| --- | --- |
| `Cactus.common.kt` | `shared/src/commonMain/kotlin/com/cactus/` |
| `Cactus.android.kt` | `shared/src/androidMain/kotlin/com/cactus/` |
| `Cactus.ios.kt` | `shared/src/iosMain/kotlin/com/cactus/` |
| `cactus.def` | `shared/src/nativeInterop/cinterop/` |

Binary files:

| Platform | Location |
| --- | --- |
| Android | `libcactus.so` → `app/src/main/jniLibs/arm64-v8a/` |
| iOS | `libcactus-device.a` → link via cinterop |

Configure `build.gradle.kts`:

```auto
kotlin {
    androidTarget()

    listOf(iosArm64(), iosSimulatorArm64()).forEach {
        it.compilations.getByName("main") {
            cinterops {
                create("cactus") {
                    defFile("src/nativeInterop/cinterop/cactus.def")
                    includeDirs("/path/to/cactus/ffi")
                }
            }
        }
        it.binaries.framework {
            linkerOpts("-L/path/to/apple", "-lcactus-device")
        }
    }

    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
        }
    }
}
```

## [Your First Completion](#your-first-completion)

FlutterKotlinCLIC++

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
# Download and run LiquidAI's LFM2-350M
cactus run LiquidAI/LFM2-350M

# Or use a specific model
cactus run google/gemma-3-270m-it
```

```auto
#include <cactus.h>

cactus_model_t model = cactus_init("path/to/weight/folder", nullptr);

const char* messages = R"([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
])";

char response[4096];
int result = cactus_complete(
    model, messages, response, sizeof(response),
    nullptr, nullptr, nullptr, nullptr
);
```

## [Supported Models](#supported-models)

v1.6 includes support for:

- **LLMs:** Gemma-3, LiquidAI LFM2/LFM2.5, Qwen3 (with completion, tools, embeddings)
- **Vision:** LFM2-VL, LFM2.5-VL (with Apple NPU support)
- **Transcription:** Whisper (Small/Medium with Apple NPU), Moonshine-Base
- **Embeddings:** Nomic-Embed, Qwen3-Embedding

See the [our Hugging Face page](https://huggingface.co/Cactus-Compute) for the complete list.

## [Requirements](#requirements)

FlutterKotlin

Flutter 3.0+, Dart 2.17+, iOS 14.0+ / macOS 13.0+, Android API 24+ / arm64-v8a

Android API 24+ / arm64-v8a, iOS 14+ / arm64 (KMP only), Kotlin 1.9+

## [Next Steps](#next-steps)

[### LLM

Text generation, vision, streaming, and model options](/docs/v1.6/llm)[### Function Calling

Structured outputs and tool use](/docs/v1.6/function-calling)[### Transcription

Audio transcription with streaming support](/docs/v1.6/transcription)[### RAG & Embedding

Embeddings, vector search, and retrieval-augmented generation](/docs/v1.6/rag)

[Overview

On-device and Hybrid cross-platform AI framework](/docs/v1.6)[LLM

Text generation, vision, streaming, and model options with Cactus](/docs/v1.6/llm)

### On this page

[Installation](#installation)[Platform Integration](#platform-integration)[Android](#android)[iOS](#ios)[macOS](#macos)[Your First Completion](#your-first-completion)[Supported Models](#supported-models)[Requirements](#requirements)[Next Steps](#next-steps)
