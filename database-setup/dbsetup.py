#!/usr/bin/python

from molar import ClientConfig, Client

admin_cfg = ClientConfig(server_url="http://localhost:8000",
                         email="default@rheed.com",
                         password="rheed",
                         database_name="main")

admin_client = Client(admin_cfg)

print(admin_client.test_token())

print(admin_client.get_alembic_revisions())