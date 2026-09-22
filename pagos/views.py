from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def pago(request):
    return render(
        request,
        "pagos/pago.html",
    )