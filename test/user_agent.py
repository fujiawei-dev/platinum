'''
Test `generate_user_agent()` function
pytest test/user_agent.py
'''


import re
from copy import deepcopy
from subprocess import check_output

import pytest
import six
from platinum import InvalidOption, generate_user_agent


def test_it():
    agent = generate_user_agent()
    assert len(agent) > 0


def test_platform_option():
    for _ in range(50):
        agent = generate_user_agent(os='linux')
        assert 'linux' in agent.lower()

        agent = generate_user_agent(os='win')
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='mac')
        assert 'mac' in agent.lower()


def test_invalid_platform_option():
    with pytest.raises(InvalidOption):
        generate_user_agent(os=11)

    with pytest.raises(InvalidOption):
        generate_user_agent(os='dos')

    with pytest.raises(InvalidOption):
        generate_user_agent(os='win,dos')


def test_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(navigator='firefox')
        assert 'firefox' in agent.lower()

        agent = generate_user_agent(navigator='chrome')
        assert 'chrome' in agent.lower()

        agent = generate_user_agent(navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()

        agent = generate_user_agent(navigator='edge')
        assert 'edge' in agent.lower()

        agent = generate_user_agent(navigator='opera')
        assert 'opr' in agent.lower() or 'opios' in agent.lower()


def test_invalid_navigator_option():
    with pytest.raises(InvalidOption):
        generate_user_agent(navigator='vim')

    with pytest.raises(InvalidOption):
        generate_user_agent(navigator='chrome,vim')


def test_navigator_option_tuple():
    for _ in range(50):
        generate_user_agent(navigator=('chrome',))
        generate_user_agent(navigator=('chrome', 'firefox'))
        generate_user_agent(navigator=('chrome', 'firefox', 'ie'))
        generate_user_agent(navigator=('chrome', 'firefox', 'ie', 'edge'))


def test_platform_option_tuple():
    for _ in range(50):
        generate_user_agent(os=('win', 'linux'))
        generate_user_agent(os=('win', 'linux', 'mac'))
        generate_user_agent(os=('win',))
        generate_user_agent(os=('linux',))
        generate_user_agent(os=('mac',))


def test_platform_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(os='win', navigator='firefox')
        assert 'firefox' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='win', navigator='chrome')
        assert 'chrome' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='win', navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='win', navigator='edge')
        assert 'edge' in agent.lower()
        assert 'windows' in agent.lower()


def test_platform_linux():
    for _ in range(50):
        agent = generate_user_agent(os='linux')
        assert agent.startswith('Mozilla/5.0 (X11;')


def test_mac_chrome():
    for _ in range(50):
        agent = generate_user_agent(os='mac', navigator='chrome')
        assert re.search(r'OS X \d+_\d+(_\d+\b|\b)', agent)


def test_impossible_combination():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(os='linux', navigator='ie')
            generate_user_agent(os='linux', navigator='edge')
        with pytest.raises(InvalidOption):
            generate_user_agent(os='mac', navigator='ie')
            generate_user_agent(os='mac', navigator='edge')


def test_gua_script_simple():
    for _ in range(5):
        out = (check_output('gua', shell=True).decode('utf-8'))
        assert re.match('^Mozilla', out)
        assert len(out.strip().splitlines()) == 1


def test_gua_script_options():
    for _ in range(5):
        out = (check_output('gua -o linux -n chrome', shell=True)
               .decode('utf-8'))
        assert re.match('^Mozilla.*Linux.*Chrome', out)


def test_device_type_option():
    for _ in range(50):
        agent = generate_user_agent(device_type='smartphone')
        assert 'Android' in agent or 'iPhone' in agent


def test_device_type_option_invalid():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='fridge')


def test_invalid_combination_device_type_os():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='smartphone', os='win')


def test_invalid_combination_device_type_navigator():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='smartphone', navigator='ie')


def test_no_os_options_default_device_type():
    for _ in range(50):
        agent = generate_user_agent()
        # by default if no os option has given
        # then device_type is "desktop"
        assert 'Android' not in agent


def test_device_type_all():
    for _ in range(50):
        generate_user_agent(device_type='all')
        generate_user_agent(device_type='all', navigator='ie')


def test_device_type_smartphone_chrome():
    for _ in range(50):
        agent = generate_user_agent(device_type='smartphone',
                                    navigator='chrome')
        assert 'Mobile' in agent
