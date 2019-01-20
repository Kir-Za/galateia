import multiprocessing as mp

from django.conf import settings

from sites.models import Site, TmpContent
from sites.tass_req import tass_circle


def get_available_sites():
    return [site.target_urls for site in Site.objects.filter(is_active=True)]


def save_results(results):
    for part in results:
        for result in part:
            if not TmpContent.objects.filter(link=result['news_link']).first():
                TmpContent.objects.create(
                    target_site=result['target'],
                    link=result['news_link'],
                    title=result['news_title'],
                    abstract=result['abstract'],
                    body=result['main_text']
                )


def run_parser():
    tass_pool = []
    process_pool = mp.Pool(processes=settings.PROCESS_AMOUNT)
    for site in get_available_sites():
        if 'tass' in site:
            tass_pool.append(site)
    results = [process_pool.apply_async(tass_circle, args=(site, )) for site in tass_pool]
    clean_data = [i.get() for i in results]
    save_results(clean_data)
    process_pool.close()
    process_pool.join()
