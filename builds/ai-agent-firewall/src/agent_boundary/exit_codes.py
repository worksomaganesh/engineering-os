"""Documented CLI exit codes for agent-boundary Phase 1."""

from enum import IntEnum


class ExitCode(IntEnum):
    """Stable exit codes based on the project workflow blueprint."""

    OK = 0
    ACTION_FAILED = 1
    CONFIG_OR_POLICY_ERROR = 2
    SANDBOX_FAILURE = 3
    INTERRUPTED = 4
    AUDIT_INTEGRITY_ERROR = 5
    REVIEW_REQUIRED = 6
