from enum import Enum
from collections import namedtuple
# Define a named tuple to represent the two fields
RegionInfo = namedtuple(
    'RegionInfo', ['name', 'aws_region', 'auth_url', 'api_url', 'apps_url'])


class Region(Enum):
    US_EAST_1 = RegionInfo("US East (Virginia)", "us-east-1", "https://login.mypurecloud.com",
                           "https://api.mypurecloud.com", "https://apps.mypurecloud.com")
    AP_SOUTHEAST_2 = RegionInfo("Asia Pacific (Sydney)", "ap-southeast-2", "https://login.mypurecloud.com.au",
                                "https://api.mypurecloud.com.au", "https://apps.mypurecloud.com.au")

    @staticmethod
    def find_by_aws_region(aws_region):
        for region in Region:
            if region.value.aws_region == aws_region:
                return region
        raise ValueError(f"Region with aws_region '{aws_region}' not found")
