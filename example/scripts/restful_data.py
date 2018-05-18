from base import *
from restapi.models import Snippet

sn = Snippet(code='print(Hello World\nHello Python\n)')
sn.save()

Snippet(code='print(Hello World\nHello Python3\n)').save()
