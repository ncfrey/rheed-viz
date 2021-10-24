#!/usr/bin/python

from molar import ClientConfig, Client
import urllib.request
import zipfile
import numpy as np
import pandas as pd
import base64
import json
from PIL import Image
import io

# needs to correspond to molarcli install local parameters
local_address = "http://localhost:8000"
default_admin_name = "default"
default_admin_pw = "rheed"
default_domain = "rheed.com"
# other params
default_user_name = "user1"

# name the database here
database_name = "test"
revision_to_use = database_name + "@d480185c54df"

# create default admin config
admin_cfg = ClientConfig(server_url=local_address,
                         email=default_admin_name + "@" + default_domain,
                         password=default_admin_pw,
                         database_name="main")

# create default user config
user_cfg = ClientConfig(server_url="http://localhost:8000",
                        email=default_user_name + "@" + default_domain,
                        password=default_admin_pw,
                        database_name=database_name)


admin_client = Client(admin_cfg)
user_client = Client(user_cfg)


# clear out the existing database
admin_client.remove_database(database_name)

# create a new database
user_client.database_creation_request(
    superuser_fullname="user1",
    alembic_revisions=[revision_to_use]
)

admin_client.approve_database(database_name)

# print(admin_client.test_token())
# print(admin_client.get_alembic_revisions())
db_info = user_client.get_database_information()

print(db_info[db_info.table_name == "sample"])
print(db_info[db_info.table_name == "rheed"])


sys.exit()

# event = user_client.create_entry(type="molecule_type", data={"name": "brain catalyst"})

# event = user_client.create_entry(type="numerical_data", data={"data": [0.]})
####


### storing raw images

## TODO: change to storing comprressed arrays

url = 'https://figshare.com/ndownloader/files/31170988?private_link=73b8ab6cb131acbbe9d4'
filehandle, _ = urllib.request.urlretrieve(url)
zip_file_object = zipfile.ZipFile(filehandle, 'r')

for fi, ff in enumerate(zip_file_object.namelist()):

    if '.jpg' in ff:

        file = zip_file_object.open(ff)
        content = np.asarray(Image.open(io.BytesIO(file.read())))
        # content = base64.encodebytes(file.read())
        # print(content)
        # print(type(content))
        timeindex = int(ff.split('_')[-1].split('.jpg')[0].lstrip('0'))
        shape = content.shape
        # print(content.flatten().squeeze().tolist())

        # print(type(timeindex))
        # print(type(content))
        # print(type(content[0]))
        # print(type(ff))

        event = user_client.create_entry(type="conformer", 
                                        data={"atomic_numbers": [26, 34], # iron and selenium
                                                "x": content.flatten().squeeze().tolist(),
                                                "y": [0.],
                                                "z": [0.],
                                                "metadata": {"data_type": "raw", "filename": ff, "samplename": "FeSe", "timeindex": timeindex, "shape": shape} # "bytestring": content.decode(),}
                                                })

    if fi > 5:
        # only store a few raw images
        break

        # print(event)

        # sys.exit()

# Compressed images using principal components
data = np.load('data/pca.npz')
components = data['arr_0']

event = user_client.create_entry(type="conformer", 
                            data={"atomic_numbers": [26, 34], # iron and selenium
                                    "x": components[0].tolist(),
                                    "y": components[1].tolist(),
                                    "z": components[2].tolist(),
                                    "metadata": {"data_type": "pca_image", "samplename": "FeSe"}
                                    })

# Principal components versus time
pc_df = pd.read_csv('data/pca.csv')
event = user_client.create_entry(type="conformer", 
                            data={"atomic_numbers": [26, 34], # iron and selenium
                                    "x": pc_df['PC1'].values.tolist(),
                                    "y": pc_df['PC2'].values.tolist(),
                                    "z": pc_df['PC3'].values.tolist(),
                                    "metadata": {"data_type": "pca_time", "samplename": "FeSe"}
                                    })

