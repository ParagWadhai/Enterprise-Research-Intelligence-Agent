from app.research.collector import collect_page


def test_collect_page():

    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    content = collect_page(url)

    assert content is not None

    assert len(content) > 500

    print(
        "\nCollected characters:",
        len(content)
    )

    print(
        "\nFirst 500 characters:\n",
        content[:500]
    )