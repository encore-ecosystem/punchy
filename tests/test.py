from core import peer

import pytest


def test_class_creation():
    peer.PunchyPeer(port=8888)
