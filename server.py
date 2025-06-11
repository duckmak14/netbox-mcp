from mcp.server.fastmcp import FastMCP
from netbox_client import NetBoxRestClient
import os
from typing import Dict, Optional
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()

import logging
from datetime import datetime, timezone
logging.basicConfig(level=logging.INFO)

# Mapping of simple object names to API endpoints

NETBOX_OBJECT_TYPES = {
    # DCIM (Device and Infrastructure)
    "cables": "dcim/cables",
    "console-ports": "dcim/console-ports", 
    "console-server-ports": "dcim/console-server-ports",
    "devices": "dcim/devices",
    "device-bays": "dcim/device-bays",
    "device-roles": "dcim/device-roles",
    "device-types": "dcim/device-types",
    "front-ports": "dcim/front-ports",
    "interfaces": "dcim/interfaces",
    "inventory-items": "dcim/inventory-items",
    "locations": "dcim/locations",
    "manufacturers": "dcim/manufacturers",
    "modules": "dcim/modules",
    "module-bays": "dcim/module-bays",
    "module-types": "dcim/module-types",
    "platforms": "dcim/platforms",
    "power-feeds": "dcim/power-feeds",
    "power-outlets": "dcim/power-outlets",
    "power-panels": "dcim/power-panels",
    "power-ports": "dcim/power-ports",
    "racks": "dcim/racks",
    "rack-reservations": "dcim/rack-reservations",
    "rack-roles": "dcim/rack-roles",
    "regions": "dcim/regions",
    "sites": "dcim/sites",
    "site-groups": "dcim/site-groups",
    "virtual-chassis": "dcim/virtual-chassis",
    
    # IPAM (IP Address Management)
    "asns": "ipam/asns",
    "asn-ranges": "ipam/asn-ranges", 
    "aggregates": "ipam/aggregates",
    "fhrp-groups": "ipam/fhrp-groups",
    "ip-addresses": "ipam/ip-addresses",
    "ip-ranges": "ipam/ip-ranges",
    "prefixes": "ipam/prefixes",
    "rirs": "ipam/rirs",
    "roles": "ipam/roles",
    "route-targets": "ipam/route-targets",
    "services": "ipam/services",
    "vlans": "ipam/vlans",
    "vlan-groups": "ipam/vlan-groups",
    "vrfs": "ipam/vrfs",
    
    # Circuits
    "circuits": "circuits/circuits",
    "circuit-types": "circuits/circuit-types",
    "circuit-terminations": "circuits/circuit-terminations",
    "providers": "circuits/providers",
    "provider-networks": "circuits/provider-networks",
    
    # Virtualization
    "clusters": "virtualization/clusters",
    "cluster-groups": "virtualization/cluster-groups",
    "cluster-types": "virtualization/cluster-types",
    "virtual-machines": "virtualization/virtual-machines",
    "vm-interfaces": "virtualization/interfaces",
    
    # Tenancy
    "tenants": "tenancy/tenants",
    "tenant-groups": "tenancy/tenant-groups",
    "contacts": "tenancy/contacts",
    "contact-groups": "tenancy/contact-groups",
    "contact-roles": "tenancy/contact-roles",
    
    # VPN
    "ike-policies": "vpn/ike-policies",
    "ike-proposals": "vpn/ike-proposals",
    "ipsec-policies": "vpn/ipsec-policies",
    "ipsec-profiles": "vpn/ipsec-profiles",
    "ipsec-proposals": "vpn/ipsec-proposals",
    "l2vpns": "vpn/l2vpns",
    "tunnels": "vpn/tunnels",
    "tunnel-groups": "vpn/tunnel-groups",
    
    # Wireless
    "wireless-lans": "wireless/wireless-lans",
    "wireless-lan-groups": "wireless/wireless-lan-groups",
    "wireless-links": "wireless/wireless-links",

    # extras
    "custom-links": "extras/custom-links",
    "custom-fields": "extras/custom-fields",
    "tags": "extras/tags",
    "export-templates": "extras/export-templates",
    "images-attachments": "extras/images-attachments",
    "save-filters": "extras/save-filters",
    "custom-field-choices": "extras/custom-field-choices",
    "webhooks": "extras/webhooks",
    "event-rules": "extras/event-rules",
    "object-types": "extras/object-types",

    # core
    "data-sources": "core/data-sources",
    "changelogs": "core/object-changes",
    "jobs": "core/jobs",

}

