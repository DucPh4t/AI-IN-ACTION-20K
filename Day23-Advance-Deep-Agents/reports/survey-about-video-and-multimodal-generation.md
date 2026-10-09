# Survey on Video and Multimodal Generation

## TL;DR
- Recent advancements shift from traditional generative models to diffusion-based transformer architectures for improved temporal coherence and controllability [1][2][3].
- Scalability is increasingly addressed by models trained from scratch, reducing reliance on massive pretraining while improving world-state physical grounding [4][5].
- New methods for long-form generation introduce specialized context-retrieval mechanisms to mitigate error accumulation over time [6][7].
- Benchmarking has evolved beyond aesthetic assessment to prioritize physical reasoning, program adherence, and semantic text rendering [8][9][10].

## Background
Video and multimodal generation aims to synthesize sequences of frames that are temporally coherent and semantically aligned with conditioning signals (e.g., text, images, or camera trajectories). Traditional approaches often relied on GANs or early autoregressive models using VQ-VAE for frame discretization [3]. The field has recently evolved toward large-scale diffusion transformer frameworks, which allow for better representation learning and temporal modeling through spatiotemporal attention mechanisms [2][11].

## Core Architectures
Modern architectures for video generation utilize masked modeling and hierarchical tokenization to process complex motion dynamics. For example, frameworks like TKCAM [1] use discrete kinematic tokens, allowing for precise control over camera motion based on textual and keyframe inputs. Complementing this, diffusion transformers such as CPA [2] leverage camera-pose-aware mechanisms to maintain structural consistency. These transformer-centric approaches have largely superseded early models that relied heavily on 3D convolutions with VQ-VAEs [3], offering superior flexibility in multi-modal conditioning.

## Training & Optimization
Efficiency in training is a central concern. Recent works investigate how to achieve high-fidelity generation without the constraints of large-scale, pretrained video backbones [4]. Training-from-scratch initiatives, such as MiniWorld, have demonstrated that it is possible to learn complex physical dynamics directly through autoregressive state transitions rather than distillation [5]. To ensure consistency in long-form generation, new techniques such as MemoryPack and Direct Forcing improve temporal continuity by implementing learnable context retrieval, effectively limiting the drift and error accumulation typically associated with autoregressive generation [6]. Visual consistency in image-to-video tasks is similarly enhanced through noise initialization optimization and spatiotemporal attention [11].

## Applications & Benchmarks
Evaluation has pivoted toward objective, program-oriented metrics. PROWBench specifically assesses the adherence of world models to defined temporal event transitions [8]. Complementing this, VTR-Bench identifies the critical need for accurate visual text rendering within dynamic video contexts [9]. On the side of physical reasoning, frameworks like PhysStream leverage online-derived positional maps for streaming, physics-grounded interactions [7]. WorldScore provides a unified framework to decompose and assess world models, emphasizing that high aesthetic scores do not necessarily correlate with controllability or physical accuracy [10]. Beyond standard 2D video generation, frameworks like OuroWorld extend synthesis to 3D dynamic scenes by generating endlessly looping cinemagraphs with periodic deformation fields [12].

## Trends and open problems
- **Physical Grounding:** Bridging the gap between visually realistic video and physics-aware world modeling remains a significant challenge [7][10].
- **Programmatic Control:** Developing models that reliably follow complex, programmatic instructions for event scheduling is an area of intense research [8].
- **Efficiency:** Further democratizing training remains a priority, with a move away from reliance on massive compute towards more data-efficient learning-from-scratch methodologies [4][5].
- **Long-form consistency:** Maintaining semantic and visual fidelity over extended durations continues to require advanced memory architectures [6].

## References
[1] TKCAM: Text and Keyframe to Camera Trajectory Generation. arxiv. https://arxiv.org/abs/2610.11105 (2026-10-08)
[2] CPA: Camera-pose-awareness Diffusion Transformer for Video Generation. hf-search. https://huggingface.co/papers/2412.01429 (2024-12-02)
[3] VideoGPT: Video Generation using VQ-VAE and Transformers. hf-search. https://huggingface.co/papers/2104.10157 (2021-04-20)
[4] Latent evolving World Action Model. arxiv. https://arxiv.org/abs/2609.27455 (2026-09-23)
[5] MiniWorld: Democratizing the Training of Video World Models from Scratch. arxiv. https://arxiv.org/abs/2608.01127 (2026-08-02)
[6] Pack and Force Your Memory: Long-form and Consistent Video Generation. hf-search. https://huggingface.co/papers/2510.01784 (2025-10-02)
[7] PhysStream: Streaming Physics-Grounded Video Generation. arxiv. https://arxiv.org/abs/2609.17521 (2026-09-15)
[8] PROWBench: Do Video Models Render What the Program Specifies?. arxiv. https://arxiv.org/abs/2610.02205 (2026-10-01)
[9] VTR-Bench: A Systematic Benchmark for Evaluating Visual Text Rendering in Video Generation. hf-search. https://huggingface.co/papers/2610.01499 (2026-10-01)
[10] WorldScore: A Unified Evaluation Benchmark for World Generation. hf-search. https://huggingface.co/papers/2504.00983 (2025-04-01)
[11] ConsistI2V: Enhancing Visual Consistency for Image-to-Video Generation. hf-search. https://huggingface.co/papers/2402.04324 (2024-02-06)
[12] OuroWorld: Bringing Any 3D World Alive as Diverse, Endlessly Looping 3D Cinemagraphs. hf-daily. https://huggingface.co/papers/2610.12461 (2026-10-08)
