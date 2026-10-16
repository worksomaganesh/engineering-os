"""Fail-closed YAML policy loader with duplicate-key rejection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from agent_boundary.policy.schema import PolicyDocument


class PolicyValidationError(Exception):
    """Raised for malformed or invalid policy files."""


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate or non-string mapping keys."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
        self.flatten_mapping(node)
        mapping: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise PolicyValidationError(
                    f"Policy YAML mapping keys must be strings (line {key_node.start_mark.line + 1})"
                )
            if key in mapping:
                raise PolicyValidationError(
                    f"Duplicate YAML key '{key}' detected at line {key_node.start_mark.line + 1}"
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def load_policy_from_text(raw_yaml: str) -> PolicyDocument:
    """Parse and strictly validate a policy YAML string."""
    try:
        data = yaml.load(raw_yaml, Loader=UniqueKeySafeLoader)
    except PolicyValidationError:
        raise
    except yaml.YAMLError as exc:
        raise PolicyValidationError(f"Invalid YAML syntax: {exc}") from exc
    if not isinstance(data, dict):
        raise PolicyValidationError("Policy root must be a YAML mapping/object")
    try:
        document = PolicyDocument.model_validate(data)
    except ValidationError as exc:
        raise PolicyValidationError(f"Policy schema validation failed:\n{exc}") from exc
    _verify_unique_rule_ids(document)
    return document


def load_policy(path: Path) -> PolicyDocument:
    """Read and validate a policy file from disk."""
    if not path.exists() or not path.is_file():
        raise PolicyValidationError(f"Policy file not found: {path}")
    try:
        raw_yaml = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PolicyValidationError(f"Failed to read policy file {path}: {exc}") from exc
    return load_policy_from_text(raw_yaml)


def _verify_unique_rule_ids(document: PolicyDocument) -> None:
    """Require rule IDs to be unique across all policy categories and decisions."""
    all_rules = [
        *document.filesystem.deny,
        *document.filesystem.require_approval,
        *document.filesystem.allow,
        *document.commands.deny,
        *document.commands.require_approval,
        *document.commands.allow,
        *document.network.deny,
        *document.network.require_approval,
        *document.network.allow,
    ]
    seen: set[str] = set()
    for rule in all_rules:
        if rule.id in seen:
            raise PolicyValidationError(f"Duplicate rule id '{rule.id}' in policy document")
        seen.add(rule.id)
