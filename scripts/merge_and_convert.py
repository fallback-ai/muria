"""
Muria — Model Merge & Multi-Format Conversion Script
=====================================================
Utility to merge Muria LoRA adapters with base model McGill-NLP/AfriqueGemma-4B
and export to target deployment formats:
  1. Full FP16 / BF16 Merged Model (Hugging Face format)
  2. GGUF format via llama.cpp (e.g. Q4_K_M, Q4_0, Q5_K_M for Android edge)
  3. Cactus format (.cact via Cactus CLI for ultra-compact mobile deployment)
  4. INT4 format (bitsandbytes / AutoAWQ)

Usage Examples:
  # Merge LoRA and save 16-bit model
  python scripts/merge_and_convert.py --action merge --output-dir ./muria-merged

  # Merge and convert to GGUF
  python scripts/merge_and_convert.py --action gguf --quant-type Q4_K_M --llama-cpp-dir /path/to/llama.cpp

  # Merge and convert to Cactus .cact
  python scripts/merge_and_convert.py --action cact --output-file muria.cact
"""

import os
import sys
import argparse
import subprocess

DEFAULT_BASE_MODEL = "McGill-NLP/AfriqueGemma-4B"
DEFAULT_ADAPTER = "fallback-ai/Muria-Afrique-Gemma-4B-LoRA"
DEFAULT_ADAPTER_SUBFOLDER = None  # Use "adapters" if pulling from fallback-ai/Muria-Afrique-Gemma-4B


def merge_lora_to_hf(
    base_model_id: str = DEFAULT_BASE_MODEL,
    adapter_id_or_path: str = DEFAULT_ADAPTER,
    adapter_subfolder: str = None,
    output_dir: str = "./muria-merged-fp16",
    device: str = "auto"
):
    """Loads base model and LoRA adapter, merges weights, and exports full precision HF model."""
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    print(f"[1/3] Loading base model: {base_model_id}...")
    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16
    
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=dtype,
        device_map=device,
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)

    print(f"[2/3] Loading LoRA adapter from: {adapter_id_or_path}...")
    if adapter_subfolder:
        model = PeftModel.from_pretrained(base_model, adapter_id_or_path, subfolder=adapter_subfolder)
    else:
        model = PeftModel.from_pretrained(base_model, adapter_id_or_path)

    print("[3/3] Merging adapter into base model weights...")
    merged_model = model.merge_and_unload()

    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving merged model to: {output_dir}...")
    merged_model.save_pretrained(output_dir, safe_serialization=True)
    tokenizer.save_pretrained(output_dir)
    print(f"Merge successful! Saved to {output_dir}")
    return output_dir


def convert_to_gguf(
    merged_dir: str,
    output_gguf_path: str,
    llama_cpp_dir: str = "/tmp/llama.cpp",
    quant_type: str = "Q4_K_M"
):
    """Converts merged Hugging Face model to GGUF format and quantizes it."""
    convert_script = os.path.join(llama_cpp_dir, "convert_hf_to_gguf.py")
    if not os.path.exists(convert_script):
        raise FileNotFoundError(f"convert_hf_to_gguf.py not found in {llama_cpp_dir}")

    f16_path = output_gguf_path.replace(".gguf", ".f16.gguf")
    print(f"Converting HF weights to F16 GGUF: {f16_path}...")
    subprocess.run([sys.executable, convert_script, merged_dir, "--outfile", f16_path, "--outtype", "f16"], check=True)

    quant_bin = os.path.join(llama_cpp_dir, "build", "bin", "llama-quantize")
    if not os.path.exists(quant_bin):
        quant_bin = "llama-quantize"  # check PATH

    print(f"Quantizing {f16_path} -> {output_gguf_path} ({quant_type})...")
    subprocess.run([quant_bin, f16_path, output_gguf_path, quant_type], check=True)

    if os.path.exists(f16_path) and os.path.exists(output_gguf_path):
        os.remove(f16_path)
    print(f"GGUF conversion complete: {output_gguf_path}")


def convert_to_cactus(
    merged_dir: str,
    output_cact_path: str = "muria.cact"
):
    """
    Builds Cactus .cact binary for ultra-low memory mobile runtime.
    Requires Cactus CLI ('cactus' installed via npm or binary).
    """
    print(f"Building Cactus (.cact) model from: {merged_dir} -> {output_cact_path}...")
    try:
        cmd = ["cactus", "build", "--model", merged_dir, "--output", output_cact_path]
        subprocess.run(cmd, check=True)
        print(f"Cactus build complete: {output_cact_path}")
    except FileNotFoundError:
        print("[WARNING] 'cactus' CLI not found on system PATH.")
        print("To build .cact on your machine, install the Cactus CLI and run:")
        print(f"  cactus build --model {merged_dir} --output {output_cact_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Muria LoRA Merge & Multi-Format Mobile Converter")
    parser.add_argument(
        "--action",
        choices=["merge", "gguf", "cact", "all"],
        default="merge",
        help="Action to perform: merge (HF FP16), gguf (llama.cpp), cact (Cactus), or all"
    )
    parser.add_argument("--base-model", default=DEFAULT_BASE_MODEL, help="Base model Hugging Face ID")
    parser.add_argument("--adapter", default=DEFAULT_ADAPTER, help="LoRA adapter ID or local directory")
    parser.add_argument("--adapter-subfolder", default=DEFAULT_ADAPTER_SUBFOLDER, help="Subfolder inside adapter repo if applicable")
    parser.add_argument("--merged-dir", default="./muria-merged-fp16", help="Path to save or read merged model")
    parser.add_argument("--output-gguf", default="./muria-afriquegemma-4b.Q4_K_M.gguf", help="Output path for GGUF model")
    parser.add_argument("--quant-type", default="Q4_K_M", help="llama.cpp quantization type (Q4_K_M, Q4_0, Q5_K_M)")
    parser.add_argument("--llama-cpp-dir", default="/tmp/llama.cpp", help="Path to llama.cpp repo")
    parser.add_argument("--output-cact", default="./muria.cact", help="Output path for Cactus .cact file")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.action in ["merge", "all"]:
        merge_lora_to_hf(
            base_model_id=args.base_model,
            adapter_id_or_path=args.adapter,
            adapter_subfolder=args.adapter_subfolder,
            output_dir=args.merged_dir
        )

    if args.action in ["gguf", "all"]:
        if not os.path.exists(args.merged_dir):
            print(f"Merged directory {args.merged_dir} not found. Running merge first...")
            merge_lora_to_hf(args.base_model, args.adapter, args.adapter_subfolder, args.merged_dir)
        convert_to_gguf(args.merged_dir, args.output_gguf, args.llama_cpp_dir, args.quant_type)

    if args.action in ["cact", "all"]:
        if not os.path.exists(args.merged_dir):
            print(f"Merged directory {args.merged_dir} not found. Running merge first...")
            merge_lora_to_hf(args.base_model, args.adapter, args.adapter_subfolder, args.merged_dir)
        convert_to_cactus(args.merged_dir, args.output_cact)


if __name__ == "__main__":
    main()
