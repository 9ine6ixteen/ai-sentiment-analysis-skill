---
name: ai-sentiment-analysis
description: Conduct traceable Chinese-comment sentiment research with configurable coding rules, human-reviewed-label analysis, quality checks, statistical tools, visualizations and reporting. Use for fixed-sample research and SPSS versus AI comparisons, not representative-population claims.
metadata:
  version: "1.1.1"
---

# AI Sentiment Analysis Skill

This skill standardizes a research workflow. It is not a new sentiment algorithm, trained classifier, or proof of greater accuracy than the reference paper. Standardization, configurability, extensibility and integration describe workflow/application design.

## Fixed workflow and variable configuration

Read data → establish research scope → identify evaluation targets → code sentiment → quality control → statistics → export.

Read [research configuration](references/research-configuration.md) when setting up or changing a study. Vary the research question, target, coding unit, source-column mapping, label definitions, special-case policies and statistical tasks while retaining the workflow. Reuse settled choices; ask only about unresolved decisions that change measurement or analysis.

Choose a mode:

- `code_and_analyze`: unlabeled comments. Agree on a codebook before formal coding; an unconfirmed scheme supports an explicitly exploratory pilot only.
- `analyze_reviewed`: the user has confirmed manually checked labels. Use those labels as the authorized input and skip AI relevance judgments, target extraction and recoding unless separately requested. Do not replace reviewed labels with old model labels.

For this course, start from [the reviewed-label configuration](assets/course-reviewed-config.json): comment-level, positive/negative focus, basic statistics. The template deliberately has unconfirmed source/tasks. When the user requests skill preparation and says analysis will be confirmed later, update files only. Do not read/run data, infer a task list, or calculate results.

## Coding mode

Use [the schema](references/schema.md). First determine `relevance` (relevant/off_target/uncertain), then evaluation target, then sentiment and `coding_status`. Non-target content, uncertainty and mixed attitudes are not automatically neutral or negative.

Preserve emojis, negation and repetition. Distinguish the author's own statements from quoted speakers. A forwarding marker does not by itself establish endorsement; look for the author's explicit additional attitude and otherwise flag attribution for review. Resolve irony only with sufficient textual/agreed context evidence. Do not import an attitude from the original post.

Binary coding uses only configured polarity labels for codable records. Relevant but mixed/ambiguous/unexpressed polarity follows the configured review/exclusion policy, not forced binary assignment. Competitor choice is a separate preference variable unless the shared codebook explicitly measures relative preference.

Save exact comment quotations and short evidence-grounded reasons. Keep likes, stage, other analysts' labels and source-model scores out of coding input where feasible. Hiding columns cannot erase prior conversation exposure. Never fabricate independent runs, model identifiers, API logs or measured efficiency gains.

## Reviewed-label mode

Preserve the original input and its codes. Map only the label column through explicit configuration; never whole-workbook replace words such as 正面 with numbers. `1=正面` and `-1=负面` do not imply `0=负面`.

Check record identity, required fields and mappings without changing meaning. Report neutral, mixed, missing or unmapped values before defining the binary analysis set. If their handling is unsettled, stop dependent analysis and ask that specific question. Do not silently delete, merge or recode them. User-confirmed manual review does not trigger another AI coding cycle or blanket approval requirement.

Report label provenance faithfully. Manual review authorizes the analysis source; it does not automatically establish infallible gold labels or independence from AI assistance.

## Quality control

Run `python3 scripts/check_config.py CONFIG.json` for configuration structure only. For new coding output run `python3 scripts/validate_results.py INPUT.jsonl RESULTS.jsonl --config CONFIG.json`. Archived v1 outputs retain the existing command without --config.

Checks establish completeness, valid fields and quote presence, not semantic correctness. Keep original versions and log substantive changes. Avoid repeating checks on already-verified unchanged data unless affected by a new change.

## Statistics and output

Execute only confirmed tasks with actual established libraries. Typical basic tasks: frequency tables, polarity pie charts, likes-by-sentiment box plots, sentiment-by-stage bars, t-tests, ANOVA and chi-square. Choose by research question and available variables; two polarity categories do not provide three groups for three-group ANOVA. State group choices and do not invent extra groups.

Record field mapping, effective N, exclusions, assumptions, effect sizes, uncertainty and multiplicity treatment. Distinguish requested classic tests from justified Welch/sensitivity results. Note skew, zero counts, sparse cells and same-post dependence. Do not pick a method or change labels for significance.

For SPSS comparisons align records, variables and algorithm settings. Same-label cross-checks after independent result freezing distinguish coding from calculator differences. Original paper model predictions are method references, not human truth; do not manufacture neutral thresholds for binary scores.

Export coding/reviewed data, configuration, figures, numeric results, code and actual run information together. General orchestration is performed by the agent with tools; bundled validators are not a universal one-click statistics engine. Report unavailable libraries, fields or groups as a concrete partial-completion limit.

## Current capability versus future extensions

Implemented: standardized workflow instructions, editable JSON configuration, reviewed-label routing, structure/quote validators, basic source/version records, and tool-orchestrated statistics/reporting. The course demonstration emphasizes standardized sentiment treatment and basic statistics.

Future directions: automatic complex codebook construction, validated emotion/stance/topic/request modules, multi-label hierarchies and automatic version migration. Present them as extensibility, not demonstrated features. Do not expand the current positive/negative assignment into these modules without a user request.
