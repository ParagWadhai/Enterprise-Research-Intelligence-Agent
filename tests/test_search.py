from app.research.search import search_web


def test_web_search():

    results = search_web(
        "generative AI telecom network operations",
        max_results=3,
    )

    assert isinstance(results, list)

    assert len(results) > 0

    for result in results:

        assert result["title"]
        assert result["url"]

        print("\nTitle:", result["title"])
        print("URL:", result["url"])
        print("Snippet:", result["snippet"])