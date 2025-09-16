from django.urls import URLResolver
from theatrebox import urls as project_urls

def test_project_has_api_include():
    has_api = any(
        isinstance(p, URLResolver) and getattr(p.pattern, "_route", "") == "api/"
        for p in project_urls.urlpatterns
    )
    assert has_api, "Expected include('theatre.urls') at path 'api/'"
