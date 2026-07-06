---
name: resume-document-creator
description: Create, refine, and tailor Markdown resume documents for this repository. Use when Codex needs to update `resume/master-resume.md`, derive shorter or role-specific resume variants, incorporate new accomplishments, rewrite summaries and bullets for a target job, or keep LinkedIn and cover-letter source material aligned with the canonical resume.
---

# Resume Document Creator

## Overview

Use this skill to maintain this repository as the source of truth for professional materials. Work from the master resume first, preserve factual accuracy, and produce concise role-targeted derivatives without inventing experience or metrics.

## Workflow

1. Read the repository context before editing:
   - `README.md`
   - `resume/master-resume.md`
   - Any existing target variant in `resume/`
   - Relevant source material in `accomplishments/`, `portfolio/`, `linkedin/`, or `cover-letters/`
2. Identify the deliverable:
   - Update the canonical master resume
   - Create or refresh a condensed resume
   - Tailor a role-specific resume for a target job
   - Reconcile supporting documents with resume content
3. Prefer the smallest set of edits that improves clarity, impact, and alignment.
4. Preserve Markdown readability with consistent heading levels, bullet formatting, and spacing.
5. After editing, sanity-check chronology, wording consistency, duplicated bullets, and whether the shorter variant still reflects the strongest evidence.

## Working Rules

- Treat `resume/master-resume.md` as the canonical source unless the user explicitly requests a one-off artifact.
- Pull supporting evidence from repository files before rewriting bullets from memory.
- Do not invent metrics, tools, dates, responsibilities, certifications, publications, or titles.
- Prefer measurable outcomes and scope when the source material supports them; otherwise improve specificity without fabricating numbers.
- Keep role-targeted resumes selective: emphasize the most relevant systems, leadership, architecture, and delivery evidence rather than copying every bullet from the master resume.
- Preserve the user’s voice: senior, technically credible, outcome-oriented, and concise.

## Resume Creation Patterns

### Update the master resume

- Merge new accomplishments into the most relevant role or project section.
- Strengthen weak bullets by clarifying system scale, ownership, architecture, reliability, automation, or business impact.
- Remove redundancy across highlights, experience, and projects when the same point appears multiple times.

### Create a concise resume

- Start from the master resume and compress aggressively.
- Keep the summary short and role-aligned.
- Limit experience bullets to the highest-signal achievements.
- Collapse early career roles when they are less relevant to the target.

### Tailor for a target role

- Map job requirements to matching evidence in the repository.
- Reorder or rewrite summary, highlights, and skills to foreground the strongest fit.
- Add relevant keywords naturally where truthful and supported.
- De-emphasize unrelated experience instead of deleting important chronology.

## Output Expectations

- Keep Markdown clean and easy to diff.
- Maintain consistent section names unless there is a strong reason to change them.
- Prefer one-page and two-page variants to be clearly derived from the master resume rather than independent rewrites.
- When creating a new variant, choose a descriptive filename in `resume/` such as `resume-platform-lead.md` or `resume-ai-infra.md`.

## Reference Files

- Read `references/repo-workflow.md` when you need repository-specific guidance on source files, tailoring flow, or quality checks.
