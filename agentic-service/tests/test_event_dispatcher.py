import pytest
from background.event_dispatcher import dispatch_event

def test_dispatch_event():
    # Currently just logging
    res = dispatch_event("test_event", {"data": 1})
    assert res == True
