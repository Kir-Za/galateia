from celery import shared_task

from sites.task_modules import RenderAndSave


@shared_task
def site_parser():
    inst = RenderAndSave()
    return inst.run_parser()
