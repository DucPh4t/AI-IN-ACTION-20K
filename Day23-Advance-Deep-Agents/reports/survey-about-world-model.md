# Survey of World Models in AI

## TL;DR
- World models serve as internal simulators that allow agents to predict environment dynamics, essential for robust decision-making [1][2].
- Architectures are shifting from pixel-level reconstruction toward latent-space predictive models to improve efficiency and task relevance [3][4].
- Recent innovations include amortized planning, which replaces computationally expensive iterative optimization [5][6].
- Embodied AI deployment remains a challenge, necessitating advancements in long-horizon manipulation benchmarks and runtime safety guardrails [7][8][9].

## Background
World models are cognitive architectures for AI agents that enable the internal representation of environmental dynamics. By predicting future states based on current observations and potential actions, these models facilitate model-based reinforcement learning and informed decision-making [1]. In complex domains like autonomous driving, world models are used to simulate potential scenarios in latent space to ensure safety and precision [2].

## Core Architectures and Formulations
Modern world models move beyond pixel-level reconstruction to avoid wasting capacity on irrelevant details. Predictive latent architectures, such as the Joint-Embedding Predictive Architecture (JEPA), are increasingly used as "world anchors" to focus on semantically significant information [3]. Transformer-based frameworks have emerged as a dominant approach, utilizing Mixture-of-Transformer (MoT) architectures to unify understanding, video generation, and action control [6]. Additionally, self-supervised learning objectives like "Next-Latent Prediction" have been shown to produce more compact and generalizable world representations compared to traditional predictive coding [4]. Beyond single-agent setups, multi-agent egocentric world models have been developed to model synchronized first-person visual and action interactions in shared physical environments [10].

## Training and Optimization
A significant bottleneck in traditional world models is the reliance on iterative, black-box online optimization during trajectory planning. Recent developments, such as generative latent flow planning, address this by amortizing the planning process, significantly reducing computational overhead at inference time [5]. For autonomous agents, hierarchical reinforcement learning is often used to fine-tune world models, enabling agents to decompose complex long-horizon tasks into manageable sub-tasks [2].

## Applications and Benchmarks
The evaluation of world models in robotics is transitioning from rigid-body environments to complex, long-horizon deformable object manipulation, as highlighted by new benchmarks like RoboFolDeX [7]. Despite these advances, there remains a significant performance gap between simulated benchmarks and physical-world execution [11]. To bridge this gap across robotic embodiments, counterfactual post-training and geometric calibration have been proposed to ensure action-faithful video predictions [12]. Furthermore, research into self-evolving humanoids suggests that post-deployment adaptation is required to handle domain shifts, though effective evaluation mechanisms for these self-improving agents are still in their infancy [8].

## Trends and Open Problems
The field faces several critical challenges, most notably the safety of autonomous embodied systems. As world models are deployed in black-box configurations, there is a pressing need for runtime authorization frameworks that can intercept or adjust harmful actions before they are executed in the physical world [9]. Additionally, ensuring generalization across diverse physical interaction regimes remains a primary hurdle. Future research is expected to focus on bridging the gap between simulation and the physical world through robust runtime guardrails and enhanced self-evolution mechanisms [8][9].

## References
[1] Redefining Affordance via Computational Rationality. arxiv. https://arxiv.org/abs/2501.09233 (2025-01-16)
[2] WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning for Autonomous Driving. hf-search. https://huggingface.co/papers/2512.19133 (2025-12-22)
[3] LeapBot-WA: World-Anchor Action Models via Predictive Latent Alignments. arxiv. https://arxiv.org/abs/2607.23969 (2026-07-27)
[4] Next-Latent Prediction Transformers Learn Compact World Models. hf-search. https://huggingface.co/papers/2511.05963 (2025-11-08)
[5] LeFlow: Generative Latent Flow Planning for World Models. arxiv. https://arxiv.org/abs/2608.24855 (2026-08-25)
[6] Motus: A Unified Latent Action World Model. hf-search. https://huggingface.co/papers/2512.13030 (2025-12-15)
[7] RoboFolDeX: A Physical-World Benchmark for Long-Horizon Robotic Manipulation of Deformable Objects. arxiv. https://arxiv.org/abs/2609.10243 (2026-09-09)
[8] Self-Evolving AI for Humanoids: Mechanisms, Safety, and Evaluation of Post-Deployment Self-Improvement. arxiv. https://arxiv.org/abs/2609.13236 (2026-09-02)
[9] Silent Failures in Physical AI: A Literature Review of Runtime Action Authorization for Autonomous Systems. hf-search. https://huggingface.co/papers/2606.00090 (2026-05-23)
[10] Multi-Agent Egocentric World Model with Fine-Grained Embodied Interaction. hf-daily. https://huggingface.co/papers/2610.12299 (2026-10-08)
[11] ACWM-Phys: Investigating Generalized Physical Interaction in Action-Conditioned Video World Models. hf-search. https://huggingface.co/papers/2605.08567 (2026-05-09)
[12] DreamTrue: Action-Faithful Robot World Model with Counterfactual Post-Training. hf-daily. https://huggingface.co/papers/2610.12468 (2026-10-08)
