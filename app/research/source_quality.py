from urllib.parse import urlparse


HIGH_AUTHORITY_DOMAINS = {
    ".gov",
    ".edu",
    "who.int",
    "oecd.org",
    "worldbank.org",
    "nasa.gov",
}


RESEARCH_DOMAINS = {
    "arxiv.org",
    "nature.com",
    "sciencedirect.com",
    "ieee.org",
}


def calculate_source_quality(
    url: str,
) -> float:

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    score = 0.5

    # Government / educational / major
    # institutional sources
    if any(
        domain.endswith(item)
        for item in HIGH_AUTHORITY_DOMAINS
    ):
        score += 0.3

    # Research sources
    elif any(
        item in domain
        for item in RESEARCH_DOMAINS
    ):
        score += 0.25

    # HTTPS
    if parsed.scheme == "https":
        score += 0.05

    return min(score, 1.0)