mcp = FastMCP("NetBox", log_level="DEBUG")
netbox = None

@mcp.tool(name="get_count_objects", description="Count objects in NetBox based on their type and filters")
def get_count_objects(object_type: str, filters:  Optional[Dict] = None):
    """
    Count objects in NetBox based on their type and filters.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        filters: dict of filters to apply to the API call based on the NetBox API filtering options
    
    Returns:
        Integer count of matching objects
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    logging.info(f"Counting objects from endpoint: {endpoint} with filters: {filters}")
    
    # Make API call with count=True
    try:
        response = netbox.get_count(endpoint, params=filters)
    except Exception as e:
        logging.error(f"Error fetching count for {object_type}: {str(e)}")
        return 0
        
    return response["count"]

@mcp.tool(name="get_objects", description="Get objects from NetBox based on their type and filters")
def get_objects(object_type: str, filters:  Optional[Dict] = None):
    """
    Get objects from NetBox based on their type and filters
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        filters: dict of filters to apply to the API call based on the NetBox API filtering options
    
    Valid object_type values:
    
    DCIM (Device and Infrastructure):
    - cables
    - console-ports
    - console-server-ports  
    - devices
    - device-bays
    - device-roles
    - device-types
    - front-ports
    - interfaces
    - inventory-items
    - locations
    - manufacturers
    - modules
    - module-bays
    - module-types
    - platforms
    - power-feeds
    - power-outlets
    - power-panels
    - power-ports
    - racks
    - rack-reservations
    - rack-roles
    - regions
    - sites
    - site-groups
    - virtual-chassis
    
    IPAM (IP Address Management):
    - asns
    - asn-ranges
    - aggregates 
    - fhrp-groups
    - ip-addresses
    - ip-ranges
    - prefixes
    - rirs
    - roles
    - route-targets
    - services
    - vlans
    - vlan-groups
    - vrfs
    
    Circuits:
    - circuits
    - circuit-types
    - circuit-terminations
    - providers
    - provider-networks
    
    Virtualization:
    - clusters
    - cluster-groups
    - cluster-types
    - virtual-machines
    - vm-interfaces
    
    Tenancy:
    - tenants
    - tenant-groups
    - contacts
    - contact-groups
    - contact-roles
    
    VPN:
    - ike-policies
    - ike-proposals
    - ipsec-policies
    - ipsec-profiles
    - ipsec-proposals
    - l2vpns
    - tunnels
    - tunnel-groups
    
    Wireless:
    - wireless-lans
    - wireless-lan-groups
    - wireless-links

    Extras:
    - custom-links
    - custom-fields
    - tags
    - export-templates
    - images-attachments
    - save-filters
    - custom-field-choices
    - webhooks
    - event-rules

    Core:
    - data-sources
    - change-logs
    - jobs
    
    See NetBox API documentation for filtering options for each object type.
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]

    logging.info(f"Fetching objects from endpoint: {endpoint} with filters: {filters}")
    # Make API call
    return netbox.get(endpoint, params=filters)

@mcp.tool(name="get_object_by_id", description="Get detailed information about a specific NetBox object by its ID")
def get_object_by_id(object_type: str, object_id: int):
    """
    Get detailed information about a specific NetBox object by its ID.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object
    
    Returns:
        Complete object details
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = f"{NETBOX_OBJECT_TYPES[object_type]}/{object_id}"
    
    return netbox.get(endpoint)

@mcp.tool(name="get_custom_fields", description="Retrieve custom fields for NetBox objects")
def get_custom_fields(object_type: str, filters: dict):
    """
    Retrieve custom fields for NetBox objects.

    Returns:
        List of custom field definitions including:
        - id: Unique identifier of the custom field
        - name: Name of the custom field
        - label: Human-readable label for the field
        - type: Data type of the field (e.g., text, integer, choice)
        - choices: List of choices if applicable
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    # Make API call
    response = netbox.get(endpoint, params=filters)
    try:
        logging.info(f"Fetching custom fields from endpoint: {endpoint} with filters: {filters}")
        custom_fields = [
            {
                "id": item["id"],
                "name": item["name"],
                "object_types": item["object_types"],
                "description": item["description"]
            }
            for item in response
        ]
        print(custom_fields)
        logging.info(f"Retrieved {len(custom_fields)} custom fields for object type '{object_type}'")
        return custom_fields 
    except Exception as e:
        logging.error(f"Error fetching custom fields: {str(e)}")
        return None

