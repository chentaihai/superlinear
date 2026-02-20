
<!--
Markdown template for storing a collection of prompts.
Fill one entry per prompt under "Prompts" using the provided template.
-->

# Prompt Library

> A simple, consistent place to store current prompts.

---

## Metadata

- Owner: 
- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD
- Version: 1.0

---

## Usage

1. Duplicate the Prompt Template for each prompt you store.
2. Keep the Title, Purpose and Example sections updated.
3. Use Tags for easy searching.

---

## Index

| ID | Title | Tags | Last updated |
|---:|-------|------|--------------|
| 1 | Example Prompt | example, test | YYYY-MM-DD |

---

## Prompt Template

### ID: <numeric-id>

- Title: <short descriptive title>
- Tags: <comma-separated tags>
- Purpose: <one-line goal / why this prompt exists>
- Context / Notes: <any background or constraints>
- Model: <model name or desired capability>
- Temperature / Settings: <temperature, max_tokens, etc.>
- Author: <your name>
- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD

#### Prompt (raw)

```
<Place the exact prompt text here>
```

#### Example Input / Variables

- var1: <description>
- var2: <description>

#### Example Output (expected)

```
<Example response or format you expect>
```

#### Notes / Iterations

- v1: <what changed>
- v2: <what changed>

---

## Example Entry

### ID: 1

- Title: Summarize Meeting Notes
- Tags: summarization, meeting
- Purpose: Quickly convert raw meeting notes into a concise summary with action items.
- Context / Notes: Focus on decisions and action items, keep to 6 bullets.
- Model: GPT-4-style
- Temperature / Settings: temperature=0.2, max_tokens=300
- Author: 
- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD

#### Prompt (raw)

```
You are an assistant that converts meeting notes into a concise summary. Extract decisions, action items (with owners and due dates when present), and a 1-2 sentence overall summary. Keep response to 6 bullets max.

Meeting notes:
{{NOTES}}
```

#### Example Input / Variables

- NOTES: raw pasted transcript or bulleted notes

#### Example Output (expected)

```
- Summary: <1-2 sentences>
- Decisions:
	- Decision 1
- Action Items:
	- Person — task — due date
```

---

End of template

