import pytest
import re
from datetime import datetime, timezone
from unittest.mock import patch

from intellistack.backend.src.shared.utils import (
    generate_uuid, generate_secret_token, utc_now, hash_string,
    slugify, truncate_string, calculate_percentage, deep_merge,
    mask_email, generate_certificate_number
)


class TestGenerateUUID:
    """Test the generate_uuid function."""

    def test_generate_uuid_returns_string(self):
        """Test that generate_uuid returns a string."""
        result = generate_uuid()
        assert isinstance(result, str)

    def test_generate_uuid_is_valid_format(self):
        """Test that generated UUID is in valid UUID v4 format."""
        result = generate_uuid()

        # UUID format: 8-4-4-4-12 hex characters separated by hyphens
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, result) is not None

    def test_generate_uuid_unique(self):
        """Test that generated UUIDs are unique."""
        uuids = [generate_uuid() for _ in range(10)]
        assert len(set(uuids)) == 10  # All should be unique


class TestGenerateSecretToken:
    """Test the generate_secret_token function."""

    def test_generate_secret_token_default_length(self):
        """Test that secret token has default length."""
        result = generate_secret_token()
        assert len(result) >= 32  # URL-safe tokens may be longer due to padding

    def test_generate_secret_token_custom_length(self):
        """Test that secret token has custom length."""
        result = generate_secret_token(16)
        assert len(result) >= 16

    def test_generate_secret_token_url_safe(self):
        """Test that secret token is URL-safe."""
        result = generate_secret_token()
        # URL-safe tokens should not contain +, /, or =
        assert '+' not in result
        assert '/' not in result
        # May contain = as padding, which is safe


class TestUtcNow:
    """Test the utc_now function."""

    def test_utc_now_returns_datetime(self):
        """Test that utc_now returns a datetime object."""
        result = utc_now()
        assert isinstance(result, datetime)

    def test_utc_now_has_utc_timezone(self):
        """Test that returned datetime has UTC timezone."""
        result = utc_now()
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc

    def test_utc_now_is_current_time(self):
        """Test that returned time is close to current time."""
        before = datetime.now(timezone.utc)
        result = utc_now()
        after = datetime.now(timezone.utc)

        assert before <= result <= after


class TestHashString:
    """Test the hash_string function."""

    def test_hash_string_basic(self):
        """Test basic string hashing."""
        result = hash_string("hello")
        assert isinstance(result, str)
        assert len(result) == 64  # SHA-256 produces 64 hex characters
        assert re.match(r'^[a-f0-9]+$', result) is not None

    def test_hash_string_with_salt(self):
        """Test string hashing with salt."""
        result1 = hash_string("hello", "salt1")
        result2 = hash_string("hello", "salt2")
        result3 = hash_string("hello")  # No salt

        assert result1 != result2 != result3  # Different hashes with different salts

    def test_hash_string_consistency(self):
        """Test that same input produces same hash."""
        result1 = hash_string("hello", "salt")
        result2 = hash_string("hello", "salt")

        assert result1 == result2

    def test_hash_string_empty_string(self):
        """Test hashing empty string."""
        result = hash_string("")
        assert isinstance(result, str)
        assert len(result) == 64


class TestSlugify:
    """Test the slugify function."""

    def test_slugify_basic(self):
        """Test basic slugification."""
        result = slugify("Hello World")
        assert result == "hello-world"

    def test_slugify_with_special_chars(self):
        """Test slugification with special characters."""
        result = slugify("Hello, World! @#$%^&*()")
        assert result == "hello-world"

    def test_slugify_with_multiple_spaces(self):
        """Test slugification with multiple spaces."""
        result = slugify("Hello    World")
        assert result == "hello-world"

    def test_slugify_with_leading_trailing_spaces(self):
        """Test slugification with leading/trailing spaces."""
        result = slugify("  Hello World  ")
        assert result == "hello-world"

    def test_slugify_with_hyphens(self):
        """Test slugification with hyphens."""
        result = slugify("Hello-World-Test")
        assert result == "hello-world-test"

    def test_slugify_empty_string(self):
        """Test slugification of empty string."""
        result = slugify("")
        assert result == ""


class TestTruncateString:
    """Test the truncate_string function."""

    def test_truncate_string_shorter_than_limit(self):
        """Test truncation when string is shorter than limit."""
        result = truncate_string("Short", 10)
        assert result == "Short"

    def test_truncate_string_exactly_limit(self):
        """Test truncation when string is exactly at limit."""
        result = truncate_string("Exact", 5)
        assert result == "Exact"

    def test_truncate_string_longer_than_limit(self):
        """Test truncation when string is longer than limit."""
        result = truncate_string("This is a longer string", 10)
        assert result == "This is..."

    def test_truncate_string_custom_suffix(self):
        """Test truncation with custom suffix."""
        # "This is a longer string" with max length 12 and suffix " [more]" (7 chars)
        # Should take first 12-7=5 chars: "This " + " [more]" = "This  [more]"
        result = truncate_string("This is a longer string", 12, " [more]")
        assert result == "This  [more]"

    def test_truncate_string_suffix_longer_than_limit(self):
        """Test truncation when suffix is longer than limit."""
        result = truncate_string("Very long string", 3, "...")
        # Should return just the suffix or a minimal part
        assert len(result) <= 3


