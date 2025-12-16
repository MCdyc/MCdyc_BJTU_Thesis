#set text(font: "Sarasa Gothic SC")
= 基于显式知识库的用户可控型 Agent 设计与实现
== 毕业设计（论文）基本内容和要求：
本课题研究大型语言模型（LLM）智能体中的记忆系统（Agentic Memory）机制，围绕智能体如何在长期任务中进行信息存储、检索、组织、反思与自演化展开。研究目标是设计并实现一个 多层次结构化记忆系统（Tri-Memory System），结合经验驱动自演进（Experience-Driven Self-Evolving Agent）、记忆图谱（A-Mem Graph）、文本分段（TextTiling）、分层摘要（Hierarchical Merging） 等技术，实现一个能够随交互持续成长的 LLM-Agent。
学生需要具备自然语言处理、信息检索、Python 工程能力与深度学习基础知识，完成以下核心研究内容：
总结并分析现有 Agentic Memory、RAG、长上下文处理、记忆管理等方向的研究进展；
设计并实现三层记忆结构（Strategic / Procedural / Tool）及其存储格式；
基于经验驱动（Experience-Driven）策略构建动态更新机制，包括记忆写入、合并、遗忘、反思与删除；
构建一套可运行的 LLM-Agent Demo 支持基于记忆的问答与任务执行；
完成论文撰写，论述系统设计、算法流程、实验结果及对比分析。
== 毕业设计（论文）重点研究的问题：
+ 如何构建结构化的三层记忆体系并在交互中实现自组织与自演进？
+ 如何利用 RAG、语义检索与图谱扩展实现跨层次的关联性联想？
+ 如何设计动态记忆管理机制，实现记忆的写入、更新、反思、合并与遗忘？
+ 整体系统如何评估？记忆质量与检索有效性如何量化？
== 毕业设计（论文）应完成的工作：
+ 系统架构设计
设计 Tri-Memory 三层记忆结构与存储 schema。
设计动态记忆管理框架：写入、合并、遗忘、删除、反思。
+ 核心算法实现
实现语义检索（RAG）、图谱扩展、时间权重与多因素重排。
实现记忆演化（经验驱动）与错误传播控制机制。
+ 系统开发与 Demo 实现
记忆存储模块、检索模块、外部文件导入模块、Agent 回答模块。
实现一个可运行的 LLM Agent Demo，展示记忆增强能力。
+ 实验设计与评估
对比 A-Mem、MemoryBank 等 baseline。
== 参考资料推荐：
[1] Brown T, Mann B, Ryder N, et al. Language models are few-shot learners[J]. Advances in neural information processing systems, 2020, 33: 1877-1901.

[2] Achiam J, Adler S, Agarwal S, et al. Gpt-4 technical report[J]. arXiv preprint arXiv:2303.08774, 2023.

[3] Hoffmann J, Borgeaud S, Mensch A, et al. Training compute-optimal large language models[C]\/\/Proceedings of the 36th International Conference on Neural Information Processing Systems. 2022: 30016-30030.

[4] Touvron H, Lavril T, Izacard G, et al. Llama: Open and efficient foundation language models[J]. arXiv preprint arXiv:2302.13971, 2023.

[5] Touvron H, Martin L, Stone K, et al. Llama 2: Open foundation and fine-tuned chat models[J]. arXiv preprint arXiv:2307.09288, 2023.

[6] Devlin J, Chang M W, Lee K, et al. Bert: Pre-training of deep bidirectional transformers for language understanding[C]\/\/Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers). 2019: 4171-4186.

[7] Raffel C, Shazeer N, Roberts A, et al. Exploring the limits of transfer learning with a unified text-to-text transformer[J]. Journal of machine learning research, 2020, 21(140): 1-67.

[8] Lewis P, Perez E, Piktus A, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks[J]. Advances in neural information processing systems, 2020, 33: 9459-9474.

[9] Borgeaud S, Mensch A, Hoffmann J, et al. Improving language models by retrieving from trillions of tokens[C]\/\/International conference on machine learning. PMLR, 2022: 2206-2240.

