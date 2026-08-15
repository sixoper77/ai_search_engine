from trafilatura import extract


def parse_urls(
    response: dict,
    photos: bool | None = False,
    photo_results: int = 4,
    url_results: int = 7,
) -> list[str]:
    res_from_resp = response["results"]
    if not photos:
        return [url["url"] for url in res_from_resp][:url_results]
    return [url["img_src"] for url in response][:photo_results]


def parse_html(html) -> str:
    result = extract(html,output_format="markdown")
    return result
