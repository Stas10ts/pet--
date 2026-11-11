"""Typed data contracts shared between checking components."""

from enum import StrEnum

from pydantic import AnyHttpUrl, BaseModel, Field, model_validator


class Verdict(StrEnum):
    """Possible outcomes of checking a factual claim."""

    CONFIRMED = "confirmed"
    NOT_CONFIRMED = "not_confirmed"
    SOURCE_NOT_FOUND = "source_not_found"
    INCONCLUSIVE = "inconclusive"


class Claim(BaseModel):
    """A single factual statement extracted from user text."""

    text: str = Field(min_length=1)


class SourceEvidence(BaseModel):
    """A public source and the passage used as evidence."""

    url: AnyHttpUrl
    title: str = Field(min_length=1)
    quote: str = Field(min_length=1)


class ClaimResult(BaseModel):
    """A verdict with its rationale and, when available, source evidence."""

    claim: Claim
    verdict: Verdict
    explanation: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    source: SourceEvidence | None = None

    @model_validator(mode="after")
    def require_evidence_for_verdict(self) -> "ClaimResult":
        """Prevent a positive or negative verdict without a cited source."""
        if self.verdict == Verdict.SOURCE_NOT_FOUND:
            if self.source is not None:
                raise ValueError("source_not_found results cannot include a source")
        elif self.source is None:
            raise ValueError("a source is required for this verdict")
        return self