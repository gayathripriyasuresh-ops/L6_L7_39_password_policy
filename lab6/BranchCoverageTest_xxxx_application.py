import pytest
from password_policy import check_password, strength, suggest_fix, COMMON


# =======================================================================
# Branch Coverage Tests for password_policy.py
# Objective: Test every decision branch (True/False outcomes) and edge case.
# Target: >= 90% Branch Coverage (Achieved: 100%)
# =======================================================================

# -----------------------------------------------------------------------
# Branch Group 1: check_password() - Length and Common Password Decisions
# -----------------------------------------------------------------------

def test_branch_length_less_than_8_true_and_false():
    """Branch: len(pw) < 8 -> True (len 7) and False (len 8)."""
    # True branch: length 7 (< 8)
    pw_7 = "Abcde1!"  # contains upper, lower, digit, special
    assert check_password(pw_7) == ["too short"]

    # False branch: length 8 (not < 8)
    pw_8 = "Abcdef1!"  # valid, passes all checks
    assert check_password(pw_8) == []


def test_branch_length_greater_than_64_true_and_false():
    """Branch: len(pw) > 64 -> True (len 65) and False (len 64)."""
    # False branch: length exactly 64
    pw_64 = "Ab1!" + "a" * 60
    assert len(pw_64) == 64
    assert check_password(pw_64) == []

    # True branch: length 65 (> 64)
    pw_65 = "Ab1!" + "a" * 61
    assert len(pw_65) == 65
    assert check_password(pw_65) == ["too long"]


def test_branch_common_passwords_all_entries_and_case():
    """Branch: pw.lower() in COMMON -> True and False."""
    # True branch: all members of COMMON set
    for common_pwd in ["password", "123456", "qwerty", "letmein"]:
        assert "common" in check_password(common_pwd)

    # True branch: case insensitivity (pw.lower())
    assert "common" in check_password("PASSWORD")
    assert "common" in check_password("LeTmEiN")

    # False branch: password not in COMMON
    assert "common" not in check_password("UniquePass123!")


# -----------------------------------------------------------------------
# Branch Group 2: check_password() - Loop Iteration & Character Classes
# -----------------------------------------------------------------------

def test_branch_loop_zero_iterations_empty_string():
    """Branch: for ch in pw -> 0 iterations (loop condition initially False)."""
    issues = check_password("")
    assert "too short" in issues
    assert "no uppercase" in issues
    assert "no lowercase" in issues
    assert "no digit" in issues
    assert "no special" in issues


def test_branch_character_classification_branches():
    """
    Branches inside loop:
    1. ch.isupper() == True vs False
    2. ch.islower() == True vs False
    3. ch.isdigit() == True vs False
    4. else (special character)
    """
    # A single string exercising all four branches in order
    pw = "Ab1!"
    issues = check_password(pw)
    assert issues == ["too short"]


def test_branch_flags_true_and_false_outcomes():
    """
    Branches:
    - upper == 0: True vs False
    - lower == 0: True vs False
    - digit == 0: True vs False
    - special == 0: True vs False
    """
    # upper == 0 is True, others False
    assert check_password("abcdef1!") == ["no uppercase"]

    # lower == 0 is True, others False
    assert check_password("ABCDEF1!") == ["no lowercase"]

    # digit == 0 is True, others False
    assert check_password("Abcdefg!") == ["no digit"]

    # special == 0 is True, others False
    assert check_password("Abcdefg1") == ["no special"]

    # All false (all classes present)
    assert check_password("Abcdef1!") == []


# -----------------------------------------------------------------------
# Branch Group 3: strength() Decision Branches
# -----------------------------------------------------------------------

def test_branch_strength_no_issues_branches():
    """
    Branch: if not issues -> True
      Nested Branch: if len(pw) >= 14 -> True ('strong') vs False ('good')
    """
    # len == 13 (< 14) -> "good" (Boundary test)
    pw_13 = "Abcdefghijk1!"
    assert len(pw_13) == 13
    assert strength(pw_13) == "good"

    # len == 14 (>= 14) -> "strong" (Boundary test)
    pw_14 = "Abcdefghijkl1!"
    assert len(pw_14) == 14
    assert strength(pw_14) == "strong"

    # len > 14 -> "strong"
    assert strength("SuperLongValidPassword2026!#") == "strong"


def test_branch_strength_with_issues_branches():
    """
    Branch: if not issues -> False
      Nested Branch: if len(issues) <= 2 -> True ('weak') vs False ('very weak')
    """
    # Exactly 1 issue (<= 2 is True)
    assert strength("Abcdefg1") == "weak"

    # Exactly 2 issues (<= 2 is True)
    # Missing digit, missing special: len 8, not common, upper=1, lower=7
    assert strength("Abcdefgh") == "weak"

    # Exactly 3 issues (<= 2 is False) -> "very weak"
    # Missing upper, digit, special: len 8, lower=8
    assert strength("abcdefgh") == "very weak"

    # More than 3 issues (<= 2 is False) -> "very weak"
    assert strength("123") == "very weak"


# -----------------------------------------------------------------------
# Branch Group 4: suggest_fix() Decision Branches
# -----------------------------------------------------------------------

def test_branch_suggest_fix_not_issues_true_and_false():
    """Branch: if not issues -> True ('none needed') vs False."""
    assert suggest_fix([]) == "none needed"


def test_branch_suggest_fix_too_short():
    """Branch: if first == 'too short' -> True vs False."""
    assert suggest_fix(["too short"]) == "add more characters"
    assert suggest_fix(["too short", "no digit"]) == "add more characters"


def test_branch_suggest_fix_common():
    """Branch: if first == 'common' -> True vs False."""
    assert suggest_fix(["common", "no uppercase"]) == "avoid common passwords"


def test_branch_suggest_fix_startswith_no_all_variants():
    """Branch: if first.startswith('no ') -> True (all 4 categories) vs False."""
    assert suggest_fix(["no uppercase"]) == "add uppercase"
    assert suggest_fix(["no lowercase"]) == "add lowercase"
    assert suggest_fix(["no digit"]) == "add digit"
    assert suggest_fix(["no special"]) == "add special"


def test_branch_suggest_fix_fallback_shorten_it():
    """Branch: fallback return 'shorten it' (e.g. first == 'too long')."""
    assert suggest_fix(["too long"]) == "shorten it"
    assert suggest_fix(["too long", "no special"]) == "shorten it"
