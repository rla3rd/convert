import datetime
from .dateAdapter import strptime
import pandas as pd
from pytz import timezone

def stringConvert(string, precision=0):
    try:
        if (
            ('.' in string and string[0] == '-')
            or (
                '.' in string
                and ':' not in string
                and '-' not in string)
        ):
            isfloat = False
            try:
                if 'e' not in '%s' % float(string):
                    isfloat = True
                else:
                    isAlpha = True
            except ValueError:
                isAlpha = True
            if isfloat and precision == 0:
                var = float(string)
                if 'e' in '%s' % var:
                    var = string
            elif isfloat and precision != 0:
                var = round(float(string), precision)
            elif isAlpha:
                var = string
        elif string == '0':
            var = int(string)
        elif string.isdigit() and precision == 0 and string[0] !='0':
            var = int(string)
        elif string.isdigit() and precision != 0 \
                and string[0] != '0' and '.' in string:
            var = round(int(string), precision)
        elif string.isdigit() and precision != 0 \
                and string[0] != '0' and '.' not in string:
            var = int(string)
        elif string[1:].isdigit() and string[0] == '-' and '.' not in string:
            var = int(string)
        elif (
            string[1:].isdigit()
            and string[0] not in ('<', '>', '$')
            and precision == 0
            and not string[0].isalpha()
        ):
            var = int(string)
        elif (
            string[1:].isdigit()
            and string[0] not in ('<', '>', '$')
            and precision != 0
            and not string[0].isalpha()
        ):
            var = round(float(string), precision)
        else:
            try:
                var = strptime(string)
            except ValueError:
                var = string
    except TypeError:
        var = None
    return var


def convertToString(x, datefmt="%Y%m%d", precision=0, csv=True, debug=False):

    if debug:
        print('x: %s, type: %s' % (x, type(x)))
    if type(x) == pd._libs.tslibs.timestamps.Timestamp:
        if debug:
            print(1)
        eastern = timezone('US/Eastern')
        if x.tzinfo is None:
            out = x.to_pydatetime().strftime(datefmt)
        else:
            out = x.tz_convert(
                eastern).to_pydatetime().strftime(datefmt)
    elif type(x) == datetime.date:
        if debug:
            print(2)
        out = x.strftime(datefmt.split(' ')[0])
    elif type(x) == datetime.datetime:
        if debug:
            print(3)
        out = x.strftime(datefmt)
    elif type(x) == pd._libs.tslibs.timedeltas.Timedelta:
        if debug:
            print(4)
        out = x.days
    elif type(x) == str and ':' in x:
        if debug:
            print(5)
        try:
            date_time = strptime(x)
            out = date_time.strftime(datefmt)
        except ValueError:
            out = stringConvert(x, precision=precision)
        except AttributeError:
            out = stringConvert(x, precision=precision)
    elif type(x) == float:
        if debug:
            print(6)
        out = pd.to_numeric(x, errors='ignore', downcast='integer')
        for i in range(precision + 1):
            if out == round(out, i):
                if i == 0:
                    out = int(out)
                else:
                    out = round(out, i)
                break
            else:
                if precision > 0:
                    out = round(out, precision)
                    break
    elif type(x) in (int, list, tuple, bool) or pd.isnull(x):
        if debug:
            print(7)
        if csv and pd.isnull(x):
            x = ''
        out = x
    else:
        if debug:
            print(8)
        out = str(x)
    if debug:
        print('output: %s,  type: %s' % (out, type(out)))
    if not csv:
        if type(out) not in (list, tuple, bool, float, int):
            if out is not None:
                out = str(out)
    else:
        out = str(out)
    return out
