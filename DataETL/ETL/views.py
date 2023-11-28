__author__ = "reed@reedjones.me"

from django.shortcuts import render

from .DataService import AwMainService
import logging

logger = logging.getLogger("django")


def make_chart(request):
    a = AwMainService()
    if request.method == "POST":
        logger.debug("post")
        form = a.get_chart_form(request.POST)
        if form.is_valid():
            logger.debug("valid")
            chart = a.make_chart(form, title="")
            c = a.field_distinct_counts(form.cleaned_data["filter_by"])
            stats = []
            stats.append({"name": form.cleaned_data["measure"], "count": c})

            desc = a.get_chart_description(form)
            chart["description"] = desc
            charts = [chart]
            context = {"charts": charts, "stats": stats}
            return render(request, "admin_core/chart_snip.html", context)
    else:
        form = a.get_chart_form()
    return render(request, "admin_core/chart_form.html", {"form": form})
