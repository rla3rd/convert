# dateAdapter 
# Copyright (C) Richard Albright
# Based on psycopgda, and zope.datetime.tzinfo
#
##############################################################################
# psycopg2da
# Copyright (C) 2006 Fabio Tranchitella <fabio@tranchitella.it>
#
# Based on psycopgda:
#
#   Copyright (c) 2002-2006 Zope Corporation and Contributors.
#   All Rights Reserved.
#
#   This software is subject to the provisions of the Zope Public License,
#   Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
#   THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
#   WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#   WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
#   FOR A PARTICULAR PURPOSE.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# If you prefer you can use this package using the ZPL license as
# published on the Zope web site, http://www.zope.org/Resources/ZPL.
#

from datetime import date, time, datetime
from datetime import tzinfo as _tzinfo, timedelta as _timedelta

class _tzinfo(_tzinfo):

    def __init__(self, minutes):
        if abs(minutes) > 1439:
            raise ValueError("Time-zone offset is too large,", minutes)
        self.__minutes = minutes
        self.__offset = _timedelta(minutes=minutes)

    def utcoffset(self, dt):
        return self.__offset

    def __reduce__(self):
        return tzinfo, (self.__minutes, )

    def dst(self, dt):
        return None

    def tzname(self, dt):
        return None

    def __repr__(self):
        return 'tzinfo(%d)' % self.__minutes


def tzinfo(offset, _tzinfos = {}):

    info = _tzinfos.get(offset)
    if info is None:
        # We haven't seen this one before. we need to save it.

        # Use setdefault to avoid a race condition and make sure we have
        # only one
        info = _tzinfos.setdefault(offset, _tzinfo(offset))

    return info

import re

# date/time parsing functions
_dateFmt = re.compile(r"^(\d\d\d\d)-?([01]\d)-?([0-3]\d)$")

def parse_date(s):
    """Parses ISO-8601 compliant dates and returns a tuple (year, month,
    day).

    The following formats are accepted:
        YYYY-MM-DD  (extended format)
        YYYYMMDD    (basic format)
    """
    m = _dateFmt.match(s)
    if m is None:
        raise ValueError, 'invalid date string: %s' % s
    year, month, day = m.groups()
    return int(year), int(month), int(day)


_timeFmt = re.compile(r"^([0-2]\d)(?::?([0-5]\d)(?::?([0-5]\d)(?:[.,](\d+))?)?)?$")

def parse_time(s):
    """Parses ISO-8601 compliant times and returns a tuple (hour, minute,
    second).

    The following formats are accepted:
        HH:MM:SS.ssss or HHMMSS.ssss
        HH:MM:SS,ssss or HHMMSS,ssss
        HH:MM:SS      or HHMMSS
        HH:MM         or HHMM
        HH
    """
    m = _timeFmt.match(s)
    if m is None:
        raise ValueError, 'invalid time string: %s' % s
    hr, mn, sc, msc = m.groups(0)
    if msc != 0:
        sc = float("%s.%s" % (sc, msc))
    else:
        sc = int(sc)
    return int(hr), int(mn), sc


_tzFmt = re.compile(r"^([+-])([0-2]\d)(?::?([0-5]\d))?$")

def parse_tz(s):
    """Parses ISO-8601 timezones and returns the offset east of UTC in
    minutes.

    The following formats are accepted:
        +/-HH:MM
        +/-HHMM
        +/-HH
        Z           (equivalent to +0000)
    """
    if s == 'Z':
        return 0
    m = _tzFmt.match(s)
    if m is None:
        raise ValueError, 'invalid time zone: %s' % s
    d, hoff, moff = m.groups(0)
    if d == "-":
        return - int(hoff) * 60 - int(moff)
    return int(hoff) * 60 + int(moff)


_tzPos = re.compile(r"[Z+-]")

def parse_timetz(s):
    """Parses ISO-8601 compliant times that may include timezone information
    and returns a tuple (hour, minute, second, tzoffset).

    tzoffset is the offset east of UTC in minutes.  It will be None if s does
    not include time zone information.

    Formats accepted are those listed in the descriptions of parse_time() and
    parse_tz().  Time zone should immediatelly follow time without intervening
    spaces.
    """
    m = _tzPos.search(s)
    if m is None:
        return parse_time(s) + (None,)
    pos = m.start()
    return parse_time(s[:pos]) + (parse_tz(s[pos:]),)


_datetimeFmt = re.compile(r"[T ]")

def _split_datetime(s):
    """Split date and time parts of ISO-8601 compliant timestamp and
    return a tuple (date, time).

    ' ' or 'T' used to separate date and time parts.
    """
    m = _datetimeFmt.search(s)
    if m is None:
        raise ValueError, 'time part of datetime missing: %s' % s
    pos = m.start()
    return s[:pos], s[pos + 1:]


def parse_datetime(s):
    """Parses ISO-8601 compliant timestamp and returns a tuple (year, month,
    day, hour, minute, second).

    Formats accepted are those listed in the descriptions of parse_date() and
    parse_time() with ' ' or 'T' used to separate date and time parts.
    """
    dt, tm = _split_datetime(s)
    return parse_date(dt) + parse_time(tm)


def parse_datetimetz(s):
    """Parses ISO-8601 compliant timestamp that may include timezone
    information and returns a tuple (year, month, day, hour, minute, second,
    tzoffset).

    tzoffset is the offset east of UTC in minutes.  It will be None if s does
    not include time zone information.

    Formats accepted are those listed in the descriptions of parse_date() and
    parse_timetz() with ' ' or 'T' used to separate date and time parts.
    """
    dt, tm = _split_datetime(s)
    return parse_date(dt) + parse_timetz(tm)

# Type conversions
def convert_date(s):
    return date(*parse_date(s))

def convert_time(s):
    hr, mn, sc = parse_time(s)
    sc, micro = divmod(sc, 1.0)
    micro = round(micro * 1000000)
    return time(hr, mn, int(sc), int(micro))

def convert_timetz(s):
    hr, mn, sc, tz = parse_timetz(s)
    sc, micro = divmod(sc, 1.0)
    micro = round(micro * 1000000)
    if tz: tz = tzinfo(tz)
    return time(hr, mn, int(sc), int(micro), tz)

def convert_timestamp(s):
    y, m, d, hr, mn, sc = parse_datetime(s)
    sc, micro = divmod(sc, 1.0)
    micro = round(micro * 1000000)
    return datetime(y, m, d, hr, mn, int(sc), int(micro))

def convert_timestamptz(s):
    y, m, d, hr, mn, sc, tz = parse_datetimetz(s)
    sc, micro = divmod(sc, 1.0)
    micro = round(micro * 1000000)
    if tz: tz = tzinfo(tz)
    return datetime(y, m, d, hr, mn, int(sc), int(micro), tz)

def strptime(s):
    try:
	return convert_timestamptz(s)
    except ValueError:
	pass
    try:
	return convert_timetz(s)
    except ValueError:
	pass
    try:
	return convert_date(s)
    except ValueError:
	return s
	
	
