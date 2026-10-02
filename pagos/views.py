from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def pago(request):
    return render(
        request,
        "pagos/pago.html",
    )
