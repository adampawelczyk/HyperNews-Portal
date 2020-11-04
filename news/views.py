from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
import json
from datetime import datetime
import itertools
import random


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


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news = json.load(json_file)
        news.append({"created": str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), "text": text, "title": title, "link": int(str.zfill(str(random.randint(000000000, 999999999)), 9))})
        with open(settings.NEWS_JSON_PATH, 'r+') as json_file:
            json.dump(news, json_file)
        return redirect('/news/')
