"""Tests for devmate shell module."""

from devmate.shell import is_dangerous, get_os_context


def test_dangerous_detection():
    """Should detect dangerous commands."""
    assert is_dangerous("rm -rf /") is True
    assert is_dangerous("sudo rm -rf /home") is True
    assert is_dangerous("mkfs.ext4 /dev/sda1") is True
    assert is_dangerous("ls -la") is False
    assert is_dangerous("find . -name '*.py'") is False
    assert is_dangerous("echo hello") is False


def test_safe_commands():
    """Normal commands should not be flagged."""
    assert is_dangerous("grep -r 'pattern' .") is False
    assert is_dangerous("cat /etc/hostname") is False
    assert is_dangerous("df -h") is False


def test_os_context():
    """OS context should return required keys."""
    ctx = get_os_context()
    assert "os_info" in ctx
    assert "shell" in ctx
    assert "cwd" in ctx
