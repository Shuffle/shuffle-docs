# Troubleshooting
Documentation for troubleshooting and debugging known issues in Shuffle.

## Table of contents
* [Debugging Executions](#debugging_executions)
* [Debugging in the non-scale mode](#debugging_in_the_non_scale_mode)
* [Orborus backend connection problems](#orborus_backend_connection_problems)
* [Load all apps locally](#load_all_apps_locally)
* [Orborus can't connect to backend](#orborus_can_not_reach_backend)
* [How to stop executions in loop](#how_to_stop_executions_in_loop)
* [Abort all specific workflow executions](#abort_all_running_executions_of_a_specific_workflow)
* [Workflows are stuck](#workflows_are_stuck)
* [Opensearch permission errors](#opensearch_permissions_error)
* [Recover admin user](#recover-admin-user)
* [Delete user](#delete_user)
* [Docker client version too new](#docker_client_version)
* [Useful OpenSearch Queries](#useful_opensearch_queries)
* [Extract all workflows](#extract_all_workflows)
* [Rebuilding an OpenSearch index](#rebuilding_an_opsearch_index)
* [Updates Failing](#updates_failing)
* [Database not starting](#database_not_starting)
* [TLS timeout error/Timeout Errors/EOF Errors](#TLS_timeout_error/Timeout_Errors/EOF_Errors)
* [Shuffle on ARM](#shuffle_on_arm)
* [Orborus can't connect to backend](#orborus_backend_connection_problems)
* [Permission denied on file upload](#permission_denied_on_files)
* [Docker Permission denied](#docker_permission_denied)
* [Server is slow](#server_is_slow)
* [How to handle wrong or bad images on old versions of docker](#how-to-handle-wrong-or-bad-images-on-old-versions-of-docker)
* [Docker not working](#docker_not_working)
* [Troubleshooting for executions not running in swarm mode](#Troubleshooting_for_executions_not_running_in_swarm_mode)
* [Find app creator Python function](#find_code_openapi_app)
* [Tenants/Suborgs seem to be lost](#reinstate_lost_tenants)
* [Find top index items opensearch](#find-top-index-items-opensearch)
* [Resetting MFA code](#resetting-mfa)
* [Re-add user to lost organization](#add-user-to-lost-org)
* [No module named 'xyz' in 'execute python' (Shuffle Tools)](#no-module-named-'xyz'-in-'execute-python'-(Shuffle-Tools))

## Debugging Executions
Please check the [Debugging section in the Configuration documentation](/docs/configuration#debugging)

## Debugging in the non scale mode

If you're running Shuffle in the non-scale mode, you can get the worker logs like this:

```bash
while true; do
    tools=$(docker container ls | grep -i worker | awk '{print $1}')
    if [ ! -z "$tools" ]; then
        echo "Found container: $tools"
        echo "Container logs:"
        docker logs --tail 10 "$tools"  # Show last 10 lines of logs
        echo "----------------------------------------"
    else
        echo "No matching container found..."
    fi
    sleep 1
done
```

Similarly, for any of the app logs, you can use the same command, but replace "worker" with the app name (this gives the shuffle tools logs):
```bash
while true; do
    tools=$(docker container ls | grep -i tools_1 | awk '{print $1}')
    if [ ! -z "$tools" ]; then
        echo "Found container: $tools"
        echo "Container logs:"
        docker logs --tail 10 "$tools"  # Show last 10 lines of logs
        echo "----------------------------------------"
    else
        echo "No matching container found..."
    fi
    sleep 1
done
```



## Resetting MFA
MFA can be enabled for your account on the settings User page of an organization, or on your [settings page](https://shuffler.io/settings). If you have lost access to your account due to this however, follow these steps:

**Cloud (shuffler.io):** Send an email to support@shuffler.io using the email you want MFA removed for.
**Onprem:** It's a bit more tricky onprem, as we'll need to modify the Opensearch database. Here is how:

1. Follow the backend logs WHILE logging into Shuffle to find your users' ID. It's a UUID in the format `550e8400-e29b-41d4-a716-446655440000`. 
```
docker logs shuffle-backend 
```

2. After you've identified the user id you want to remove MFA for, docker exec to get bash session into OpenSearch container or any other container so long as the said container can communicate to the Opensearch container 
```
docker exec -it shuffle-opensearch bash 
```

3. Once in the container from step 2 above, run the following command after modifying the USERID field.
```
curl -k -u admin:admin -H 'Content-Type: application/json' 'https://localhost:9200/users/_update/USERID' -d '{"doc": {"mfa_info.active": false, "mfa_info.active_code": "", "mfa_info.previous_code": ""}}'
```

4. Restart the backend server: `docker restart shuffle-backend`. This is to fix potential caching problems.

 

## Orborus backend connection problems
Due to the nature of Shuffle at scale, there are bound to be network issues. As Shuffle runs in Docker, and sometimes in swarm with k8s networking, it complicates the matter even further. Here's a list of things to help with debugging networking. If all else fails; reboot the machine & docker.

1. Is the Orborus container speaking to an IP in the same network? Check with docker inspect shuffle-oroburs -> is the same CIDR / network address to be seen in the list of Network IPs?
2. Do all the required networks exist?
   1. WITHOUT swarm: minimum 1 bridge network.
   1. WITH swarm: 3 networks (ingress, shuffle_shuffle, shuffle_swarm_executions). All in overlay mode.
3. Are all the networks configured properly? If in swarm mode; delete the networks, then restart Orborus (it will remake them).
4. Are the right network modes in use? Bridge (normal) vs Overlay (swarm). This depends on the server structure (1 vs. many).
5. Is net.ipv4.ip_forward=1 set in the /etc/sysctl.conf file? If not, add it to the file, then exit it and type `sysctl -p`. This allows network cards to talk to each other on the same machine.
6. Is DNS available inside the container? You can configure DNS in ALL docker containers on a server by editing this file: /etc/docker/daemon.json. To add DNS entries, add them as such:
```
{
    "dns": ["10.0.0.2", "8.8.8.8"]
}
```

"Fixes" (in order):
- Remake all networks (docker network rm)
- Restart Docker (systemctl stop -> start)
- Reboot (the whole server)

## Orborus can not reach backend
In certain cases there may be DNS issues, leading to hanging executions. This is in most cases due to apps not being able to find the backend in some way. That's why the best solution _if possible_ is to use the IP as hostname for Orborus -> Backend communication.

## Load all apps locally
In certain cases, you may have an issue loading apps into Shuffle. If this is the case, it most likely means you have proxy issues, and can't reach github.com, where [our apps are hosted](https://github.com/shuffle/python-apps).

Here's how to manually load them into Shuffle using git.

```
#1. If a proxy is required for your environment: Set up the proxy for Git (install if you don't have it).
git config --global http.proxy http://proxy.mycompany:80

#2. Go to the shuffle folder where you have Shuffle installed, then go to the shuffle-apps folder (./shuffle/shuffle-apps)
git clone https://github.com/shuffle/python-apps

#3. Go to the UI and hotload the apps: https://shuffler.io/docs/app_creation#hotloading_your_app (click the hotload button in the top left in the /apps UI)
```

**Alternatively:** You can go download [the latest Shuffle apps](https://github.com/Shuffle/python-apps/archive/refs/heads/master.zip) in your browser, and manually extract the `.zip` file into the `./shuffle/shuffle-apps` folder.


## How to stop executions in loop
1. Run **docker ps**
   ```
   CONTAINER ID   IMAGE                                     COMMAND                  CREATED       STATUS      PORTS                                                  NAMES
   869c99231ed0   opensearchproject/opensearch:latest       "./opensearch-docker…"   5 weeks ago   Up 2 days   9300/tcp, 9600/tcp, 0.0.0.0:9200->9200/tcp, 9650/tcp   shuffle-opensearch
   ```
1. Run **docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id**
   ```
   docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 869c99231ed0
   or
   docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' shuffle-opensearch
   ```
   Output:
   ```
   172.21.0.4
   ```
1. Run **curl -XDELETE http://<container_ip>:9200/workflowqueue-shuffle**
   ```
   curl -XDELETE http://172.21.0.4:9200/workflowqueue-shuffle
   ```
   Output:
   ```
   {"acknowledged":true}
   ```

## Abort all running executions of a specific workflow
Follow Python scripts allows to massively stop all running executions of a workflow
```python
import sys
import requests

API_ENDPOINT = "http(s)://<shuffle_endpoint>/api/v1"
API_KEY = "<your_api_key>"
WORKFLOW_NAME = "<workflow_name>"

def main():
    headers = {
        "Authorization": "Bearer " + API_KEY
    }

    with requests.get(API_ENDPOINT + "/workflows", headers=headers) as response:
        response.raise_for_status()
        data = response.json()

    wflows = list(filter(lambda wf: wf.get("name") == WORKFLOW_NAME, data))
    if len(wflows) == 0:
        print("Workflow not found")
        return 2
    if len(wflows) != 1:
        print("Something goes wrong")
        return 1

    wflow = wflows[0]

    # Get executions
    # example: http(s)://<shuffle_endpoint>/api/v1/workflows/b519c8f7-e9b0-4b47-b93d-cac013e4522f/executions
    wflow_id = wflow.get("id")
    url = "{}/workflows/{}/executions".format(API_ENDPOINT, wflow_id)
    with requests.get(url, headers=headers) as response:
        response.raise_for_status()
        data = response.json()

    still_running = list(filter(lambda ex: ex.get("status") == "EXECUTING", data))

    for exec in still_running:
        exec_id = exec.get("execution_id")
        print("[INFO] We're going to abort execution with ID {}".format(exec_id))

        url = "{}/workflows/{}/executions/{}/abort".format(API_ENDPOINT, wflow_id, exec_id)

        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            data = response.json()

        if data.get("success"):
            print("[INFO] Execution successfully aborted")
        else:
            print("[ERROR] Unable to abort execution")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```
Copy the script into a file called `abort_running_executions.py` and run it with
```
**Use python or python3 depending of your environment**
python abort_running_executions.py
```
In order to work _requests_ Python library must be installed in your Python execution env.

## Opensearch permissions error
![image](https://user-images.githubusercontent.com/21691729/124939209-d5694580-e000-11eb-8025-e2d475432e1b.png)
![image](https://user-images.githubusercontent.com/21691729/124939333-ec0f9c80-e000-11eb-9e56-5fbd06c7bfe3.png)
Set the ownership of the shuffle-database folder that the `shuffle-opensearch` container expects.
```
sudo chown 1000:1000 -R shuffle-database
```

## Delete user
**We recommend you to know what you're doing when you delete a user! It can have unpredictable consequences**

1. Find the ID of the user (Replace the username of your user in the query with the placeholder!)
    ```
    curl -X GET "https://localhost:9200/users/_search?pretty" -H 'Content-Type: application/json' -d' { "query": { "match": {"username": "<USERNAME>"} } } --insecure -u <opensearch_user>:<opensearch_password>
    ```

2. Find and take the "_id" value of your user from the returned!
    ```
    ...
    "_id" : "<user_id>",
    ...
    ```

3. Delete the user
    ```
    curl -X DELETE "https://localhost:9200/users/_doc/<user_id>?pretty" -H 'Content-Type: application/json' --insecure -u <opensearch_user>:<opensearch_password>
    ```

## Docker client version too new
If we run into "Failed to build: Error in Docker build: Error response from daemon: client version 1.51 is too new. Maximum supported APl version is 1.43" add the following environment variable into docker-compose under the backend section.

```- DOCKER_API_VERSION=1.40```


## Recover admin user
If you find yourself in a situation where you have forgotten your passowrd and need a reset for your user, you can reset your lost password in your local instance by doing the following: 
1. docker exec to get bash session into OpenSearch container `docker exec -it <container_id> bash`

2. Dump the results of users index query into `users.log` file
   ```
   curl -X GET "https://localhost:9200/users/_search?pretty" --insecure  -u <opensearch_user>:<opensearch_password> -H 'Content-Type: application/json' -d'
   {
       "query": {
           "match_all": {}
       }
   }
   ' > users.log
   ```
3. open the `users.log` file with `less` and search for the admin user. Once found, scroll down to the `apikey` section. this value will be the api key of the admin user.

4. I jumped onto another server within the same vlan as my Shuffle server but these could be ran on local host too. We will create a new user and update the user's role to admin with the Shuffle API.

5. (Optional step): If you have multiple organizations, Change active org like this and repeat for each org:

   ```
   curl 'https://ip of shuffle server/api/v1/orgs/{org_id}/change' \ -H ' "Authorization: Bearer {API_KEY}' --data-raw '{"org_id":"{org_id}"}'
   ```

6. Create a new user
   ```
   curl https://ip of shuffle server/api/v1/users/register -H "Authorization: Bearer APIKEY" -d '{"username": "username", "password": "P@ssw0rd"}'
   ```
7. Retrieve all the users and identify the user_id of the newly created user
   ```
   curl https://ip of shuffle server/api/v1/users/getusers -H "Authorization: Bearer APIKEY"
   ```
8. Assign the new user to the admin role.
   ```
   curl https://ip of shuffle server*/api/v1/users/updateuser -H "Authorization: Bearer APIKEY" -d '{"user_id": "USERID", "role": "admin"}' -X PUT
   ```
9. Log into webui with the new user, and you should now have admin rights.


## Useful OpenSearch Queries

### Find a user and their Orgs

```
curl -X GET "https://localhost:9200/users/_search?pretty"  -u <opensearch_user>:<opensearch_password> --insecure -H 'Content-Type: application/json' -d' { "query": { "match": {"username": "myuser"} } }
```

### Find all org

```
curl -X GET "https://localhost:9200/organizations/_search?pretty"  -u <opensearch_user>:<opensearch_password> --insecure -H 'Content-Type: application/json' -d' { "size": 10000, "query": { "match_all": {}}}'
```

Find all org IDs

```
curl -X GET "https://localhost:9200/organizations/_search?pretty"  -u <opensearch_user>:<opensearch_password> --insecure -H 'Content-Type: application/json' -d' { "size": 10000, "query": { "match_all": {}}}' | grep "\"id\" : \"" | sed 's/ *$//g' | sed 's/^[ \t]*//;s/[ \t]*$//' | uniq -u
```

## Extract all workflows

This procedure can help you extract workflows directly from OpenSearch even if the Backend and FrontEnd are in an awkward situation.

1. Extract the index info from OpenSearch. **NOTE:** You may need to create a bind mount for the location where the workflows will be extracted to.
   ```
   curl -X GET "https://localhost:9200/workflow/_search?pretty"  -u admin:StrongShufflePassword321! -k -H 'Content-Type: application/json' -d' { "size": 10000, "query": { "match_all": {}}}' > workflows.json
   ```
 
2. Script to separate all workflows

   ```
   import json
   import os
   
   data = {}
   
   with open("workflows.json", "r") as tmp:
       data = json.loads(tmp.read())
   
   foldername = "./workflows_loaded"
   try:
       os.mkdir(foldername)
   except:
       pass
   
   ## Will break  with keyerror lol
   for item in data["hits"]["hits"]:
       #print(item)
       try:
           item = item["_source"]
       except:
           continue
   
       filename = f"""{foldername}/{item["name"]}.json"""
       print(f"Writing {filename}")
       with open(filename, "w+") as tmp:
           tmp.write(json.dumps(item))
   
   ```
This script need to be run on the folder with the file `workflows.json`, it will create a `workflows_loaded` directory with all the workflows in it.
This can also be very useful to either backup a copy your work or export it from a lab to a prod instance.
* [Rebuilding an OpenSearch index](#rebuilding_an_opensearch_index)

## Rebuilding an OpenSearch index
If you lost an index due to corruption or other causes, there is no easy way to handle it. Here's a workaround we have for certain scenarios. What you'll need: access to another Shuffle instance, OR someone willing to share. Lets do an example rebuilding the environments index. This assumes opensearch is on the same server.

1. Cleanup the index
   ```
   curl -XDELETE http://localhost:9200/environments
   ```
1. Start refilling the index with info. For environments, make sure the "org_id" is correct according to the ID you can find in the /admin UI or the org index.
   ```
   curl -XPOST -H "Content-Type: application/json" "https://localhost:9200/environments/_doc"  -u <opensearch_user>:<opensearch_password> --insecure -d '{"Name" : "Shuffle","Type" : "onprem","Registered" : false,"default" : true,"archived" : false,"id" : "26ae5c79-a6f3-4225-be18-39fa6018cdba","org_id" : "49eeb866-c8b4-4ea0-bc19-9e650e3bba9e"}'
   ```
1. Check the index
   ```
   curl https://localhost:9200/environments/_search?pretty  -u <opensearch_user>:<opensearch_password> --insecure
   ```
   
## OpenSearch consumes too much memory
After narrowing down your problem to opensearch is what is consuming your system resources you need to figure out why? Might be too many indices in OpenSearch or just a java heap size problem

1. You'll need to list out all indices in elasticsearch opensearch.
   ``` 
   docker exec -u0 -it "opensearch_ID" curl https://localhost:9200/_cat/indices?pretty -k -u admin:StrongShufflePassword321!    ```
2. You could grep to narrow down on your search.
```
docker exec -u0 -it "opensearch_ID" curl https://localhost:9200/_cat/indices?pretty -k -u admin:StrongShufflePassword321! | grep -v security
```
3. Once you see what's causing the problem in our case it was workflowexecution which was at 13 gb. We deleted it using the below command.
```
docker exec -u0 -it "opensearch_ID" curl -X DELETE "https://localhost:9200/workflowexecution?pretty" -k -u admin:StrongShufflePassword321! -v
```

## Workflows are stuck

If you're on the default setup for shuffle and you start to notice that your workflows are getting stuck, It might be because you're running out of CPU needed to run the workflows. 

To fix this, You will have to move towards setting up shuffle for [production readiness](/docs/configuration#production_readiness) in our configuration documentation.


## Disclaimer
If you are doing this in a production server you will have to comb through the indices and delete them manually with respect to you organisations priorities, old executions and such.

4. You should notice a reduction in memory  consumption check this by running top. Do a docker-compose down then a docker-compose up -d for good measure and you are good to go. 

5. If the above steps do not fix the issue then this might mean its a java heap size issue, go into your docker-compose.yml file, move down till you locate the opensearch configurations and navigate to the OPENSEARCH_JAVA_OPTS settings and change them if initially they were running at 4 gb half that to 2 gb and save the file.

```
 - "OPENSEARCH_JAVA_OPTS=-Xms2048m -Xmx2048m" # minimum and maximum Java heap size, recommend setting both to 50% of system RAM
```
6. Do a docker-compose down then a docker-compose up -d. You should notice a difference in the memory consumption by Opensearch

## Updates failing
1. After an update, click CTRL+SHIFT+R on your keyboard while in your browser. This runs a hard refresh without cache.
1. Make sure you have the right version of Shuffle. Even if "nightly" is chosen, download them again with docker-compose pull or docker pull <image>
1. Ensure environment variables are defined properly for the misbehaving service.

## Database not starting
In certain cases, you may experience OpenSearch continuously restarting. PS: All of these can be spotted in the logs. There are a few reasons for this which should be checked in the following order:

1. Have you set `vm.max_map_count=262144` setting?
1. Did you change the folder ownership (`1000:1000` by default)?
1. Is the folder ownership a proper user (`1000:1000`) working?
1. Is there enough RAM on the device?
1. Is there enough storage space on the device?
1. Do you have security enabled (https & username & password), but not configured it in the `.env` file?


## TLS timeout error/Timeout Errors/EOF Errors
In certain cases, especially when you're running in swarm mode (Make sure ports: 2377, 7946 and 4789 between your machines **internally**), you may experience timeouts, EOFs. Or maybe, in different cases a TLS timeout error, or a similar network request issue. This is most likely due to the network configuration of your Shuffle instances not matching the server it's running on. 

The main configuration is "MTUs", AKA Maximum Transmission Unit. This has to match _exactly_ - with the both the docker network driver bridge and shuffle_swarm_executions.

Find the MTU of your preferred network interface:
```
ip addr | grep mtu
```
<img width="697" alt="Screenshot 2023-06-23 at 7 17 56 AM" src="https://github.com/Shuffle/Shuffle-docs/assets/60684641/b1aff6a8-7cae-4707-ac4a-cda1af484b79">

It is usually the network interface in the second line. Get it's MTU!

To set the MTU in Docker, do it in the docker-compose, in the networking section. Say the MTU you found was 1460, then use 1460, as can be seen below.
```
networks:
  shuffle:
    driver: bridge

    # uncomment to set MTU for swarm mode.
    # MTU should be whatever is your host's preferred MTU is.
    # Refer to this doc to figure out what your host's MTU is:
    # https://shuffler.io/docs/troubleshooting#TLS_timeout_error/Timeout_Errors/EOF_Errors
     driver_opts: # removed comment from here
       com.docker.network.driver.mtu: 1460 # removed comment from here.
```

Next, if you're running on swarm mode, delete the existing `shuffle_swarm_executions` network if it already exists. You can do that by using:

```
sudo docker network rm shuffle_swarm_executions
```

This might be an essential step to enforce what we did in the last step. Shuffle things a lot of things under the hood and syncing up the right interfaces is one of them so that you don't have to worry about it.

**If it requires removing dependant services, proceed to do that.**

When done, restart the docker-compose. Now the **issue should be automatically taken care of. If not, and you're on swarm mode, Proceed to the next step of manually setting the network MTU:**

We need to make a network named the same as the environment SHUFFLE_SWARM_NETWORK_NAME for Orborus (default: shuffle_swarm_executions):
```
docker network create --driver=overlay --ingress=false --attachable=true -o "com.docker.network.driver.mtu"="1460" shuffle_swarm_executions
```

If the issue still persists, Please look into changing the environment variable `SHUFFLE_SWARM_BRIDGE_DEFAULT_INTERFACE`. Shuffle takes care of syncing the docker0 bridge interface to the preferred interface of the container. Changing this value might help docker sync up things better. We assume that the interface name is "eth0" by default, which is the default setting.

If none of this works, Often times it's simply because of the virtualisation used by your cloud provider. For example, We have found these issues to be persistent with providers using VMware underneath, [Refer to this for a fix](https://portal.portainer.io/knowledge/known-issues-with-vmware)

## Shuffle on ARM
ARM is supported on Shuffle since 1.3.0!

## Permission denied on files 
In certain scenarios, permissions inside and outside a container may be different. This has a lot of causes, and we'll try to help figure them out below. Thankfully most fixes are relatively simple. To test this try to go to /admin?tab=files in Shuffle, and upload a file. If the file is uploaded and it says status "active", all is good. If it's not being uploaded, then it's most likely a permission issue.

![23 03 2022_22 51 18_REC](https://user-images.githubusercontent.com/31187099/160091632-3f5af407-1385-42bd-a2ab-01cabf456518.png)

#### Fix 1: share permissions.
In the docker-compose.yml file, find the "shuffle-files" volume mounted for the backend service. Simply add a ":z" on the end of it like so:
```
	- ${SHUFFLE_FILE_LOCATION}:/shuffle-files:z
```

Then restart the docker-compose (down & up -d), and try to upload a file again.

#### Fix 2: Selinux problems
Disable Selinux to test. This should take immediate effect (run as root). 
```
setenforce 0
```

After, try to upload a file again

#### See permissions on the inside of the container
To find the folder permissions inside the container
```
docker exec -u 0 shuffle-backend ls -la /
```


## Docker Permission denied 
In certain scenarios or environments, you may find the docker socket to not have the right permissions. To work around this, we've built support for the [docker socket proxy](https://github.com/Tecnativa/docker-socket-proxy), which will give the containers the same permissions. Another good reason to use the docker socket proxy is to control the docker permissions required.

To use the docker socket proxy, add the following to your docker-compose.yml as a service:
```
  docker-socket-proxy:
    image: tecnativa/docker-socket-proxy
    privileged: true
    environment:
      - SERVICES=1
      - TASKS=1
      - NETWORKS=1
      - NODES=1
      - BUILD=1
      - IMAGES=1
      - GRPC=1
      - CONTAINERS=1
      - PLUGINS=1
      - SYSTEM=1
      - VOLUMES=1
      - INFO=1
      - DISTRIBUTION=1
      - POST=1
      - AUTH=1
      - SECRETS=1
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - shuffle

```

When done, remove the "/var/run/docker.sock" volume from the backend and orborus services in the docker-compose. These containers should route their docker traffic through this proxy. To enable the docker rerouting, add this environment variable to both of them:
```
      - DOCKER_HOST=tcp://docker-socket-proxy:2375
```

This will route all docker traffic through the docker-socket-proxy giving you granular access to each API. 

PS: Adding :z to the end of the volume may fix this issue as well.

## Server is slow 
If the server Shuffle is running on is slow, it's likely due to the same constraints of any other server. One of these are typically the culprit:
- Disk space
- CPU
- RAM

The normal reason this happens is due to too many processes running concurrently in Docker (too many containers). To look at ideal configurations, look at [production readiness](/docs/configuration#production_readiness) in our configuration documentation. 

----------------------------------

First we check **CPU**. This is can be done using the "top" command.
```
top
```

The typical near the top is something like this. If the CPU usage is too high (see line three '%Cpu(s): 11.0 us'" - this means 11% is used total), you've most likely not configured Shuffle to run with the appropriate amount of containers as a maximum, with bad cleanup routines (CLEANUP=true). 
```
top - 20:14:37 up 27 days, 24 min,  2 users,  load average: 17.88, 15.17, 13.21
Tasks: 244 total,   2 running, 241 sleeping,   0 stopped,   1 zombie
%Cpu(s): 11.0 us, 10.7 sy,  0.0 ni,  2.0 id, 74.8 wa,  0.0 hi,  1.5 si,  0.0 st
KiB Mem :  8008956 total,   142236 free,  7561784 used,   304936 buff/cache
KiB Swap:  8257532 total,  4550684 free,  3706848 used.    69760 avail Mem 
```

Fix: Stop docker containers and reduce the amount that are allowed to run. If everything is TOO slow, reboot the server and stop all containers when it's started back up:
```
docker stop $(docker ps -aq) --force
```

---------------------------------

Next up is **RAM**. This is can also be done using the "top" command.
```
top
```

As with CPU, the information is near the top of your screen and looks something like this. If the RAM usage is too high (see line four 'KiB Mem :  8008956 total,   142236 free'" - this means that almost no memory is left on the device). This is a typical problem if you've enabled app log forwarding into Shuffle. To disable log forwarding, add the environment "SHUFFLE_LOGS_DISABLED=true" to Orborus, then bring it down and back up again.
```
top - 20:14:37 up 27 days, 24 min,  2 users,  load average: 17.88, 15.17, 13.21
Tasks: 244 total,   2 running, 241 sleeping,   0 stopped,   1 zombie
%Cpu(s): 11.0 us, 10.7 sy,  0.0 ni,  2.0 id, 74.8 wa,  0.0 hi,  1.5 si,  0.0 st
KiB Mem :  8008956 total,   142236 free,  7561784 used,   304936 buff/cache
KiB Swap:  8257532 total,  4550684 free,  3706848 used.    69760 avail Mem 
```

Fix: Stop docker containers and reduce the amount that are allowed to run. If everything is TOO slow, reboot the server and stop all containers when it's started back up:
```
docker stop $(docker ps -aq) --force
```

---------------------------------


Next up is disk space - can Shuffle save anything? See whether there is space on the machine in the location Shuffle is running
```
df -h
```

To get more space, either delete some files, clean up the Opensearch instance or add more disk space.




## How to handle wrong or bad images on old versions of docker.

![WhatsApp Image 2022-04-06 at 11 06 20 AM](https://user-images.githubusercontent.com/31187099/162938392-6d08bbba-df36-439b-a25e-c218bc88eade.jpeg)

Download the correct app version from shuffle cloud 

Once downloaded upload it on your onprem shuffle instance by dragging and dropping it on the activated app list

![upload app](https://user-images.githubusercontent.com/31187099/162938372-6d999a9b-efe8-4037-bca0-4b33e87f112c.png)

Once done check the server for misp images present

![list images](https://user-images.githubusercontent.com/31187099/162938324-a45ad395-d245-440c-a0c6-ce642b600600.png)

You should see previous existing images and the newly added apps image

The last step is to refer the target image to the source image that you uploaded

You do this by using the docker tag command see more information here (https://docs.docker.com/engine/reference/commandline/tag/)
docker tag frikky/shuffle:misp_1.0.0 davvyshuffle/shuffle:MISP-e72b9e9c5b0a40753e184c8ce0ba6c2b
i.e docker tag source_image:{TAG} target_image:{TAG}.

![docker tag](https://user-images.githubusercontent.com/31187099/162938293-519775fd-0455-4e5f-a9f5-00638a6d0b4b.png)

Go back to your shuffle interface and your app should run success.

If you intend on uploading the app in a remote server you could push the app image onto docker hub using the docker push command more info here(https://docs.docker.com/engine/reference/commandline/image_push/)

Sign up on docker here (https://login.docker.com/u/login/) then push the intended image into your docker hub repository, from your server's cli. You might be prompted to enter your password, do so and your image will be uploaded successfully.

![docker push](https://user-images.githubusercontent.com/31187099/162938270-3c43e748-bd6a-4fc9-a6fd-86e5d2385193.png)

![docker hub image](https://user-images.githubusercontent.com/31187099/162938242-d089acca-c65f-41b1-9cf1-dce80eb00403.png)

From your remote server cli pull the image from your docker hub repository. for more info about docker image pull see here (https://docs.docker.com/engine/reference/commandline/pull/)

![docker pull](https://user-images.githubusercontent.com/31187099/163127595-1ec69dc6-4e2a-4343-bd25-4cff67d94734.png)

Once this is done you have to tag the existing images of this app to the working app you just downloaded from your docker hub repo. 

![docker tag](https://user-images.githubusercontent.com/31187099/162938293-519775fd-0455-4e5f-a9f5-00638a6d0b4b.png)

  
 
## Docker not working
In certain cases, Docker may not be working due to too large an amount of containers running, and Docker not being able to keep up. The cause of this is typically Orborus starting too many workflows in unison. To fix this, either reduce the amount of containers able to run, or set up swarm mode (paid).
	
This can be controlled by the environment variables:
```
- SHUFFLE_ORBORUS_EXECUTION_TIMEOUT=600
- SHUFFLE_ORBORUS_EXECUTION_CONCURRENCY=10 
- CLEANUP=true
```

Then manually clean up the containers:
```
service docker stop
rm -rf /var/lib/docker/containers/*
rm -rf /var/lib/docker/vfs/dir/*
service docker start
```
	
**PS: You may need to use "systemctl stop docker" instead of using "service".**

Now restart the Shuffle stack again, and all the containers should be gone

## Troubleshooting for executions not running in swarm mode

* You'll need to check whether swarm is configured properly and running. Do this by orborus logs using the following command.

```
docker logs -f shuffle-orborus
```
* You should get results similar to the image below, if not check [here](https://shuffler.io/docs/configuration#shuffle_swarm_orborus_setup)

![Inkedswarm2_LI](https://user-images.githubusercontent.com/31187099/165058404-294b8231-e7ac-4141-8e39-6e51034b2f60.jpg)

* Once you've assertained that swarm mode is running as it should, go ahead and list services running in swarm using the below command.

```
docker service ls
```
* You should get results similar to the image below, the REPLICAS column should be AT LEAST 1 replica created for each running service. i.e A 0/1 means that the app isn't available to handle the executions that you need it to, so you'll have to reinstall the app, see [here](https://github.com/Shuffle/Shuffle-docs/blob/master/docs/troubleshooting.md#how-to-handle-wrong-or-bad-images-on-old-versions-of-docker) for more information on how to do this.

![Inkedswarm1_LI](https://user-images.githubusercontent.com/31187099/165058264-9d032d30-5250-4b13-929c-266308e8cb0b.jpg)

* Once you've ensured that all services have replicas created and are running, move on to the next step.

* Check logs for the worker. First, run the below command to get a list of tasks that are running 

```
docker ps
```
![Inkedswarm3_LI](https://user-images.githubusercontent.com/31187099/165058479-f5e0eab5-f117-4f96-aee4-04bd31c4ecc6.jpg)

* Get the name of the worker and run the following command. If not, this means you will have to go on local of each node to get logs of workers running on it or using a docker management tool.


```
docker logs <name_of_worker>
```
* All you have to do now is comb the logs and identify where the problem is, if you can't figure out where the problem is reach out to our community on discord.

## Find code OpenAPI app 
You may have had problems with an app and need some help getting it fixed. Apps created in the app creator of Shuffle also do generate underlying Python code utilizing the same capabilities as if you make a Python function from scratch. Here's how to find the code for a function.

1. Decide on an app to find. In our example, let's use "DefectDojo". 
Start by finding the Docker image:
```
docker images | grep -i defectdojo
```

2. From the list above, you should see an image called "Defectdojo". The next step is to run it and extract the code. Copy the name of it, then type this:
```
docker run <imagename> cat app.py > app.py
```

3. You should now have a file called "app.py" locally. Now lets say the function you're having trouble with is called "importscan create". In the app.py file we just created, go into it, and search for that exact name. All spaces ( ) and dashes (-) have been turned into underscores (_), and all text is LOWERCASE. The line should start with something akin to:
```
def post_importscan_create(self,...)
```

Copy everything indented under this function and sent to support@shuffler.io for further help!

## Tenants/Suborgs seem to be lost

If you loose your tenants/suborgs for any reason at all and you need to reinstate them then you will need to do the following;

1. Get the org id's from your backend logs. It's a UUID in the format `550e8400-e29b-41d4-a716-446655440000`. 
```
docker logs shuffle-backend 
```

2. After you've identified the org id's for the orgs you want to reinstate, docker exec to get bash session into OpenSearch container or any other container so long as the said container can communicate to the Opensearch container 
```
docker exec -it shuffle-opensearch bash 
```

3. Once in the container from step 2 above, run the following command.
```
curl -k -u admin:StrongShufflePassword321! -H 'Content-Type: application/json' 'https://shuffle-opensearch:9200/organizations/_update/<org_id goes here>/' -d '{"doc": {"id": "org-id-goes-here", "name": "org-name-goes-here"}}'
```

4. Exit out of the container

5. Restart docker
```
$docker-compose down
$docker-compose up -d
```
Go back to your shuffle instance and you should see the org in question reinstated in the tenants tab. 

## Find top index items opensearch (NOT FULLY DISCOVERED YET)
As the Opensearch index may fill up over time, it is important to be able to debug the the available indexes. One particular issue we have had has been that it takes >60 seconds to load apps onprem at times. Here is how to resolve them.

Get into the Opensearch container of port 9200 is not exposed by default:
```
docker exec -u0 -it shuffle-opensearch bash
```

[Get the indexes and look at them:](https://opensearch.org/docs/latest/api-reference/cat/cat-indices/)
```
curl https://localhost:9200/_cat/indices?v -u admin:StrongShufflePassword321! -k
```

Find the largest items in the workflowapp index (for apps in shuffle):
```
curl https://localhost:9200/workflowapp/_search?v -u admin:StrongShufflePassword321! -k
```

Delete an index if it's too large (normal ones to delete if problems: workflowexecution, workflowqueue-shuffle, environment_stats) 
```
curl -XDELETE https://localhost:9200/workflowqueue-shuffle -u admin:StrongShufflePassword321! -k
```

## Add user to lost org
If you have lost access to Shuffle, it usually due to an unforeseen disconnect to the Database during startup, leading to more Organizations being added. To fix this, your user needs to be re-added to the original Organization

Find the Organization and User Id of your account. They are in the UUID format `550e8400-e29b-41d4-a716-446655440000`
```
docker logs -f shuffle-backend
```

Get into the Opensearch container of port 9200 is not exposed by default:
```
docker exec -u0 -it shuffle-opensearch bash
```



Update the USERID and ORGID, ORGNAME fields, then run this command to re-add your account to the right org
```
curl -k -u admin:StrongShufflePassword321! https://localhost:9200/users/_update/USERID -d '{"doc": {"active_org.id": "ORGID", "active_org.name": "ORGNAME", "orgs": ["ORGID"]}}' -H "Content-Type: application/json"
```

## No module named 'xyz' in 'execute python' (Shuffle Tools)

If you want to install a custom module like pandas (although, 'execute python' isn't made for heavy processing. We recommend making a custom python app for it).

There are two primary ways to it:
1. Learn about dynamic library loading in your code (not recommended)
2. Build the Shuffle Tools app again locally and add the libraries you want to it! Library configuration is over in this [requirements.txt file](https://github.com/Shuffle/python-apps/blob/master/shuffle-tools/1.2.0/requirements.txt)




To build this app again, I would:
- Add in the requirement in requirements.txt linked above.
- Rebuild the app again by doing:




```bash
sudo docker build -t shuffle-tools:1.2.0 .
```

### Changing timestamps for an index from Unix to timestamps
This may be necessary if you want to do additional modifications or exploration of an existing Index. [See this Issue on how it was fixed by a Shuffle user](https://github.com/Shuffle/Shuffle/issues/1531#issuecomment-2440021952).
