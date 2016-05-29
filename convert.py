__version__='1.0'

import dateAdapter

def stringConvert( string, precision = 0 ):
    try:
        if ('.' in string and string[0]=='-') or ('.' in string and ':' not in string and '-' not in string):
            isfloat = False
            try:
                float( string )
                isfloat = True
            except ValueError:
                isAlpha = True
            if isfloat and precision == 0:
                var = float( string )
            elif isfloat and precision != 0:
                var = round( float( string ), precision )
            elif isAlpha:
                var = string
        elif string == '0' and precision == 0:
            var = int( string )
        elif string == '0' and precision != 0:
            var = round( int( string ), precision )
        elif string.isdigit() and precision == 0 and string[0] !='0':
            var = int( string )
        elif string.isdigit() and precision != 0 and string[0] !='0':
            var = round( int( string ), precision )
        elif string[1:].isdigit() and precision == 0 and not string[0].isalpha():
            var = int( string )
        elif string[1:].isdigit() and precision != 0 and not string[0].isalpha():
            var = round( float( string ), precision )
        else:
            try:
                var = dateAdapter.strptime( string )
            except ValueError:
                var = string
    except TypeError:
        var = None
    return var

