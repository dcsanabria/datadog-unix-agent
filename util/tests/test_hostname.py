import mock
import pytest

from util.hostname import get_hostname, is_valid_hostname
from config import config

def test_is_valid_hostname():
    assert not is_valid_hostname("localhost")
    assert not is_valid_hostname('localhost')
    assert not is_valid_hostname('localhost.localdomain')
    assert not is_valid_hostname('localhost6.localdomain6')
    assert not is_valid_hostname('ip6-localhost')

    # test MAX_HOSTNAME_LEN
    assert not is_valid_hostname("a" * 256)

    # test RFC 1123
    assert not is_valid_hostname("-test-")
    assert not is_valid_hostname(".test.")

    assert is_valid_hostname("test.test-test")

def test_get_hostname_conf():
    config.set("hostname", "test-hostname")
    assert get_hostname() == "test-hostname"
    config.reset("hostname")

@mock.patch('subprocess.check_output', return_value="subprocess-hostname")
def test_get_hostname_bin(subprocess):
    assert get_hostname() == "subprocess-hostname"

@mock.patch("subprocess.check_output", return_value="")
@mock.patch("socket.gethostname", return_value="socket-hostname")
def test_get_hostname_socket(subprocess, socket):
    assert get_hostname() == "socket-hostname"


@mock.patch("subprocess.check_output", return_value="")
@mock.patch("socket.gethostname", return_value="")
def test_get_hostname_error(subprocess, socket):
    with pytest.raises(Exception) as err:
        get_hostname()
    assert "Unable to reliably determine host name. You can define one in datadog.conf or in your hosts file" in str(err)
