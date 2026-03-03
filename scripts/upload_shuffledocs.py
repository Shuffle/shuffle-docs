# Uploads documentation into Algolia when ran. 
# Primarily focuses on each part of markdown files.

import os
import hashlib
import requests
from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import RequestException

client = SearchClient.create(os.getenv("ALGOLIA_CLIENT"), os.getenv("ALGOLIA_SECRET"))
index = client.init_index("documentation")

validurls = []
for basedir in ["../docs", "../articles", "../legal"]:
    for dirname in os.listdir(basedir):
        if "md" not in dirname:
            continue

        if ".swo" in dirname or ".swp" in dirname:
            continue

        to_upload = []
        filename = ".".join(dirname.split(".")[0:-1])
        fileread = "%s/%s" % (basedir, dirname)

        #print("Reading %s" % dirname)
        with open(fileread, "r") as tmp:
            try:
                data = tmp.read().split("\n")
            except UnicodeDecodeError as e:
                print("Error loading %s: %s" % (dirname, e))
                continue
        
            wrappeditem = {}
            curitem = ""
            for item in data:
                if item.startswith("#"):
                    if curitem and "ref_url" in wrappeditem:
                        if basedir == "../docs":
                            if wrappeditem["ref_url"] not in validurls:
                                ret = requests.get(wrappeditem["ref_url"])
                                #print("RET: %d - %s" % (ret.status_code, wrappeditem["ref_url"]))
                                if ret.status_code != 200:
                                    print("SKIPPING %s (doesn't exist)" % wrappeditem["ref_url"])
                                    break
                                else:
                                    validurls.append(wrappeditem["ref_url"])
                        
                        to_upload.append(wrappeditem)
                        
                    # Priority based on title
                    title = " ".join(item.split("# ")[1:]).strip()
                    priority = 5
                    for char in item:
                        if char == "#":
                            priority -= 1
        
                    # Hash is used for prioritizing the search
                    title_hash = hashlib.md5(("%s_%s" % (filename, title)).encode("utf-8")).hexdigest()
                    folder_name = basedir.replace("../", "")
                    wrappeditem = {
                        "filename": filename,
                        "title": title.strip(),
                        "data": "",
                        "url": "https://shuffler.io/%s/%s#%s" % (folder_name, filename, title.replace(" ", "_").lower()),
                        "urlpath": "/%s/%s#%s" % (folder_name, filename, title.replace(" ", "_").lower()),
                        "objectID": title_hash,
                        "priority": priority,
                        "ref_url": "https://github.com/shuffle/shuffle-docs/blob/master/%s/%s.md" % (folder_name, filename),
                    }
                    curitem = item
                    continue
        
                if item:
                    curitem += item+"\n"
                    try:
                        wrappeditem["data"] += item
                    except KeyError:
                        wrappeditem["data"] = item
        
        if len(to_upload) > 0:
            try:
                ret = index.save_objects(to_upload)
                print("%s: %d objects" % (filename, len(to_upload)))
            except RequestException as e:
                print("ERROR: %s: %d objects: %s" % (filename, len(to_upload), e))
