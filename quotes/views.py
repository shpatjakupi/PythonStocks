from django.shortcuts import render


def home(request):
    # pk_76c76fe8830641698a54009a397061fe
    import requests
    import json

    api_request = requests.get(
        "https://sandbox.iexapis.com/stable/stock/AAPL/quote?token=Tpk_1ffd0fa5cbb241889288941e2f4e0e0f")

    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error ... "

    return render(request, 'home.html', {'api': api})


def about(request):
    return render(request, 'about.html', {})
