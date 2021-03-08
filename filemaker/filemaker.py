from pyfilemaker2 import FmServer

fm = FmServer('http://login:password@filemaker.server.com', 'dbname', 'layoutname')
print(help(FmServer))
