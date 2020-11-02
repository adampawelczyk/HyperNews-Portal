from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import json
from datetime import datetime
import itertools


class MainView(View):
    def simple_date_fun(self, date):
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news = json.load(json_file)
        news.sort(key=lambda x: datetime.strptime(x['created'], "%Y-%m-%d %H:%M:%S"), reverse=True)
        sorted_news = [{'date': date, 'values': list(news)} for date, news in itertools.groupby(news, lambda x: self.simple_date_fun(x['created']))]
        context = {"news": sorted_news}
        return render(request, "news/index.html", context=context)



class NewsView(View):
    def get(self, request, post_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news = json.load(json_file)
        context = {"news": news, "link": post_id}
        return render(request, "news/news.html", context=context)