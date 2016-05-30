# openstackclient

A small library to simplify the authentication of various openstack clients
with keystone.

### Usage

Source your credentials file (`*openrc.sh`) before running the scripts.

**OR**

Write your script using the parser from `utils.utils.get_parser()` and parse
the credentials from the commandline.


Examples are given in [`examples.py`](https://github.com/safiyat/openstackclient/blob/master/examples.py).
