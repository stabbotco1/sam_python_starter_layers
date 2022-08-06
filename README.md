# sam-python-relative-imports

## Python Relative Imports

##### This project shows how to setup a sam project that implements relative imports using Python Modules.

##### This is to b used when absolute imports are not justified.
<br>
[https://binx.io/2021/10/25/python-and-relative-imports-in-aws-lambda-functions/](https://binx.io/2021/10/25/python-and-relative-imports-in-aws-lambda-functions/)
<br>
## Layer Creation

##### rm -rf libs/python
pip freeze \| xargs pip uninstall \-y
pip install -r requirements.txt -t libs/python --upgrade