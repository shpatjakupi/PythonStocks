from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from models import Stock
from .forms import StockForm
from django.contrib import messages
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
import requests
import io
import urllib, base64

# def home(request):
#     import requests
#     import json

#     if request.method == "POST":
#         ticker = request.POST["ticker"]
#         api_request = requests.get(
#             "https://sandbox.iexapis.com/stable/stock/"
#             + ticker
#             + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
#         )
#         try:
#             api = json.loads(api_request.content)
#         except Exception as e:
#             api = "Error..."
#         return render(request, "home.html", {"api": api})
#     else:
#         return render(request, "home.html", {"ticker": "Enter a ticker symbol above"})

def showstock1(request):
    import matplotlib.pyplot as plt
    import requests
    import io
    import json
    import urllib, base64
    
    if request.method == "POST":
        ticker = request.POST["ticker"]
        api_request = requests.get(
            "https://sandbox.iexapis.com/stable/stock/"
            + ticker
            + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
        )
        api = json.loads(api_request.content)
        plt.switch_backend('agg') #https://www.programcreek.com/python/example/102348/matplotlib.pyplot.switch_backend
        print(api['latestPrice'])
        plt.plot(int(api['latestPrice']),int(api['previousClose']))
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string) 
           
        return render(request, "graph.html", {"api": api},{"data": uri}) + print(2)
    else:
        return render(request, "graph.html", {"ticker": "fuck"}) + print(2)


def about(request):
    return render(request, "about.html", {})


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added..."))
            return redirect("add_stock")
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://sandbox.iexapis.com/stable/stock/"
                + str(ticker_item)
                + "/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f"
            )
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, "add_stock.html", {"ticker": ticker, "output": output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, "delete_stock.html", {"ticker": ticker})


def showstock(request):
    import matplotlib.pyplot as plt
    import requests
    import io
    import urllib, base64
    import pandas as pd

    params = {
        "currency": "EURUSD",
        "start_date": "2018-07-02",
        "end_date": "2018-12-06",
        "api_key": "**************",
    }
    response = requests.get("https://fxmarketapi.com/apipandas", params=params)
    df = pd.read_json(response.text)
    plt.switch_backend('agg')
    plt.plot(df.close)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, "chart.html", {"data": uri})





def showstock2(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    messages.success(request, ("Stock Has Been showed!"))
    plt.switch_backend('agg') #https://www.programcreek.com/python/example/102348/matplotlib.pyplot.switch_backend
    plt.plot(item)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return redirect(show_stock, {"data": uri})

def show_stock(request):
     ticker = Stock.objects.all()
     return render(request, "chart.html", {"ticker": ticker})


# def delete(request, stock_id):
#     item = Stock.objects.get(pk=stock_id)
#     item.delete()
#     messages.success(request, ("Stock Has Been Deleted!"))
#     return redirect(delete_stock)
