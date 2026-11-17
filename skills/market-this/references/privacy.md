# Privacy

The user's business data is theirs. Handle it with the minimum needed.

## Rules

1. **Ask only what the method needs.** Counts, durations, amounts and process steps. No names of customers or employees are needed; use roles.
2. **Anonymize exports first.** CRM, invoicing, mailbox or HR exports contain personal data (names, emails, phone numbers, addresses). Before analyzing, offer to strip those columns. If you can run code and the user agrees, use `scripts/anonymize.py` (it keeps dates and amounts, removes personal columns and masks emails and phone numbers). Otherwise ask the user to remove those columns or share only counts.
3. **Never send personal data outside the conversation.** External tools (Monid or others) are only for public business information, such as a company website or public reviews.
4. **The dossier stays with the user.** Share it with a professional, Market This, or anyone else only with explicit consent, and let the user do the sharing.
5. **Employees are people.** Do not profile individual employees. Talk about roles, workload and steps, not about who is slow.
6. **Health data** is a special category under the GDPR. For care providers: no patient or client data at all, only counts, and no health claims without checking the advertising rules.
7. **Sensitive topics** such as health, conflicts or dismissals: note only what is needed for routing, and refer to the right professional.

## Phrase to use

"For this I only need the counts per week, not the customer names. Could you remove names, emails and phone numbers from the export first, or shall I do that for you?"
