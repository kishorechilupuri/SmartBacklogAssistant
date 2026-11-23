Meeting Notes — Sprint Planning
Date: Oct 15, 2026 | Attendees: Alice (PM), Bob (Dev), Carol (QA), Dave (DevOps)

Issues Discussed:
- CRITICAL: Login page is completely broken on Firefox v120+. Users cannot log in.
  Bob will investigate — likely CSS isolation bug introduced last sprint.

- Performance: The admin dashboard takes 8+ seconds to load with > 10k users.
  Users have complained in Slack. Dave thinks adding a DB index will help.

- Feature Request: Marketing wants an email newsletter subscription toggle in user settings.
  Alice estimates moderate effort. Low priority but a common user ask.

- Feature Request: Admins need bulk CSV export of all user accounts for compliance audit.
  Legal flagged this as required before the Q4 deadline.

- Tech Debt: The old Python 2 script that runs nightly ETL jobs needs to be upgraded.
  It hasn't failed yet but it's a ticking bomb. Carol found a security CVE last week.