[10] Gao Y, Xiong Y, Gao X, et al. Retrieval-Augmented Generation for Large Language Models: A Survey[J]. CoRR, 2023.

[11] Khandelwal U, Levy O, Jurafsky D, et al. Generalization through Memorization: Nearest Neighbor Language Models[C]\/\/International Conference on Learning Representations.

[12] Zhang Z, Dai Q, Bo X, et al. A survey on the memory mechanism of large language model-based agents[J]. ACM Transactions on Information Systems, 2025, 43(6): 1-47.

[13] Zhong W, Guo L, Gao Q, et al. Memorybank: Enhancing large language models with long-term memory[C]\/\/Proceedings of the AAAI Conference on Artificial Intelligence. 2024, 38(17): 19724-19731.

[14] Fathullah Y, Wu C, Lakomkin E, et al. Audiochatllama: Towards general-purpose speech abilities for llms[C]\/\/Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). 2024: 5522-5532.

[15] Arandas L, Grierson M, Carvalhais M. Antagonising explanation and revealing bias directly through sequencing and multimodal inference[J]. arXiv e-prints, 2023: arXiv: 2309.12345.

[16] Shinn N, Cassano F, Gopinath A, et al. Reflexion: Language agents with verbal reinforcement learning[J]. Advances in Neural Information Processing Systems, 2023, 36: 8634-8652.

[17] HU M, MU Y, YU X, et al. Tree-Planner: Efficient Close-loop Task Planning with Large Language Models[C]\/\/ Kim B, Yue Y, Chaudhuri S, et al. International Conference on Learning Representations. 2024: 48669-48696.

[18] Masson S J, Yan Z, Ho J, et al. State-insensitive wavelengths for light shifts and photon scattering from Zeeman states[J]. Physical Review A, 2024, 109(6): 063105.

[19] Xu W, Mei K, Gao H, et al. A-mem: Agentic memory for llm agents[J]. arXiv preprint arXiv:2502.12110, 2025.

[20] Xiong Z, Lin Y, Xie W, et al. How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior[J]. arXiv e-prints, 2025: arXiv: 2505.16067.

[21] Yang C, Yang X, Wen L, et al. Learning on the Job: An Experience-Driven Self-Evolving Agent for Long-Horizon Tasks[J]. arXiv preprint arXiv:2510.08002, 2025.

[22] Chatterjee M, Agarwal D. Semantic Anchoring in Agentic Memory: Leveraging Linguistic Structures for Persistent Conversational Context[J]. arXiv preprint arXiv:2508.12630, 2025.

[23] Lu B R, Hu Y, Cheng H, et al. Unsupervised Learning of Hierarchical Conversation Structure[C]\/\/Findings of the Association for Computational Linguistics: EMNLP 2022. 2022: 5657-5670.

[24] Ou L, Lapata M. Context-aware hierarchical merging for long document summarization[J]. arXiv preprint arXiv:2502.00977, 2025.

[25] Park J S, O'Brien J, Cai C J, et al. Generative agents: Interactive simulacra of human behavior[C]\/\/Proceedings of the 36th annual acm symposium on user interface software and technology. 2023: 1-22.

[26] Wang G, Xie Y, Jiang Y, et al. Voyager: An Open-Ended Embodied Agent with Large Language Models[J]. Transactions on Machine Learning Research.

[27] Ake D, Bouzas A O, Larios F. Top Quark Flavor Changing Couplings at a Muon Collider, Adv[J]. High Energy Phys, 2024, 2038180(2311.09488).

[28] Liu X, Yu H, Zhang H, et al. AgentBench: Evaluating LLMs as Agents[C]\/\/The Twelfth International Conference on Learning Representations.

[29] Yan S, Yang X, Huang Z, et al. Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning[J]. arXiv preprint arXiv:2508.19828, 2025.

[30] Zhang Z, Dai Q, Li R, et al. Learn to memorize: Optimizing llm-based agents with adaptive memory framework[J]. arXiv preprint arXiv:2508.16629, 2025.

[31] Ai Q, Tang Y, Wang C, et al. MemoryBench: A Benchmark for Memory and Continual Learning in LLM Systems[J]. arXiv preprint arXiv:2510.17281, 2025.


