from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from bs4 import BeautifulSoup
import requests

class GetStats(APIView):

    def get(self, request):
        countries = self.request.query_params.get('countries', '')
        if not countries:
            return Response({'result':"Please Enter a Country"})
        content = requests.get('https://www.worldometers.info/coronavirus/').text
        soup = BeautifulSoup(content, "lxml")
        covid_table = soup.find("table", attrs={"id": "main_table_countries_today"})
        body = covid_table.tbody.find_all("tr")
        data_dict = {}
        for i in range(8, len(body)):
            row = body[i].find_all("td")
            data_dict[row[1].text.replace("\n", "").strip()] = {'country':row[1].text.replace("\n", "").strip(), 'total':row[2].text.replace(",", ""),\
                'death': row[4].text.replace(",", ""), 'active': row[8].text.replace(",", ""), \
                'recoverd': row[6].text.replace(",", ""), 'population':row[14].text.replace(",", "")}
            
        result = []
        for country in countries.split(', '):
            result_dict = {}
            result_dict['Country'] = data_dict[country]['country']
            result_dict['Total'] = data_dict[country]['total']
            result_dict['Deaths'] = data_dict[country]['death']
            result_dict['Active'] = data_dict[country]['active']
            try:
                result_dict['RecoveryRate'] = str(int(data_dict[country]['recoverd'])/int(data_dict[country]['total']))
            except:
                result_dict['RecoveryRate'] = 'insufficient data'
            try:    
                result_dict['PPInfected'] = str(int(data_dict[country]['total'])/int(data_dict[country]['population']))
            except:
                result_dict['PPInfected'] = 'insufficient data'
            result.append(result_dict)
        return Response({'result':result})




