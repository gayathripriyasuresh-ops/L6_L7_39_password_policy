import pytest
from password_policy import check_password, strength, suggest_fix, COMMON


# ==========================================
# Code Coverage Tests for password_policy.py
# Target: >= 90% Line / Code Coverage
# ==========================================

# 1. Tests for check_password
def test_valid_password_no_issues():
    """Test valid passwords of standard length having all required character classes."""
    assert check_password("Abcdef1!") == []
    assert check_password("SecurePass99#") == []


def test_password_too_short():
    """Test passwords with length less than 8 characters."""
    issues = check_password("Ab1!")
    assert "too short" in issues


def test_password_too_long():
    """Test passwords with length greater than 64 characters."""
    long_pw = "Ab1!" + "x" * 65
    issues = check_password(long_pw)
    assert "too long" in issues


def test_common_passwords():
    """Test passwords matching the common password blacklist."""
    assert "common" in check_password("password")
    assert "common" in check_password("123456")
    assert "common" in check_password("qwerty")
    assert "common" in check_password("letmein")
    # Case insensitivity test
    assert "common" in check_password("PASSWORD")


def test_missing_character_types():
    """Test passwords lacking specific character categories."""
    # Missing uppercase
    assert "no uppercase" in check_password("abcdef1!")
    # Missing lowercase
    assert "no lowercase" in check_password("ABCDEF1!")
    # Missing digit
    assert "no digit" in check_password("Abcdefg!")
    # Missing special character
    assert "no special" in check_password("Abcdefg1")


def test_empty_password():
    """Test empty password edge case."""
    issues = check_password("")
    assert "too short" in issues
    assert "no uppercase" in issues
    assert "no lowercase" in issues
    assert "no digit" in issues
    assert "no special" in issues


# 2. Tests for strength
def test_strength_strong():
    """Test strong password evaluation (length >= 14 and no issues)."""
    assert strength("Abcdefghijkl1!") == "strong"
    assert strength("SuperSecurePass123!@#") == "strong"


def test_strength_good():
    """Test good password evaluation (length 8-13 and no issues)."""
    assert strength("Abcdef1!") == "good"
    assert strength("Abcdefghijk1!") == "good"


def test_strength_weak():
    """Test weak password evaluation (1 or 2 issues)."""
    # 1 issue: no special
    assert strength("Abcdefg1") == "weak"
    # 2 issues: no digit, no special
    assert strength("Abcdefgh") == "weak"


def test_strength_very_weak():
    """Test very weak password evaluation (more than 2 issues)."""
    # 3 issues: no upper, no digit, no special
    assert strength("abcdefgh") == "very weak"
    # 4 issues: too short, no upper, no lower, no special
    assert strength("12345") == "very weak"


# 3. Tests for suggest_fix
def test_suggest_fix_none_needed():
    """Test suggest_fix when there are no issues."""
    assert suggest_fix([]) == "none needed"


def test_suggest_fix_too_short():
    """Test suggest_fix when first issue is 'too short'."""
    assert suggest_fix(["too short", "no uppercase"]) == "add more characters"


def test_suggest_fix_common():
    """Test suggest_fix when first issue is 'common'."""
    assert suggest_fix(["common", "no uppercase"]) == "avoid common passwords"


def test_suggest_fix_no_prefix():
    """Test suggest_fix when first issue starts with 'no '."""
    assert suggest_fix(["no uppercase"]) == "add uppercase"
    assert suggest_fix(["no lowercase"]) == "add lowercase"
    assert suggest_fix(["no digit"]) == "add digit"
    assert suggest_fix(["no special"]) == "add special"


def test_suggest_fix_too_long():
    """Test suggest_fix fallback (e.g., 'too long')."""
    assert suggest_fix(["too long"]) == "shorten it"
