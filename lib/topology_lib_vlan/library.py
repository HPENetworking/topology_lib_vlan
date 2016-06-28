# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_lib_vlan communication library implementation.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division


CONFIG_FILE_SYSCTL = '/etc/sysctl.conf'


def update_packet_list(enode,
                       _shell='bash',
                       _shell_args={
                                    'matches': None,
                                    'newline': True,
                                    'timeout': None,
                                    'connection': None
                                    }
                       ):
    """
    Resynchronize the package index files from their sources in host machine.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    shell = enode.get_shell(_shell)

    cmd = 'rm /var/lib/apt/lists/* -vf'
    shell.send_command(cmd, **_shell_args)

    cmd = 'apt-get update'
    shell.send_command(cmd, **_shell_args)

    assert 'Done' in shell.get_response()


def install_vlan_packet(enode,
                        _shell='bash',
                        _shell_args={
                                    'matches': None,
                                    'newline': True,
                                    'timeout': 120,
                                    'connection': None
                                    }
                        ):
    """
    Install the vlan packet in host machine.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    update_packet_list(enode, _shell, _shell_args)

    shell = enode.get_shell(_shell)

    cmd = 'apt-get install vlan'
    shell.send_command(cmd, **_shell_args)

    assert 'Setting up vlan' in shell.get_response()


def load_8021q_module(enode,
                      _shell='bash',
                      _shell_args={
                                    'matches': None,
                                    'newline': True,
                                    'timeout': None,
                                    'connection': None
                                    }
                      ):
    """
    Load 8021q kernel module.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    shell = enode.get_shell(_shell)

    cmd = 'modprobe 8021q'
    shell.send_command(cmd, **_shell_args)


def enable_ip_forward(enode,
                      _shell='bash',
                      _shell_args={
                                    'matches': None,
                                    'newline': True,
                                    'timeout': None,
                                    'connection': None
                                    }
                      ):
    """
    Enable packet forwarding for IPv4

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    shell = enode.get_shell(_shell)

    cmd = 'echo "net.ipv4.ip_forward=1" >> {file}'.format(
        file=CONFIG_FILE_SYSCTL
    )
    shell.send_command(cmd, **_shell_args)


def add_vlan(enode, interface, vlan_id,
             _shell='bash',
             _shell_args={
                         'matches': None,
                         'newline': True,
                         'timeout': None,
                         'connection': None
                        }
             ):
    """
    Creates a vlan-device on specific interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str interface: Interface which vlan will be added
    :param int vlan_id: VLAN ID that will be added to interface
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    assert interface
    assert vlan_id

    shell = enode.get_shell(_shell)

    cmd = 'vconfig add {interface} {vlan_id}'.format(
            interface=interface, vlan_id=str(vlan_id)
    )
    shell.send_command(cmd, **_shell_args)

    assert 'Added VLAN with VID == {vlan_id} to IF -:{interface}:-'.format(
        vlan_id=str(vlan_id), interface=interface) in shell.get_response()


def remove_vlan(enode, interface, vlan_id,
                _shell='bash',
                _shell_args={
                             'matches': None,
                             'newline': True,
                             'timeout': None,
                             'connection': None
                             }
                ):
    """
    Deletes a vlan-device on specific interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str interface: Interface which vlan will be deleted
    :param int vlan_id: VLAN ID that will be deleted
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    assert interface
    assert vlan_id

    shell = enode.get_shell(_shell)

    cmd = 'vconfig rem {interface}.{vlan_id}'.format(
            interface=interface, vlan_id=str(vlan_id)
    )
    shell.send_command(cmd, **_shell_args)

    assert 'Removed VLAN -:{interface}.{vlan_id}:-'.format(
        vlan_id=str(vlan_id), interface=interface) in shell.get_response()


def link_set_up(enode, interface, vlan_id,
                _shell='bash',
                _shell_args={
                             'matches': None,
                             'newline': True,
                             'timeout': None,
                             'connection': None
                             }
                ):
    """
    Start the new interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str interface: Interface which vlan will be enabled
    :param int vlan_id: VLAN ID that will be added to interface
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    assert interface
    assert vlan_id

    shell = enode.get_shell(_shell)

    cmd = 'ip link set up {interface}.{vlan_id}'.format(
            interface=interface, vlan_id=str(vlan_id)
    )
    shell.send_command(cmd, **_shell_args)


def add_ip_address_vlan(enode, ip_address, interface, vlan_id,
                        _shell='bash',
                        _shell_args={
                                     'matches': None,
                                     'newline': True,
                                     'timeout': None,
                                     'connection': None
                                     }
                        ):
    """
    Add an ip address to vlan interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str ip_address: IP addresses that will be added to vlan.
        Format A.B.C.D/M
    :param str interface: Interface which vlan will be added
    :param int vlan_id: VLAN ID that will be added to interface
    :param str _shell: shell to be selected
    :param dict _shell_args: low-level shell API arguments
    """

    assert ip_address
    assert interface
    assert vlan_id

    shell = enode.get_shell(_shell)

    cmd = 'ip addr add {ip_address} dev {interface}.{vlan_id}'.format(
            ip_address=ip_address, interface=interface, vlan_id=str(vlan_id)
    )
    shell.send_command(cmd, **_shell_args)

    link_set_up(enode, interface, vlan_id, _shell, _shell_args)


__all__ = [
    'update_packet_list', 'install_vlan_packet', 'load_8021q_module',
    'enable_ip_forward', 'add_vlan', 'add_ip_address_vlan', 'remove_vlan',
    'link_set_up'
]
