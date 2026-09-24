# Veeam package — solution gating

| Product | Include when | Do not infer from |
|---|---|---|
| Veeam Backup & Replication | virtual machines need backup, a secondary copy or replication | a backup platform (e.g. Avamar) that the client wants to keep as primary, unless the Veeam copy is in scope |
| Veeam Backup for Microsoft 365 | Exchange Online, OneDrive, SharePoint or Teams data must be backed up | Microsoft 365 use without a backup requirement |

When Veeam already runs at the client, the licenses may be `already_contracted`; the proposal may still cover services on top of it.
