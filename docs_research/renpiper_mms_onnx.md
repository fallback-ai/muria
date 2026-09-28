# Source: https://huggingface.co/Axiveri/Renpiper-mms-onnx-V1

# [Axiveri](/Axiveri) / [Renpiper-mms-onnx-V1](/Axiveri/Renpiper-mms-onnx-V1) Like 0 Follow Axiveri 14

[Text-to-Speech](/models?pipeline_tag=text-to-speech)[ONNX](/models?library=onnx)[Yoruba](/models?language=yor)[Hausa](/models?language=hau)[Nigerian Pidgin](/models?language=pcm)[vits](/models?other=vits)[mms](/models?other=mms)[sherpa-onnx](/models?other=sherpa-onnx)

License: cc-by-nc-4.0

[Model card](/Axiveri/Renpiper-mms-onnx-V1)  [Files Files and versions  

xet](/Axiveri/Renpiper-mms-onnx-V1/tree/main)  [Community](/Axiveri/Renpiper-mms-onnx-V1/discussions)

 

Copy to bucket new

 

# Renpiper MMS ONNX V1

**This is an ONNX conversion of Meta AI's [`facebook/mms-tts`](https://huggingface.co/facebook/mms-tts)
checkpoints**, converted using the approach documented by the sherpa-onnx
project (<https://k2-fsa.github.io/sherpa/onnx/tts/mms.html>), for on-device
mobile inference via the `sherpa_onnx` runtime. The weights are unmodified
from Meta AI's originals -- no fine-tuning has been applied, only a format
conversion (PyTorch checkpoint -> ONNX) and vocabulary re-export
(`vocab.txt` -> `tokens.txt`).

## Language status

This table reflects exactly what this repo's own build notebook found and
produced -- not an assumption about MMS's general language coverage.

| Language | Status | ONNX size | Sample rate |
| --- | --- | --- | --- |
| Yoruba (`yor`) | Converted | 108.8 MB | 16000 Hz |
| Hausa (`hau`) | Converted | 108.8 MB | 16000 Hz |
| Igbo (`ibo`) | No raw checkpoint found (tried `models/ibo`, `models/ig`, `models/igbo`, `models/ib`, `full_models/ibo`, `full_models/ig`). A separate transformers-wrapped `facebook/mms-tts-ibo` repo does not exist, for reference -- not usable for this notebook's ONNX pipeline either way. | -- | -- |
| Nigerian Pidgin (`pcm`) | Converted | 108.8 MB | 16000 Hz |

Each converted language lives in its own subfolder (`yor/`, `hau/`, `ibo/`,
`pcm/` -- whichever succeeded) containing `model.onnx` and `tokens.txt`.

## What this is NOT

- Not an original or independently trained model.
- Not fine-tuned or adapted beyond the format conversion described above.
- Not available for commercial use or commercial relicensing under any name
  -- see License below.
- Not a claim that every language listed in Meta's general "1107 languages"
  MMS coverage is available here -- only what this notebook actually
  verified and converted.

## License

**CC-BY-NC 4.0**, inherited unchanged from the source checkpoints.
Non-commercial use only. This means this repo cannot be used as the basis
for a paid product, client deliverable, or commercial deployment (including
under a different product name) without a separate commercial license from
Meta AI.

## Citation

```auto
@article{pratap2023mms,
  title={Scaling Speech Technology to 1,000+ Languages},
  author={Vineel Pratap and Andros Tjandra and Bowen Shi and Paden Tomasello
    and Arun Babu and Sayani Kundu and Ali Elkahky and Zhaoheng Ni and
    Apoorv Vyas and Maryam Fazel-Zarandi and Alexei Baevski and Yossi Adi
    and Xiaohui Zhang and Wei-Ning Hsu and Alexis Conneau and Michael Auli},
  journal={arXiv},
  year={2023}
}
```

Model developed by Vineel Pratap et al., Meta AI. All credit for the
underlying model belongs to Meta AI / the MMS project, not to this repo's
maintainer.

## Inference (sherpa-onnx)

```auto
# pip install sherpa-onnx
import sherpa_onnx

tts = sherpa_onnx.OfflineTts(
    sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model="yor/model.onnx",
                tokens="yor/tokens.txt",
            ),
        ),
    )
)
audio = tts.generate("Your Yoruba text here")
```

Downloads last month
:   -
:   Downloads are not tracked for this model. [How to track](https://huggingface.co/docs/hub/models-download-stats)

  

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

[Text-to-Speech](/tasks/text-to-speech "Learn more about text-to-speech")

   

This model isn't deployed by any Inference Provider. [🙋  Ask for provider support](/spaces/huggingface/InferenceSupport/discussions/new?title=Axiveri/Renpiper-mms-onnx-V1&description=React%20to%20this%20comment%20with%20an%20emoji%20to%20vote%20for%20%5BAxiveri%2FRenpiper-mms-onnx-V1%5D(%2FAxiveri%2FRenpiper-mms-onnx-V1)%20to%20be%20supported%20by%20Inference%20Providers.%0A%0A(optional)%20Which%20providers%20are%20you%20interested%20in%3F%20(Novita%2C%20Hyperbolic%2C%20Together%E2%80%A6)%0A)

 

## Model tree for Axiveri/Renpiper-mms-onnx-V1

Base model

[facebook/mms-tts](/facebook/mms-tts)

Quantized

 ([3](/models?other=base_model:quantized:facebook/mms-tts)) 

this model
