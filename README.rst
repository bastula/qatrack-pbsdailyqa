============
PBS Daily QA
============

PBS Daily QA is a Django app for QATrack+ to review and analyze Proton Pencil Beam Scanning (PBS) Daily QA.

Required files:
---------------

* A file upload test in QATrack+ that is used to store ASCII OPG files exported from OmniPro IMRT.

Required modules:
-----------------

The code has been tested on Python 2 and requires the following modules:

* `QATrack+ <http://bitbucket.org/tohccmedphys/qatrackplus>`_ - Web application for radiation therapy QA
* `numpy <http://www.numpy.org>`_ - used to process the data
* `scipy <http://www.scipy.org>`_ - used to interpolate the values for Full Width Half Max
* `pandas <http://pandas.pydata.org>`_ - used to read the OPG dose grid
* `matplotlib <http://matplotlib.org>`_ - used to generate plots

Quick start
-----------

1. Add "pbsdailyqa" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'pbsdailyqa',
    )

2. Include the pbsdailyqa URLconf in your project urls.py like this::


    url(r'^pbsdailyqa/', include('pbsdailyqa.urls')),

3. Add the following settings to your local_settings.py like this::

    PBS_DAILY_QA_UTC_IDS = [6, 7]
    PBS_DAILY_QA_SPOTFILE_TEST_ID = 399

These ID values are specific to your clinic's UTC and test IDs.

3. Start the development server.

4. Visit http://127.0.0.1:8000/pbsdailyqa/ to review PBS Daily QA.

5. Once you are in production, don't forget to copy the static files using::

    python manage.py collectstatic

Version History:
----------------
* 0.2 - Added support for multiple treatment units
* 0.1 - Initial Release
