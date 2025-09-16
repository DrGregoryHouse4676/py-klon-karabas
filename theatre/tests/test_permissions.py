from theatre.permissions import IsAdminOrReadOnly

class DummyUser:
    def __init__(self, is_staff=False):
        self.is_staff = is_staff

class DummyRequest:
    def __init__(self, method="GET", user=None):
        self.method = method
        self.user = user

def test_readonly_allows_anonymous_get():
    perm = IsAdminOrReadOnly()
    req = DummyRequest(method="GET", user=None)  # анонім + SAFE_METHOD
    assert perm.has_permission(req, view=None) is True

def test_write_denied_for_nonstaff():
    perm = IsAdminOrReadOnly()
    req = DummyRequest(method="POST", user=DummyUser(is_staff=False))
    assert perm.has_permission(req, view=None) is False

def test_write_allowed_for_staff():
    perm = IsAdminOrReadOnly()
    req = DummyRequest(method="POST", user=DummyUser(is_staff=True))
    assert perm.has_permission(req, view=None) is True
