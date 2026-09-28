# Source: https://huggingface.co/Shinzmann/soro-tts-hau

# [Shinzmann](/Shinzmann) / [soro-tts-hau](/Shinzmann/soro-tts-hau) Like 0

[Text-to-Speech](/models?pipeline_tag=text-to-speech)[Transformers](/models?library=transformers)[Safetensors](/models?library=safetensors)

google/WaxalNLP

[Hausa](/models?language=hau)[vits](/models?other=vits)[text-to-audio](/models?other=text-to-audio)[tts](/models?other=tts)[mms](/models?other=mms)[nigerian-languages](/models?other=nigerian-languages)[low-resource](/models?other=low-resource)[waxal](/models?other=waxal)[soro-tts](/models?other=soro-tts)[hausa](/models?other=hausa)[Eval Results (legacy)](/models?other=model-index)

arxiv: 2305.13516

License: cc-by-nc-4.0

[Model card](/Shinzmann/soro-tts-hau)  [Files Files and versions  

xet](/Shinzmann/soro-tts-hau/tree/main)  [Community](/Shinzmann/soro-tts-hau/discussions)

 

Deploy

  Copy to bucket new   

Use this model

 

# Soro-TTS — Hausa 🇳🇬

Part of **[Soro-TTS](https://huggingface.co/Shinzmann)**, a multilingual text-to-speech system for Nigerian languages.
This checkpoint is a fine-tune of [`facebook/mms-tts-hau`](https://huggingface.co/facebook/mms-tts-hau) on the
[`google/WaxalNLP`](https://huggingface.co/datasets/google/WaxalNLP) `hau_tts` subset.

## Languages in the Soro-TTS suite

| Language | Model |
| --- | --- |
| Hausa | [`Shinzmann/soro-tts-hau`](https://huggingface.co/Shinzmann/soro-tts-hau) |
| Igbo | [`Shinzmann/soro-tts-ibo`](https://huggingface.co/Shinzmann/soro-tts-ibo) |
| Yoruba | [`Shinzmann/soro-tts-yor`](https://huggingface.co/Shinzmann/soro-tts-yor) |

## Quick start

```auto
from transformers import VitsModel, AutoTokenizer
import torch, scipy.io.wavfile

model = VitsModel.from_pretrained("Shinzmann/soro-tts-hau")
tokenizer = AutoTokenizer.from_pretrained("Shinzmann/soro-tts-hau")

text = "Sannu da zuwa Najeriya, ƙasarmu mai albarka."
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    waveform = model(**inputs).waveform[0].numpy()

scipy.io.wavfile.write("out.wav", rate=model.config.sampling_rate, data=waveform)
```

## Training data

Trained on the `hau_tts` configuration of WAXAL — studio-quality, phonetically balanced single-speaker recordings collected by Media Trust under Google Research's WAXAL initiative.

| Statistic | Value |
| --- | --- |
| Total audio | 13.12 hours |
| Training audio | 10.45 hours (1572 clips) |
| Validation audio | 1.27 hours |
| Test audio | 1.39 hours |
| Speakers (train) | 8 |
| % words containing diacritics | 0.0% |
| Sample rate | 16 kHz |

## Architecture

VITS / MMS-TTS — a conditional VAE with adversarial training, a flow-based prior, and a HiFi-GAN-style decoder.

- **Parameters:** ~83M
- **Sample rate:** 16 kHz
- **Base model:** `facebook/mms-tts-hau` (Pratap et al., 2023)

## Training procedure

| Hyperparameter | Value |
| --- | --- |
| Epochs | 100 |
| Batch size | 128 |
| Learning rate | 2e-05 |
| Optimizer | AdamW (β₁=0.8, β₂=0.99) |
| Precision | bf16 |
| Loss weights | mel=35, kl=1.5, gen=1, fmaps=1, disc=3, duration=1 |
| Recipe | [`ylacombe/finetune-hf-vits`](https://github.com/ylacombe/finetune-hf-vits) |

## Evaluation

**Character Error Rate (CER)** measured by transcribing synthesised audio with [`facebook/mms-1b-all`](https://huggingface.co/facebook/mms-1b-all) ASR (target\_lang=`hau`):

| Metric | n | Value |
| --- | --- | --- |
| CER (ASR-based) | 20 | **24.51%** |

This proxy metric measures intelligibility, not naturalness. Human MOS evaluation by native speakers is recommended for the latter.

## Limitations and biases

- **Single voice.** WAXAL TTS is recorded by 1–2 professional voice actors per language. The model inherits that voice and accent.
- **Domain.** Training text covers news, narration, and read speech; conversational, code-switched, or highly informal text may be out of distribution.
- **Tonal nuance.** Hausa relies on tone marks for meaning. Inputs without proper diacritics will produce flat or incorrect prosody.
- **Non-commercial.** MMS-TTS base is **CC BY-NC 4.0**; this fine-tune inherits that license.

## License

CC BY-NC 4.0 (inherited from `facebook/mms-tts-hau`). The WAXAL data itself is CC-BY-4.0.
**This model is for research only and may not be used commercially.**

## Citation

```auto
@misc{soro_tts_hau_2026,
  title  = {{Soro-TTS: A Multilingual Text-to-Speech System for Nigerian Languages — Hausa}},
  author = {{Soro-TTS authors}},
  year   = {{2026}},
  url    = {{https://huggingface.co/Shinzmann/soro-tts-hau}},
}
@article{pratap2023mms,
  title  = {{Scaling Speech Technology to 1{,}000+ Languages}},
  author = {{Pratap, Vineel and Tjandra, Andros and Shi, Bowen and others}},
  journal= {{arXiv:2305.13516}},
  year   = {{2023}}
}
```

## Acknowledgements

- Google Research and Media Trust for releasing WAXAL
- Meta AI for the MMS base models
- Yoach Lacombe for [`finetune-hf-vits`](https://github.com/ylacombe/finetune-hf-vits)

Downloads last month
:   87

 

Safetensors

Model size

39.6M params

Tensor type

F32

·

Files info

 

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[Text-to-Speech](/tasks/text-to-speech "Learn more about text-to-speech")

   

This model isn't deployed by any Inference Provider. [🙋  Ask for provider support](/spaces/huggingface/InferenceSupport/discussions/new?title=Shinzmann/soro-tts-hau&description=React%20to%20this%20comment%20with%20an%20emoji%20to%20vote%20for%20%5BShinzmann%2Fsoro-tts-hau%5D(%2FShinzmann%2Fsoro-tts-hau)%20to%20be%20supported%20by%20Inference%20Providers.%0A%0A(optional)%20Which%20providers%20are%20you%20interested%20in%3F%20(Novita%2C%20Hyperbolic%2C%20Together%E2%80%A6)%0A)

 

## Model tree for Shinzmann/soro-tts-hau

Base model

[facebook/mms-tts-hau](/facebook/mms-tts-hau)

Finetuned

 ([6](/models?other=base_model:finetune:facebook/mms-tts-hau)) 

this model

 

## Dataset used to train Shinzmann/soro-tts-hau

   

## Paper for Shinzmann/soro-tts-hau

[#### Scaling Speech Technology to 1,000+ Languages

Paper • 2305.13516 • Published May 22, 2023 •  13](/papers/2305.13516)

 

## Evaluation results

 

- Character Error Rate (ASR-based) on WAXAL TTS — Hausa

  [test set](/Shinzmann/soro-tts-hau/blob/main/README.md) [self-reported](/Shinzmann/soro-tts-hau/blob/main/README.md)

  24.510
