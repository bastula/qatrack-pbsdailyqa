# Create your views here.

from django.conf import settings
from django.http import HttpResponse

from qatrack.qa.views.charts import ChartView
from qatrack.qa import models

import os
import json

from tzlocal import get_localzone
dtformat = "%Y-%m-%d"
localformat = "%Y-%m-%d %H:%M:%S"

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import analysis

JSON_CONTENT_TYPE = "application/json"


class PBSDailyQAReview(ChartView):
    """A simple view wrapper to filter by :model:`units.Unit`"""

    permission_required = "qa.can_view_charts"
    raise_exception = True

    template_name = "pbsdailyqa.html"

    def get_page_title(self):
        return "Review PBS Daily QA"


def get_testlistinstancelist(request):
    """Return all TestListInstances for the given UnitTestCollection."""

    test_list_instances = models.TestListInstance.objects.filter(
        unit_test_collection=4
    ).values("id", "work_completed")

    datedict = {}
    for x in test_list_instances:
        date = x['work_completed'].astimezone(
            get_localzone()).strftime(dtformat)
        x.update({'work_completed': x['work_completed'].astimezone(
            get_localzone()).strftime(localformat)})
        if date in datedict:
            datedict[date].append(x)
        else:
            datedict[date] = [x]

    json_context = json.dumps(
        {"test_list_instances": datedict})

    return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)


def get_testlistinstance(request, pk):
    """Return the tests that are part of the requested TestListInstance."""

    tests = models.TestInstance.objects.filter(
        test_list_instance_id=pk
    ).values('string_value', 'unit_test_info_id')

    json_context = json.dumps(
        {"tests": list(tests)})

    return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)


def get_value_from_request(request, param, default, dtype=int):
    """Look for a value in GET and convert it to the given datatype."""
    try:
        v = dtype(request.GET.get(param, default))
    except:
        v = default
    return v


def get_plot(request):
    """Return a SVG plot of the requested PBS Daily QA data."""

    # Get the primary key for the test instance and obtain the filenames
    pk = get_value_from_request(request, 'id', 0)
    tests = models.TestInstance.objects.filter(
        test_list_instance_id=pk
    ).values('string_value', 'unit_test_info_id')

    # Return the test list is empty
    if not len(tests):
        json_context = "No data found for id: " + str(pk)
        return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)
    else:
        # Initialize the PBS Daily QA analysis with the spot file
        spotfilename = [t['string_value'] for t in tests][0]
        spot = os.path.join(settings.UPLOAD_ROOT, str(pk), spotfilename)
        spots, spotdata = analysis.read_file(spot)

        # Get the plot parameters from the request
        axis = get_value_from_request(request, 'axis', 'x', str)
        plot_type = get_value_from_request(
            request, 'plot_type', 'profile', str)
        annotations = get_value_from_request(
            request, 'annotations', 'position', str)

        # Check if parameters are valid
        if (axis not in ['x', 'y']) or \
           (annotations not in ['position', 'size']) or \
           (plot_type not in ['profile', 'spot']):

            error_msg = {'Invalid parameters': {
                         'plot_type': plot_type,
                         'annotations': annotations,
                         'axis': axis},
                         'Allowable parameters': {
                         'plot_type': ['profile', 'spot'],
                         'annotations': ['position', 'size'],
                         'axis': ['x', 'y']}}
            json_context = json.dumps(error_msg)
            return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)

        # Return the requested plot image
        fig = analysis.plot_data(
            spotdata,
            plot_type=plot_type,
            annotations=annotations,
            axis=axis)
        canvas = FigureCanvas(fig)
        # response = HttpResponse(content_type='image/svg+xml')
        # fig.savefig(response, format="svg")
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response

    return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)
