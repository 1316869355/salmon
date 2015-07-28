from mock import patch
from nose.tools import with_setup

from salmon import utils

from .setup_env import setup_salmon_dirs, teardown_salmon_dirs


def test_make_fake_settings():
    settings = utils.make_fake_settings('localhost', 8800)
    assert settings
    assert settings.receiver
    assert settings.relay is None
    settings.receiver.close()


def test_import_settings():
    settings = utils.import_settings(True, from_dir='tests', boot_module='config.testing')
    assert settings
    assert settings.receiver_config


@with_setup(setup_salmon_dirs, teardown_salmon_dirs)
@patch('daemon.DaemonContext.open')
def test_daemonize_not_fully(dc_open):
    context = utils.daemonize("run/tests.pid", ".", False, False, do_open=False)
    assert context
    assert not dc_open.called
    dc_open.reset_mock()

    context = utils.daemonize("run/tests.pid", ".", "/tmp", 0o002, do_open=True)
    assert context
    assert dc_open.called


@patch("daemon.daemon.change_process_owner")
def test_drop_priv(cpo):
    utils.drop_priv(100, 100)
    assert cpo.called
