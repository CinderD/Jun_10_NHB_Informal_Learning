# Derived Label Tables

These files provide de-identified analytic labels for the manuscript's main public-chat task settings. They are intended to complement the aggregate figure source data and statistical-output files.

## Scope

- Included main corpora: WildChat, LMSYS Chat and ShareChat strict-English.
- Included tasks: coding-oriented and writing-oriented conversations.
- Excluded data: raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories and API credentials.
- Identifier handling: `conversation_id_hash` and turn-level hashes use SHA-256 over `nhb_informal_learning_label_release_v1:<raw id or raw id + role + turn index>`.
- Raw public corpora must still be obtained from the original providers under their own licences and terms.

## Files

Each dataset folder contains:

- `conversation_labels.csv`: one row per analytic conversation, with conversation-level user engagement, assistant scaffolding and contextual labels.
- `user_to_assistant_pair_labels.csv`: one row per user turn that can be paired with the next assistant turn, with the user-side label and next assistant support labels.
- `assistant_to_user_pair_labels.csv`: one row per assistant turn that can be paired with a surrounding user state and next user outcome, with support labels and adjacent user engagement labels.

## Row Counts

| Dataset | Task | Scope | Conversations | User-to-assistant pairs | Assistant-to-user pairs |
|---|---|---|---:|---:|---:|
| WildChat | coding | main_six_setting | 31878 | 124073 | 92322 |
| WildChat | writing | main_six_setting | 39534 | 163705 | 124388 |
| LMSYS Chat | coding | main_six_setting | 32114 | 105130 | 74147 |
| LMSYS Chat | writing | main_six_setting | 21023 | 76271 | 56182 |
| ShareChat | coding | main_six_setting | 2481 | 11511 | 9062 |
| ShareChat | writing | main_six_setting | 1539 | 7358 | 5849 |

## Notes

The adjacent-pair files are not a complete raw turn dump. They preserve the analytic turn-pair units used in the temporal and adjacent-turn models. Conversation-level counts in `conversation_labels.csv` retain the full user-turn and assistant-turn totals used for Table 1 and conversation-level analyses.
