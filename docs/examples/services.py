from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# TCP service configuration
tcp_service = {
    "name": "web-service",
    "protocol": {
        "tcp": {"port": "80,443", "override": {"timeout": 60, "halfclose_timeout": 30}}
    },
    "description": "Web service ports",
    "folder": "Texas",
    "tag": ["Web", "Production"],
}

# Create TCP service
tcp_service_obj = client.service.create(tcp_service)

# UDP service configuration
udp_service = {
    "name": "dns-service",
    "protocol": {"udp": {"port": "53", "override": {"timeout": 30}}},
    "description": "DNS service",
    "folder": "Texas",
    "tag": ["DNS"],
}

# Create UDP service
udp_service_obj = client.service.create(udp_service)

# Fetch by name and folder
service = client.service.fetch(name="web-service", folder="Texas")
print(f"Found service: {service.name}")

# Get by ID
service_by_id = client.service.get(service.id)
print(f"Protocol: {'TCP' if service_by_id.protocol.tcp else 'UDP'}")
if service_by_id.protocol.tcp:
    print(f"Ports: {service_by_id.protocol.tcp.port}")


# Fetch existing service
existing_service = client.service.fetch(name="web-service", folder="Texas")

# Update ports and timeouts
if existing_service.protocol.tcp:
    existing_service.protocol.tcp.port = "80,443,8443"
    existing_service.protocol.tcp.override.timeout = 120

# Update description and tags
existing_service.description = "Updated web service ports"
existing_service.tag = ["Web", "Production", "Updated"]

# Perform update
updated_service = client.service.update(existing_service)

# Pass filters directly into the list method
filtered_services = client.service.list(
    folder="Texas", protocols=["tcp"], tags=["Production"]
)

# Process results
for svc in filtered_services:
    print(f"Name: {svc.name}")
    if svc.protocol.tcp:
        print(f"TCP Ports: {svc.protocol.tcp.port}")
    elif svc.protocol.udp:
        print(f"UDP Ports: {svc.protocol.udp.port}")

# Define filter parameters as a dictionary
list_params = {"folder": "Texas", "protocols": ["udp"], "tags": ["DNS"]}

# List services with filters as kwargs
filtered_services = client.service.list(**list_params)

# Only return services defined exactly in 'Texas'
exact_services = client.service.list(folder="Texas", exact_match=True)

for svc in exact_services:
    print(f"Exact match: {svc.name} in {svc.folder}")

# Exclude all services from the 'All' folder
no_all_services = client.service.list(folder="Texas", exclude_folders=["All"])

for svc in no_all_services:
    assert svc.folder != "All"
    print(f"Filtered out 'All': {svc.name}")

# Exclude services that come from 'default' snippet
no_default_snippet = client.service.list(folder="Texas", exclude_snippets=["default"])

for svc in no_default_snippet:
    assert svc.snippet != "default"
    print(f"Filtered out 'default' snippet: {svc.name}")

# Exclude services associated with 'DeviceA'
no_deviceA = client.service.list(folder="Texas", exclude_devices=["DeviceA"])

for svc in no_deviceA:
    assert svc.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {svc.name}")

# Combine exact_match with multiple exclusions
combined_filters = client.service.list(
    folder="Texas",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
)

for svc in combined_filters:
    print(f"Combined filters result: {svc.name} in {svc.folder}")

from scm.client import ScmClient
from scm.config.objects import Service

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Two options for setting max_limit:

# Option 1: Use the unified client interface but create a custom Service instance with max_limit
service_service = Service(client, max_limit=4321)
all_services1 = service_service.list(folder="Texas")

# Option 2: Use the unified client interface directly
# This will use the default max_limit (2500)
all_services2 = client.service.list(folder="Texas")

# Both options will auto-paginate through all available objects.
# The services are fetched in chunks according to the max_limit.

# Delete by ID
service_id = "123e4567-e89b-12d3-a456-426655440000"
client.service.delete(service_id)

# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Updated service definitions",
    "sync": True,
    "timeout": 300,  # 5 minute timeout
}

# Commit the changes directly on the client
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
    # Create service configuration
    service_config = {
        "name": "test-service",
        "protocol": {"tcp": {"port": "8080", "override": {"timeout": 30}}},
        "folder": "Texas",
        "description": "Test service",
        "tag": ["Test"],
    }

    # Create the service using the unified client interface
    new_service = client.service.create(service_config)

    # Commit changes directly from the client
    result = client.commit(
        folders=["Texas"], description="Added test service", sync=True
    )

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid service data: {e.message}")
except NameNotUniqueError as e:
    print(f"Service name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"Service not found: {e.message}")
except ReferenceNotZeroError as e:
    print(f"Service still in use: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
