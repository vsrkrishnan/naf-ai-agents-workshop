from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Prepare IP/Netmask address configuration
netmask_config = {
    "name": "internal_network",
    "ip_netmask": "192.168.1.0/24",
    "description": "Internal network segment",
    "folder": "Texas",
    "tag": ["Python", "Automation"],
}

# Create the address object using the unified client interface
netmask_address = client.address.create(netmask_config)

# Prepare FQDN address configuration
fqdn_config = {
    "name": "example_site",
    "fqdn": "example.com",
    "folder": "Texas",
    "description": "Example website",
}

# Create the FQDN address object
fqdn_address = client.address.create(fqdn_config)

# Prepare IP Range address configuration
range_config = {
    "name": "dhcp_pool",
    "ip_range": "192.168.1.100-192.168.1.200",
    "folder": "Texas",
    "description": "DHCP address pool",
}

# Create the IP Range address object
range_address = client.address.create(range_config)


# Fetch by name and folder
address = client.address.fetch(name="internal_network", folder="Texas")
print(f"Found address: {address.name}")

# Get by ID
address_by_id = client.address.get(address.id)
print(f"Retrieved address: {address_by_id.name}")


# Fetch existing address
existing_address = client.address.fetch(name="internal_network", folder="Texas")

# Update specific attributes
existing_address.description = "Updated network segment"
existing_address.tag = ["Network", "Internal", "Updated"]

# Perform update
updated_address = client.address.update(existing_address)

# Pass filters directly into the list method
filtered_addresses = client.address.list(
    folder="Texas", types=["fqdn"], tags=["Automation"]
)

# Process results
for addr in filtered_addresses:
    print(f"Name: {addr.name}, Value: {addr.fqdn}")

# Define filter parameters as a dictionary
list_params = {"folder": "Texas", "types": ["netmask"], "tags": ["Production"]}

# List addresses with filters as kwargs
filtered_addresses = client.address.list(**list_params)

# Process results
for addr in filtered_addresses:
    print(f"Name: {addr.name}, Value: {addr.ip_netmask}")

# Only return addresses defined exactly in 'Texas'
exact_addresses = client.address.list(folder="Texas", exact_match=True)

for addr in exact_addresses:
    print(f"Exact match: {addr.name} in {addr.folder}")

# Exclude all addresses from the 'All' folder
no_all_addresses = client.address.list(folder="Texas", exclude_folders=["All"])

for addr in no_all_addresses:
    assert addr.folder != "All"
    print(f"Filtered out 'All': {addr.name}")

    # Exclude addresses that come from 'default' snippet
    no_default_snippet = client.address.list(
        folder="Texas", exclude_snippets=["default"]
    )

for addr in no_default_snippet:
    assert addr.snippet != "default"
    print(f"Filtered out 'default' snippet: {addr.name}")

# Exclude addresses associated with 'DeviceA'
no_deviceA = client.address.list(folder="Texas", exclude_devices=["DeviceA"])

for addr in no_deviceA:
    assert addr.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {addr.name}")

# Combine exact_match with multiple exclusions
combined_filters = client.address.list(
    folder="Texas",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
)

for addr in combined_filters:
    print(f"Combined filters result: {addr.name} in {addr.folder}")

from scm.client import ScmClient
from scm.config.objects import Address

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Two options for setting max_limit:

# Option 1: Use the unified client interface but create a custom Address instance with max_limit
address_service = Address(client, max_limit=4321)
all_addresses1 = address_service.list(folder="Texas")

# Option 2: Use the unified client interface directly
# This will use the default max_limit (2500)
all_addresses2 = client.address.list(folder="Texas")

# Both options will auto-paginate through all available objects.
# The addresses are fetched in chunks according to the max_limit.

# Delete by ID
address_id = "123e4567-e89b-12d3-a456-426655440000"
client.address.delete(address_id)

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
)

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

try:
    # Create address configuration
    address_config = {
        "name": "test_address",
        "ip_netmask": "192.168.1.0/24",
        "folder": "Texas",
        "description": "Test network segment",
        "tag": ["Test"],
    }

    # Create the address using the unified client interface
    new_address = client.address.create(address_config)

    # Commit changes directly from the client
    result = client.commit(
        folders=["Texas"], description="Added test address", sync=True
    )

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid address data: {e.message}")
except NameNotUniqueError as e:
    print(f"Address name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"Address not found: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
