"""Strict, versioned policy schemas with fail-closed validation."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Decision(StrEnum):
    """Deterministic policy decision."""

    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    ALLOW = "allow"


class ActionCategory(StrEnum):
    """Supported action categories."""

    FILESYSTEM = "filesystem"
    COMMAND = "command"
    NETWORK = "network"


class FileOperation(StrEnum):
    """Supported filesystem operations."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"


class FilesystemRule(BaseModel):
    """One filesystem rule."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_-]+$")
    operations: list[FileOperation] = Field(min_length=1)
    paths: list[str] = Field(min_length=1)
    reason: str = Field(min_length=1)

    @field_validator("paths")
    @classmethod
    def validate_paths(cls, values: list[str]) -> list[str]:
        if any(not value.strip() for value in values):
            raise ValueError("Filesystem path globs cannot be empty or whitespace")
        return values


class CommandRule(BaseModel):
    """One command policy rule."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_-]+$")
    executables: list[str] = Field(min_length=1)
    arg_patterns: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)

    @field_validator("executables")
    @classmethod
    def validate_executables(cls, values: list[str]) -> list[str]:
        if any(not value.strip() for value in values):
            raise ValueError("Command executable patterns cannot be empty")
        return values


class NetworkRule(BaseModel):
    """One outbound network policy rule."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_-]+$")
    hosts: list[str] = Field(min_length=1)
    ports: list[int] = Field(min_length=1)
    reason: str = Field(min_length=1)

    @field_validator("ports")
    @classmethod
    def validate_port_range(cls, values: list[int]) -> list[int]:
        if any(port < 1 or port > 65535 for port in values):
            raise ValueError("Network ports must be in range 1..65535")
        return values

    @field_validator("hosts")
    @classmethod
    def validate_hosts(cls, values: list[str]) -> list[str]:
        if any(not value.strip() for value in values):
            raise ValueError("Network host patterns cannot be empty")
        return values


class FilesystemPolicySection(BaseModel):
    """Filesystem rules grouped by decision tier."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    deny: list[FilesystemRule] = Field(default_factory=list)
    require_approval: list[FilesystemRule] = Field(default_factory=list)
    allow: list[FilesystemRule] = Field(default_factory=list)


class CommandPolicySection(BaseModel):
    """Command rules grouped by decision tier."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    deny: list[CommandRule] = Field(default_factory=list)
    require_approval: list[CommandRule] = Field(default_factory=list)
    allow: list[CommandRule] = Field(default_factory=list)


class NetworkPolicySection(BaseModel):
    """Network rules grouped by decision tier."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    deny: list[NetworkRule] = Field(default_factory=list)
    require_approval: list[NetworkRule] = Field(default_factory=list)
    allow: list[NetworkRule] = Field(default_factory=list)


class PolicyDocument(BaseModel):
    """Top-level versioned policy specification."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["1.0"]
    policy_id: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_-]+$")
    description: str = Field(min_length=1)
    workspace_root: str = Field(default="/workspace", min_length=1)
    default_decision: Literal[Decision.DENY] = Decision.DENY
    filesystem: FilesystemPolicySection = Field(default_factory=FilesystemPolicySection)
    commands: CommandPolicySection = Field(default_factory=CommandPolicySection)
    network: NetworkPolicySection = Field(default_factory=NetworkPolicySection)

    @field_validator("workspace_root")
    @classmethod
    def validate_absolute_workspace_root(cls, value: str) -> str:
        if not value.startswith("/") or value == "/":
            raise ValueError("workspace_root must be an absolute path other than filesystem root '/'")
        return value
