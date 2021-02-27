from configparser import ConfigParser, ExtendedInterpolation

parser = ConfigParser(interpolation=ExtendedInterpolation())

parser.read('dev.ini')

print(parser.sections())
print(parser.options('personal'))
print(parser.get('personal', 'id'))
print('db' in parser)
print(parser.get('db', 'user'), type(parser.get('db', 'user')))
print(parser.getint('mysite', 'port', fallback=80))
print(parser.getint('mysite', 'numbers', fallback=50000)) #fallback은 default를 뜻한다고 보면 됨.
# print(parser.getboolean('db', 'password')) # True: 1, yes, true, on / False: 0, no, false, off (include)
print(parser.get('python_settings', 'package_path'))