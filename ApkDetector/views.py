from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth


@login_required()
def index(request):
    """
    :param request
    :return: 用户首页
    """
    return render(request, "base.html")
