"""Replaceable boundaries for extraction, search, and claim evaluation."""

from typing import Protocol

from app.schemas import Claim, ClaimResult, SourceEvidence


class ClaimExtractor(Protocol):
    """Extract checkable factual claims from input text."""

    def extract(self, text: str) -> list[Claim]:
        """Return factual claims found in the text."""
        ...


class SourceSearcher(Protocol):
    """Find public sources that may support or contradict a claim."""

    def search(self, claim: Claim) -> list[SourceEvidence]:
        """Return source passages relevant to the claim."""
        ...


class ClaimEvaluator(Protocol):
    """Evaluate a claim against retrieved evidence."""

    def evaluate(
        self, claim: Claim, sources: list[SourceEvidence]
    ) -> ClaimResult:
        """Return a cautious verdict grounded in the supplied sources."""
        ...