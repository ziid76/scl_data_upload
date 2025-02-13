from django.shortcuts import render, redirect
import urllib3
import requests
import json, time
import os
from pyairtable import Api
import pandas as pd
import numpy as np
from datetime import datetime

def number_format(input):
        # 100만 단위로 변환하고 천 단위 구분 기호 추가
    formatted_number = "{:,.0f}".format(input / 1000000)

    return formatted_number


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

    for records in table.iterate(page_size=100, max_records=1000):
    #    dataset.append(records[2])
        print('data fetch')
     

    data = [entry['fields'] for entry in records]

    # 'specialValue': 'NaN'을 np.nan으로 변환
    for row in data:
        for key, value in row.items():
            if isinstance(value, dict) and value.get("specialValue") == "NaN":
                row[key] = np.nan

    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # date 필드를 datetime 형식으로 변환
    df['date'] = pd.to_datetime(df['date'])
  

    # 오늘 날짜
    today = datetime.today()

    # 이번 달의 첫째 날
    year_start_date = "2025-01-01"
    month_start_date = today.replace(day=1)
    search_date = "2025-02-06"

    # 기간 내 데이터 필터링 후 합산
    y_b_d_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['chai_budget'].sum()
    y_a_d_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['chai_actual'].sum()
    m_b_d_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['chai_budget'].sum()
    m_a_d_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['chai_actual'].sum()
    d_b_d_sum = df[(df['date'] >= search_date) & (df['date'] <= search_date)]['chai_budget'].sum()
    d_a_d_sum = df[(df['date'] >= search_date) & (df['date'] <= search_date)]['chai_actual'].sum()

    values ={
        'd_b_d_sum': number_format(d_b_d_sum),
        'd_a_d_sum': number_format(d_a_d_sum),
        'm_b_d_sum': number_format(m_b_d_sum),
        'm_a_d_sum': number_format(m_a_d_sum),
        'y_b_d_sum': number_format(y_b_d_sum),
        'y_a_d_sum': number_format(y_a_d_sum),
    }
    
    return render(request, 'report_dinning.html', values)

