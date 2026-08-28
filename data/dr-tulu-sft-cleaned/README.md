---
license: odc-by
task_categories:
- text-generation
- text-retrieval
- text-ranking
- table-question-answering
language:
- en
tags:
- agent
- deep-research
- dr-tulu
- search
- tool-use
pretty_name: DR-Tulu SFT Data Cleaned
size_categories:
- 10K<n<100K
---
# Deep Research - Tulu SFT Data Cleaned Rectified

<div align="center">

### 👥 Follow the Author

**Supriti Vijay**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/supriti-vijay/)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/SupritiVijay)
[![Website](https://img.shields.io/badge/Website-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://supritivijay.github.io/)

</div>

## Overview

This dataset is a cleaned and restructured version of the [DR-TULU SFT dataset](https://huggingface.co/datasets/rl-research/dr-tulu-sft-data) released by AllenAI's RL Research team. The original DR-TULU dataset represents significant work in creating high-quality training data for reasoning-enhanced language models with tool use capabilities. This version addresses structural issues in the original release while preserving the content quality and expanding the dataset's utility for multi-turn tool-use training.

**Original Dataset:** [rl-research/dr-tulu-sft-data](https://huggingface.co/datasets/rl-research/dr-tulu-sft-data)  
**Original Paper:** [DR-TULU Paper](https://arxiv.org/abs/2511.19399)  
**Tool-Use Format Inspiration:** [interstellarninja/hermes_reasoning_tool_use](https://huggingface.co/datasets/interstellarninja/hermes_reasoning_tool_use)

---

## Dataset Statistics

- **Total Examples:** 12,010 (cleaned from 13,062 original)
- **Dropped Examples:** 1,052 (manual review + automated validation)
- **Validation Status:** 100% clean (0 tool-call JSON errors, 0 tag pollution errors)

---

## What Changed from Original DR-TULU

### Issues Identified in Original Dataset

The original DR-TULU dataset contained a single-turn format where each assistant response embedded the entire interaction trace (reasoning, tool calls, tool outputs, and final answer) in one monolithic turn. This structure presented several limitations:

#### 1. **Structural/Transition Issues**
- `reasoning → text` - Reasoning blocks followed by unstructured text
- `tool_call → tool_call` - Consecutive tool calls without intermediate tool outputs
- `tool_output → text` - Tool outputs followed by unstructured text
- `text → tool_call` - Unstructured text appearing before tool calls
- `text → reasoning` - Unstructured text appearing before reasoning blocks
- `text → answer` - Unstructured text appearing before answers
- `tool_output → answer` - Tool outputs transitioning directly to answers without reasoning
- `answer → text` - Answers followed by additional unstructured text
- `tool_call → reasoning` - Tool calls followed by reasoning without tool outputs in between
- `reasoning → reasoning` - Consecutive reasoning blocks without intervening actions

#### 2. **Nested/Embedded Tag Issues**
- `tool_call inside reasoning` - `<call_tool>` tags embedded within `<think>` blocks
- `tool_output inside reasoning` - `<tool_output>` tags embedded within `<think>` blocks
- `reasoning inside answer` - `<think>` tags embedded within `<answer>` blocks
- `tool_call inside answer` - `<call_tool>` tags embedded within `<answer>` blocks
- `tool_output inside answer` - `<tool_output>` tags embedded within `<answer>` blocks
- `reasoning inside tool_call` - `<think>` tags embedded within `<call_tool>` blocks
- `answer inside reasoning` - `<answer>` tags embedded within `<think>` blocks
- `reasoning inside tool_output` - `<think>` tags embedded within `<tool_output>` blocks
- `answer inside tool_output` - `<answer>` tags embedded within `<tool_output>` blocks
- `tool_call inside tool_output` - `<call_tool>` tags embedded within `<tool_output>` blocks
- `tool_output inside tool_call` - `<tool_output>` tags embedded within `<call_tool>` blocks

#### 3. **Format Inconsistencies**
- Tool calls used XML attribute syntax: `<call_tool name="google_search" num="5">query</call_tool>`
- No separation between reasoning steps and tool execution

---

## Improvements Made

### 1. **Multi-Turn Conversation Structure**

Transformed single-turn monolithic responses into proper multi-turn conversations:

**Original Format:**
```
- system: [DR-TULU system prompt]
- user: [question]
- assistant: [entire trace with <think>, <call_tool>, <tool_output>, <answer> all embedded]
```

**New Format:**
```
- system: [Updated system prompt inspired by interstellarninja/hermes_reasoning_tool_use]
- user: [question]
- reasoning: <think>...</think>
- tool_call: <tool_call>{JSON}</tool_call> [again inspired by interstellarninja/hermes_reasoning_tool_use]
- tool_output: <tool_response>...</tool_response> [tags inspired by interstellarninja/hermes_reasoning_tool_use]
- reasoning: <think>...</think>
- tool_call: <tool_call>{JSON}</tool_call>
- tool_output: <tool_response>...</tool_response>
...
- reasoning: <think>...</think>
- answer: <answer>...</answer>
```

### 2. **interstellarninja/hermes_reasoning_tool_use Tool Call Format**

**Before:**
```xml
<call_tool name="google_search" num="5" gl="us" hl="en">query text</call_tool>
```

**After:**
```xml
<tool_call>
{"name": "google_search", "parameters": {"query": "query text", "num": 5, "gl": "us", "hl": "en"}}
</tool_call>
```

This JSON-based format:
- Uses `parameters` instead of `arguments` for consistency with common tool-use datasets
- Properly types parameter values (integers, strings, etc.)
- Follows the format established by [interstellarninja/hermes_reasoning_tool_use](https://huggingface.co/datasets/interstellarninja/hermes_reasoning_tool_use)

### 3. **Updated System Prompt**

The system prompt was rewritten to:
- Define tools using JSON schema format with `parameters` key
- Specify multi-turn interaction patterns
- Clarify the turn-taking model between assistant and tool responses

### 4. **Tag Consistency**

- Renamed `<tool_output>` to `<tool_response>` for consistency
- Ensured each role contains only its designated tags:
  - `reasoning`: Only `<think>...</think>`
  - `tool_call`: Only `<tool_call>...</tool_call>`
  - `tool_output`: Only `<tool_response>...</tool_response>`
  - `answer`: Only `<answer>...</answer>`
- Eliminated all nested tag structures

### 5. **Validated Transitions**

All role transitions now follow valid patterns:
- `reasoning → tool_call` (42,327 occurrences)
- `tool_call → tool_output` (42,345 occurrences)
- `tool_output → reasoning` (42,345 occurrences)
- `reasoning → answer` (12,003 occurrences)
- 100% of conversations end with `answer` role

---

## Dataset Schema

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Unique identifier (preserved from original) |
| `source_id` | string | Source dataset identifier |
| `question` | string | Original question/prompt |
| `source` | string | Source dataset name (taskcraft, searcharena, openscholar, webwalkerqa-silver, popqa_tydiqa_en) |
| `type` | string | Question type (exact_answer, short_form, long_form) |
| `num_tool_calls` | int | Number of tool calls in the conversation |
| `tokenized_length` | int | Approximate token count |
| `conversations` | list[dict] | Multi-turn conversation with roles: system, user, reasoning, tool_call, tool_output, answer |

### Conversation Roles

Each conversation contains the following role types:

1. **system** (1 occurrence)
   - Updated system prompt with tool definitions
   - JSON-based tool call format specification
   - Multi-turn interaction guidelines

2. **user** (1 occurrence)
   - Original question with task instructions

3. **reasoning** (multiple occurrences)
   - Contains: `<think>reasoning text</think>`
   - Represents model's internal reasoning before actions or conclusions

4. **tool_call** (multiple occurrences)
   - Contains: `<tool_call>{"name": "...", "parameters": {...}}</tool_call>`
   - Valid JSON with proper parameter typing
   - Tools: google_search, browse_webpage, snippet_search

5. **tool_output** (multiple occurrences)
   - Contains: `<tool_response><snippet id="...">...</snippet></tool_response>`
   - Returns search results or webpage content

6. **answer** (1 occurrence, always last)
   - Contains: `<answer>final answer with <cite> tags</answer>`
   - Includes citations to retrieved snippets

---

## Validation Results

### JSON Validation
- **Total tool_call chunks:** 42,345
- **Valid JSON:** 42,345 (100%)
- **Errors:** 0

All tool calls contain properly formatted JSON with:
- `name` field present
- `parameters` field present
- Correct parameter types (string, int, etc.)

### Tag Pollution Check
- **Total chunks analyzed:** ~126,000+
- **Pollution errors:** 0
- **Clean rate:** 100%

No instances of:
- Tags nested within wrong role types
- Multiple tag types in single chunks
- Malformed tag structures

### Structural Validation
- **Valid transitions:** 100%
- **Invalid transition patterns:** 0
- **Conversations ending with answer:** 12,010 (100%)

---

## Data Cleaning Process

1. **Manual Review:** Extracted all 13,062 assistant responses to individual text files
2. **Manual Correction:** Reviewed and corrected problematic traces, dropped 1,051 examples
3. **Automated Validation:** Identified 1 additional example with tag pollution
4. **Final Dataset:** 12,010 clean, validated examples

The minimal number of dropped rows (8.05%) ensured retention of high-quality content while eliminating structural issues.

---

## Use Cases

This dataset is suitable for:

1. **Multi-Turn Tool Use Training**
   - Natural turn-taking between reasoning and tool execution
   - Proper JSON-based tool call formatting
   - Iterative search and refinement patterns

2. **Reasoning Trace Learning**
   - Explicit `<think>` blocks showing step-by-step reasoning
   - Reasoning before tool calls and before final answers
   - Chain-of-thought style deliberation

3. **Citation-Grounded Generation**
   - All claims in answers backed by `<cite id="...">` tags
   - References to specific retrieved snippets
   - Evidence-based response generation

4. **Research Assistant Training**
   - Web search, webpage browsing, and academic paper retrieval
   - Multi-source information synthesis
   - Factual question answering with source attribution


## Acknowledgments

This dataset builds directly on the work of the AllenAI RL Research team and their DR-TULU project. The original dataset represents substantial effort in creating high-quality reasoning and tool-use training data. The issues addressed here are structural rather than content-related, and the original content quality has been preserved. The tool-use format adopted here draws inspiration from the [Hermes Reasoning Tool Use dataset](https://huggingface.co/datasets/interstellarninja/hermes_reasoning_tool_use), whose established conventions for JSON-based tool calling were used.

## License

This dataset maintains the original ODC-BY license from the source dataset. It is intended for research and educational use in accordance with Ai2's Responsible Use Guidelines.

## Citation

```
@misc{vijay2025drtulu,
  title={{DR-TULU Cleaned}},
  author={Vijay, Supriti},
  year={2025},
  howpublished={\url{https://huggingface.co/datasets/SupritiVijay/deep-research-dr-tulu-sft-data-cleaned-rectified}}
}
```

## References

[1] AllenAI RL Research Team, "DR-TULU SFT Data," 2024. https://huggingface.co/datasets/rl-research/dr-tulu-sft-data