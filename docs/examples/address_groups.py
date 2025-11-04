from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Static group configuration
static_config = {
    "name": "web_servers",
    "static": ["web-server1", "web-server2"],
    "description": "Web server group",
    "folder": "Texas",
    "tag": ["Production", "Web"],
}

# Create static group using the unified client interface
static_group = client.address_group.create(static_config)

# Dynamic group configuration
dynamic_config = {
    "name": "python_servers",
    "dynamic": {"filter": "'Python' and 'Production'"},
    "description": "Python production servers",
    "folder": "Texas",
    "tag": ["Automation"],
}

# Create dynamic group using the unified client interface
dynamic_group = client.address_group.create(dynamic_config)

# Fetch by name and folder using the unified client interface
group = client.address_group.fetch(name="web_servers", folder="Texas")
print(f"Found group: {group.name}")

# Get by ID using the unified client interface
group_by_id = client.address_group.get(group.id)
print(f"Retrieved group: {group_by_id.name}")

# Fetch existing group using the unified client interface
existing_group = client.address_group.fetch(name="web_servers", folder="Texas")

# Update static members
existing_group.static = ["web-server1", "web-server2", "web-server3"]
existing_group.description = "Updated web server group"
existing_group.tag = ["Production", "Web", "Updated"]

# Perform update using the unified client interface
updated_group = client.address_group.update(existing_group)

# List with direct filter parameters using the unified client interface
filtered_groups = client.address_group.list(
    folder="Texas", types=["static"], tags=["Production"]
)

# Process results
for group in filtered_groups:
    print(f"Name: {group.name}")
    if group.static:
        print(f"Members: {', '.join(group.static)}")
    elif group.dynamic:
        print(f"Filter: {group.dynamic.filter}")

# Define filter parameters as dictionary
list_params = {"folder": "Texas", "types": ["dynamic"], "tags": ["Automation"]}

# List with filters as kwargs using the unified client interface
filtered_groups = client.address_group.list(**list_params)

# Only return address groups defined exactly in 'Texas'
exact_address_groups = client.address_group.list(folder="Texas", exact_match=True)

for each in exact_address_groups:
    print(f"Exact match: {each.name} in {each.folder}")

# Exclude all address groups from the 'All' folder
no_all_address_groups = client.address_group.list(
    folder="Texas", exclude_folders=["All"]
)

for each in no_all_address_groups:
    assert each.folder != "All"
    print(f"Filtered out 'All': {each.name}")

# Exclude address groups that come from 'default' snippet
no_default_snippet = client.address_group.list(
    folder="Texas", exclude_snippets=["default"]
)

for addr in no_default_snippet:
    assert addr.snippet != "default"
    print(f"Filtered out 'default' snippet: {addr.name}")

# Exclude address groups associated with 'DeviceA'
no_deviceA = client.address_group.list(folder="Texas", exclude_devices=["DeviceA"])

for each in no_deviceA:
    assert each.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {each.name}")

# Combine exact_match with multiple exclusions
combined_filters = client.address_group.list(
    folder="Texas",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
)

for each in combined_filters:
    print(f"Combined filters result: {each.name} in {each.folder}")


from scm.client import ScmClient
from scm.config.objects import AddressGroup

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Two options for setting max_limit:

# Option 1: Use the unified client interface but create a custom AddressGroup instance with max_limit
address_group_service = AddressGroup(client, max_limit=4321)
all_groups1 = address_group_service.list(folder="Texas")

# Option 2 (traditional approach): Create a dedicated AddressGroup instance
# This will retrieve up to 4321 objects per API call, up to the API limit of 5000.
all_groups2 = client.address_group.list(folder="Texas")

# Both options will auto-paginate through all available objects.
# 'all_groups' contains all objects from 'Texas', fetched in chunks according to the max_limit.

# Delete by ID using the unified client interface
group_id = "123e4567-e89b-12d3-a456-426655440000"
client.address_group.delete(group_id)

# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Updated address groups",
    "sync": True,
    "timeout": 300,  # 5 minute timeout
}

# Commit the changes directly using the client
# Note: Commits should always be performed on the client object directly, not on service objects
result = client.commit(**commit_params)

print(f"Commit job ID: {result.job_id}")

# Get status of specific job directly from the client
job_status = client.get_job_status(result.job_id)
print(f"Job status: {job_status.data[0].status_str}")

# List recent jobs directly from the client
recent_jobs = client.list_jobs(limit=10)
for job in recent_jobs.data:
    print(f"Job {job.id}: {job.type_str} - {job.status_str}")


from scm.client import ScmClient
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
    ReferenceNotZeroError,
)

# Initialize client using ScmClient
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

try:
    # Create group configuration
    group_config = {
        "name": "test_group",
        "static": ["server1", "server2"],
        "folder": "Texas",
        "description": "Test server group",
        "tag": ["Test"],
    }

    # Create the group using the unified client interface
    new_group = client.address_group.create(group_config)

    # Commit changes directly from the client
    result = client.commit(folders=["Texas"], description="Added test group", sync=True)

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid group data: {e.message}")
except NameNotUniqueError as e:
    print(f"Group name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"Group not found: {e.message}")
except ReferenceNotZeroError as e:
    print(f"Group still in use: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
