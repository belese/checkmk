#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from tests.testlib import Check

from cmk.base.plugins.agent_based.mtr import Hop

pytestmark = pytest.mark.checks

SECTION = {
    "ipv6.google.com": [],
    "mathias-kettner.de": [
        Hop(
            name="1.2.3.4",
            pl=0.0,
            response_time=0.0013,
            rta=0.0022,
            rtmin=0.0012,
            rtmax=0.007,
            rtstddev=0.0016,
        ),
        Hop(
            name="232.142.105.70",
            pl=0.0,
            response_time=0.0018,
            rta=0.0027,
            rtmin=0.0015,
            rtmax=0.0044,
            rtstddev=0.0011,
        ),
        Hop(
            name="146.26.170.63",
            pl=0.0,
            response_time=0.017,
            rta=0.016800000000000002,
            rtmin=0.0145,
            rtmax=0.019899999999999998,
            rtstddev=0.0012,
        ),
        Hop(
            name="195.164.42.167",
            pl=0.0,
            response_time=0.0172,
            rta=0.0184,
            rtmin=0.0155,
            rtmax=0.0254,
            rtstddev=0.0027,
        ),
        Hop(
            name="145.111.28.11",
            pl=0.0,
            response_time=0.0212,
            rta=0.019600000000000003,
            rtmin=0.0162,
            rtmax=0.0298,
            rtstddev=0.0040999999999999995,
        ),
        Hop(
            name="98.216.107.58",
            pl=0.0,
            response_time=0.0554,
            rta=0.0533,
            rtmin=0.0281,
            rtmax=0.1281,
            rtstddev=0.0281,
        ),
    ],
    "www.google.com": [
        Hop(
            name="1.2.3.4",
            pl=0.0,
            response_time=0.0014,
            rta=0.0016,
            rtmin=0.0014,
            rtmax=0.0022,
            rtstddev=0.0,
        ),
        Hop(
            name="232.142.105.70",
            pl=0.0,
            response_time=0.0165,
            rta=0.0179,
            rtmin=0.0035,
            rtmax=0.027,
            rtstddev=0.0065,
        ),
        Hop(
            name="ae0.rt-inxs-1.m-online.net",
            pl=0.0,
            response_time=0.0156,
            rta=0.0184,
            rtmin=0.0149,
            rtmax=0.0252,
            rtstddev=0.0033,
        ),
        Hop(
            name="whatever",
            pl=0.0,
            response_time=0.015300000000000001,
            rta=0.019100000000000002,
            rtmin=0.0145,
            rtmax=0.032299999999999995,
            rtstddev=0.0052,
        ),
        Hop(
            name="210.233.222.159",
            pl=0.0,
            response_time=0.0156,
            rta=0.018699999999999998,
            rtmin=0.0156,
            rtmax=0.0211,
            rtstddev=0.0018,
        ),
        Hop(
            name="9.32.75.54",
            pl=0.0,
            response_time=0.019,
            rta=0.020300000000000002,
            rtmin=0.0149,
            rtmax=0.0303,
            rtstddev=0.0048,
        ),
        Hop(
            name="7.69.211.19",
            pl=0.0,
            response_time=0.0247,
            rta=0.027800000000000002,
            rtmin=0.023399999999999997,
            rtmax=0.0432,
            rtstddev=0.0058,
        ),
        Hop(
            name="145.80.196.60",
            pl=0.0,
            response_time=0.0255,
            rta=0.0247,
            rtmin=0.0222,
            rtmax=0.0263,
            rtstddev=0.0009,
        ),
        Hop(
            name="0.253.40.93",
            pl=0.0,
            response_time=0.023899999999999998,
            rta=0.0229,
            rtmin=0.0212,
            rtmax=0.023899999999999998,
            rtstddev=0.0007,
        ),
        Hop(
            name="85.26.182.623",
            pl=0.0,
            response_time=0.0237,
            rta=0.024,
            rtmin=0.0202,
            rtmax=0.027100000000000003,
            rtstddev=0.0022,
        ),
        Hop(
            name="last-host.net",
            pl=0.0,
            response_time=0.023399999999999997,
            rta=0.023600000000000003,
            rtmin=0.0215,
            rtmax=0.026600000000000002,
            rtstddev=0.0015,
        ),
    ],
}


def test_discover_mtr() -> None:
    assert list(Check("mtr").run_discovery(SECTION)) == [
        ("ipv6.google.com", {}),
        ("mathias-kettner.de", {}),
        ("www.google.com", {}),
    ]