@mcp.tool(name="get_current_time_iso", description="Get the current time in ISO 8601 format")
def get_current_time_iso():
    """
    Get the current time in ISO 8601 format.

    Returns:
        String representing the current time in ISO 8601 format.
    """
    current_time = datetime.now(timezone.utc).isoformat()
    current_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    logging.info(f"Current time in ISO 8601 format: {current_time}")
    return current_time

@mcp.tool(name="get_changelogs", description="Get object change records (changelogs) from NetBox")
def get_changelogs(filters: Optional[dict] = None):
    """
    Get object change records (changelogs) from NetBox based on filters.
    
    Args:
        filters: Optional dict of filters to apply to the API call based on the NetBox API filtering options.
        Note: The filters can include any combination of the following fields:
        - user_id: Filter by user ID who made the change
        - user: Filter by username who made the change
        - changed_object_type_id: Filter by ContentType ID of the changed object
        - changed_object_id: Filter by ID of the changed object
        - object_repr: Filter by object representation (usually contains object name)
        - action: Filter by action type (create, update, delete)
        - time_before: Filter for changes made before a given time (ISO 8601 format)
        - time_after: Filter for changes made after a given time (ISO 8601 format)
        - q: Search term to filter by object representation
    
    Returns:
        List of changelog objects matching the specified filters.
    
    Example filters:
    {
        "user_id": 1,
        "user": "admin",
        "changed_object_type_id": "dcim.device",
        "changed_object_id": 123,
        "object_repr": "router1",
        "action": "create",
        "time_before": "2023-10-01T00:00:00Z",
        "time_after": "2023-10-01T00:00:00Z",
        "q": "router1"
    }
    Note: The filters can include any combination of the above fields to narrow down the results.
    """
    logging.info(f"Fetching changelogs with filters: {filters}")
    endpoint = "core/object-changes"

    # Make API call
    response = netbox.get(endpoint, params=filters or {})
    logging.info(f"Retrieved {len(response)} changelogs from NetBox")
    if not response:
        logging.warning("No changelogs found with the specified filters.")
        return []    

    return response

@mcp.tool(name="create_object", description="Create a new object in NetBox")
def create_object(object_type: str, data: dict):
    """
    Create a new object in NetBox.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data: Dictionary containing the data for the new object
    
    Returns:
        The created object with its ID and other details
    
    Example:
    To create a new device:
    {
        "name": "router1",
        "device_type": 1,
        "device_role": 1,
        "site": 1,
        "status": "active"
    }
    
    See NetBox API documentation for required and optional fields for each object type.
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]

    logging.info(f"Creating object at endpoint: {endpoint} with data: {data}")
    
    # Make API call to create object
    return netbox.create(endpoint, data=data)

@mcp.tool(name="update_object", description="Update an existing object in NetBox")
def update_object(object_type: str, object_id: int, data: dict):
    """
    Update an existing object in NetBox using PATCH method.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object to update
        data: Dictionary containing the fields to update
    
    Returns:
        The updated object with its modified fields
    
    Example:
    To update a device with ID 123:
    {
        "name": "new-router-name",
        "status": "maintenance"
    }
    
    Note: Only include the fields you want to update in the data dictionary.
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = f"{NETBOX_OBJECT_TYPES[object_type]}"
    logging.info(f"Updating object at endpoint: {endpoint} with ID: {object_id} and data: {data}")
    # Make API call to update object using PATCH method
    return netbox.update(endpoint,id=object_id, data=data)

