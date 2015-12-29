# Create your views here.

from django.conf import settings
from django.http import HttpResponse

from qatrack.qa.views.charts import ChartView
from qatrack.qa import models
from qatrack.units import models as unitmodels

import os
import json
from collections import defaultdict

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


def get_unitlist(request):
    """Return all machines and their UnitTestCollections."""

    # Get the UTCs and their respective unit ids
    unitlist = models.UnitTestCollection.objects.filter(
        pk__in=settings.PBS_DAILY_QA_UTC_IDS).values_list("unit_id", "id")
    units = defaultdict(list)

    # Create a mapping of units to UTCs
    for k, v in unitlist:
        units[k].append(v)
    units = dict(units)

    # Get the name of each unit
    unitnames = dict(unitmodels.Unit.objects.filter(
        pk__in=units.keys()).values_list("id", "name"))

    # Get the mapping for the spot position upload test to the UnitTestInfo id
    spotposlist = dict(models.UnitTestInfo.objects.filter(
        test_id__in=[settings.PBS_DAILY_QA_SPOTFILE_TEST_ID],
        unit_id__in=units.keys()
    ).values_list("unit_id", "id"))
    print(spotposlist)

    # Add the additional information to each unit
    for unit, utc in units.items():
        units[unit] = {'utc': utc,
                       'name': unitnames[unit],
                       'spot_uti': spotposlist[unit]}
    print(units)

    json_context = json.dumps({'units': units})

    return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)


def get_testlistinstancelist(request):
    """Return all TestListInstances for the given UnitTestCollection."""

    test_list_instances = models.TestListInstance.objects.filter(
        unit_test_collection__id__in=settings.PBS_DAILY_QA_UTC_IDS
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
    """Return a PNG plot of the requested PBS Daily QA data."""

    # Get the primary key for the test instance and obtain the filenames
    pk = get_value_from_request(request, 'id', 0)
    tests = models.TestInstance.objects.filter(
        test_list_instance_id=pk
    ).values('string_value', 'unit_test_info_id')

    # Determine the spot filename
    spotfilename = [t['string_value'] for t in tests
                    if t['unit_test_info_id'] ==
                    settings.PBS_DAILY_QA_SPOTFILE_TEST_ID]

    # Return if the test list is empty or the spot filename is invalid
    if not len(tests) or not len(spotfilename):
        json_context = "No data found for id: " + str(pk)
        return HttpResponse(json_context, content_type=JSON_CONTENT_TYPE)
    else:
        # Initialize the PBS Daily QA analysis with the spot file

        spot = os.path.join(settings.UPLOAD_ROOT, str(pk), spotfilename[0])
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
