"""CLI exit-code propagation for `hermes kanban` subcommands.

Regression guard for the wrapper bug where `main()` discarded the kanban
dispatcher's return code, so a blocked/failed subcommand (e.g. an F3
commit-safety block on `kanban complete`) still exited 0 — invisible to
`&&`-chained worker briefs. `cmd_kanban` must surface a non-zero rc as the
process exit code, while leaving the success path (0/None) to exit 0.
"""
import argparse
import pytest


def test_cmd_kanban_propagates_nonzero_rc(monkeypatch):
    from hermes_cli import main as m
    monkeypatch.setattr("hermes_cli.kanban.kanban_command", lambda args: 1)
    with pytest.raises(SystemExit) as ei:
        m.cmd_kanban(argparse.Namespace())
    assert ei.value.code == 1


def test_cmd_kanban_propagates_rc_2(monkeypatch):
    from hermes_cli import main as m
    monkeypatch.setattr("hermes_cli.kanban.kanban_command", lambda args: 2)
    with pytest.raises(SystemExit) as ei:
        m.cmd_kanban(argparse.Namespace())
    assert ei.value.code == 2


def test_cmd_kanban_zero_rc_does_not_exit(monkeypatch):
    from hermes_cli import main as m
    monkeypatch.setattr("hermes_cli.kanban.kanban_command", lambda args: 0)
    rc = m.cmd_kanban(argparse.Namespace())  # must NOT raise SystemExit
    assert rc in (0, None)


def test_cmd_kanban_none_rc_does_not_exit(monkeypatch):
    from hermes_cli import main as m
    monkeypatch.setattr("hermes_cli.kanban.kanban_command", lambda args: None)
    rc = m.cmd_kanban(argparse.Namespace())  # must NOT raise SystemExit
    assert rc in (0, None)
