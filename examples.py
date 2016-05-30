from utils import utils, keystoneutils, novautils


# Create a parser and parse the args and/or the environment variables.
p = utils.get_parser()
args = p.parse_args()



# Create a keystone client from the args and run supported operations.
kc = keystoneutils.get_client(args)

# List all projects.
print kc.projects.list()
# Show details of a project.
print kc.projects.get(kc.projects.list()[0].id)
# Create a project.
print kc.projects.create('my_project', 'default',
                         description='This is my_project.')
# List all users with admin roles.
print kc.role_assignments.list(role=kc.roles.list(name='admin')[0].id)



# Create a nova client and run supported operations.
nc = novautils.get_client(kc.session)
#            OR
# session = keystoneutils.get_session(args)
# nc = novautils.get_client()

# List all instances. Like `nova list --all-tenants`.
print nc.servers.list(search_opts={'all_tenants': 1})
# List all flavors.
print nc.flavors.list()
# Print hypervisor stats.
print nc.hypervisor_stats.statistics().__dict__
# Create an instance. flavor_id == 3
print nc.servers.create('my_instance', nc.images.list()[0].id, 3)
