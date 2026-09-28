# Source: https://cactuscompute.com/docs/v1.6/cli

CLI Reference

# CLI Reference

Command-line interface for Cactus LLM completion, transcription, and function calling

The Cactus CLI provides a command-line interface for running AI models locally.

![Cactus CLI completion demo](/assets/cactus-run-demo.png)

`cactus run`

![Cactus CLI transcription demo](/assets/cactus-transcribe-demo.png)

`cactus transcribe`

## [Installation](#installation)

macOSLinux

```auto
git clone https://github.com/cactus-compute/cactus && cd cactus && source ./setup
```

```auto
sudo apt-get install python3 python3-venv python3-pip cmake build-essential libcurl4-openssl-dev
git clone https://github.com/cactus-compute/cactus && cd cactus && source ./setup
```

## [Commands](#commands)

| Command | Description |
| --- | --- |
| `cactus run [model]` | Opens interactive playground (auto-downloads model) |
| `cactus download [model]` | Downloads model weights to `./weights` |
| `cactus convert [model] [dir]` | Converts model to `.cact` format, supports LoRA merging via `--lora <path>` |
| `cactus build` | Builds native libraries for ARM (`--apple` or `--android`) |
| `cactus test` | Runs tests with platform/model flags (`--ios`, `--android`, `--model`, `--precision`) |
| `cactus transcribe [model]` | Transcribe audio file (`--file`) or live microphone input |
| `cactus clean` | Removes build artifacts |
| `cactus --help` | Shows all available commands and flags |

## [Download Models](#download-models)

```auto
# Download a model for offline use
cactus download LiquidAI/LFM2.5-1.2B-Instruct

# Models are stored in ./weights/
```

## [LoRA Fine-tuning](#lora-fine-tuning)

```auto
# Convert a model with LoRA adapter
cactus convert LiquidAI/LFM2-350M ./output --lora path/to/lora
```

## [Testing](#testing)

```auto
# Test on iOS simulator
cactus test --ios --model LiquidAI/LFM2-350M

# Test on Android with specific precision
cactus test --android --model google/gemma-3-270m-it --precision int8
```

## [Next Steps](#next-steps)

[### Join our Discord

Ask questions and engage the community](https://discord.gg/nPGWGxXSwr)[### View Source Code

Contribute to the Cactus CLI on GitHub](https://github.com/cactus-compute/cactus)[### Try the iOS Demo

Experience Cactus on your iPhone](https://apps.apple.com/gb/app/cactus-chat/id6744444212)

[RAG & Embedding

Embeddings, vector search, and retrieval-augmented generation](/docs/v1.6/rag)[C++ Engine

Cactus Graph API, precision types, and native C++ engine internals](/docs/v1.6/cpp)

### On this page

[Installation](#installation)[Commands](#commands)[Download Models](#download-models)[LoRA Fine-tuning](#lora-fine-tuning)[Testing](#testing)[Next Steps](#next-steps)
