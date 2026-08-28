---
license: odc-by
size_categories:
- 10K<n<100K
---
> [!NOTE]
> For full information, go check out the Dr Tulu paper [here](https://arxiv.org/abs/2511.19399).

<img src="https://huggingface.co/rl-research/DR-Tulu-SFT-8B/resolve/main/dr_tulu_logo.png" alt="Figure 1" width="500"/>

# DR Tulu SFT Data

This dataset contains the SFT training data for DR Tulu, containing prompts and full trajectories including reasoning traces, tool calls, and answers with citations. 
The source prompts are curated from [OpenScholar](https://huggingface.co/datasets/allenai/openscilm_queries), [Search Arena](https://huggingface.co/datasets/lmarena-ai/search-arena-24k), and short-form QA datasets inclduing [WebWalker-Silver](https://huggingface.co/datasets/callanwu/WebWalkerQA), [TaskCraft](https://huggingface.co/datasets/PersonalAILab/TaskCraft), [PopQA](https://huggingface.co/datasets/akariasai/PopQA) and [TyDiQA (English)](https://github.com/google-research-datasets/tydiqa).

**Important**: This does *not* contain the SFT subsets created using prompts from [MegaScicen](MegaScience/MegaScience), [HotpotQA](https://hotpotqa.github.io/), and ScholarQA. We will release those subsets shortly in a separate file. 


## License

This dataset is licensed under ODC-BY. It is intended for research and educational use in accordance with [Ai2's Responsible Use Guidelines](https://allenai.org/responsible-use).