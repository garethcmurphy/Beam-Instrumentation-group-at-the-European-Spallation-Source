#!/usr/bin/env python3
"""read beam"""

import datetime
import json
import urllib.parse

import requests
import h5py


class ReadBeam:
    """read beam"""
    url_base = "https://scicat.esss.se"
    file_name = "WSAFE.hdf5"
    user_dict = {}
    nx_entry_attributes = {}
    attributes_dict = {}
    urls = []
    scicat_dataset = {
        "contactEmail": "clement.derrez@ess.eu",
        "creationTime": datetime.datetime.now().isoformat(),
        "owner": "Clement Derrez",
        "principalInvestigator": "Clement Derrez",
        "proposalId": "ZJKF12",
        "creationLocation": "ZJKF12",
        "ownerGroup": "ess",
        "sourceFolder": "/nfs/groups/beamlines/beamInstrumentation/wsafe",
        "keywords": ["beam_test"],
        "type": "raw",
    }
    orig_data_block = {
        "size": 526848,
        "dataFileList": [
            {
                "path": "/nfs/groups/beamlines/wsafe/WSAFE.hdf5",
                "size": 526848,
                "time": "2019-12-11T12:48:03Z",
                "chk": "34782",
                "uid": "101",
                "gid": "101",
                "perm": "755"
            }
        ],
        "ownerGroup": "ess",
        "accessGroups": ["ess", "odin", "loki", "nmx"],
        "createdBy": "ingestor",
        "datasetId": "20.500.12269/beam_test17"
    }

    def read(self):
        """loop over datasets"""
        print("start read")
        file = h5py.File(self.file_name, 'r')
        entry_name = "WSAFE_WSBE_F01 _A01"
        nx_entry = file[entry_name]
        self.nx_entry_attributes = dict(list(nx_entry.attrs.items()))

        nx_user = file[entry_name]["NXUSER"]
        self.user_dict = dict(list(nx_user.attrs.items()))
        self.scicat_dataset["principalInvestigator"] = self.user_dict["name"]
        self.scicat_dataset["owner"] = self.user_dict["name"]

        nx_instruments = file["WSAFE_WSBE_F01 _A01"]["NXInstruments"]
        group_number = 0
        for group in nx_instruments:
            group_number = group_number+1
            print(group)
            group_attributes = nx_instruments[group].attrs.items()
            # print(list(group_attributes))
            self.attributes_dict = dict(list(group_attributes))
            self.edit_attributes()
            print(self.attributes_dict)
            self.scicat_dataset["scientificMetadata"] = self.attributes_dict
            self.scicat_dataset["description"] = self.attributes_dict["description"]
            self.scicat_dataset["datasetName"] = group
            self.scicat_dataset["creationTime"] = self.nx_entry_attributes.get(
                "start_time")

            self.scicat_dataset["pid"] = "beam_test"+str(group_number)
            print(json.dumps(self.scicat_dataset, indent=2))

            access_token = "rgDUQ2MClMiRskrf2FtqVhQV9iWKT7cSyQID65uL8bGx9L4a6o4pgnEYOyExASKK"
            url = self.url_base + "/api/v3/Datasets?access_token="+access_token
            response = requests.post(url=url, json=self.scicat_dataset)
            url = self.url_base + "/api/v3/OrigDatablocks?access_token="+access_token
            response = requests.post(url=url, json=self.orig_data_block)
            print(response.json())
            url_beg = self.url_base + "/datasets/"
            url_end = urllib.parse.quote_plus(
                "20.500.12269/"+self.scicat_dataset["pid"])
            url = url_beg + url_end
            self.urls.append(url)
        for url in self.urls:
            print(url)

        # post each to scicat

    def edit_attributes(self):
        """edit attributes"""
        self.attributes_dict.pop("NX_class")


def main():
    """main"""
    read = ReadBeam()
    read.read()


if __name__ == "__main__":
    main()
