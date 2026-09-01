import trafilatura


def collect_page(url: str) -> str | None:

    try:

        downloaded = trafilatura.fetch_url(
            url
        )

        if not downloaded:
            return None

        content = trafilatura.extract(
            downloaded,
            include_links=False,
            include_images=False,
            include_tables=True,
        )

        return content

    except Exception as exc:

        print(
            f"Failed to collect {url}: {exc}"
        )

        return None