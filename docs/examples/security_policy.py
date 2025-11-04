from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Basic allow rule configuration
allow_rule = {
    "name": "allow-web",
    "folder": "Texas",
    "from_": ["trust"],
    "to_": ["untrust"],
    "source": ["internal-net"],
    "destination": ["any"],
    "application": ["web-browsing", "ssl"],
    "service": ["application-default"],
    "action": "allow",
    "log_end": True,
}

# Create basic allow rule
basic_rule = client.security_rule.create(allow_rule, rulebase="pre")

# Security profile rule configuration
secure_rule = {
    "name": "secure-web",
    "folder": "Texas",
    "from_": ["trust"],
    "to_": ["untrust"],
    "source": ["internal-net"],
    "destination": ["any"],
    "application": ["web-browsing", "ssl"],
    "service": ["application-default"],
    "profile_setting": {"group": ["best-practice"]},
    "action": "allow",
    "log_start": False,
    "log_end": True,
}

# Create rule with security profiles
profile_rule = client.security_rule.create(secure_rule, rulebase="pre")

# Fetch by name and folder
rule = client.security_rule.fetch(name="allow-web", folder="Texas", rulebase="pre")
print(f"Found rule: {rule.name}")

# Get by ID
rule_by_id = client.security_rule.get(rule.id, rulebase="pre")
print(f"Retrieved rule: {rule_by_id.name}")
print(f"Applications: {rule_by_id.application}")

# Fetch existing rule
existing_rule = client.security_rule.fetch(
    name="allow-web", folder="Texas", rulebase="pre"
)

# Update attributes
existing_rule.description = "Updated web access rule"
existing_rule.application = ["web-browsing", "ssl", "http2"]
existing_rule.profile_setting = {"group": ["strict-security"]}

# Perform update
updated_rule = client.security_rule.update(existing_rule, rulebase="pre")

# Pass filters directly into the list method
filtered_rules = client.security_rule.list(
    folder="Texas",
    rulebase="pre",
    action=["allow"],
    application=["web-browsing", "ssl"],
)

# Process results
for rule in filtered_rules:
    print(f"Name: {rule.name}")
    print(f"Action: {rule.action}")
    print(f"Applications: {rule.application}")

# Define filter parameters as a dictionary
list_params = {
    "folder": "Texas",
    "rulebase": "pre",
    "from_": ["trust"],
    "to_": ["untrust"],
    "tag": ["Production"],
}

# List with filters as kwargs
filtered_rules = client.security_rule.list(**list_params)

# Only return security rules defined exactly in 'Texas'
exact_rules = client.security_rule.list(
    folder="Texas", rulebase="pre", exact_match=True
)

for rule in exact_rules:
    print(f"Exact match: {rule.name} in {rule.folder}")

# Exclude all security rules from the 'All' folder
no_all_rules = client.security_rule.list(
    folder="Texas", rulebase="pre", exclude_folders=["All"]
)

for rule in no_all_rules:
    assert rule.folder != "All"
    print(f"Filtered out 'All': {rule.name}")

# Exclude security rules that come from 'default' snippet
no_default_snippet = client.security_rule.list(
    folder="Texas", rulebase="pre", exclude_snippets=["default"]
)

for rule in no_default_snippet:
    assert rule.snippet != "default"
    print(f"Filtered out 'default' snippet: {rule.name}")

# Exclude security rules associated with 'DeviceA'
no_deviceA = client.security_rule.list(
    folder="Texas", rulebase="pre", exclude_devices=["DeviceA"]
)

for rule in no_deviceA:
    assert rule.device != "DeviceA"
    print(f"Filtered out 'DeviceA': {rule.name}")

# Combine exact_match with multiple exclusions
combined_filters = client.security_rule.list(
    folder="Texas",
    rulebase="pre",
    exact_match=True,
    exclude_folders=["All"],
    exclude_snippets=["default"],
    exclude_devices=["DeviceA"],
)

for rule in combined_filters:
    print(f"Combined filters result: {rule.name} in {rule.folder}")

from scm.client import ScmClient
from scm.config.security_services import SecurityRule

# Initialize client
client = ScmClient(
    client_id="your_client_id", client_secret="your_client_secret", tsg_id="your_tsg_id"
)

# Two options for setting max_limit:

# Option 1: Use the unified client interface but create a custom SecurityRule instance with max_limit
security_rule_service = SecurityRule(client, max_limit=4321)
all_rules1 = security_rule_service.list(folder="Texas", rulebase="pre")

# Option 2: Use the unified client interface directly
# This will use the default max_limit (2500)
all_rules2 = client.security_rule.list(folder="Texas", rulebase="pre")

# Both options will auto-paginate through all available objects.
# The rules are fetched in chunks according to the max_limit.

# Move rule to top of rulebase
top_move = {"destination": "top", "rulebase": "pre"}
client.security_rule.move(rule.id, top_move)

# Move rule before another rule
before_move = {
    "destination": "before",
    "rulebase": "pre",
    "destination_rule": "987fcdeb-54ba-3210-9876-fedcba098765",
}
client.security_rule.move(rule.id, before_move)

# Move rule after another rule
after_move = {
    "destination": "after",
    "rulebase": "pre",
    "destination_rule": "987fcdeb-54ba-3210-9876-fedcba098765",
}
client.security_rule.move(rule.id, after_move)

# Delete by ID
rule_id = "123e4567-e89b-12d3-a456-426655440000"
client.security_rule.delete(rule_id, rulebase="pre")

# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Updated security rules",
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
    # Create rule configuration
    rule_config = {
        "name": "test-rule",
        "folder": "Texas",
        "from_": ["trust"],
        "to_": ["untrust"],
        "source": ["internal-net"],
        "destination": ["any"],
        "application": ["web-browsing"],
        "service": ["application-default"],
        "action": "allow",
    }

    # Create the rule using the unified client interface
    new_rule = client.security_rule.create(rule_config, rulebase="pre")

    # Move the rule
    move_config = {"destination": "top", "rulebase": "pre"}
    client.security_rule.move(new_rule.id, move_config)

    # Commit changes directly from the client
    result = client.commit(folders=["Texas"], description="Added test rule", sync=True)

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid rule data: {e.message}")
except NameNotUniqueError as e:
    print(f"Rule name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"Rule not found: {e.message}")
except ReferenceNotZeroError as e:
    print(f"Rule still in use: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
