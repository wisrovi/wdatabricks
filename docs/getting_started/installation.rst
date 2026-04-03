Installation
============

Requirements
------------

* Python 3.8+
* Databricks account with SQL warehouse access

Install via pip
---------------

.. code-block:: bash

    pip install wdatabricks

Install with development dependencies
-------------------------------------

.. code-block:: bash

    pip install wdatabricks[dev]

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/wisrovi/wdatabricks.git
    cd wdatabricks
    pip install -e .

Dependencies
~~~~~~~~~~~~

Required dependencies:

* ``databricks-sql-connector>=2.0.0`` - Databricks SQL connector for Python

Optional dependencies:

* ``pytest>=7.0.0`` - Testing framework
* ``pytest-cov>=4.0.0`` - Coverage plugin
* ``black>=23.0.0`` - Code formatter
* ``mypy>=1.0.0`` - Type checker