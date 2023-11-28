__author__ = "reed@reedjones.me"


if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aw.settings.reed")
    os.environ["DJANGO_SETTINGS_MODULE"] = "aw.settings.reed"
    # settings.configure()
    import django

    django.setup()

    from DataETL.ETL.DataService import demo

    demo()
