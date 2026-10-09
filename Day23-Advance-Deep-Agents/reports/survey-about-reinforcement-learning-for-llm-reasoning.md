# Reinforcement Learning for LLM Reasoning: A Survey

## TL;DR
- Reinforcement learning (RL) has become a primary driver for enhancing LLM reasoning, transitioning from standard PPO to preference-based methods (DPO) and process-supervised training (GRPO, CAPO) [1][2][3][4].
- Aligning the reasoning process, rather than focusing solely on final outcomes, is crucial to mitigating reward hacking and deceptive alignment [3][5].
- Effective reasoning scaling now combines RL training with test-time compute strategies, such as verifier integration [6].
- Emerging research highlights the importance of leveraging pre-training data and autonomous trajectory exploration to achieve generalizable reasoning [7][8].

## Background
Reasoning in large language models refers to the capacity to decompose complex problems into logical, sequential steps to reach a correct conclusion. Traditional fine-tuning often struggles to capture the nuances of multi-step logical progression. Reinforcement Learning has emerged as a powerful framework to steer model outputs toward valid reasoning paths by assigning rewards for intermediate steps or final logical correctness [1]. Fundamental frameworks include PPO [9] and more recent, efficient alternatives like DPO [2], which simplify optimization by avoiding explicit value function estimation.

## Core Architectures and Formulations
Modern RL frameworks for reasoning prioritize structural alignment over raw performance. Methods like GRPO [1] and CAPO [4] leverage process-supervision, providing feedback at the token level to refine reasoning chains. The shift toward process-supervised RL is largely motivated by the need for interpretable and reliable chains of thought [3][10]. Furthermore, Turn-PPO [9] enhances multi-turn reasoning by implementing turn-level advantage estimation, addressing stability issues in long-horizon tasks. While some approaches advocate for complex algorithmic strategies, systematic reviews suggest that minimalist implementations can often achieve superior performance [11].

## Training and Optimization
Optimization at scale presents a significant challenge. Systems like DAPO [12] demonstrate that decoupled policy optimization and dynamic sampling are essential for reproducibility and efficiency when training at scale. Moreover, researchers are exploring innovative reward generation methods; inverse reinforcement learning (IRL) frameworks can learn token-level reasoning rewards directly from expert demonstrations [10]. The training process is further enriched by exploring pre-training data distributions, which allows models to acquire generalizable reasoning skills without relying solely on costly, curated human labels [7][8]. Recent studies even investigate the geometry of the activation space, suggesting that RL-induced gains occupy low-dimensional manifolds, providing insights into model trainability and compression [13].

## Applications and Benchmarks
Benchmark performance, particularly on datasets like MATH, serves as the primary metric for evaluating progress. Integration with verifiers enables models to scale through test-time compute, where RL^V [6] exemplifies how unified reasoners can significantly improve reasoning accuracy. Furthermore, outcome-based reward modeling has proven insufficient for complex tasks, as models often arrive at correct answers via flawed reasoning—a phenomenon termed "deceptive alignment" [5]. Consequently, robust evaluation frameworks now emphasize rationale consistency and step-by-step verification, which effectively combat reward hacking [3].

## Trends and Open Problems
- **Process Supervision:** A definitive trend toward process-supervised reward models to replace outcome-only approaches.
- **Test-Time Scaling:** Leveraging verifiers and test-time compute as a key scaling pillar distinct from pre-training parameter counts [6].
- **Data Efficiency:** Reducing reliance on human-labeled data by leveraging existing pre-training data and autonomous trajectory exploration [7][8].
- **Interpretability & Geometry:** Investigating the internal representations and activation patterns of RL-tuned models to understand how they acquire "reasoning" skills [13].
- **Reward Robustness:** Tackling the fundamental challenge of reward hacking and ensuring that models learn valid, logical processes rather than simply optimizing for the reward signal [5].

## References
[1] Reasoning-Aware GRPO using Process Mining. hf-search. https://huggingface.co/papers/2510.25065 (2025-10-29)
[2] Enhancing LLM Reasoning with Iterative DPO: A Comprehensive Empirical Investigation. hf-search. https://huggingface.co/papers/2503.12854 (2025-03-17)
[3] Save the Good Prefix: Precise Error Penalization via Process-Supervised RL to Enhance LLM Reasoning. hf-search. https://huggingface.co/papers/2601.18984 (2026-01-26)
[4] CAPO: Towards Enhancing LLM Reasoning through Verifiable Generative Credit Assignment. hf-search. https://huggingface.co/papers/2508.02298 (2025-08-04)
[5] Outcome Accuracy is Not Enough: Aligning the Reasoning Process of Reward Models. hf-search. https://huggingface.co/papers/2602.04649 (2026-02-04)
[6] Putting the Value Back in RL: Better Test-Time Scaling by Unifying LLM Reasoners With Verifiers. hf-search. https://huggingface.co/papers/2505.04842 (2025-05-07)
[7] Reinforcement Learning on Pre-Training Data. hf-search. https://huggingface.co/papers/2509.19249 (2025-09-23)
[8] Training Large Language Models for Reasoning through Reverse Curriculum Reinforcement Learning. arxiv. https://arxiv.org/abs/2402.05808 (2024-02-08)
[9] Turn-PPO: Turn-Level Advantage Estimation with PPO for Improved Multi-Turn RL in Agentic LLMs. hf-search. https://huggingface.co/papers/2512.17008 (2025-12-18)
[10] Learning Reasoning Reward Models from Expert Demonstration via Inverse Reinforcement Learning. arxiv. https://arxiv.org/abs/2510.01857 (2025-10-02)
[11] Part I: Tricks or Traps? A Deep Dive into RL for LLM Reasoning. hf-search. https://huggingface.co/papers/2508.08221 (2025-08-11)
[12] DAPO: An Open-Source LLM Reinforcement Learning System at Scale. hf-search. https://huggingface.co/papers/2503.14476 (2025-03-18)
[13] Learning to Steer, Steering to See: Unveiling the Geometry of RLVR in Large Language Models via Trainable Vectors. hf-daily. https://huggingface.co/papers/2609.34344 (2026-09-28)
