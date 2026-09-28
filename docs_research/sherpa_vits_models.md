# Source: https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/vits.html

# vits[](#vits "Permalink to this heading")

This page lists pre-trained [vits](https://github.com/jaywalnut310/vits) models.

## All models in a single table[](#all-models-in-a-single-table "Permalink to this heading")

See also <https://k2-fsa.github.io/sherpa/onnx/tts/all/>

The following table summarizes the information of all models in this page.

Note

Since there are more than `100` pre-trained models for over `40` languages,
we don’t list all of them on this page. Please find them at
<https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models>.

You can try all the models at the following huggingface space.
<https://huggingface.co/spaces/k2-fsa/text-to-speech>.

Hint

You can find Android APKs for each model at the following page

<https://k2-fsa.github.io/sherpa/onnx/tts/apk.html>

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Model | Language | # Speakers | Dataset | Model filesize (MB) | Sample rate (Hz) |
| [vits-melo-tts-zh\_en (Chinese + English, 1 speaker)](#vits-melo-tts-zh-en) | Chinese + English | 1 | N/A | 163 | 44100 |
| [vits-piper-en\_US-libritts\_r-medium (English, 904 speakers)](#vits-piper-en-us-libritts-r-medium) | English | 904 | [LibriTTS-R](https://www.openslr.org/141/) | 75 | 22050 |
| [vits-piper-en\_US-glados (English, 1 speaker)](#vits-piper-en-us-glados) | English | 1 | N/A | 61 | 22050 |
| [csukuangfj/sherpa-onnx-vits-zh-ll (Chinese, 5 speakers)](#sherpa-onnx-vits-zh-ll) | Chinese | 5 | N/A | 115 | 16000 |
| [csukuangfj/vits-zh-hf-fanchen-C (Chinese, 187 speakers)](#vits-zh-hf-fanchen-c) | Chinese | 187 | N/A | 116 | 16000 |
| [csukuangfj/vits-zh-hf-fanchen-wnj (Chinese, 1 male)](#vits-zh-hf-fanchen-wnj) | Chinese | 1 | N/A | 116 | 16000 |
| [csukuangfj/vits-zh-hf-theresa (Chinese, 804 speakers)](#vits-zh-hf-theresa) | Chinese | 804 | N/A | 117 | 22050 |
| [csukuangfj/vits-zh-hf-eula (Chinese, 804 speakers)](#vits-zh-hf-eula) | Chinese | 804 | N/A | 117 | 22050 |
| [aishell3 (Chinese, multi-speaker, 174 speakers)](#vits-model-aishell3) | Chinese | 174 | [aishell3](https://www.openslr.org/93/) | 116 | 8000 |
| [ljspeech (English, single-speaker)](#vits-model-vits-ljspeech) | English (US) | 1 (Female) | [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) | 109 | 22050 |
| [VCTK (English, multi-speaker, 109 speakers)](#vits-model-vits-vctk) | English | 109 | [VCTK](https://datashare.ed.ac.uk/handle/10283/2950) | 116 | 22050 |
| [en\_US-lessac-medium (English, single-speaker)](#vits-model-en-us-lessac-medium) | English (US) | 1 (Male) | [lessac\_blizzard2013](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/) | 61 | 22050 |

## vits-melo-tts-zh\_en (Chinese + English, 1 speaker)[](#vits-melo-tts-zh-en-chinese-english-1-speaker "Permalink to this heading")

This model is converted from <https://huggingface.co/myshell-ai/MeloTTS-Chinese>
and it supports only 1 speaker. It supports both Chinese and English.

Note that if you input English words, only those that are present in the `lexicon.txt`
can be pronounced. See
<https://github.com/k2-fsa/sherpa-onnx/pull/1209>
for how to add new words.

Hint

The converting script is available at
<https://github.com/k2-fsa/sherpa-onnx/tree/master/scripts/melo-tts>

You can convert more models from <https://github.com/myshell-ai/MeloTTS>
by yourself.

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#download-the-model "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-melo-tts-zh_en.tar.bz2
tar xvf vits-melo-tts-zh_en.tar.bz2
rm vits-melo-tts-zh_en.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
ls -lh vits-melo-tts-zh_en/
total 346848
-rw-r--r--  1 fangjun  staff   1.0K Jul 16 13:38 LICENSE
-rw-r--r--  1 fangjun  staff   156B Jul 16 13:38 README.md
-rw-r--r--  1 fangjun  staff    58K Jul 16 13:38 date.fst
drwxr-xr-x  9 fangjun  staff   288B Apr 19 20:42 dict
-rw-r--r--  1 fangjun  staff   6.5M Jul 16 13:38 lexicon.txt
-rw-r--r--  1 fangjun  staff   163M Jul 16 13:38 model.onnx
-rw-r--r--  1 fangjun  staff    63K Jul 16 13:38 number.fst
-rw-r--r--  1 fangjun  staff    87K Jul 16 13:38 phone.fst
-rw-r--r--  1 fangjun  staff   655B Jul 16 13:38 tokens.txt
```

### Generate speech with executables compiled from C++[](#generate-speech-with-executables-compiled-from-c "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
 --vits-model=./vits-melo-tts-zh_en/model.onnx \
 --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt \
 --vits-tokens=./vits-melo-tts-zh_en/tokens.txt \
 --output-filename=./zh-en-0.wav \
 "This is a 中英文的 text to speech 测试例子。"

./build/bin/sherpa-onnx-offline-tts \
 --vits-model=./vits-melo-tts-zh_en/model.onnx \
 --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt \
 --vits-tokens=./vits-melo-tts-zh_en/tokens.txt \
 --output-filename=./zh-en-1.wav \
 "我最近在学习machine learning，希望能够在未来的artificial intelligence领域有所建树。"

./build/bin/sherpa-onnx-offline-tts-play \
 --vits-model=./vits-melo-tts-zh_en/model.onnx \
 --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt \
 --vits-tokens=./vits-melo-tts-zh_en/tokens.txt \
 --tts-rule-fsts="./vits-melo-tts-zh_en/date.fst,./vits-melo-tts-zh_en/number.fst" \
 --output-filename=./zh-en-2.wav \
 "Are you ok 是雷军2015年4月小米在印度举行新品发布会时说的。他还说过 I am very happy to be in China.雷军事后在微博上表示「万万没想到，视频火速传到国内，全国人民都笑了」、「现在国际米粉越来越多，我的确应该把英文学好，不让大家失望！加油！」"
```

After running, it will generate three files `zh-en-1.wav`,
`zh-en-2.wav`, and `zh-en-3.wav` in the current directory.

```auto
soxi zh-en-*.wav

Input File     : 'zh-en-0.wav'
Channels       : 1
Sample Rate    : 44100
Precision      : 16-bit
Duration       : 00:00:03.54 = 156160 samples = 265.578 CDDA sectors
File Size      : 312k
Bit Rate       : 706k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : 'zh-en-1.wav'
Channels       : 1
Sample Rate    : 44100
Precision      : 16-bit
Duration       : 00:00:05.98 = 263680 samples = 448.435 CDDA sectors
File Size      : 527k
Bit Rate       : 706k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : 'zh-en-2.wav'
Channels       : 1
Sample Rate    : 44100
Precision      : 16-bit
Duration       : 00:00:18.92 = 834560 samples = 1419.32 CDDA sectors
File Size      : 1.67M
Bit Rate       : 706k
Sample Encoding: 16-bit Signed Integer PCM

Total Duration of 3 files: 00:00:28.44
```

| Wave filename | Content | Text |
| --- | --- | --- |
| zh-en-0.wav | Your browser does not support the `audio` element. | This is a 中英文的 text to speech 测试例子。 |
| zh-en-1.wav | Your browser does not support the `audio` element. | 我最近在学习machine learning，希望能够在未来的artificial intelligence领域有所建树。 |
| zh-en-2.wav | Your browser does not support the `audio` element. | Are you ok 是雷军2015年4月小米在印度举行新品发布会时说的。他还说过 I am very happy to be in China.雷军事后在微博上表示「万万没想到，视频火速传到国内，全国人民都笑了」、「现在国际米粉越来越多，我的确应该把英文学好，不让大家失望！加油！」 |

### Generate speech with Python script[](#generate-speech-with-python-script "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts-play.py \
 --vits-model=./vits-melo-tts-zh_en/model.onnx \
 --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt \
 --vits-tokens=./vits-melo-tts-zh_en/tokens.txt \
 --output-filename=./zh-en-3.wav \
 "它也支持繁体字. 我相信你們一定聽過愛迪生說過的這句話Genius is one percent inspiration and ninety-nine percent perspiration. "
```

After running, it will generate a file `zh-en-3.wav` in the current directory.

```auto
soxi zh-en-3.wav

Input File     : 'zh-en-3.wav'
Channels       : 1
Sample Rate    : 44100
Precision      : 16-bit
Duration       : 00:00:09.83 = 433664 samples = 737.524 CDDA sectors
File Size      : 867k
Bit Rate       : 706k
Sample Encoding: 16-bit Signed Integer PCM
```

| Wave filename | Content | Text |
| --- | --- | --- |
| zh-en-3.wav | Your browser does not support the `audio` element. | 它也支持繁体字. 我相信你們一定聽過愛迪生說過的這句話Genius is one percent inspiration and ninety-nine percent perspiration. |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#rtf-on-raspberry-pi-4-model-b-rev-1-5 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-melo-tts-zh_en/model.onnx \
   --vits-lexicon=./vits-melo-tts-zh_en/lexicon.txt \
   --vits-tokens=./vits-melo-tts-zh_en/tokens.txt \
   "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与 温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 6.727 | 3.877 | 2.914 | 2.518 |

## vits-piper-en\_US-glados (English, 1 speaker)[](#vits-piper-en-us-glados-english-1-speaker "Permalink to this heading")

This model is converted from <https://github.com/dnhkng/Glados/raw/main/models/glados.onnx>
and it supports only English.

See also <https://github.com/dnhkng/GlaDOS> .

If you are interested in how the model is converted to [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx), please see
the following colab notebook:

> <https://colab.research.google.com/drive/1m3Zr8H1RJaoZu4Y7hpQlav5vhtw3A513?usp=sharing>

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id1 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-glados.tar.bz2
tar xvf vits-piper-en_US-glados.tar.bz2
rm vits-piper-en_US-glados.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
ls -lh vits-piper-en_US-glados/

-rw-r--r--    1 fangjun  staff   242B Dec 13  2023 README.md
-rw-r--r--    1 fangjun  staff    61M Dec 13  2023 en_US-glados.onnx
drwxr-xr-x  122 fangjun  staff   3.8K Dec 13  2023 espeak-ng-data
-rw-r--r--    1 fangjun  staff   940B Dec 13  2023 tokens.txt
```

### Generate speech with executables compiled from C++[](#id2 "Permalink to this heading")

```auto
 cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
  --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
  --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
  --output-filename=./glados-liliana.wav \
  "liliana, the most beautiful and lovely assistant of our team!"

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
  --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
  --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
  --output-filename=./glados-code.wav \
  "Talk is cheap. Show me the code."

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
  --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
  --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
  --output-filename=./glados-men.wav \
   "Today as always, men fall into two groups: slaves and free men. Whoever does not have two-thirds of his day for himself, is a slave, whatever he may be: a statesman, a businessman, an official, or a scholar."
```

After running, it will generate 3 files `glados-liliana.wav`,
`glados-code.wav`, and `glados-men.wav` in the current directory.

```auto
soxi glados*.wav

Input File     : 'glados-code.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:02.18 = 48128 samples ~ 163.701 CDDA sectors
File Size      : 96.3k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : 'glados-liliana.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.97 = 87552 samples ~ 297.796 CDDA sectors
File Size      : 175k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : 'glados-men.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:15.31 = 337664 samples ~ 1148.52 CDDA sectors
File Size      : 675k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Total Duration of 3 files: 00:00:21.47
```

| Wave filename | Content | Text |
| --- | --- | --- |
| glados-liliana.wav | Your browser does not support the `audio` element. | liliana, the most beautiful and lovely assistant of our team! |
| glados-code.wav | Your browser does not support the `audio` element. | Talk is cheap. Show me the code. |
| glados-men.wav | Your browser does not support the `audio` element. | Today as always, men fall into two groups: slaves and free men. Whoever does not have two-thirds of his day for himself, is a slave, whatever he may be: a statesman, a businessman, an official, or a scholar. |

### Generate speech with Python script[](#id3 "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
 --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
 --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
 --output-filename=./glados-ship.wav \
 "A ship in port is safe, but that's not what ships are built for."

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
 --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
 --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
 --output-filename=./glados-bug.wav \
 "Given enough eyeballs, all bugs are shallow."
```

After running, it will generate two files `glados-ship.wav`
and `glados-bug.wav` in the current directory.

```auto
soxi ./glados-{ship,bug}.wav

Input File     : './glados-ship.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.74 = 82432 samples ~ 280.381 CDDA sectors
File Size      : 165k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : './glados-bug.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:02.67 = 58880 samples ~ 200.272 CDDA sectors
File Size      : 118k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Total Duration of 2 files: 00:00:06.41
```

| Wave filename | Content | Text |
| --- | --- | --- |
| glados-ship.wav | Your browser does not support the `audio` element. | A ship in port is safe, but that's not what ships are built for. |
| glados-bug.wav | Your browser does not support the `audio` element. | Given enough eyeballs, all bugs are shallow. |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id4 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-piper-en_US-glados/en_US-glados.onnx\
   --vits-tokens=./vits-piper-en_US-glados/tokens.txt \
   --vits-data-dir=./vits-piper-en_US-glados/espeak-ng-data \
   "Friends fell out often because life was changing so fast. The easiest thing in the world was to lose touch with someone."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 0.812 | 0.480 | 0.391 | 0.349 |

## vits-piper-en\_US-libritts\_r-medium (English, 904 speakers)[](#vits-piper-en-us-libritts-r-medium-english-904-speakers "Permalink to this heading")

This model is converted from <https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/libritts_r/medium>
and it supports 904 speakers. It supports only English.

See also <https://k2-fsa.github.io/sherpa/onnx/tts/all/English/vits-piper-en_US-libritts_r-medium.html>.

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id5 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-libritts_r-medium.tar.bz2
tar xvf vits-piper-en_US-libritts_r-medium.tar.bz2
rm vits-piper-en_US-libritts_r-medium.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
ls -lh vits-piper-en_US-libritts_r-medium/
total 153552
-rw-r--r--    1 fangjun  staff   279B Nov 29  2023 MODEL_CARD
-rw-r--r--    1 fangjun  staff    75M Nov 29  2023 en_US-libritts_r-medium.onnx
-rw-r--r--    1 fangjun  staff    20K Nov 29  2023 en_US-libritts_r-medium.onnx.json
drwxr-xr-x  122 fangjun  staff   3.8K Nov 28  2023 espeak-ng-data
-rw-r--r--    1 fangjun  staff   954B Nov 29  2023 tokens.txt
-rwxr-xr-x    1 fangjun  staff   1.8K Nov 29  2023 vits-piper-en_US.py
-rwxr-xr-x    1 fangjun  staff   730B Nov 29  2023 vits-piper-en_US.sh
```

### Generate speech with executables compiled from C++[](#id6 "Permalink to this heading")

```auto
 cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx \
  --vits-tokens=./vits-piper-en_US-libritts_r-medium/tokens.txt \
  --vits-data-dir=./vits-piper-en_US-libritts_r-medium/espeak-ng-data \
  --output-filename=./libritts-liliana-109.wav \
  --sid=109 \
  "liliana, the most beautiful and lovely assistant of our team!"

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx \
  --vits-tokens=./vits-piper-en_US-libritts_r-medium/tokens.txt \
  --vits-data-dir=./vits-piper-en_US-libritts_r-medium/espeak-ng-data \
  --output-filename=./libritts-liliana-900.wav \
  --sid=900 \
  "liliana, the most beautiful and lovely assistant of our team!"
```

After running, it will generate two files `libritts-liliana-109.wav`
and `libritts-liliana-900.wav` in the current directory.

```auto
soxi libritts-liliana-*.wav

Input File     : 'libritts-liliana-109.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:02.73 = 60160 samples ~ 204.626 CDDA sectors
File Size      : 120k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : 'libritts-liliana-900.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.36 = 73984 samples ~ 251.646 CDDA sectors
File Size      : 148k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Total Duration of 2 files: 00:00:06.08
```

| Wave filename | Content | Text |
| --- | --- | --- |
| libritts-liliana-109.wav | Your browser does not support the `audio` element. | liliana, the most beautiful and lovely assistant of our team! |
| libritts-liliana-900.wav | Your browser does not support the `audio` element. | liliana, the most beautiful and lovely assistant of our team! |

### Generate speech with Python script[](#id7 "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx \
 --vits-tokens=./vits-piper-en_US-libritts_r-medium/tokens.txt \
 --vits-data-dir=./vits-piper-en_US-libritts_r-medium/espeak-ng-data \
 --sid=200 \
 --output-filename=./libritts-armstrong-200.wav \
 "That's one small step for a man, a giant leap for mankind."

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx \
 --vits-tokens=./vits-piper-en_US-libritts_r-medium/tokens.txt \
 --vits-data-dir=./vits-piper-en_US-libritts_r-medium/espeak-ng-data \
 --sid=500 \
 --output-filename=./libritts-armstrong-500.wav \
 "That's one small step for a man, a giant leap for mankind."
```

After running, it will generate two files `libritts-armstrong-200.wav`
and `libritts-armstrong-500.wav` in the current directory.

```auto
soxi ./libritts-armstrong*.wav

Input File     : './libritts-armstrong-200.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.11 = 68608 samples ~ 233.361 CDDA sectors
File Size      : 137k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Input File     : './libritts-armstrong-500.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.42 = 75520 samples ~ 256.871 CDDA sectors
File Size      : 151k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM

Total Duration of 2 files: 00:00:06.54
```

| Wave filename | Content | Text |
| --- | --- | --- |
| libritts-armstrong-200.wav | Your browser does not support the `audio` element. | That's one small step for a man, a giant leap for mankind. |
| libritts-armstrong-500.wav | Your browser does not support the `audio` element. | That's one small step for a man, a giant leap for mankind. |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id8 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx \
   --vits-tokens=./vits-piper-en_US-libritts_r-medium/tokens.txt \
   --vits-data-dir=./vits-piper-en_US-libritts_r-medium/espeak-ng-data \
   "Friends fell out often because life was changing so fast. The easiest thing in the world was to lose touch with someone."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 0.790 | 0.493 | 0.392 | 0.357 |

## ljspeech (English, single-speaker)[](#ljspeech-english-single-speaker "Permalink to this heading")

This model is converted from [pretrained\_ljspeech.pth](https://drive.google.com/file/d/1q86w74Ygw2hNzYP9cWkeClGT5X25PvBT/view?usp=drive_link),
which is trained by the [vits](https://github.com/jaywalnut310/vits) author [Jaehyeon Kim](https://github.com/jaywalnut310) on
the [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) dataset. It supports only English and is a single-speaker model.

Note

If you are interested in how the model is converted, please see
<https://github.com/k2-fsa/sherpa-onnx/blob/master/scripts/vits/export-onnx-ljs.py>

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id9 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-ljs.tar.bz2
tar xvf vits-ljs.tar.bz2
rm vits-ljs.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
-rw-r--r-- 1 1001 127 109M Apr 22 02:38 vits-ljs/vits-ljs.onnx
```

### Generate speech with executables compiled from C++[](#id10 "Permalink to this heading")

```auto
 cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-ljs/vits-ljs.onnx \
  --vits-lexicon=./vits-ljs/lexicon.txt \
  --vits-tokens=./vits-ljs/tokens.txt \
  --output-filename=./liliana.wav \
  "liliana, the most beautiful and lovely assistant of our team!"
```

After running, it will generate a file `liliana.wav` in the current directory.

```auto
soxi ./liliana.wav

Input File     : './liliana.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:04.39 = 96768 samples ~ 329.143 CDDA sectors
File Size      : 194k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM
```

| Wave filename | Content | Text |
| --- | --- | --- |
| liliana.wav | Your browser does not support the `audio` element. | liliana, the most beautiful and lovely assistant of our team! |

### Generate speech with Python script[](#id11 "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-ljs/vits-ljs.onnx \
 --vits-lexicon=./vits-ljs/lexicon.txt \
 --vits-tokens=./vits-ljs/tokens.txt \
 --output-filename=./armstrong.wav \
 "That's one small step for a man, a giant leap for mankind."
```

After running, it will generate a file `armstrong.wav` in the current directory.

```auto
soxi ./armstrong.wav

Input File     : './armstrong.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:04.81 = 105984 samples ~ 360.49 CDDA sectors
File Size      : 212k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM
```

| Wave filename | Content | Text |
| --- | --- | --- |
| armstrong.wav | Your browser does not support the `audio` element. | That's one small step for a man, a giant leap for mankind. |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id12 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-ljs/vits-ljs.onnx \
   --vits-lexicon=./vits-ljs/lexicon.txt \
   --vits-tokens=./vits-ljs/tokens.txt \
   "Friends fell out often because life was changing so fast. The easiest thing in the world was to lose touch with someone."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 6.057 | 3.517 | 2.535 | 2.206 |

## VCTK (English, multi-speaker, 109 speakers)[](#vctk-english-multi-speaker-109-speakers "Permalink to this heading")

This model is converted from [pretrained\_vctk.pth](https://drive.google.com/file/d/11aHOlhnxzjpdWDpsz1vFDCzbeEfoIxru/view?usp=drive_link),
which is trained by the [vits](https://github.com/jaywalnut310/vits) author [Jaehyeon Kim](https://github.com/jaywalnut310) on
the [VCTK](https://datashare.ed.ac.uk/handle/10283/2950) dataset. It supports only English and is a multi-speaker model. It contains
109 speakers.

Note

If you are interested in how the model is converted, please see
<https://github.com/k2-fsa/sherpa-onnx/blob/master/scripts/vits/export-onnx-vctk.py>

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id14 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-vctk.tar.bz2
tar xvf vits-vctk.tar.bz2
rm vits-vctk.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
vits-vctk fangjun$ ls -lh *.onnx
-rw-r--r--  1 fangjun  staff    37M Oct 16 10:57 vits-vctk.int8.onnx
-rw-r--r--  1 fangjun  staff   116M Oct 16 10:57 vits-vctk.onnx
```

### Generate speech with executables compiled from C++[](#id15 "Permalink to this heading")

Since there are 109 speakers available, we can choose a speaker from 0 to 108.
The default speaker ID is 0.

We use speaker ID 0, 10, and 108 below to generate audio for the same text.

```auto
cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-vctk/vits-vctk.onnx \
  --vits-lexicon=./vits-vctk/lexicon.txt \
  --vits-tokens=./vits-vctk/tokens.txt \
  --sid=0 \
  --output-filename=./kennedy-0.wav \
  "Ask not what your country can do for you; ask what you can do for your country."

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-vctk/vits-vctk.onnx \
  --vits-lexicon=./vits-vctk/lexicon.txt \
  --vits-tokens=./vits-vctk/tokens.txt \
  --sid=10 \
  --output-filename=./kennedy-10.wav \
  "Ask not what your country can do for you; ask what you can do for your country."

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-vctk/vits-vctk.onnx \
  --vits-lexicon=./vits-vctk/lexicon.txt \
  --vits-tokens=./vits-vctk/tokens.txt \
  --sid=108 \
  --output-filename=./kennedy-108.wav \
  "Ask not what your country can do for you; ask what you can do for your country."
```

It will generate 3 files: `kennedy-0.wav`, `kennedy-10.wav`, and `kennedy-108.wav`.

| Wave filename | Content | Text |
| --- | --- | --- |
| kennedy-0.wav | Your browser does not support the `audio` element. | Ask not what your country can do for you; ask what you can do for your country. |
| kennedy-10.wav | Your browser does not support the `audio` element. | Ask not what your country can do for you; ask what you can do for your country. |
| kennedy-108.wav | Your browser does not support the `audio` element. | Ask not what your country can do for you; ask what you can do for your country. |

### Generate speech with Python script[](#id16 "Permalink to this heading")

We use speaker ID 30, 66, and 99 below to generate audio for different transcripts.

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-vctk/vits-vctk.onnx \
 --vits-lexicon=./vits-vctk/lexicon.txt \
 --vits-tokens=./vits-vctk/tokens.txt \
 --sid=30 \
 --output-filename=./einstein-30.wav \
 "Life is like riding a bicycle. To keep your balance, you must keep moving."

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-vctk/vits-vctk.onnx \
 --vits-lexicon=./vits-vctk/lexicon.txt \
 --vits-tokens=./vits-vctk/tokens.txt \
 --sid=66 \
 --output-filename=./franklin-66.wav \
 "Three can keep a secret, if two of them are dead."

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-vctk/vits-vctk.onnx \
 --vits-lexicon=./vits-vctk/lexicon.txt \
 --vits-tokens=./vits-vctk/tokens.txt \
 --sid=99 \
 --output-filename=./martin-99.wav \
 "Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that"
```

It will generate 3 files: `einstein-30.wav`, `franklin-66.wav`, and `martin-99.wav`.

| Wave filename | Content | Text |
| --- | --- | --- |
| einstein-30.wav | Your browser does not support the `audio` element. | Life is like riding a bicycle. To keep your balance, you must keep moving. |
| franklin-66.wav | Your browser does not support the `audio` element. | Three can keep a secret, if two of them are dead. |
| martin-99.wav | Your browser does not support the `audio` element. | Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id17 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-vctk/vits-vctk.onnx \
   --vits-lexicon=./vits-vctk/lexicon.txt \
   --vits-tokens=./vits-vctk/tokens.txt \
   "Friends fell out often because life was changing so fast. The easiest thing in the world was to lose touch with someone."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 6.079 | 3.483 | 2.537 | 2.226 |

## csukuangfj/sherpa-onnx-vits-zh-ll (Chinese, 5 speakers)[](#csukuangfj-sherpa-onnx-vits-zh-ll-chinese-5-speakers "Permalink to this heading")

You can download the model using the following commands:

```auto
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-vits-zh-ll.tar.bz2
tar xvf sherpa-onnx-vits-zh-ll.tar.bz2
rm sherpa-onnx-vits-zh-ll.tar.bz2
```

Hint

This model is trained with the following framework

> <https://github.com/Plachtaa/VITS-fast-fine-tuning>

Please check the file sizes of the downloaded model:

```auto
ls -lh sherpa-onnx-vits-zh-ll/

-rw-r--r--  1 fangjun  staff   2.3K Apr 25 17:58 G_multisperaker_latest.json
-rw-r-----@ 1 fangjun  staff   2.2K Apr 25 17:22 G_multisperaker_latest_low.json
-rw-r--r--  1 fangjun  staff   127B Apr 25 17:58 README.md
-rw-r--r--  1 fangjun  staff    58K Apr 25 17:58 date.fst
drwxr-xr-x  9 fangjun  staff   288B Jun 21 16:32 dict
-rw-r--r--  1 fangjun  staff   368K Apr 25 17:58 lexicon.txt
-rw-r--r--  1 fangjun  staff   115M Apr 25 17:58 model.onnx
-rw-r--r--  1 fangjun  staff    21K Apr 25 17:58 new_heteronym.fst
-rw-r--r--  1 fangjun  staff    63K Apr 25 17:58 number.fst
-rw-r--r--  1 fangjun  staff    87K Apr 25 17:58 phone.fst
-rw-r--r--  1 fangjun  staff   331B Apr 25 17:58 tokens.txt
```

**usage**:

```auto
sherpa-onnx-offline-tts \
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
  --vits-length-scale=0.5 \
  --sid=0 \
  --output-filename="./0-value-2x.wav" \
  "小米的核心价值观是什么？答案是真诚热爱！"

sherpa-onnx-offline-tts \
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
  --sid=1 \
  --tts-rule-fsts=./sherpa-onnx-vits-zh-ll/number.fst \
  --output-filename="./1-numbers.wav" \
  "小米有14岁了"

sherpa-onnx-offline-tts \
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
  --tts-rule-fsts=./sherpa-onnx-vits-zh-ll/phone.fst,./sherpa-onnx-vits-zh-ll/number.fst \
  --sid=2 \
  --output-filename="./2-numbers.wav" \
  "有困难，请拨打110 或者18601200909"

sherpa-onnx-offline-tts \
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
  --sid=3 \
  --output-filename="./3-wo-mi.wav" \
  "小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。"

sherpa-onnx-offline-tts \
  --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
  --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
  --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
  --tts-rule-fsts=./sherpa-onnx-vits-zh-ll/number.fst \
  --sid=4 \
  --output-filename="./4-heteronym.wav" \
  "35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| 0-value-2x.wav | Your browser does not support the `audio` element. | 小米的核心价值观是什么？答案是真诚热爱！ |
| 1-numbers.wav | Your browser does not support the `audio` element. | 小米有14岁了 |
| 2-numbers.wav | Your browser does not support the `audio` element. | 有困难，请拨打110 或者18601200909 |
| 3-wo-mi.wav | Your browser does not support the `audio` element. | 小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。 |
| 4-heteronym.wav | Your browser does not support the `audio` element. | 35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。 |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id18 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./sherpa-onnx-vits-zh-ll/model.onnx \
   --vits-lexicon=./sherpa-onnx-vits-zh-ll/lexicon.txt \
   --vits-tokens=./sherpa-onnx-vits-zh-ll/tokens.txt \
   '当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与温柔.'
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 4.275 | 2.494 | 1.840 | 1.593 |

## csukuangfj/vits-zh-hf-fanchen-C (Chinese, 187 speakers)[](#csukuangfj-vits-zh-hf-fanchen-c-chinese-187-speakers "Permalink to this heading")

You can download the model using the following commands:

```auto
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-hf-fanchen-C.tar.bz2
tar xvf vits-zh-hf-fanchen-C.tar.bz2
rm vits-zh-hf-fanchen-C.tar.bz2
```

Hint

This model is converted from
<https://huggingface.co/spaces/lkz99/tts_model/tree/main/zh>

```auto
# information about model files

total 291M
-rw-r--r-- 1 1001 127  58K Apr 21 05:40 date.fst
drwxr-xr-x 3 1001 127 4.0K Apr 19 12:42 dict
-rwxr-xr-x 1 1001 127 4.0K Apr 21 05:40 export-onnx-zh-hf-fanchen-models.py
-rwxr-xr-x 1 1001 127 2.5K Apr 21 05:40 generate-lexicon-zh-hf-fanchen-models.py
-rw-r--r-- 1 1001 127 2.4M Apr 21 05:40 lexicon.txt
-rw-r--r-- 1 1001 127  22K Apr 21 05:40 new_heteronym.fst
-rw-r--r-- 1 1001 127  63K Apr 21 05:40 number.fst
-rw-r--r-- 1 1001 127  87K Apr 21 05:40 phone.fst
-rw-r--r-- 1 1001 127 173M Apr 21 05:40 rule.far
-rw-r--r-- 1 1001 127  331 Apr 21 05:40 tokens.txt
-rw-r--r-- 1 1001 127 116M Apr 21 05:40 vits-zh-hf-fanchen-C.onnx
-rwxr-xr-x 1 1001 127 2.0K Apr 21 05:40 vits-zh-hf-fanchen-models.sh
```

**usage**:

```auto
sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
  --vits-length-scale=0.5 \
  --output-filename="./value-2x.wav" \
  "小米的核心价值观是什么？答案是真诚热爱！"

sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
  --vits-length-scale=1.0 \
  --tts-rule-fsts=./vits-zh-hf-fanchen-C/number.fst \
  --output-filename="./numbers.wav" \
  "小米有14岁了"

sherpa-onnx-offline-tts \
  --sid=100 \
  --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
  --vits-length-scale=1.0 \
  --tts-rule-fsts=./vits-zh-hf-fanchen-C/phone.fst,./vits-zh-hf-fanchen-C/number.fst \
  --output-filename="./numbers-100.wav" \
  "有困难，请拨打110 或者18601200909"

sherpa-onnx-offline-tts \
  --sid=14 \
  --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
  --vits-length-scale=1.0 \
  --output-filename="./wo-mi-14.wav" \
  "小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。"

sherpa-onnx-offline-tts \
  --sid=102 \
  --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
  --tts-rule-fsts=./vits-zh-hf-fanchen-C/number.fst \
  --vits-length-scale=1.0 \
  --output-filename="./heteronym-102.wav" \
  "35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。1天前莅临我行指导工作。"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| value-2x.wav | Your browser does not support the `audio` element. | 小米的核心价值观是什么？答案是真诚热爱！ |
| numbers.wav | Your browser does not support the `audio` element. | 小米有14岁了 |
| numbers-100.wav | Your browser does not support the `audio` element. | 有困难，请拨打110 或者18601200909 |
| wo-mi-14.wav | Your browser does not support the `audio` element. | 小米的使命是，始终坚持做感动人心、价格厚道的好产品，让全球每个人都能享受科技带来的美好生活。 |
| heteronym-102.wav | Your browser does not support the `audio` element. | 35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。1天前莅临我行指导工作。 |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id19 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-zh-hf-fanchen-C/vits-zh-hf-fanchen-C.onnx \
   --vits-lexicon=./vits-zh-hf-fanchen-C/lexicon.txt \
   --vits-tokens=./vits-zh-hf-fanchen-C/tokens.txt \
   "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与 温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 4.306 | 2.451 | 1.846 | 1.600 |

## csukuangfj/vits-zh-hf-fanchen-wnj (Chinese, 1 male)[](#csukuangfj-vits-zh-hf-fanchen-wnj-chinese-1-male "Permalink to this heading")

You can download the model using the following commands:

```auto
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-hf-fanchen-wnj.tar.bz2
tar xvf vits-zh-hf-fanchen-wnj.tar.bz2
rm vits-zh-hf-fanchen-wnj.tar.bz2
```

Hint

This model is converted from
<https://huggingface.co/spaces/lkz99/tts_model/blob/main/G_wnj_latest.pth>

```auto
# information about model files
total 594760
-rw-r--r--  1 fangjun  staff    58K Apr 21 13:40 date.fst
drwxr-xr-x  9 fangjun  staff   288B Apr 19 20:42 dict
-rwxr-xr-x  1 fangjun  staff   3.9K Apr 21 13:40 export-onnx-zh-hf-fanchen-models.py
-rwxr-xr-x  1 fangjun  staff   2.4K Apr 21 13:40 generate-lexicon-zh-hf-fanchen-models.py
-rw-r--r--  1 fangjun  staff   2.3M Apr 21 13:40 lexicon.txt
-rw-r--r--  1 fangjun  staff    21K Apr 21 13:40 new_heteronym.fst
-rw-r--r--  1 fangjun  staff    63K Apr 21 13:40 number.fst
-rw-r--r--  1 fangjun  staff    87K Apr 21 13:40 phone.fst
-rw-r--r--  1 fangjun  staff   172M Apr 21 13:40 rule.far
-rw-r--r--  1 fangjun  staff   331B Apr 21 13:40 tokens.txt
-rwxr-xr-x  1 fangjun  staff   1.9K Apr 21 13:40 vits-zh-hf-fanchen-models.sh
-rw-r--r--  1 fangjun  staff   115M Apr 21 13:40 vits-zh-hf-fanchen-wnj.onnx
```

**usage**:

```auto
sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-fanchen-wnj/vits-zh-hf-fanchen-wnj.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-wnj/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-wnj/tokens.txt \
  --output-filename="./kuayue.wav" \
  "升级人车家全生态，小米迎跨越时刻。"

sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-fanchen-wnj/vits-zh-hf-fanchen-wnj.onnx \
  --vits-lexicon=./vits-zh-hf-fanchen-wnj/lexicon.txt \
  --vits-tokens=./vits-zh-hf-fanchen-wnj/tokens.txt \
  --tts-rule-fsts=./vits-zh-hf-fanchen-wnj/number.fst \
  --output-filename="./os.wav" \
  "这一全新操作系统，是小米14年来技术积淀的结晶。"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| kuayue.wav | Your browser does not support the `audio` element. | 升级人车家全生态，小米迎跨越时刻。 |
| os.wav | Your browser does not support the `audio` element. | 这一全新操作系统，是小米14年来技术积淀的结晶。 |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id20 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-zh-hf-fanchen-wnj/vits-zh-hf-fanchen-wnj.onnx \
   --vits-lexicon=./vits-zh-hf-fanchen-wnj/lexicon.txt \
   --vits-tokens=./vits-zh-hf-fanchen-wnj/tokens.txt \
   "当夜幕 降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的 奇迹与温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 4.276 | 2.505 | 1.827 | 1.608 |

## csukuangfj/vits-zh-hf-theresa (Chinese, 804 speakers)[](#csukuangfj-vits-zh-hf-theresa-chinese-804-speakers "Permalink to this heading")

You can download the model with the following commands:

```auto
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-hf-theresa.tar.bz2
tar xvf vits-zh-hf-theresa.tar.bz2
rm vits-zh-hf-theresa.tar.bz2
```

Hint

This model is converted from
<https://huggingface.co/spaces/zomehwh/vits-models-genshin-bh3/tree/main/pretrained_models/theresa>

```auto
# information about model files

total 596992
-rw-r--r--  1 fangjun  staff    58K Apr 21 13:39 date.fst
drwxr-xr-x  9 fangjun  staff   288B Apr 19 20:42 dict
-rw-r--r--  1 fangjun  staff   2.6M Apr 21 13:39 lexicon.txt
-rw-r--r--  1 fangjun  staff    21K Apr 21 13:39 new_heteronym.fst
-rw-r--r--  1 fangjun  staff    63K Apr 21 13:39 number.fst
-rw-r--r--  1 fangjun  staff    87K Apr 21 13:39 phone.fst
-rw-r--r--  1 fangjun  staff   172M Apr 21 13:39 rule.far
-rw-r--r--  1 fangjun  staff   116M Apr 21 13:39 theresa.onnx
-rw-r--r--  1 fangjun  staff   268B Apr 21 13:39 tokens.txt
-rwxr-xr-x  1 fangjun  staff   5.3K Apr 21 13:39 vits-zh-hf-models.py
-rwxr-xr-x  1 fangjun  staff   571B Apr 21 13:39 vits-zh-hf-models.sh
```

**usage**:

```auto
sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-theresa/theresa.onnx \
  --vits-lexicon=./vits-zh-hf-theresa/lexicon.txt \
  --vits-tokens=./vits-zh-hf-theresa/tokens.txt \
  --sid=0 \
  --output-filename="./reai-0.wav" \
  "真诚就是不欺人也不自欺。热爱就是全心投入并享受其中。"

sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-theresa/theresa.onnx \
  --vits-lexicon=./vits-zh-hf-theresa/lexicon.txt \
  --vits-tokens=./vits-zh-hf-theresa/tokens.txt \
  --tts-rule-fsts=./vits-zh-hf-theresa/number.fst \
  --debug=1 \
  --sid=88 \
  --output-filename="./mi14-88.wav" \
  "小米14一周销量破1000000！"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| reai-0.wav | Your browser does not support the `audio` element. | 真诚就是不欺人也不自欺。热爱就是全心投入并享受其中。 |
| m14-88.wav | Your browser does not support the `audio` element. | 小米14一周销量破1000000！ |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id21 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-zh-hf-theresa/theresa.onnx \
   --vits-lexicon=./vits-zh-hf-theresa/lexicon.txt \
   --vits-tokens=./vits-zh-hf-theresa/tokens.txt \
   "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与 温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 6.032 | 3.448 | 2.566 | 2.210 |

## csukuangfj/vits-zh-hf-eula (Chinese, 804 speakers)[](#csukuangfj-vits-zh-hf-eula-chinese-804-speakers "Permalink to this heading")

You can download the model using the following commands:

```auto
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-hf-eula.tar.bz2
tar xvf vits-zh-hf-eula.tar.bz2
rm vits-zh-hf-eula.tar.bz2
```

Hint

This model is converted from
<https://huggingface.co/spaces/zomehwh/vits-models-genshin-bh3/tree/main/pretrained_models/eula>

```auto
# information about model files

total 596992
-rw-r--r--  1 fangjun  staff    58K Apr 21 13:39 date.fst
drwxr-xr-x  9 fangjun  staff   288B Apr 19 20:42 dict
-rw-r--r--  1 fangjun  staff   116M Apr 21 13:39 eula.onnx
-rw-r--r--  1 fangjun  staff   2.6M Apr 21 13:39 lexicon.txt
-rw-r--r--  1 fangjun  staff    21K Apr 21 13:39 new_heteronym.fst
-rw-r--r--  1 fangjun  staff    63K Apr 21 13:39 number.fst
-rw-r--r--  1 fangjun  staff    87K Apr 21 13:39 phone.fst
-rw-r--r--  1 fangjun  staff   172M Apr 21 13:39 rule.far
-rw-r--r--  1 fangjun  staff   268B Apr 21 13:39 tokens.txt
-rwxr-xr-x  1 fangjun  staff   5.3K Apr 21 13:39 vits-zh-hf-models.py
-rwxr-xr-x  1 fangjun  staff   571B Apr 21 13:39 vits-zh-hf-models.sh
```

**usage**:

```auto
sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-eula/eula.onnx \
  --vits-lexicon=./vits-zh-hf-eula/lexicon.txt \
  --vits-tokens=./vits-zh-hf-eula/tokens.txt \
  --debug=1 \
  --sid=666 \
  --output-filename="./news-666.wav" \
  "小米在今天上午举办的核心干部大会上，公布了新十年的奋斗目标和科技战略，并发布了小米价值观的八条诠释。"

sherpa-onnx-offline-tts \
  --vits-model=./vits-zh-hf-eula/eula.onnx \
  --vits-lexicon=./vits-zh-hf-eula/lexicon.txt \
  --vits-tokens=./vits-zh-hf-eula/tokens.txt \
  --tts-rule-fsts=./vits-zh-hf-eula/number.fst \
  --sid=99 \
  --output-filename="./news-99.wav" \
  "9月25日消息，雷军今日在微博发文称"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| news-666.wav | Your browser does not support the `audio` element. | 小米在今天上午举办的核心干部大会上，公布了新十年的奋斗目标和科技战略，并发布了小米价值观的八条诠释。 |
| news-99.wav | Your browser does not support the `audio` element. | 9月25日消息，雷军今日在微博发文称 |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id22 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-zh-hf-eula/eula.onnx \
   --vits-lexicon=./vits-zh-hf-eula/lexicon.txt \
   --vits-tokens=./vits-zh-hf-eula/tokens.txt \
   "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与 温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 6.011 | 3.473 | 2.537 | 2.231 |

## aishell3 (Chinese, multi-speaker, 174 speakers)[](#aishell3-chinese-multi-speaker-174-speakers "Permalink to this heading")

This model is trained on the [aishell3](https://www.openslr.org/93/) dataset using [icefall](https://github.com/k2-fsa/icefall).

It supports only Chinese and it’s a multi-speaker model and contains 174 speakers.

Hint

You can download the Android APK for this model at

<https://k2-fsa.github.io/sherpa/onnx/tts/apk-engine.html>

(Please search for `vits-icefall-zh-aishell3` in the above Android APK page)

Note

If you are interested in how the model is converted, please see
the documentation of [icefall](https://github.com/k2-fsa/icefall).

If you are interested in training your own model, please also refer to
[icefall](https://github.com/k2-fsa/icefall).

[icefall](https://github.com/k2-fsa/icefall) is also developed by us.

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id23 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-icefall-zh-aishell3.tar.bz2
tar xvf vits-icefall-zh-aishell3.tar.bz2
rm vits-icefall-zh-aishell3.tar.bz2
```

Please check that the file sizes of the pre-trained models are correct. See
the file sizes of `*.onnx` files below.

```auto
vits-icefall-zh-aishell3 fangjun$ ls -lh *.onnx
-rw-r--r--  1 fangjun  staff    29M Mar 20 22:50 model.onnx
```

### Generate speech with executables compiled from C++[](#id24 "Permalink to this heading")

Since there are 174 speakers available, we can choose a speaker from 0 to 173.
The default speaker ID is 0.

We use speaker ID 10, 33, and 99 below to generate audio for the same text.

```auto
cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-icefall-zh-aishell3/model.onnx \
  --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
  --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
  --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
  --sid=10 \
  --output-filename=./liliana-10.wav \
  "林美丽最美丽、最漂亮、最可爱！"

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-icefall-zh-aishell3/model.onnx \
  --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
  --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
  --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
  --sid=33 \
  --output-filename=./liliana-33.wav \
  "林美丽最美丽、最漂亮、最可爱！"

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-icefall-zh-aishell3/model.onnx \
  --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
  --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
  --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
  --sid=99 \
  --output-filename=./liliana-99.wav \
  "林美丽最美丽、最漂亮、最可爱！"
```

It will generate 3 files: `liliana-10.wav`, `liliana-33.wav`, and `liliana-99.wav`.

We also support rule-based text normalization, which is implemented with [OpenFst](https://www.openfst.org/).
Currently, only number normalization is supported.

Hint

We will support other normalization rules later.

The following is an example:

```auto
./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-icefall-zh-aishell3/model.onnx \
  --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
  --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
  --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
  --sid=66 \
  --output-filename=./rule-66.wav \
  "35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。1天前莅临我行指导工作。"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| liliana-10.wav | Your browser does not support the `audio` element. | 林美丽最美丽、最漂亮、最可爱！ |
| liliana-33.wav | Your browser does not support the `audio` element. | 林美丽最美丽、最漂亮、最可爱！ |
| liliana-99.wav | Your browser does not support the `audio` element. | 林美丽最美丽、最漂亮、最可爱！ |
| rule-66.wav | Your browser does not support the `audio` element. | 35年前，他于长沙出生, 在长白山长大。9年前他当上了银行的领导，主管行政。1天前莅临我行指导工作。 |

### Generate speech with Python script[](#id25 "Permalink to this heading")

We use speaker ID 21, 41, and 45 below to generate audio for different transcripts.

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-icefall-zh-aishell3/model.onnx \
 --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
 --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
 --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
 --sid=21 \
 --output-filename=./liubei-21.wav \
 "勿以恶小而为之，勿以善小而不为。惟贤惟德，能服于人。"

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-icefall-zh-aishell3/model.onnx \
 --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
 --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
 --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
 --sid=41 \
 --output-filename=./demokelite-41.wav \
 "要留心，即使当你独自一人时，也不要说坏话或做坏事，而要学得在你自己面前比在别人面前更知耻。"

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-icefall-zh-aishell3/model.onnx \
 --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
 --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
 --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
 --sid=45 \
 --output-filename=./zhugeliang-45.wav \
 "夫君子之行，静以修身，俭以养德，非淡泊无以明志，非宁静无以致远。"
```

It will generate 3 files: `liubei-21.wav`, `demokelite-41.wav`, and `zhugeliang-45.wav`.

The Python script also supports rule-based text normalization.

```auto
python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-icefall-zh-aishell3/model.onnx \
 --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
 --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
 --tts-rule-fsts=./vits-icefall-zh-aishell3/phone.fst,./vits-icefall-zh-aishell3/date.fst,./vits-icefall-zh-aishell3/number.fst \
 --sid=103 \
 --output-filename=./rule-103.wav \
 "根据第7次全国人口普查结果表明，我国总人口有1443497378人。普查登记的大陆31个省、自治区、直辖市和现役军人的人口共1411778724人。电话号码是110。手机号是13812345678"
```

| Wave filename | Content | Text |
| --- | --- | --- |
| liube-21.wav | Your browser does not support the `audio` element. | 勿以恶小而为之，勿以善小而不为。惟贤惟德，能服于人。 |
| demokelite-41.wav | Your browser does not support the `audio` element. | 要留心，即使当你独自一人时，也不要说坏话或做坏事，而要学得在你自己面前比在别人面前更知耻。 |
| zhugeliang-45.wav | Your browser does not support the `audio` element. | 夫君子之行，静以修身，俭以养德，非淡泊无以明志，非宁静无以致远。 |
| rule-103.wav | Your browser does not support the `audio` element. | 根据第7次全国人口普查结果表明，我国总人口有1443497378人。普查登记的大陆31个省、自治区、直辖市和现役军人的人口共1411778724人。电话号码是110。手机号是13812345678 |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id26 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-icefall-zh-aishell3/model.onnx \
   --vits-lexicon=./vits-icefall-zh-aishell3/lexicon.txt \
   --vits-tokens=./vits-icefall-zh-aishell3/tokens.txt \
   --sid=66  \
   "当夜幕降临，星光点点，伴随着微风拂面，我在静谧中感受着时光的流转，思念如涟漪荡漾，梦境如画卷展开，我与自然融为一体，沉静在这片宁静的美丽之中，感受着生命的奇迹与温柔."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 0.365 | 0.220 | 0.171 | 0.156 |

## en\_US-lessac-medium (English, single-speaker)[](#en-us-lessac-medium-english-single-speaker "Permalink to this heading")

This model is converted from <https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/medium>.

The dataset used to train the model is [lessac\_blizzard2013](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/).

Hint

The model is from [piper](https://github.com/rhasspy/piper).

See also <https://k2-fsa.github.io/sherpa/onnx/tts/all/English/vits-piper-en_US-lessac-medium.html>.

In the following, we describe how to download it and use it with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

### Download the model[](#id27 "Permalink to this heading")

Please use the following commands to download it.

```auto
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-medium.tar.bz2
tar xf vits-piper-en_US-lessac-medium.tar.bz2
```

Hint

You can find a lot of pre-trained models for over 40 languages at
<https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models>.

### Generate speech with executables compiled from C++[](#id28 "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

./build/bin/sherpa-onnx-offline-tts \
  --vits-model=./vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx \
  --vits-data-dir=./vits-piper-en_US-lessac-medium/espeak-ng-data \
  --vits-tokens=./vits-piper-en_US-lessac-medium/tokens.txt \
  --output-filename=./liliana-piper-en_US-lessac-medium.wav \
  "liliana, the most beautiful and lovely assistant of our team!"
```

Hint

You can also use

> ```auto
> cd /path/to/sherpa-onnx
>
> ./build/bin/sherpa-onnx-offline-tts-play \
>   --vits-model=./vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx \
>   --vits-data-dir=./vits-piper-en_US-lessac-medium/espeak-ng-data \
>   --vits-tokens=./vits-piper-en_US-lessac-medium/tokens.txt \
>   --output-filename=./liliana-piper-en_US-lessac-medium.wav \
>   "liliana, the most beautiful and lovely assistant of our team!"
> ```
>
> which will play the audio as it is generating.

After running, it will generate a file `liliana-piper.wav` in the current directory.

```auto
soxi ./liliana-piper-en_US-lessac-medium.wav

Input File     : './liliana-piper-en_US-lessac-medium.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.48 = 76800 samples ~ 261.224 CDDA sectors
File Size      : 154k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM
```

| Wave filename | Content | Text |
| --- | --- | --- |
| liliana-piper-en\_US-lessac-medium.wav | Your browser does not support the `audio` element. | liliana, the most beautiful and lovely assistant of our team! |

### Generate speech with Python script[](#id29 "Permalink to this heading")

```auto
cd /path/to/sherpa-onnx

python3 ./python-api-examples/offline-tts.py \
 --vits-model=./vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx \
 --vits-data-dir=./vits-piper-en_US-lessac-medium/espeak-ng-data \
 --vits-tokens=./vits-piper-en_US-lessac-medium/tokens.txt \
 --output-filename=./armstrong-piper-en_US-lessac-medium.wav \
 "That's one small step for a man, a giant leap for mankind."
```

Hint

You can also use

> ```auto
> cd /path/to/sherpa-onnx
>
> python3 ./python-api-examples/offline-tts-play.py \
>   --vits-model=./vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx \
>   --vits-data-dir=./vits-piper-en_US-lessac-medium/espeak-ng-data \
>   --vits-tokens=./vits-piper-en_US-lessac-medium/tokens.txt \
>   --output-filename=./armstrong-piper-en_US-lessac-medium.wav \
>   "That's one small step for a man, a giant leap for mankind."
> ```
>
> which will play the audio as it is generating.

After running, it will generate a file `armstrong-piper-en_US-lessac-medium.wav` in the current directory.

```auto
soxi ./armstrong-piper-en_US-lessac-medium.wav

Input File     : './armstrong-piper-en_US-lessac-medium.wav'
Channels       : 1
Sample Rate    : 22050
Precision      : 16-bit
Duration       : 00:00:03.74 = 82432 samples ~ 280.381 CDDA sectors
File Size      : 165k
Bit Rate       : 353k
Sample Encoding: 16-bit Signed Integer PCM
```

| Wave filename | Content | Text |
| --- | --- | --- |
| armstrong-piper-en\_US-lessac-medium.wav | Your browser does not support the `audio` element. | That's one small step for a man, a giant leap for mankind. |

### RTF on Raspberry Pi 4 Model B Rev 1.5[](#id30 "Permalink to this heading")

We use the following command to test the RTF of this model on Raspberry Pi 4 Model B Rev 1.5:

```auto
for t in 1 2 3 4; do
 ./build/bin/sherpa-onnx-offline-tts \
   --num-threads=$t \
   --vits-model=./vits-piper-en_US-lessac-medium/en_US-lessac-medium.onnx \
   --vits-data-dir=./vits-piper-en_US-lessac-medium/espeak-ng-data \
   --vits-tokens=./vits-piper-en_US-lessac-medium/tokens.txt \
   "Friends fell out often because life was changing so fast. The easiest thing in the world was to lose touch with someone."
done
```

The results are given below:

> | num\_threads | 1 | 2 | 3 | 4 |
> | --- | --- | --- | --- | --- |
> | RTF | 0.774 | 0.482 | 0.390 | 0.357 |
