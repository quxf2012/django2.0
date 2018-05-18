from django.shortcuts import HttpResponse
from django.urls import reverse
from django.views.generic import View


# Create your views here.


def index(request, *args, **kwargs):
    """index"""
    res = HttpResponse()
    res.write("Hello World!" + str(kwargs))
    return res
    # return HttpResponseRedirect(reverse("web:index", args=(2014,)))


def index1(request, *args, **kwargs):
    """index"""
    res = HttpResponse()
    name = request.resolver_match.namespace
    url1 = reverse("web1:tns", args=("web1",))
    url10 = reverse("web10:tns", args=("web10",))
    url9 = reverse("web9:tns", args=("web9",))
    res.write(str(locals()))

    return res


class IndexView(View):
    def get1(self, request):
        namespace = request.resolver_match.namespace
        data = request.GET
        res = HttpResponse()
        res.write("Hello World!\n" + str(locals()))
        return res

    def get(self, request):
        data = dict(request.GET)
        return HttpResponse("Hello World!\n" + str(locals()))
