import datetime
from sites.models import Site, TmpContent
# from django.contrib.auth.models import User
from requests_html import HTMLSession
from sites.tass_req import get_news_tuple, get_content


def get_available_sites(user=None):
    #return Site.objects.all()
    return ['https://tass.ru/ekonomika', ]


def get_site_content(site_url, need_urls=True):
    if need_urls:
        if 'tass' in site_url:
            return get_news_tuple(site_url)
    abstract, main_text = get_content(site_url)
    return main_text


def save_results(site, topic, content):
    if not TmpContent.objects.filter(link=topic[1]).first():
        TmpContent.objects.create(
            target_site=site,
            link=topic[1],
            title=topic[0],
            body=content
        )


def main_circle():
    t1 = datetime.datetime.now()
    target_site = get_available_sites() #  User.objects.last())
    for site in target_site:
        site_topics = get_site_content(site, need_urls=True)
        for topic in site_topics:
            content = get_site_content(topic[1], need_urls=False)
            save_results(site, topic, content)
    print("{}".format((datetime.datetime.now() - t1)))


def run_parser():
    main_circle()

if __name__ == '__main__':
    run_parser()