class TestCalculatePercentage:
    """Test the calculate_percentage function."""

    def test_calculate_percentage_normal(self):
        """Test normal percentage calculation."""
        result = calculate_percentage(5, 10)
        assert result == 50.0

    def test_calculate_percentage_rounding(self):
        """Test percentage calculation with rounding."""
        result = calculate_percentage(1, 3)
        assert result == 33.33

    def test_calculate_percentage_zero_total(self):
        """Test percentage calculation with zero total."""
        result = calculate_percentage(5, 0)
        assert result == 0.0

    def test_calculate_percentage_zero_completed(self):
        """Test percentage calculation with zero completed."""
        result = calculate_percentage(0, 10)
        assert result == 0.0

    def test_calculate_percentage_equal(self):
        """Test percentage calculation when completed equals total."""
        result = calculate_percentage(10, 10)
        assert result == 100.0


class TestDeepMerge:
    """Test the deep_merge function."""

    def test_deep_merge_basic(self):
        """Test basic dictionary merging."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = deep_merge(base, override)

        expected = {"a": 1, "b": 3, "c": 4}
        assert result == expected

    def test_deep_merge_nested_dictionaries(self):
        """Test merging of nested dictionaries."""
        base = {"a": {"x": 1, "y": 2}, "b": 3}
        override = {"a": {"y": 20, "z": 30}, "c": 4}
        result = deep_merge(base, override)

        expected = {"a": {"x": 1, "y": 20, "z": 30}, "b": 3, "c": 4}
        assert result == expected

    def test_deep_merge_override_with_non_dict(self):
        """Test overriding dict with non-dict value."""
        base = {"a": {"x": 1}}
        override = {"a": "not_a_dict"}
        result = deep_merge(base, override)

        expected = {"a": "not_a_dict"}
        assert result == expected

    def test_deep_merge_empty_override(self):
        """Test merging with empty override."""
        base = {"a": 1, "b": {"x": 2}}
        override = {}
        result = deep_merge(base, override)

        assert result == base

    def test_deep_merge_override_with_empty_base(self):
        """Test merging empty base with non-empty override."""
        base = {}
        override = {"a": 1, "b": {"x": 2}}
        result = deep_merge(base, override)

        assert result == override

    def test_deep_merge_independence(self):
        """Test that original dictionaries are not modified."""
        base = {"a": {"x": 1}}
        override = {"a": {"y": 2}}
        original_base = {"a": {"x": 1}}  # Copy for comparison
        original_override = {"a": {"y": 2}}

        result = deep_merge(base, override)

        # Original dicts should remain unchanged
        assert base == original_base
        assert override == original_override


class TestMaskEmail:
    """Test the mask_email function."""

    def test_mask_email_basic(self):
        """Test basic email masking."""
        result = mask_email("john@example.com")
        assert result == "j**n@example.com"

    def test_mask_email_short_local_part(self):
        """Test masking with short local part."""
        result = mask_email("a@example.com")
        assert result == "a*@example.com"

        result = mask_email("ab@example.com")
        assert result == "a*@example.com"

    def test_mask_email_long_local_part(self):
        """Test masking with long local part."""
        # "verylongusername" is 16 characters, so it should be "v" + 14 "*" + "e" = v**************e
        result = mask_email("verylongusername@example.com")
        assert result == "v**************e@example.com"

    def test_mask_email_invalid_format(self):
        """Test masking with invalid email format."""
        result = mask_email("not-an-email")
        assert result == "not-an-email"

    def test_mask_email_no_at_symbol(self):
        """Test masking with no @ symbol."""
        result = mask_email("no-at-symbol")
        assert result == "no-at-symbol"

    def test_mask_email_multiple_at_symbols(self):
        """Test masking with multiple @ symbols."""
        # "user@domain@com" splits into local="user", domain="domain@com"
        # "user" is 4 chars, so mask becomes "u" + "**" + "r" = "u**r"
        result = mask_email("user@domain@com")
        assert result == "u**r@domain@com"  # Masks before first @


class TestGenerateCertificateNumber:
    """Test the generate_certificate_number function."""

    def test_generate_certificate_number_format(self):
        """Test that certificate number follows expected format."""
        result = generate_certificate_number()

        # Format should be: IS-YYYYMMDD-HHHHHHHH (where H is hex)
        pattern = r'^IS-\d{8}-[A-F0-9]{8}$'
        assert re.match(pattern, result) is not None

    def test_generate_certificate_number_unique(self):
        """Test that generated certificate numbers are unique."""
        numbers = [generate_certificate_number() for _ in range(10)]
        assert len(set(numbers)) == 10  # All should be unique

    def test_generate_certificate_number_prefix(self):
        """Test that certificate number has correct prefix."""
        result = generate_certificate_number()
        assert result.startswith("IS-")