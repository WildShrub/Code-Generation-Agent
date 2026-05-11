import socket
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Change the hostname in pytest-metadata
    if hasattr(config, "_metadata"):
        config._metadata["Host name"] = "my-custom-host"

    # Optional: also change Python's reported hostname
    socket.gethostname = lambda: "my-custom-host2"