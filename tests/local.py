
import unittest

from msgraph import ClientCredential, MicrosoftGraphAPI
from genesys import Region, GenesysCloudAPI
from genesys import ClientCredential as GenesysClientCredential
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization.pkcs12 import load_pkcs12
from dotenv import dotenv_values

config = dotenv_values(".env")


def load_private_key(pfx_file_path, pfx_password):
   # Load the PFX file and extract the private key
    with open(pfx_file_path, "rb") as pfx_file:
        pfx_data = pfx_file.read()
    private_key = None
    try:
        pfx = load_pkcs12(pfx_data, pfx_password.encode(
            "utf-8"), default_backend())
        private_key = pfx.key
    except ValueError as e:
        print("Error loading PFX file:", e)

    return private_key


class TestFunctions(unittest.TestCase):
    def test_graph_client_secret(self):
        tenant_id = config.get("graph.tenant_id")
        client_id = config.get("graph.client_id")
        client_secret = config.get("graph.client_secret")

        client_credential = ClientCredential(
            tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        client = MicrosoftGraphAPI(
            credential=client_credential, log_requests=True)
        users = client.find_user_by_mobile_phone("0423456585")
        self.assertTrue(len(users) > 0)

    def test_graph_client_private_key(self):

        tenant_id = config.get("graph.tenant_id")
        client_id = config.get("graph.client_id")

        sha1_thumbprint = config.get("graph.sha1_thumbprint")
        pfx_file_path = config.get("graph.pfx_file_path")
        pfx_password = config.get("graph.pfx_password")

        # the private key can be RSAPrivateKey, string, or bytes
        private_key = load_private_key(pfx_file_path, pfx_password)

        client_credential = ClientCredential(
            tenant_id=tenant_id, client_id=client_id, private_key=private_key, sha1_thumbprint=sha1_thumbprint)
        client = MicrosoftGraphAPI(
            credential=client_credential, log_requests=True)
        users = client.find_user_by_mobile_phone("0423456585")
        self.assertTrue(len(users) > 0)

    def test_genesys(self):
        client_id = config.get("genesys.client_id")
        client_secret = config.get("genesys.client_secret")
        aws_region = config.get("genesys.region")
        region = Region.find_by_aws_region(aws_region)
        client_credential = GenesysClientCredential(
            region=region, client_id=client_id, client_secret=client_secret)
        client = GenesysCloudAPI(
            region=region, credential=client_credential, log_requests=True)
        users = client.list_user()
        self.assertTrue(len(users) > 0)


if __name__ == '__main__':
    unittest.main()
