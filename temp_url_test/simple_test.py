import os
import string
import urllib.parse
import urllib.request


def read_utf8_from_url(url):
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    text = data.decode('utf-8')

    return text


# Naive URL encoding
def _encode_url(url):
    scheme, netloc, path, query, fragment = list(urllib.parse.urlsplit(url))

    path = urllib.parse.quote(path)  # path
    query = urllib.parse.quote_plus(query)  # query
    fragment = urllib.parse.quote(fragment)  # fragment

    encoded_url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

    return encoded_url


if __name__ == "__main__":
    base_url = "https://raw.githubusercontent.com/sanghoon/Bulk-Bing-Image-downloader/temp/non-ascii-url/temp_url_test/"

    paths_to_lookup = [
        "an_ordinary_path.txt",
        "a path with spaces.txt",
        "a_path_with_non_ascii_테스트.txt",
        "a path with spaces and non ascii 테스트.txt",
    ]

    url_quote_methods = {
        'A plain URL': lambda x: x,
        'Simple quote()': lambda x: urllib.parse.quote(x, safe=string.printable),
        'An encoded URL': _encode_url,
    }

    for p in paths_to_lookup:
        print(f"## URL: https://.../{p}")
        url = os.path.join(base_url, p)

        for name, url_func in url_quote_methods.items():
            try:
                assert read_utf8_from_url(url_func(url)) == p
                print(f"[ ] {name}")
            except Exception as e:
                print(f"[X] {name}")
                print(f"    - {str(e)}")

        print("")
