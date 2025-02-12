from django.shortcuts import render, redirect

def report_energy(request):

    return render(request, 'index.html')

def report_energy_tab(request):

    return render(request, 'report_energy_tab.html')


def report_life(request):

    return render(request, 'report_life.html')

def report_ev(request):

    return render(request, 'report_ev.html')

