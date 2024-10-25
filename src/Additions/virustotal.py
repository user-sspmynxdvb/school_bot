from aiohttp import ClientSession

from warnings import filterwarnings
from cryptography.utils import CryptographyDeprecationWarning
from pymongo import MongoClient

filterwarnings("ignore", category=CryptographyDeprecationWarning)


class VirusTotal:
    def __init__(self, apikey: str, mongo_url: str):
        """
        Initializes the VirusTotal class with the specified API key and MongoDB URL.

        Parameters:
            - apikey (str): The API key for accessing the VirusTotal service.
            - mongo_url (str): The URL for connecting to the MongoDB database.

        Note:
            - The VirusTotal class provides methods for scanning files and URLs and storing the scan information in a MongoDB database.
        """
        self.base_url = "https://www.virustotal.com/vtapi/v2/"
        self.apikey = apikey

        # Create a MongoDB client and connect to the specified database
        self.mongo_client = MongoClient(mongo_url)
        self.db = self.mongo_client["virus_total"]

        # Create collections if they don't exist
        self.create_collections()

    def create_collections(self):
        """
        Create 'file_scans' and 'url_scans' collections if they don't exist.
        """
        collections = ["file_scans", "url_scans"]
        for collection_name in collections:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)

    async def fetch(self, url, params, session):
        async with session.get(url, params=params) as response:
            return await response.json()

    async def scan_file(
        self, file_path: str, file_id: str, file_name: str, file_size: int
    ) -> str:
        url = self.base_url + "file/scan"
        params = {"apikey": self.apikey}

        async with ClientSession() as session:
            with open(file_path, "rb") as file:
                scanfile = {"file": file}
                async with session.post(url, params=params, data=scanfile) as response:
                    sha1 = (await response.json())["sha1"]

                    # Store the scan information in the 'file_scans' collection of the MongoDB database
                    collection = self.db["file_scans"]
                    collection.insert_one(
                        {
                            "sha1": sha1,
                            "file_id": file_id,
                            "file_name": file_name,
                            "file_size": file_size,
                            "response": None,
                        }
                    )

                    return sha1

    async def file_report(self, sha1: str) -> dict:
        url = self.base_url + "file/report"
        params = {"apikey": self.apikey, "resource": sha1}

        # Check if the sha1 exists in the database
        collection = self.db["file_scans"]
        result = collection.find_one({"sha1": sha1})

        if result:
            response = result["response"]

            if not response:
                # If the response is not already in the database, retrieve it from VirusTotal
                async with ClientSession() as session:
                    response = await self.fetch(url, params, session)

                # Update the record in the database with the scan information
                collection.update_one({"sha1": sha1}, {"$set": {"response": response}})

            return response

        # If the record does not exist in the database, retrieve the response from VirusTotal and store it in the database
        async with ClientSession() as session:
            response = await self.fetch(url, params, session)

        collection.insert_one({"sha1": sha1, "response": response})
        return response

    def scan_file_id(self, file_id: str, file_name: str, file_size: int) -> str | None:
        """
        Retrieves the SHA1 hash of a previously scanned file from the MongoDB database.

        Parameters:
            - file_id (str): The unique identifier for the file.

        Returns:
            - str: The SHA1 hash of the scanned file, or None if not found in the database.

        Note:
            - The file scan information is retrieved from the 'file_scans' collection of the MongoDB database based on the file_id.
        """
        collection = self.db["file_scans"]
        result = collection.find_one({"file_id": file_id})
        if not result:
            result = collection.find_one(
                {"file_name": file_name, "file_size": file_size}
            )

        return result["sha1"] if result else None

    async def url_report(self, scan_url: str) -> dict:
        url = self.base_url + "url/report"
        params = {"apikey": self.apikey, "resource": scan_url}

        collection = self.db["url_scans"]
        result = collection.find_one({"scan_url": scan_url})

        if result:
            # If the response is already in the database, return it
            return result["response"]

        # If the response does not exist in the database, retrieve it from VirusTotal and store it in the database
        async with ClientSession() as session:
            response = await self.fetch(url, params, session)

        collection.insert_one({"scan_url": scan_url, "response": response})
        return response
