"""LIFU sonication interface.

Wraps ``openlifu-python`` (AGPL-3.0 — see NOTICE) to issue sonications when the trigger
gate permits. In --dry-run mode this layer logs the decision but issues no sonication.

Scaffolding: the concrete interface is migrated in with the developer's code. Acoustic
output parameters are run configuration, not constants baked into this repository
(see docs/protocol.md).
"""
