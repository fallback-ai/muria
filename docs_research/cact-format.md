# Source: https://cactuscompute.com/blog/cact-format

[![Cactus](https://cactuscompute.com/assets/cactus_white.png)Cactus](/)

⌘K[4.2k+ stars](https://github.com/cactus-compute/needle)

[Fine-tune Needle](/signup)

[[NEW]Needle 3: our 8-29 MB foundation model for tiny devices](/needle)

[Back to blog](/blog)

Guides

# The .cact Format

Needle ships as one file that the engine maps into memory and reads in place: a 196-byte header with the whole architecture, a nameless tensor directory, and Cactus-Quantised blobs at 2.125 bits per weight. What is in it, how the quantisation works, how the kernel reads it without ever unpacking, and how to parse it yourself in twenty lines.

PS

Parkirat Sandhu

|September 18, 2026|9 min read

A model that runs on a router or a watch cannot afford a loader. It cannot parse JSON, resolve tensor names, convert dtypes, or hold two copies of the weights while it rearranges one into the other. Needle's answer is `.cact`: a single little-endian file whose bytes are already in the shape the kernel wants, so the engine maps it into memory and starts computing. This post is the format, the quantisation inside it, and the reasons for both.

## [Five regions](#five-regions)

One file, read in placethe shipped 20-layer needle3.cact, 29 MB, mapped into memory and never parsed into anything elseheader196 Bcodebooks112 Bdirectory581 × 44 Btensor blobs29 MBtokenizer111 KBoffset 0end of filelittle-endian throughout; every offset in the directory is absolute

The layout. A fixed header carries the geometry, so one engine binary loads any depth or width of the architecture; a nameless directory says where each tensor is; the blobs follow in the order the forward pass reads them.

**Header, 196 bytes.** Forty-nine 32-bit fields: a format tag, the number of tensors, the codebook length, then the entire architecture geometry: vocabulary and output vocabulary, model width, heads and KV heads, layer count, head dimensions, context length, the Hadamard size, the number of residual lanes, the sliding window and the bitmask of global-attention layers, the conv tap count, and every engram parameter (slots, sub-dimension, table count, taps, dilation, orders, the layer sites). The last field is `rope_theta` as a float. Because the geometry rides in the file, one engine binary loads any configuration of the architecture: the 20-layer archive, an 8-layer subnetwork, a fine-tune with the same shape.

Two header fields are numerics rather than geometry. `kv_window` is the sliding-window width the model was trained with, and `kv_bits` is the KV-cache precision it was post-trained for (8 for int8, else 2, 3 or 4). They are in the blob because a model quantised for one must be run at it; leaving either to a runtime flag would silently serve the wrong numerics.

**Codebooks, 112 bytes.** Twenty-eight floats: the 4-entry, 8-entry and 16-entry Lloyd-Max codebooks for 2-, 3- and 4-bit weights, concatenated so the runtime can index by width. The ternary and binary codebooks are analytic and are not stored.

**Directory, 44 bytes per tensor.** `u8 dtype, u8 ndim, u16 pad, u32 shape[4], u64 offset, u64 nbytes, u32 group, u32 bits`. There are no names. Tensors are positional, in a fixed order the runtime knows: the embedding, then every tensor of layer 0, then layer 1, and so on, then the lane-mixing blocks, the engram sites, the final norm, the optional probe heads, and one RAW attachment. The order is layer-major on purpose: the working set for one block is one contiguous span of the file, which is what a cache and a prefetcher want.

**Blobs.** Each tensor's bytes at its absolute offset, 64-byte aligned. Matrices are stored `[out, in]`, pre-transposed, so an output row is contiguous along the reduction axis and quantisation groups run along it. The dtype is one of FP16, FP32, CQ (with `bits` giving the width) or RAW.

**Tokenizer.** The RAW attachment is a self-contained dump of the SentencePiece BPE model: piece count, the special ids, and one record per piece with its score, type and UTF-8 surface. The engine tokenises from it directly; nothing else is needed on the device.

## [Cactus Quants](#cactus-quants)

Every matrix in the file is quantised in groups of 128 weights along the input dimension. A group is not quantised as it is; it is first rotated.

1 · take a group128 consecutive weights of one output row0

Cactus Quants on one group (24 of the 128 lanes shown). The rotation makes every group look Gaussian, so one codebook fits all of them; the norm keeps the scale; the indices are all that is stored per weight.

Multiplying a group by the normalised Walsh-Hadamard matrix HHH spreads every weight's energy across all 128 coordinates, so whatever the group looked like before, after rotation it looks like a sample from a Gaussian. That is the property that makes a single codebook work for every group in the model. The rotated group is then split into its length, stored as one fp16 number, and its direction, a point on the unit sphere whose coordinates are quantised independently against the Lloyd-Max codebook for that width. What is written per group is 128⋅b128 \cdot b128⋅b bits of indices and 16 bits of norm, so the cost per weight is b+1/8b + 1/8b+1/8: 2.125 bits at CQ2, 4.125 at CQ4.

Reconstruction is the reverse: w=(codebook[idx]⋅norm) Hw = (\mathrm{codebook}[idx] \cdot \mathrm{norm})\, Hw=(codebook[idx]⋅norm)H. HHH is symmetric and orthogonal, so it is its own inverse and there is nothing to invert. The bit packing is one continuous LSB-first stream per row; at four bits it is the familiar low-nibble-first layout, at two bits four indices per byte. Ternary weights use a separate 2-bit "crumb" encoding whose codes sign-extend straight to −1,0,+1-1, 0, +1−1,0,+1 in the kernel, and binary weights pack eight per byte; both have closed-form centroids, which is why their codebooks are not in the header.

Fine-tuning in the Python package trains through these numerics at 4 bits, so an adapter merged by `needle build` lands in the same format; the 2-bit archive that ships is produced by the post-training and quantisation on the [Cactus Platform](/dashboard).

## [How the kernel reads it](#how-the-kernel-reads-it)

The point of storing indices rather than values is that the kernel never expands them. For a matmul it takes the activation, rotates each 128-lane group of it with the same Hadamard transform (a fast Walsh-Hadamard butterfly in registers), and quantises the rotated group to int8 with one scale per group. From there a dot product between a weight row and the activation is a table lookup of int8 centroids by the packed indices, a `sdot` accumulate against the int8 activations, and one multiply per group by the product of the weight norm, the activation scale and the codebook scale. The rotation on the weight side cancels against the rotation on the activation side because HHH is orthogonal, so the answer is exact up to the quantisation itself, and no weight is ever materialised as a float.

That is what the exporter calls CQ-W2A8: weights at 2 bits, activations at 8, groups of 128, and a kernel that consumes the file's bytes as they are. The same path serves the KV cache at whatever `kv_bits` the header declares.

## [The shipped archive by the numbers](#the-shipped-archive-by-the-numbers)

What the bytes areneedle3.cact, 20 layers, 581 tensors, read from its own directoryCQ2 · 115 tensorsattention, MLP, engram tables and projections84.7%CQ4 · 7 tensorsembedding, lane maps, confidence head11.4%FP16 · 456 tensorsnorms, diagonals, gates, taps, biases3.6%RAW · 1 tensorthe tokenizer0.3%2.125 bits per weight at CQ2 · 4.125 at CQ4 · the five engram tables alone are two thirds of the weight bytes

Every matrix the blocks multiply through is CQ2; the embedding, which is also the output head, the lane maps and the confidence head keep 4 bits; everything elementwise stays half precision. The numbers come straight from the directory records.

The 20-layer `needle3.cact` is 29 MB of 2-bit weights in 581 tensors. 115 of them are CQ2 and carry 85% of the bytes; five of those, one per engram site, are the n-gram tables, 110,592 rows of 128 each, two thirds of the weight bytes on their own. Seven tensors are CQ4: the embedding, which is also the tied output head, the three lane-mixing maps of the multi-lane residual, and the three matrices of the confidence head. The 456 FP16 tensors are the norms, Hadamard diagonals, gates, conv taps and biases, under 4% of the file, and the tokenizer is 111 KB. The header says the rest: 20 layers, width 768, 12 query heads over 2 KV heads, context 8192, a 1024-token local window, four residual lanes, an int8 KV cache trained at a window of 256.

## [Subnetworks are just shorter files](#subnetworks-are-just-shorter-files)

The [intelligence ladder](/blog/intelligence-ladders) makes every depth from 2 to 20 a trained model, and the format makes each one a file. `needle build --layers 8` keeps the blocks that depth selects, writes `num_layers = 8` and the matching engram sites into the header, and emits only those blocks' tensors. The engine reads the header, sizes itself, and runs; nothing in the binary knows or cares which depth it was handed. That is how one engine under 1 MB serves the whole ladder, and how a fine-tune exported at 2 layers ends up a few megabytes.

## [Reading one yourself](#reading-one-yourself)

The format needs no library. This reads the header and the directory and adds up the bytes by type:

```auto
import struct, collections

b = open("needle3.cact", "rb").read()
u = lambda o: struct.unpack_from("<I", b, o)[0]
assert u(0) == 0x05E12A84, "not a Needle 3 archive"
n_tensors, cb_len = u(4), u(8)
layers, d_model, vocab = u(40), u(28), u(20)
print(f"{layers} layers, width {d_model}, vocab {vocab}, kv {u(16)} bits")

off = 196 + cb_len * 4
by_kind = collections.Counter()
for _ in range(n_tensors):
    dtype, ndim = b[off], b[off + 1]
    shape = struct.unpack_from("<4I", b, off + 4)[:ndim]
    start, nbytes = struct.unpack_from("<QQ", b, off + 20)
    group, bits = struct.unpack_from("<II", b, off + 36)
    by_kind[{1: "fp16", 2: "fp32", 3: f"cq{bits}", 4: "raw"}[dtype]] += nbytes
    off += 44
print({k: round(v / 1e6, 2) for k, v in by_kind.items()})
```

`needle.model.export.read_export` in the package does the same and also dequantises, which is the reference for anyone writing a loader in another language.

## [Versions](#versions)

The tag is the contract. `0x05E12A83` is the Needle 2 format and `0x05E12A84` is Needle 3; the Python package reads the first four bytes and picks the matching engine, and an engine handed the other generation's tag refuses with a message rather than guessing. Within a generation the archive is tied to the engine version that wrote it, so a `.cact` built by an older package should be rebuilt with the current one rather than patched. Everything else about the file is meant to be boring: fixed offsets, fixed order, little-endian, and a directory that says exactly where every byte is.
