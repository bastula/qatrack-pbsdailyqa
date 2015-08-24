=====
PBS Daily QA
=====

PBS Daily QA is a Django app to review and analyze
Proton Pencil Beam Scanning (PBS) Daily QA.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "pbsdailyqa" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'pbsdailyqa',
    )

2. Include the pbsdailyqa URLconf in your project urls.py like this::


    url(r'^pbsdailyqa/', include('pbsdailyqa.urls')),

3. Start the development server.

4. Visit http://127.0.0.1:8000/pbsdailyqa/ to review PBS Daily QA.
