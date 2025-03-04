import network_as_code as nac

from network_as_code.models.device import DeviceIpv4Addr

from network_as_code.models.slice import (
    NetworkIdentifier,
    SliceInfo,
)

# We begin by creating a Network as Code client
client = nac.NetworkAsCodeClient(
    token="<your-application-key-here>"
)

# This is the device object we'll attach to the slice
my_device = client.devices.get(
    "device@testcsp.net",
    ipv4_address=DeviceIpv4Addr(
        public_address="233.252.0.2",
        private_address="192.0.2.25",
        public_port=80
    ),
)

# Then, we create a slice
my_slice = client.slices.create(
    name="slice-name",
    network_id=NetworkIdentifier(mcc="236", mnc="30"),
    slice_info=SliceInfo(service_type="eMBB", differentiator="123456"),
    # Use HTTPS to send notifications
    notification_url="http://notify.me/here",
    notification_auth_token="replace-with-your-auth-token"
)

# The slice needs to be activated
# before attaching a device or app to it.
# Once it's OPERATING, devices and apps can be attached:
my_slice.activate()
await my_slice.wait_for(desired_state="OPERATING")

# Attach the device to the slice just created
# and get notifications
my_slice.attach(
    my_device,
    notification_url="https://notify.me/here",
    notification_auth_token="replace-with-your-auth-token"
)
