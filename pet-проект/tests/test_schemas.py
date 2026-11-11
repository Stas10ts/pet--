import pytest
from pydantic import ValidationError

from app.schemas import Claim, ClaimResult, SourceEvidence, Verdict


def test_source_not_found_can_have_no_source() -> None:
    result = ClaimResult(
        claim=Claim(text="The claim"),
        verdict=Verdict.SOURCE_NOT_FOUND,
        explanation="No relevant source was found.",
        confidence=0.2,
    )

    assert result.source is None


def test_confirmed_result_requires_source() -> None:
    with pytest.raises(ValidationError):
        ClaimResult(
            claim=Claim(text="The claim"),
            verdict=Verdict.CONFIRMED,
            explanation="A supporting source is required.",
            confidence=0.9,
        )


def test_confirmed_result_accepts_cited_source() -> None:
    evidence = SourceEvidence(
        url="https://example.org/facts",
        title="Example facts",
        quote="A relevant passage.",
    )

    result = ClaimResult(
        claim=Claim(text="The claim"),
        verdict=Verdict.CONFIRMED,
        explanation="The passage supports the claim.",
        confidence=0.9,
        source=evidence,
    )

    assert result.source == evidence