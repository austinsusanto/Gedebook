from django.shortcuts import render


def show_main(request):
    context = {
        'name': 'Austin Susanto',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)
