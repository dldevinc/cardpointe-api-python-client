class MockResponse:
    def __init__(self, method, url, status=200, content=None, **kwargs):
        self.method = method
        self.url = url
        self.status_code = status
        self.content = content
        self.kwargs = kwargs

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item):
        return self.content[item]

    def __contains__(self, item):
        return item in self.content

    def json(self):
        return self


def mock_response(content, status=200):
    def inner(method, url, **kwargs):
        return MockResponse(
            method=method,
            url=url,
            status=status,
            content=content,
            **kwargs,
        )
    return inner
