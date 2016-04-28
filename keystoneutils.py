from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client

auth = v3.Password(auth_url='http://controller:35357/v3', password='snapdeal@1234', username='osadmin', user_domain_id='default', project_name='admin', project_domain_id='default')

sess = session.Session(auth=auth)

keystone = client.Client(session=sess)
