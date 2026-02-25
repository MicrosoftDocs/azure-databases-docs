# Copilot Instructions for Microsoft Learn

These instructions define a unified style and process standard for authoring and maintaining learn.microsoft.com documentation with GitHub Copilot or other AI assistance.

## Learn-wide Instructions

Below are instructions that apply to all Microsoft Learn documentation authored with AI assistance. Learn product team will update this periodically as needed. Each repository SHOULD NOT update this to avoid being overwritten, but update the repository-specific instructions below as needed.

### AI Usage & Disclosure
All Markdown content created or substantially modified with AI assistance must include an `ai-usage` front matter entry:
- `ai-usage: ai-generated` – AI produced the initial draft with minimal human authorship
- `ai-usage: ai-assisted` – Human-directed, reviewed, and edited with AI support
- Omit only for purely human-authored legacy content

If missing, **add it**. However, do not add or update the ai-usage tag if the changes proposed are confined solely to:
- Links (link text and/or URLs)
- Single words or short phrases, such as entries in table cells
- Less than 5% of the article's word count

### Writing Style

Follow [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/) with these specifics:

#### Voice and Tone

- Active voice, second person addressing reader directly
- Conversational tone with contractions
- Present tense for instructions/descriptions
- Imperative mood for instructions ("Call the method" not "You should call the method")
- Use "might" instead of "may" for possibility
- Avoid "we"/"our" referring to documentation authors

#### Structure and Format

- Sentence case headings (no gerunds in titles)
- Be concise, break up long sentences
- Oxford comma in lists
- Number all ordered list items as "1." (not sequential numbering like "1.", "2.", "3.", etc.)
- Complete sentences with proper punctuation in all list items
- Avoid "etc." or "and so on" - provide complete lists or use "for example"
- No consecutive headings without content between them

#### Formatting Conventions

- **Bold** for UI elements
- `Code style` for file names, folders, custom types, non-localizable text
- Raw URLs in angle brackets
- Use relative links for files in this repo
- Remove `https://learn.microsoft.com/en-us` from learn.microsoft.com links

## Repository-Specific Instructions

Below are instructions specific to this repository. These may be updated by repository maintainers as needed.

<!--- Add additional repository level instructions below. Do NOT update this line or above. --->

### Content structure

### Content completeness

- Procedures must include all steps - check for missing prerequisites or follow-up actions
- Code samples must be complete and runnable - no placeholder comments like `// add code here`

### Alert usage

- Limit alerts to one or two per article
- Never place multiple notes consecutively
- Use the correct alert type:
  - `[!NOTE]` - Information the user should notice even if skimming
  - `[!TIP]` - Optional information to help a user be more successful
  - `[!IMPORTANT]` - Essential information required for user success
  - `[!WARNING]` - Dangerous certain consequences of an action

### Markdown Formatting

#### Headings

- Each file must have exactly one H1 heading
- Do not skip heading levels (H2 to H4 without H3)

#### Code blocks

- Always specify the language identifier for syntax highlighting
- Use `azurecli` for Azure CLI commands
- Use `bash` for generic command line instructions

#### Tables

- Use exactly `| --- |` for column separators, not `|--------|`
- For alignment: `| :-- |` (left), `| :--: |` (center), `| --: |` (right)
- Empty first column headers are allowed when first column values are bolded

### Writing Style

#### Word choice

| Use | Instead of |
| --- | --- |
| use | utilize |
| remove | eliminate |
| because | since (when meaning "because") |
| to | in order to |

#### Input-agnostic verbs

Use verbs that work for all input methods (mouse, keyboard, touch):

| Use | Instead of |
| --- | --- |
| Select | Click |
| Choose | Tap |
| Enter | Type |

#### Bias-free language

- Use people-first language: "users who are blind" not "blind users"
- Use gender-neutral terms: "sales representative" not "salesman"
- Show diverse perspectives in examples

### Review Style

When providing feedback:

- Be specific and actionable - explain what to change and why
- Acknowledge good patterns when you see them
- Ask clarifying questions when intent is unclear
- Prioritize terminology issues and technical accuracy
- Focus on improvements that help readers succeed
