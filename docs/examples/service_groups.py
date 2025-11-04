from scm.client import Scm

# Initialize client
client = Scm(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Access service groups directly through the client
# No need to initialize a separate ServiceGroup object

# Basic service group configuration
basic_group = {
    "name": "web-services",
    "members": ["HTTP", "HTTPS"],
    "folder": "Texas",
    "tag": ["Web"],
}

# Create basic group using the client
basic_group_obj = client.service_group.create(basic_group)

# Extended service group configuration
extended_group = {
    "name": "app-services",
    "members": ["HTTP", "HTTPS", "SSH", "FTP"],
    "folder": "Texas",
    "tag": ["Application", "Production"],
}

# Create extended group
extended_group_obj = client.service_group.create(extended_group)

# Fetch by name and folder
group = client.service_group.fetch(name="web-services", folder="Texas")
print(f"Found group: {group.name}")

# Get by ID
group_by_id = client.service_group.get(group.id)
print(f"Retrieved group: {group_by_id.name}")
print(f"Members: {', '.join(group_by_id.members)}")

# Fetch existing group
existing_group = client.service_group.fetch(name="web-services", folder="Texas")

# Update members
existing_group.members = ["HTTP", "HTTPS", "HTTP-8080"]
existing_group.tag = ["Web", "Updated"]

# Perform update
updated_group = client.service_group.update(existing_group)

# List with direct filter parameters
filtered_groups = client.service_group.list(
    folder="Texas", values=["HTTP", "HTTPS"], tags=["Production"]
)

# Process results
for group in filtered_groups:
    print(f"Name: {group.name}")
    print(f"Members: {', '.join(group.members)}")

# Define filter parameters as dictionary
list_params = {"folder": "Texas", "values": ["SSH", "FTP"], "tags": ["Application"]}

# List with filters as kwargs
filtered_groups = client.service_group.list(**list_params)

# Only return service_groups defined exactly in 'Texas'
exact_service_groups = service_groups.list(folder="Texas", exact_match=True)

for app in exact_service_groups:
    print(f"Exact match: {app.name} in {app.folder}")

# Exclude all service_groups from the 'All' folder
no_all_service_groups = service_groups.list(folder="Texas", exclude_folders=["All"])

for app in no_all_service_groups:
    assert app.folder != "All"
    print(f"Filtered out 'All': {app.name}")

# Exclude service_groups that come from 'default' snippet
no_default_snippet = service_groups.list(folder="Texas", exclude_snippets=["default"])

for app in no_default_snippet:
    assert app.snippet != "default"
    print(f"Filtered out 'default' snippet: {app.name}")

# Exclude service_groups associated with 'DeviceA'
no_deviceA = service_groups.list(folder="Texas", exclude_devices=["DeviceA"])

for app in no_deviceA:
    assert app.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {app.name}")

# Combine exact_match with multiple exclusions
combined_filters = service_groups.list(
    folder="Texas",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
)

for app in combined_filters:
    print(f"Combined filters result: {app.name} in {app.folder}")

# Initialize the client with a custom max_limit for service groups
# This will retrieve up to 4321 objects per API call, up to the API limit of 5000.
client = Scm(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id",
    service_group_max_limit=4321,
)

# Now when we call list(), it will use the specified max_limit for each request
# while auto-paginating through all available objects.
all_groups = client.service_group.list(folder="Texas")

# 'all_groups' contains all objects from 'Texas', fetched in chunks of up to 4321 at a time.

# Delete by ID
group_id = "123e4567-e89b-12d3-a456-426655440000"
client.service_group.delete(group_id)

# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Updated service groups",
    "sync": True,
    "timeout": 300,  # 5 minute timeout
}

# Commit the changes directly using the client
result = client.commit(**commit_params)

print(f"Commit job ID: {result.job_id}")

# Get status of specific job using the client
job_status = client.get_job_status(result.job_id)
print(f"Job status: {job_status.data[0].status_str}")

# List recent jobs using the client
recent_jobs = client.list_jobs(limit=10)
for job in recent_jobs.data:
    print(f"Job {job.id}: {job.type_str} - {job.status_str}")

from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
    ReferenceNotZeroError,
)

try:
    # Create group configuration
    group_config = {
        "name": "test-group",
        "members": ["HTTP", "HTTPS"],
        "folder": "Texas",
        "tag": ["Test"],
    }

    # Create the group using the client
    new_group = client.service_group.create(group_config)

    # Commit changes using the client
    result = client.commit(folders=["Texas"], description="Added test group", sync=True)

    # Check job status using the client
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

from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
    ReferenceNotZeroError,
)

try:
    # Create group configuration
    group_config = {
        "name": "test-group",
        "members": ["HTTP", "HTTPS"],
        "folder": "Texas",
        "tag": ["Test"],
    }

    # Create the group using the client
    new_group = client.service_group.create(group_config)

    # Commit changes using the client
    result = client.commit(folders=["Texas"], description="Added test group", sync=True)

    # Check job status using the client
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
