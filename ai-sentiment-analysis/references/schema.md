# Data contracts

## New coding input
JSONL: unique nonempty string record_id, original comment_text string and optional agreed post_text string. Map source columns through configuration, preserving text.

## Configured coding output
Required: record_id, relevance (relevant/off_target/uncertain), coding_status (coded/needs_review/not_applicable), target (string), sentiment (configured label or null), reason (nonempty string), evidence (list of exact comment substrings) and review_flag (boolean).

Example:
```json
{"record_id":"a","relevance":"relevant","coding_status":"coded","target":"产品外观","sentiment":"正面","reason":"明确赞美外观","evidence":["很好看"],"review_flag":false}
```

Off-target uses not_applicable and null sentiment. Uncertain relevance uses needs_review, null sentiment and review_flag=true. Relevant but unresolvable polarity also uses needs_review and null sentiment. A coded record needs a target, allowed label and quote. Neutral is a configured substantive label, not uncertainty. The legacy checker without --config preserves v1 archive compatibility, not the binary protocol.

## Reviewed input
Use the configured reviewed sentiment column directly. AI reasons, quotations and target extraction are not prerequisites for statistics on reviewed labels. Record mappings, source, effective N and agreed exclusions when running; do not change the original workbook.

## Extensions
Additional aspect/stance/emotion/topic/request fields require a separately specified study. The current validators do not implement those modules. Multiple aspects do not increase independent comment N.
