from django.shortcuts import render
from .models import Stock


def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST["ticker"]
        api_request = requests.get(
            "https://sandbox.iexapis.com/stable/stock/"
            + ticker
            + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
        )
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, "home.html", {"api": api})
    else:
        return render(request, "home.html", {"ticker": "Enter a ticker symbol above"})


def about(request):
    return render(request, "about.html", {})


def add_stock(request):
    if request.method == "POST":
        ticker = request.POST["ticker"]
    ticker = Stock.objects.all()
    return render(request, "add_stock.html", {"ticker": ticker})
