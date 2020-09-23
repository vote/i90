# i90/urls.py

from urllib.parse import (
    urlencode, unquote, urlparse, parse_qsl, parse_qs, ParseResult
)

import validators


class urls:
    @staticmethod
    def is_valid(url):
        return validators.url(url)

    @staticmethod
    def extract_dimensions(url):
        parsed = urlparse(url)
        params = {}

        for k, vs in parse_qs(parsed.query).items():
            if len(vs) == 1:
                params[f"query_{k}"] = vs[0]
            else:
                for i, v in enumerate(sorted(vs)):
                    params[f"query_{k}_{i}"] = v

        dimensions = {
            "scheme": parsed.scheme,
            "domain": parsed.hostname,
            "path": parsed.path.lstrip("/"),
            "query": parsed.query,
        }
        dimensions.update(params)
        dimensions = {k: v for k, v in dimensions.items() if v}
        return dimensions

    @staticmethod
    def append_query_params(destination, additional_params):
        parsed_dest = urlparse(unquote(destination))
        query_dict = dict(parse_qsl(parsed_dest.query))
        query_dict.update(additional_params)
        return parsed_dest._replace(query=urlencode(query_dict)).geturl()

