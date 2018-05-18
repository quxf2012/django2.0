from _base import *
from django.urls import reverse

def main():
    # url1=reverse("web1:tns",args=("web1",),current_app="web1")
    # url10=reverse("web10:tns",args=("web10",),current_app="web10")
    # url9=reverse("web9:tns",args=("web9",))
    # weburl1 = reverse("web1:index")
    weburl = reverse("web:index")
    wwwurl = reverse("www:index")
    print(locals())


main()
