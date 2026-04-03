wdatabricks Documentation
=========================

|Version| |License| |Python|

wdatabricks is a Python library that provides a high-level interface for Databricks operations.
It simplifies working with Databricks workspaces, clusters, and jobs.

.. |Version| image:: https://img.shields.io/pypi/v/wdatabricks.svg
   :target: https://pypi.org/project/wdatabricks/
   :alt: PyPI Version

.. |License| image:: https://img.shields.io/pypi/l/wdatabricks.svg
   :target: https://pypi.org/project/wdatabricks/
   :alt: License

.. |Python| image:: https://img.shields.io/pypi/pyversions/wdatabricks.svg
   :target: https://pypi.org/project/wdatabricks/
   :alt: Python Versions

Quick Start
-----------

.. code-block:: bash

   pip install wdatabricks

.. code-block:: python

   from wdatabricks import Databricks

   dbx = Databricks(host="https://community.cloud.databricks.com", token="your-token")
   clusters = dbx.list_clusters()

Key Capabilities
----------------

- **Cluster Management** - Create, manage, and monitor clusters
- **Job Scheduling** - Schedule and manage Databricks jobs
- **SQL warehouses** - Manage SQL warehouses
- **Workspace Operations** - Manage workspace objects
- **MLflow Integration** - Built-in MLflow support

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started/index
   api_reference/index
   tutorials/index
   faq
   glossary

.. toctree::
   :maxdepth: 1
   :caption: Additional

   License <license>
   bibliography

.. toctree::
   :maxdepth: 1
   :caption: External Links

   GitHub <https://github.com/wisrovi/wdatabricks>
   PyPI <https://pypi.org/project/wdatabricks/>
   LinkedIn <https://www.linkedin.com/in/william-steve-rodriguez-villamizar>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`