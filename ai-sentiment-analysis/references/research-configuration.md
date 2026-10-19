# Research configuration

The fixed workflow supports standardization, editable choices support configuration, and connecting tools supports integration. These are application/workflow improvements, not a new algorithm or evidence of superiority over a reference paper.

Configure: research_question, research_target, coding_unit, source path/sheet, columns, labels, value_map, out_of_scope_policy, missing_label_policy, mixed_policy, irony_policy, tasks and analysis_confirmed. Record actual skill_version and codebook_version. Only request fields necessary for the selected tasks.

Use code_and_analyze for new coding and analyze_reviewed for user-confirmed manually checked labels. Binary and three-class polarity are different profiles. Unmapped 0 does not become negative. An empty task list with analysis_confirmed=false prepares the study without running it.

The bundled course configuration is an unconfirmed binary example, not a statement about an uploaded file. Apply the current user request. For three-class data, configure positive/neutral/negative explicitly; never drop neutral records silently. A preparation-only request does not authorize analysis.

Topic examples: Mate60 may use polarity/target; games may add systems/requests; crisis responses may add attribution/stance; public events may add stages/themes; copyright debates may add stance/reasons. These are possible configurations, not all implemented extraction modules. Changing the topic name alone does not validate transfer.

For a genuinely new complex codebook, first draft category definitions, single/multi-select rules and edge cases; obtain researcher agreement before formal coding. Do not impose repeated confirmations on already agreed runs.

Basic version records are implemented: preserve old skill/configuration and identify substantive rule changes. Automatic version migration and complex multi-dimensional version management remain future work.
