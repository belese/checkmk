#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from .agent_based_api.v1 import Metric, register, Result, State, type_defs
from .utils.cmciii import (
    DiscoveryParams,
    CheckParams,
    discover_cmciii_sensors,
    get_sensor,
    discovery_default_parameters,
    Section,
)


def discover_cmciii_can_current(params: DiscoveryParams,
                                section: Section) -> type_defs.DiscoveryResult:
    yield from discover_cmciii_sensors("can_current", params, section)


def check_cmciii_can_current(item: str, params: CheckParams,
                             section: Section) -> type_defs.CheckResult:
    entry = get_sensor(item, params, section["can_current"])
    if not entry:
        return

    state_readable = entry["Status"]
    value = entry["Value"]
    warn = entry["SetPtHighWarning"]
    crit = entry["SetPtHighAlarm"]

    state = State.OK if state_readable == "OK" else State.CRIT
    yield Result(state=state,
                 summary="Status: %s, Current: %s mA (warn/crit at %s/%s mA)" %
                 (state_readable, value, warn, crit))
    yield Metric("current", value / 1000.0, levels=(warn, crit))


register.check_plugin(
    name="cmciii_can_current",
    sections=['cmciii'],
    service_name="%s",
    discovery_function=discover_cmciii_can_current,
    check_function=check_cmciii_can_current,
    discovery_ruleset_name="discovery_cmciii",
    discovery_default_parameters=discovery_default_parameters(),
    discovery_ruleset_type=register.RuleSetType.MERGED,
    check_default_parameters={},
)
