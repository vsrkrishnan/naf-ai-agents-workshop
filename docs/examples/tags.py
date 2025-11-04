from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Basic tag configuration
basic_tag = {
    "name": "Production",
    "color": "Red",
    "comments": "Production environment resources",
    "folder": "Texas",
}

# Create basic tag using the unified client interface
basic_tag_obj = client.tag.create(basic_tag)

# Tag with different color
dev_tag = {
    "name": "Development",
    "color": "Blue",
    "comments": "Development environment resources",
    "folder": "Texas",
}

dev_tag_obj = client.tag.create(dev_tag)

# Tag for a specific application
app_tag = {
    "name": "Web-Servers",
    "color": "Green",
    "comments": "Web server resources",
    "folder": "Texas",
}

app_tag_obj = client.tag.create(app_tag)

# Fetch by name and folder using the unified client interface
tag = client.tag.fetch(name="Production", folder="Texas")
print(f"Found tag: {tag.name}")
print(f"Color: {tag.color}")

# Get by ID using the unified client interface
tag_by_id = client.tag.get(tag.id)
print(f"Retrieved tag: {tag_by_id.name}")

# Fetch existing tag using the unified client interface
existing_tag = client.tag.fetch(name="Production", folder="Texas")

# Update attributes
existing_tag.color = "Azure Blue"
existing_tag.comments = "Updated production environment tag"

# Perform update using the unified client interface
updated_tag = client.tag.update(existing_tag)

# List tags from a specific folder using the unified client interface
filtered_tags = client.tag.list(folder="Texas")

# Apply color filters using the unified client interface
filtered_tags = client.tag.list(folder="Texas", colors=["Red", "Blue"])

for tag in filtered_tags:
    print(f"Name: {tag.name}, Color: {tag.color}")

from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Only return tags defined exactly in 'Texas' using the unified client interface
exact_tags = client.tag.list(folder="Texas", exact_match=True)

for tag in exact_tags:
    print(f"Exact match: {tag.name} in {tag.folder}")

# Exclude all tags from the 'All' folder using the unified client interface
no_all_tags = client.tag.list(folder="Texas", exclude_folders=["All"])

for tag in no_all_tags:
    assert tag.folder != "All"
    print(f"Filtered out 'All': {tag.name}")

# Exclude tags that come from 'default' snippet using the unified client interface
no_default_snippet = client.tag.list(folder="Texas", exclude_snippets=["default"])

for tag in no_default_snippet:
    assert tag.snippet != "default"
    print(f"Filtered out 'default' snippet: {tag.name}")

# Exclude tags associated with 'DeviceA' using the unified client interface
no_deviceA = client.tag.list(folder="Texas", exclude_devices=["DeviceA"])

for tag in no_deviceA:
    assert tag.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {tag.name}")

# Combine exact_match with multiple exclusions and colors using the unified client interface
refined_tags = client.tag.list(
    folder="Texas",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
    colors=["Red", "Blue"],
)

for tag in refined_tags:
    print(f"Refined filter result: {tag.name} in {tag.folder}, Color: {tag.color}")

from scm.client import ScmClient
from scm.config.objects import Tag

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Two options for setting max_limit:

# Option 1: Use the unified client interface but create a custom Tag instance with max_limit
tag_service = Tag(client, max_limit=4321)
all_tags1 = tag_service.list(folder="Texas")

# Option 2: Use the unified client interface directly
# This will use the default max_limit (2500)
all_tags2 = client.tag.list(folder="Texas")

# Both options will auto-paginate through all available objects.
# The tags are fetched in chunks according to the max_limit.

# Delete by ID using the unified client interface
tag_id = "123e4567-e89b-12d3-a456-426655440000"
client.tag.delete(tag_id)

# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Updated tag definitions",
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

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

try:
    # Create tag configuration
    tag_config = {
        "name": "test_tag",
        "color": "Red",
        "folder": "Texas",
        "comments": "Test tag",
    }

    # Create the tag using the unified client interface
    new_tag = client.tag.create(tag_config)

    # Commit changes directly from the client
    result = client.commit(folders=["Texas"], description="Added test tag", sync=True)

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid tag data: {e.message}")
except NameNotUniqueError as e:
    print(f"Tag name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"Tag not found: {e.message}")
except ReferenceNotZeroError as e:
    print(f"Tag still in use: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
