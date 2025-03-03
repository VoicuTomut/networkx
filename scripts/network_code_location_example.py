import network_as_code as nac

from network_as_code.models.device import DeviceIpv4Addr

# We initialize the client object with your application key
client = nac.NetworkAsCodeClient(
    token="843e60b7b2msh82e9a3197834d2dp159035jsnfb5d26de206c"
)

# Create a device object for the mobile device we want to use
my_device = client.devices.get(
    "device@testcsp.net",
    ipv4_address=DeviceIpv4Addr(
        public_address="233.252.0.2",
        private_address="192.0.2.25",
        public_port=80
    ),
    ipv6_address="2001:db8:1234:5678:9abc:def0:fedc:ba98",
    # The phone number does not accept spaces or parentheses
    phone_number="+36721601234567"
)

# For estimations, use the is_there object
# followed by the `verify_location()` method
# with the geo-coordinates and maximum age in seconds.
# If the amount in seconds is not given, the default will be 60 seconds.
result = my_device.verify_location(
    longitude=60.252,
    latitude=25.227,
    radius=10_000,
    max_age=3600
)
print("verify location: {}".format(result))

# Specify the maximum amount of time accepted
# to get location information, it's a mandatory parameter.
# If the amount in seconds is not given, the default will be 60 seconds.
location = my_device.location(max_age=3600)

# The location object contains fields for longitude, latitude and also elevation
longitude = location.longitude
latitude = location.latitude

print(longitude)
print(latitude)
print(location.civic_address)



