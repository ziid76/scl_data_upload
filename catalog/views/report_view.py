from django.shortcuts import render, redirect
import urllib3
import requests
import json, time
import os
from pyairtable import Api
import pandas as pd

def report_energy(request):

    return render(request, 'index.html')

def report_energy_tab(request):

    return render(request, 'report_energy_tab.html')


def report_life(request):

    return render(request, 'report_life.html')

def report_ev(request):

    return render(request, 'report_ev.html')


def report_dinning(request):
    urllib3.disable_warnings()

    token = "patDs94pPtxWMacxB.e626ab06168396d4388d5e571097f288f8fe8444fe304e61c28025877d917939"
    api = Api(token)
    table = api.table('appoYNBPdtDWEP3jr', 'SL&C')
    table.all(sort=["date"])
    dataset = []


    for records in table.iterate(page_size=100, max_records=1000):
    #    dataset.append(records[2])
        print(records)
    
    return render(request, 'report_dinning.html', dataset)

