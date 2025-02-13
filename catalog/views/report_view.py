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
                row[key] = 0

    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # date 필드를 datetime 형식으로 변환
    df['date'] = pd.to_datetime(df['date'])
  

    # 오늘 날짜
    today = datetime.today()

    # 이번 달의 첫째 날
    year_start_date = "2025-01-01"
    month_start_date = today.replace(day=1).strftime("%Y-%m-%d")
    search_date = "2025-02-06"

    # 기간 내 데이터 필터링 후 합산
    # 차이797
    y_b_c_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['chai_budget'].sum()
    y_a_c_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['chai_actual'].sum()
    m_b_c_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['chai_budget'].sum()
    m_a_c_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['chai_actual'].sum()
    d_b_c_sum = df[(df['date'] == search_date)]['chai_budget'].sum()
    d_a_c_sum = df[(df['date'] == search_date)]['chai_actual'].sum()

    # 정육점
    y_b_j_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['j_budget'].sum()
    y_a_j_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['j_actual'].sum()
    m_b_j_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['j_budget'].sum()
    m_a_j_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['j_actual'].sum()
    d_b_j_sum = df[(df['date'] == search_date)]['j_budget'].sum()
    d_a_j_sum = df[(df['date'] == search_date)]['j_actual'].sum()

    # 서리재
    y_b_s_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['s_budget'].sum()
    y_a_s_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['s_actual'].sum()
    m_b_s_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['s_budget'].sum()
    m_a_s_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['s_actual'].sum()
    d_b_s_sum = df[(df['date'] == search_date)]['s_budget'].sum()
    d_a_s_sum = df[(df['date'] == search_date)]['s_actual'].sum()

    # 호우섬
    y_b_h_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['h_budget'].sum()
    y_a_h_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['h_actual'].sum()
    m_b_h_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['h_budget'].sum()
    m_a_h_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['h_actual'].sum()
    d_b_h_sum = df[(df['date'] == search_date)]['h_budget'].sum()
    d_a_h_sum = df[(df['date'] == search_date)]['h_actual'].sum()

    # 호우섬
    y_b_i_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['i_budget'].sum()
    y_a_i_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['i_actual'].sum()
    m_b_i_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['i_budget'].sum()
    m_a_i_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['i_actual'].sum()
    d_b_i_sum = df[(df['date'] == search_date)]['i_budget'].sum()
    d_a_i_sum = df[(df['date'] == search_date)]['i_actual'].sum()

    # 외식합계
    y_b_d_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['dinning_budget'].sum()
    y_a_d_sum = df[(df['date'] >= year_start_date) & (df['date'] <= search_date)]['dinning_actual'].sum()
    m_b_d_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['dinning_budget'].sum()
    m_a_d_sum = df[(df['date'] >= month_start_date) & (df['date'] <= search_date)]['dinning_actual'].sum()
    d_b_d_sum = df[(df['date'] == search_date)]['dinning_budget'].sum()
    d_a_d_sum = df[(df['date'] == search_date)]['dinning_actual'].sum()

    values ={
        # 차이797
        'd_b_c_sum': number_format(d_b_c_sum),
        'd_a_c_sum': number_format(d_a_c_sum),
        'd_c_per': d_a_c_sum/d_b_c_sum * 100,
        'm_b_c_sum': number_format(m_b_c_sum),
        'm_a_c_sum': number_format(m_a_c_sum),
        'm_c_per': m_a_c_sum/m_b_c_sum * 100,
        'y_b_c_sum': number_format(y_b_c_sum),
        'y_a_c_sum': number_format(y_a_c_sum),
        'y_c_per': y_a_c_sum/y_b_c_sum * 100,
        # 정육점
        'd_b_j_sum': number_format(d_b_j_sum),
        'd_a_j_sum': number_format(d_a_j_sum),
        'd_j_per': d_a_j_sum/d_b_j_sum * 100,
        'm_b_ㅓ_sum': number_format(m_b_j_sum),
        'm_a_j_sum': number_format(m_a_j_sum),
        'm_j_per': m_a_j_sum/m_b_j_sum * 100,
        'y_b_j_sum': number_format(y_b_j_sum),
        'y_a_j_sum': number_format(y_a_j_sum),
        'y_j_per': y_a_j_sum/y_b_j_sum * 100,
        # 서리재
        'd_b_s_sum': number_format(d_b_s_sum),
        'd_a_s_sum': number_format(d_a_s_sum),
        'd_s_per': d_a_s_sum/d_b_s_sum * 100,
        'm_b_s_sum': number_format(m_b_s_sum),
        'm_a_s_sum': number_format(m_a_s_sum),
        'm_s_per': m_a_s_sum/m_b_s_sum * 100,
        'y_b_s_sum': number_format(y_b_s_sum),
        'y_a_s_sum': number_format(y_a_s_sum),
        'y_s_per': y_a_s_sum/y_b_s_sum * 100,
        # 호우섬
        'd_b_h_sum': number_format(d_b_h_sum),
        'd_a_h_sum': number_format(d_a_h_sum),
        'd_h_per': d_a_h_sum/d_b_h_sum * 100,
        'm_b_h_sum': number_format(m_b_h_sum),
        'm_a_h_sum': number_format(m_a_h_sum),
        'm_h_per': m_a_h_sum/m_b_h_sum * 100,
        'y_b_h_sum': number_format(y_b_h_sum),
        'y_a_h_sum': number_format(y_a_h_sum),
        'y_h_per': y_a_h_sum/y_b_h_sum * 100,
        # 일식
        'd_b_i_sum': number_format(d_b_i_sum),
        'd_a_i_sum': number_format(d_a_i_sum),
        'd_i_per': d_a_i_sum/d_b_i_sum * 100,
        'm_b_i_sum': number_format(m_b_i_sum),
        'm_a_i_sum': number_format(m_a_i_sum),
        'm_i_per': m_a_i_sum/m_b_i_sum * 100,
        'y_b_i_sum': number_format(y_b_i_sum),
        'y_a_i_sum': number_format(y_a_i_sum),
        'y_i_per': y_a_i_sum/y_b_i_sum * 100,
        # 외식합계
        'd_b_d_sum': number_format(d_b_d_sum),
        'd_a_d_sum': number_format(d_a_d_sum),
        'd_d_per': d_a_d_sum/d_b_d_sum * 100,
        'm_b_d_sum': number_format(m_b_d_sum),
        'm_a_d_sum': number_format(m_a_d_sum),
        'm_d_per': m_a_d_sum/m_b_d_sum * 100,
        'y_b_d_sum': number_format(y_b_d_sum),
        'y_a_d_sum': number_format(y_a_d_sum),
        'y_d_per': y_a_d_sum/y_b_d_sum * 100,
    }
    
    return render(request, 'report_dinning.html', values)

