from core import peer

import pytest


def test_class_creation():
    peer.CasperPeer(port=8888)
