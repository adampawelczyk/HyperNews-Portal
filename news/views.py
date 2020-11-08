from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
import json
from datetime import datetime
import itertools
import random


news = []


def load_json_file():
    global news
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news = json.load(json_file)


def dump_json_file():
    with open(settings.NEWS_JSON_PATH, 'r+') as json_file:
        json.dump(news, json_file)


def simple_date_fun(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")


def sort_news(news):
    news.sort(key=lambda x: datetime.strptime(x['created'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    sorted_news = [{'date': date, 'values': list(news)} for date, news in
                   itertools.groupby(news, lambda x: simple_date_fun(x['created']))]
    return sorted_news


def search_news(phrase):
    searched_news = []
    for i in news:
        if phrase in i.get("title"):
            searched_news.append(i)
    return searched_news


class MainView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('q')
        load_json_file()
        sorted_news = sort_news(news)
        context = {"news": sorted_news}
        if search:
            searched_news = search_news(search)
            sorted_searched_news = sort_news(searched_news)
            context["news"] = sorted_searched_news
        return render(request, "news/index.html", context=context)


class NewsView(View):
    def get(self, request, post_id, *args, **kwargs):
        load_json_file()
        context = {"news": news, "link": post_id}
        return render(request, "news/news.html", context=context)


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):
        news_title = request.POST.get('title')
        news_text = request.POST.get('text')
        load_json_file()
        news.append({"created": str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')), "text": news_text,
                     "title": news_title, "link": int(str.zfill(str(random.randint(000000000, 999999999)), 9))})
        dump_json_file()
        return redirect('/news/')
