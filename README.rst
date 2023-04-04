DRIPS
============================


Links
-----

+--------------------+----------------+--------------+--------------------+
| Stable             |                | |master-cov| |                    |
+--------------------+----------------+--------------+--------------------+
| Development        |                | |dev-cov|    |                    |
+--------------------+----------------+--------------+--------------------+
| Source Code        |https://github.com/unicef/drips                     |
+--------------------+----------------+-----------------------------------+
| Issue tracker      |https://unicef.visualstudio.com/SCS-Drips/          |
+--------------------+----------------+-----------------------------------+


.. |master-cov| image:: https://circleci.com/gh/unicef/drips/tree/master.svg?style=svg
                    :target: https://circleci.com/gh/unicef/aaa/tree/master


.. |dev-cov| image:: https://circleci.com/gh/unicef/drips/tree/develop.svg?style=svg
                    :target: https://circleci.com/gh/unicef/aaa/tree/develop





Troubleshoot
--------------------
*  Exception are logged in Sentry: https://excubo.unicef.io/sentry/
*  Each container in devops allows to access local logs


Get Started
--------------------
* populate your .env file from template .env_template
* python manage.py init_setup --all


Development Release
--------------------
init version
* update requirements (sys - python)
* `make build-base`

develop features
* develop features
* `make build release`

finish version
* `git flow release start`
* update CHANGES
* update version (__init__.py)
* update makefile version
