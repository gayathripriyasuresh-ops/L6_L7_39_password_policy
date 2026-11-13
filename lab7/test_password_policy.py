from hypothesis import given, strategies as st
from password_policy import first_character_type, split_credentials, digit_ratio

unexpected_inputs = st.one_of(
    st.none(),
    st.text(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.binary(),
    st.lists(st.integers()),
    st.lists(st.text()),
    st.dictionaries(st.text(), st.text()),
)

valid_first_char_categories = {"digit", "letter", "whitespace", "symbol", None}


@given(st.text() | st.none())
def test_first_character_type_no_crash(s):
    try:
        result = first_character_type(s)
    except Exception as e:
        assert False, f"first_character_type crashed with: {e}"
    assert result in valid_first_char_categories


@given(unexpected_inputs)
def test_first_character_type_unexpected_types(val):
    try:
        result = first_character_type(val)
    except Exception as e:
        assert False, f"first_character_type crashed on {type(val).__name__}: {e}"
    assert result in valid_first_char_categories


@given(st.text())
def test_first_character_type_valid_category(s):
    try:
        result = first_character_type(s)
    except Exception as e:
        assert False, f"first_character_type crashed with: {e}"
    if s == "":
        assert result is None
    else:
        assert result in {"digit", "letter", "whitespace", "symbol"}


@given(st.text() | st.none())
def test_split_credentials_no_crash(s):
    try:
        result = split_credentials(s)
    except Exception as e:
        assert False, f"split_credentials crashed with: {e}"
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(part, str) and len(part) > 0 for part in result)
    )


@given(unexpected_inputs)
def test_split_credentials_unexpected_types(val):
    try:
        result = split_credentials(val)
    except Exception as e:
        assert False, f"split_credentials crashed on {type(val).__name__}: {e}"
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


@given(
    st.text(alphabet=st.characters(blacklist_characters=":")),
    st.text(),
    st.text(),
)
def test_split_credentials_multiple_colons(user, part1, part2):
    combined = f"{user}:{part1}:{part2}"
    try:
        result = split_credentials(combined)
    except Exception as e:
        assert False, f"split_credentials crashed on multiple colons: {e}"
    if user.strip() and f"{part1}:{part2}".strip():
        assert result == (user.strip(), f"{part1}:{part2}".strip())
    else:
        assert result is None


@given(st.text(alphabet=st.characters(blacklist_characters=":")))
def test_split_credentials_no_colon(s):
    try:
        result = split_credentials(s)
    except Exception as e:
        assert False, f"split_credentials crashed without colon: {e}"
    assert result is None


@given(st.text() | st.none())
def test_digit_ratio_no_crash(s):
    try:
        result = digit_ratio(s)
    except Exception as e:
        assert False, f"digit_ratio crashed with: {e}"
    assert isinstance(result, float) and 0.0 <= result <= 1.0


@given(unexpected_inputs)
def test_digit_ratio_unexpected_types(val):
    try:
        result = digit_ratio(val)
    except Exception as e:
        assert False, f"digit_ratio crashed on {type(val).__name__}: {e}"
    assert isinstance(result, float) and 0.0 <= result <= 1.0


@given(st.text())
def test_digit_ratio_bounds(s):
    try:
        result = digit_ratio(s)
    except Exception as e:
        assert False, f"digit_ratio crashed with: {e}"
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0
    if s == "":
        assert result == 0.0
