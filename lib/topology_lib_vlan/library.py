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


def install_vlan_packet(enode):
    """
    Install the vlan packet in host machine.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    """

    cmd = 'apt-get install vlan'
    install_vlan_packet_re = enode(cmd, shell='bash')

    assert 'Setting up vlan' in install_vlan_packet_re


def load_8021q_module(enode):
    """
    Load 8021q kernel module.

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    """

    cmd = 'modprobe 8021q'
    enode(cmd, shell='bash')


def enable_ip_forward(enode):
    """
    Enable packet forwarding for IPv4

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    """

    cmd = 'echo "net.ipv4.ip_forward=1" >> {file}'.format(
        file=CONFIG_FILE_SYSCTL
    )
    enode(cmd, shell='bash')


def add_vlan(enode, interface, vlan_id):
    """
    Creates a vlan-device on specific interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str interface: Interface which vlan will be added
    :param int vlan_id: VLAN ID that will be added to interface
    """

    assert interface
    assert vlan_id

    cmd = 'vconfig add {interface} {vlan_id}'.format(
            interface=interface, vlan_id=str(vlan_id)
    )
    add_vlan_re = enode(cmd, shell='bash')

    assert 'Added VLAN with VID == {vlan_id} to IF -:{interface}:-'.format(
        vlan_id=str(vlan_id), interface=interface) in add_vlan_re


def add_ip_address_vlan(enode, ip_address, interface, vlan_id):
    """
    Add an ip address to vlan interface

    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str ip_address: IP addresses that will be added to vlan.
        Format A.B.C.D/M
    :param str interface: Interface which vlan will be added
    :param int vlan_id: VLAN ID that will be added to interface
    """

    assert interface
    assert vlan_id

    cmd = 'ip addr add {ip_address} dev {interface}.{vlan_id}'.format(
            ip_address=ip_address, interface=interface, vlan_id=str(vlan_id)
    )
    enode(cmd, shell='bash')


__all__ = [
    'install_vlan_packet', 'load_8021q_module', 'enable_ip_forward',
    'add_vlan', 'add_ip_address_vlan'
]
