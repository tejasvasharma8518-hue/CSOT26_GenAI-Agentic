import requests


def paper_search(query, limit=5):

    try:
        url = "https://huggingface.co/api/papers/search"

        response = requests.get(
            url,
            params={
                "q": query,
                "limit": limit
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }


def read_paper(arxiv_id):

    try:
        url = f"https://huggingface.co/api/papers/{arxiv_id}"

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }