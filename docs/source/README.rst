Wave Data Generator
===================

Requirements
------------

-  Python version 3.6 installed locally. See the installation guides for
   `OS
   X <http://docs.python-guide.org/en/latest/starting/install3/osx/>`__,
   `Windows <http://docs.python-guide.org/en/latest/starting/install3/win/>`__,
   and
   `Linux <http://docs.python-guide.org/en/latest/starting/install3/linux/>`__.
-  Setuptools and Pip installed locally. See the Python install guides
   above for installation instructions.

On OS X, you can verify your system by running
``python3 --version; pip3 --version``.

While not required, it is recommended you have
`virtualenv <https://virtualenv.pypa.io/en/latest/>`__ installed locally
to avoid package conflicts. Accomplish this by running
``pip install virtualenv`` or ``pip3 install virtualenv`` on OS X.

Dependencies
~~~~~~~~~~~~

Install all dependencies by running:

::

    pip3 install -r requirements.txt


Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The following environment variables can be set to read and write files from AWS

-  **AWS_ACCESS_KEY_ID**: Your AWS Access Key ID.
-  **AWS_SECRET_ACCESS_KEY**: Your AWS Secret Access Key.
-  **S3_BUCKET_NAME**: The bucket name to read and write files from.
-  **READ_MODE**: Set to either S3 or LOCAL. If S3, all input files will be read from the AWS bucket specified.
-  **WRITE_MODE**: Set to either S3 or LOCAL. If S3, all output files will be written to the AWS bucket specified.

Locally, you can try:

::

    export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    export AWS_ACCESS_KEY_ID=<your-access-key-id>
    export S3_BUCKET_NAME=ac-sdo-repo-dev
    export READ_MODE=LOCAL
    export WRITE_MODE=S3

With those environment variables are set, you can run ``python3 sales_data_gen.py`` or
``python3 services_data_gen.py`` and it will read input files locally but write all output
files to S3.