@mcp.tool(name="delete_object", description="Delete an object from NetBox by its ID")
def delete_object(object_type: str, object_id: int):
    """
    Delete an object from NetBox by its ID.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object to delete
    
    Returns:
        None if successful, raises an exception if the deletion fails
    
    Example:
    To delete a device with ID 123:
    delete_object("devices", 123)
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = f"{NETBOX_OBJECT_TYPES[object_type]}"
    logging.info(f"Deleting object at endpoint: {endpoint} with ID: {object_id}")
    # Make API call to delete object
    return netbox.delete(endpoint, id=object_id)

@mcp.prompt(
    name="netbox-mcp",
    description="NetBox MCP (Multi-Channel Protocol) server for managing NetBox objects",
)
def netbox_mcp():
    return """
    Main function to handle NetBox MCP (Multi-Channel Protocol) server.
    
    Available Tools:
    
    1. get_objects(object_type: str, filters: dict)
       - Retrieves objects from NetBox based on type and filters
       - object_type: Type of object to retrieve (e.g., "devices", "ip-addresses")
       - filters: Dictionary of filter criteria
       - Returns a list of matching objects
    
    2. get_object_by_id(object_type: str, object_id: int)
       - Gets detailed information about a specific NetBox object
       - object_type: Type of object to retrieve
       - object_id: Numeric ID of the object
       - Returns complete object details
    
    3. create_object(object_type: str, data: dict)
       - Creates a new object in NetBox
       - object_type: Type of object to create
       - data: Dictionary containing object data
       - Returns the created object
    
    4. update_object(object_type: str, object_id: int, data: dict)
       - Updates an existing object
       - object_type: Type of object to update
       - object_id: ID of object to update
       - data: Dictionary of fields to update
       - Returns the updated object
    
    5. delete_object(object_type: str, object_id: int)
       - Deletes an object from NetBox
       - object_type: Type of object to delete
       - object_id: ID of object to delete
       - Returns None if successful
    
    Supported Object Types:
    - DCIM: devices, interfaces, sites, racks, etc.
    - IPAM: ip-addresses, prefixes, vlans, vrfs, etc.
    - Circuits: circuits, providers, etc.
    - Virtualization: virtual-machines, clusters, etc.
    - Tenancy: tenants, contacts, etc.
    - VPN: tunnels, policies, etc.
    - Wireless: wireless-lans, wireless-links, etc.
    
    Example Usage:
    1. To get percentage of space in the rack named H01 in site named HCM:
        # Note: vietnamese prompts is "Phần trăm không gian còn trống trong giá H01 tại site HCM"
        # First, find the site by name
        site = get_objects("sites", {"name": "HCM"})
        if not site:
            raise ValueError("No site found with name 'HCM'")
        # Second, find the rack by name in that site
        racks = get_objects("racks", {"name": "H01", "site_id": site[0]["id"]})
        if not racks:
            raise ValueError("No rack found with name 'H01' in site 'HCM'")
        
        rack_height = racks[0].get("u_height", 42)  # Default to 42U if not specified
        # Thrid, get list device in that rack:
        devices = get_objects("devices", {"rack_id": racks[0]["id"]})
        if not devices:
            return "Rack H01 in site HCM free space is 100%"
        
        # Calculate total used space in the rack is total u_height of all devices in the rack
        total_u_height = 0
        for device in devices:
            # get device_type form device
            device_type = get_object_by_id("device-types", device["device_type"]["id"])
            # get u_height from device_type
            u_height = device_type.get("u_height", 1)  # Default to 1 if not specified
            # Add u_height to total used space
            total_u_height += u_height
        
        percentage_free_space = ((rack_height - total_u_height) / rack_height) * 100
        return f"Rack H01 in site HCM free space is {percentage_free_space:.2f}%"    
    2. To get list devices in a site:
        # First, find the site by name
        site = get_objects("sites", {"name": "site-name"})

        # Then, get devices in that site
        devices = get_objects("devices", {"site_id": site[0]["id"]})
        
        # Returns the list of devices in the specified site
        return devices 

    3. To get list devices in a rack:
        # First, find the rack by name
        rack = get_objects("racks", {"name": "rack-name"})
        
        # Then, get devices in that rack
        devices = get_objects("devices", {"rack_id": rack[0]["id"]})
        
        # Returns the list of devices in the specified rack
        return devices

    4. To get list devices on netbox:
        devices = get_objects("devices", {})
        return devices

    5. To get a specific device:
        get_object_by_id("devices", 123)

    6. To create a new device:
        create_object("devices", {
            "name": "router1",
            "device_type": 1,
            "device_role": 1,
            "site": 1,
            "status": "active"
        })
    
    7. To update a device:
        # First, find the device by name
        devices = get_objects("devices", {"name": "router1"})
        
        # If multiple devices are found, you can use the first one
        if devices and len(devices) > 0:
            device_id = devices[0]["id"]
            
            # Then update the device using its ID
            update_object("devices", device_id, {
                "name": "new-router-name",
                "status": "maintenance",
                "comments": "Updated via MCP"
            })
        else:
            print("No device found with name 'router1'")
      
    8. To delete a device:
        delete_object("devices", 123)
        
    Remember to:
    - Always validate object types before making requests
    - Check required fields for object creation
    - Use appropriate filters to narrow down results
    - Handle errors gracefully
    - Consider the impact of changelogs before making them
    
    """

@mcp.prompt(name="netbox_prompt_get_count_objects", description="Count objects in NetBox based on their type and filters")
def netbox_prompt_get_count_objects():
    return """
    Use the `get_count_objects` tool to count objects in NetBox based on their type and filters.
    
    Example:
    1. To count devices with a specific custom field:
    count = get_count_objects("devices", {"cf_year_of_investment": "3/2022"})
    return Netbox has {count} devices with Year of investment in 3/2022.

    2. To how many devices are in NetBox:
    count = get_count_objects("devices", {})
    return Netbox has {count} devices.

    3. To count virtual machines with platform (Operating System - OS, hệ điều hành) as Ubuntu 24:
        # Search for virtual machines with the platform field set to Ubuntu 24 ( platforms are used to represent Operating Systems in NetBox)
        # First find the platform by name
        platforms = get_objects("platforms", {"name": "Ubuntu 24"})
        if not platforms:
            raise ValueError("No platform found with name 'Ubuntu 24'")
        # Then get virtual machines with that platform
        vms = get_objects("virtual-machines", {"platform_id": platforms[0]["id"]})
        # Returns the list of virtual machines running Ubuntu 24
        return vms[0]["count"]

    Valid object types include:
    - devices
    - ip-addresses
    - vlans
    - prefixes
    - sites
    - racks
    - etc.
    
    See the documentation for a full list of supported object types and filtering options.
    """

@mcp.prompt(name="netbox_prompt_get_objects", description="Retrieve objects from NetBox based on their type and filters")
def netbox_prompt_get_objects():
    return """
    Use the `get_objects` tool to retrieve objects from NetBox based on their type and filters.
    
    Example:
    1. To get all devices:
        devices = get_objects("devices", {})
        return devices

    2. To get devices with Year of investment in 3/2022:
        # First, search for devices with the "Year of investment" field
        devices = get_objects("devices", {"cf_year_of_investment": 3/2022})
       
        # If no devices are found, search for devices with a custom field "Year of investment"
        if not devices:
            devices = get_objects("devices", {"year_of_investment": 3/2022})
        
        # Returns the list of matching devices
        return devices

    3. To get virtual machines with platform (Operating System - OS, hệ điều hành) as Ubuntu 24:
        # Search for virtual machines with the platform field set to Ubuntu 24
        # First find the platform by name
        platforms = get_objects("platforms", {"name": "Ubuntu 24"})
        if not platforms:
            raise ValueError("No platform found with name 'Ubuntu 24'")
        # Then get virtual machines with that platform
        vms = get_objects("virtual-machines", {"platform_id": platforms[0]["id"]})
        # Returns the list of virtual machines running Ubuntu 24
        return vms

    Valid object types include:
    - devices
    - ip-addresses
    - vlans
    - prefixes
    - sites
    - racks
    - virtual-machines
    - etc.
    
    See the documentation for a full list of supported object types and filtering options.
    """

@mcp.prompt(name="netbox_prompt_get_changelogs", description="Retrieve changelogs from NetBox based on filters")
def netbox_prompt_get_changelogs():
    return """
    Use the `get_changelogs` tool to retrieve object change records (changelogs) from NetBox based on filters.

    Example:
    1. To Fetching all changelogs:
        changelogs = get_changelogs({})
        return changelogs

    2. To Fetching changelogs for a specific device with ID 123:
        changelogs = get_changelogs({"changed_object_type": "dcim.device", "changed_object_id": 123})
        return changelogs

    3. To Fetching list changelogs in the day:
        # The frist get the current date and add variable is current_date.
        current_date = get_current_time_iso()
        # Fetch changelogs with time after the current time
        changelogs = get_changelogs({"time_after": current_date})

        return changelogs

    4. To Fetching changelogs filtered by user admin:
        # get user by username
        user = get_objects("users", {"username": "admin"})
        if not user:
            return "No user found with username 'admin'"
        # Fetch changelogs for that user 
        changelogs = get_changelogs({"user": user[0]["id"]})
        return changelogs

    5. To Fetching changelogs filtered by action type:
        # Fetch changelogs for create objects
        changelogs = get_changelogs({"action": "create"})
        return changelogs
    
    6. To Fetching changelogs filtered by object type is device:
        # get objects of type device
        object_types = get_objects("object-types", {"model": "device"})
        changelogs = get_changelogs({"changed_object_type_id": object_types[0]["id"]})
        return changelogs

    7. How many changelogs are in NetBox:
        count = get_count_objects("changelogs", {})
        return NetBox has {count} changelogs.
    8. How many changelogs are in NetBox in the day:
        # The frist get the current date and add variable is current_date.
        current_date = get_current_time_iso()
        # Fetch changelogs with time after the current time
        count = get_count_objects("changelogs", {"time_after": current_date})
        return NetBox has {count} changelogs in the day.
    9. How many changelogs are in NetBox by user admin:
        # get user by username
        user = get_objects("users", {"username": "admin"})
        if not user:
            return "No user found with username 'admin'"
        # Fetch changelogs for that user 
        count = get_count_objects("changelogs", {"user": user[0]["id"]})
        return NetBox has {count} changelogs by user admin.
    10. How many changelogs are in NetBox by action type:
        # Fetch changelogs for create objects
        count = get_count_objects("changelogs", {"action": "create"})
        return NetBox has {count} changelogs by action type create.
    
    11. How many changelogs are in NetBox by object type is device and action type create:
        # get objects of type device
        object_types = get_objects("object-types", {"model": "device"})
        count = get_count_objects("changelogs", {"changed_object_type_id": object_types[0]["id"] , "action": "create"})
        return NetBox has {count} changelogs by object type is device.
    
    Filtering options include:
    - user_id: Filter by user ID who made the change
    - user: Filter by username who made the change
    - changed_object_type_id: Filter by ContentType ID of the changed object
    - changed_object_id: Filter by ID of the changed object
    - object_repr: Filter by object representation (usually contains object name)
    - action: Filter by action type (create, update, delete)
    - time_before: Filter for changes made before a given time (ISO 8601 format)
    - time_after: Filter for changes made after a given time (ISO 8601 format)
    - q: Search term to filter by object representation

    See the NetBox API documentation for more details on filtering options.
    """

if __name__ == "__main__":
    # Load NetBox configuration from environment variables
    netbox_url = os.getenv("NETBOX_URL")
    netbox_token = os.getenv("NETBOX_TOKEN")
    
    if not netbox_url or not netbox_token:
        raise ValueError("NETBOX_URL and NETBOX_TOKEN environment variables must be set")
    
    # Initialize NetBox client
    netbox = NetBoxRestClient(url=netbox_url, token=netbox_token)
    
   #mcp.run(transport="stdio")
    mcp.run(transport="sse")