@pytest.mark.parametrize(
    "item, params, check_result",
    [
        pytest.param(
            "mathias-kettner.de",
            {
                "pl": (10, 25),
                "rta": (150, 250),
                "rtstddev": (150, 250),
            },
            [
                (
                    0,
                    "Number of Hops: 6",
                    [
                        ("hops", 6),
                    ],
                ),
                (
                    0,
                    "Packet loss: 0%, Round trip average: 53.3 ms, Standard deviation: 28.1 ms\n"
                    "Hop 1: 1.2.3.4\n"
                    "Hop 2: 232.142.105.70\n"
                    "Hop 3: 146.26.170.63\n"
                    "Hop 4: 195.164.42.167\n"
                    "Hop 5: 145.111.28.11\n"
                    "Hop 6: 98.216.107.58",
                    [
                        ("hop_1_rta", 0.0022),
                        ("hop_1_rtmin", 0.0012),
                        ("hop_1_rtmax", 0.007),
                        ("hop_1_rtstddev", 0.0016),
                        ("hop_1_response_time", 0.0013),
                        ("hop_1_pl", 0.0),
                        ("hop_2_rta", 0.0027),
                        ("hop_2_rtmin", 0.0015),
                        ("hop_2_rtmax", 0.0044),
                        ("hop_2_rtstddev", 0.0011),
                        ("hop_2_response_time", 0.0018),
                        ("hop_2_pl", 0.0),
                        ("hop_3_rta", 0.016800000000000002),
                        ("hop_3_rtmin", 0.0145),
                        ("hop_3_rtmax", 0.019899999999999998),
                        ("hop_3_rtstddev", 0.0012),
                        ("hop_3_response_time", 0.017),
                        ("hop_3_pl", 0.0),
                        ("hop_4_rta", 0.0184),
                        ("hop_4_rtmin", 0.0155),
                        ("hop_4_rtmax", 0.0254),
                        ("hop_4_rtstddev", 0.0027),
                        ("hop_4_response_time", 0.0172),
                        ("hop_4_pl", 0.0),
                        ("hop_5_rta", 0.019600000000000003),
                        ("hop_5_rtmin", 0.0162),
                        ("hop_5_rtmax", 0.0298),
                        ("hop_5_rtstddev", 0.0040999999999999995),
                        ("hop_5_response_time", 0.0212),
                        ("hop_5_pl", 0.0),
                        ("hop_6_pl", 0.0, 10, 25),
                        ("hop_6_rta", 0.0533, 0.15, 0.25),
                        ("hop_6_rtstddev", 0.0281, 0.15, 0.25),
                        ("hop_6_rtmin", 0.0281),
                        ("hop_6_rtmax", 0.1281),
                        ("hop_6_response_time", 0.0554),
                    ],
                ),
            ],
            id="normal case",
        ),
        pytest.param(
            "mathias-kettner.de",
            {
                "pl": (0, 1),
                "rta": (0, 1),
                "rtstddev": (0, 1),
            },
            [
                (
                    0,
                    "Number of Hops: 6",
                    [
                        ("hops", 6),
                    ],
                ),
                (
                    2,
                    "Packet loss: 0% (warn/crit at 0%/1.0%), Round trip average: 53.3 ms "
                    "(warn/crit at 0.00 s/1.00 ms), Standard deviation: 28.1 ms (warn/crit at "
                    "0.00 s/1.00 ms)\n"
                    "Hop 1: 1.2.3.4\n"
                    "Hop 2: 232.142.105.70\n"
                    "Hop 3: 146.26.170.63\n"
                    "Hop 4: 195.164.42.167\n"
                    "Hop 5: 145.111.28.11\n"
                    "Hop 6: 98.216.107.58",
                    [
                        ("hop_1_rta", 0.0022),
                        ("hop_1_rtmin", 0.0012),
                        ("hop_1_rtmax", 0.007),
                        ("hop_1_rtstddev", 0.0016),
                        ("hop_1_response_time", 0.0013),
                        ("hop_1_pl", 0.0),
                        ("hop_2_rta", 0.0027),
                        ("hop_2_rtmin", 0.0015),
                        ("hop_2_rtmax", 0.0044),
                        ("hop_2_rtstddev", 0.0011),
                        ("hop_2_response_time", 0.0018),
                        ("hop_2_pl", 0.0),
                        ("hop_3_rta", 0.016800000000000002),
                        ("hop_3_rtmin", 0.0145),
                        ("hop_3_rtmax", 0.019899999999999998),
                        ("hop_3_rtstddev", 0.0012),
                        ("hop_3_response_time", 0.017),
                        ("hop_3_pl", 0.0),
                        ("hop_4_rta", 0.0184),
                        ("hop_4_rtmin", 0.0155),
                        ("hop_4_rtmax", 0.0254),
                        ("hop_4_rtstddev", 0.0027),
                        ("hop_4_response_time", 0.0172),
                        ("hop_4_pl", 0.0),
                        ("hop_5_rta", 0.019600000000000003),
                        ("hop_5_rtmin", 0.0162),
                        ("hop_5_rtmax", 0.0298),
                        ("hop_5_rtstddev", 0.0040999999999999995),
                        ("hop_5_response_time", 0.0212),
                        ("hop_5_pl", 0.0),
                        ("hop_6_pl", 0.0, 0, 1),
                        ("hop_6_rta", 0.0533, 0, 0.001),
                        ("hop_6_rtstddev", 0.0281, 0, 0.001),
                        ("hop_6_rtmin", 0.0281),
                        ("hop_6_rtmax", 0.1281),
                        ("hop_6_response_time", 0.0554),
                    ],
                ),
            ],
            id="normal case with low levels",
        ),
        pytest.param(
            "ipv6.google.com",
            {
                "pl": (10, 25),
                "rta": (150, 250),
                "rtstddev": (150, 250),
            },
            [(3, "Insufficient data: No hop information available")],
            id="no hops",
        ),
    ],
)
def test_check_mtr(
    item: str,
    params,
    check_result,
) -> None:
    assert list(Check("mtr").run_check(
        item,
        params,
        SECTION,
    )) == check_result
