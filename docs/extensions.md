# Shuffle extensions
This is documentation for integrating and sending data from third-party services to Shuffle. Not to be confused with [apps](/apps) and [workflows](/workflows)

## Table of contents
* [Introduction](#introduction)
* [Single Signon (OpenID/SAML)](#single-signon-sso)
  * [Okta](#okta)
  * [Google SSO - SAML](#google-saml-sso)
  * [Auth0](#auth0)
  * [PingIdentity](#ping-id)
  * [Keycloak - OpenID](#keycloak)
  * [Azure AD - OpenID](#azure-ad)
  * [Other SSO providers](#other)
  * [Testing SSO](#sso-testing)
* [Detection Manager](#detection-manager)
* [KMS](#KMS)
* [Native Actions](#native-actions)
* [Webhooks](#webhooks)
  * [Wazuh Webhook](#wazuh)
  * [TheHive Webhook](#thehive)
  * [Logz.io Webhook](#logzio)
  * [MISP forwarder](#misp)
  * [AWS S3 forwarder](#aws-s3-forwarder)
  * [QRadar Webhook](#qradar)
  * [FortiSIEM Webhook](#fortisiem)
  * [ELK Webhook](#elk)
  * [Cortex Webhook](#cortex)
  * [Splunk Webhook](#splunk-siem)
  * [Eventlog Analyzer - SIEM](#eventlog-analyzer)
  * [ServicePilot - SIEM](#servicepilot-siem)

## Introduction
From the start, Shuffle has been a platform about integrations. We've focused on making them as open and usable as possible, but were missing one part; inbound data. The general way Shuffle handles this has been through third-party API's, where we poll for data on a schedule. There are however some cases where this doesn't do the trick. That's what extensions are. 

These integrations will typically entail third party services connecting to Shuffle with inbound Webhooks as triggers in a workflow.

## Single Signon
Shuffle added Single Signon (SAML v1.0) from Shuffle version 0.9.16 & OpenID in Shuffle version 1.0.0. This allows you to log into Shuffle from other identity platforms, entirely controlled by you. SSO is available for **onprem AND cloud**. It works by setting an Entrypoint (IdP) and X509 Certificate, both used to validate who the requester is. This can be added in [your admin panel](/admin). 

### Org Swapping behavior
If an Organization requires SSO, it will FORCE you through the SSO login unless your session already has been through SSO for that organization. This may feel counter-intuitive at first, but is a required system as each organization is controlled for SSO individually, and there is no limit to how many organizations a user can have.

### Using ANY SSO platform 
**ONPREM ONLY:** You will have to change the SSO_REDIRECT_URL variable in the .env file to match your front end server link i.e `SSO_REDIRECT_URL=http://<URL>:<PORT>` 

![Single Signon button](https://github.com/frikky/shuffle-docs/blob/master/assets/sso-3.png?raw=true)

**How it works:**
- Every user gets the role "user" by default.
- If the user DOESN'T exist, it will be created, based on an identifier provided from the SSO provider.
- If the user DOES exist, it will simply log them in.
- After login, each user is redirected to /workflows as per a normal login.

**PS**: In some cases, the persons' username may be appear an ID in Shuffle. If so, an admin should login to Shuffle and change their username. SSO should still work.
**PPS**: The callback URL/redirect URL/recipient URL is `https://<URL>:<PORT>/api/v1/login_sso`

![Single signon configuration](https://github.com/frikky/shuffle-docs/blob/master/assets/sso-1.png?raw=true)

### Okta
To use Okta SSO with Shuffle, first make an app in Okta. Their guide for making an app [can be found here](https://developer.okta.com/docs/guides/build-sso-integration/saml2/create-your-app/). 

Once an application is made, it's time to find the required information. Go to the app > Sign On > Click "View Setup Instructions" under SAML 2.0. This will open a new page with the credentials.
![Okta SSO setup](https://github.com/frikky/shuffle-docs/blob/master/assets/sso-2.png?raw=true)

**Move these fields over to Shuffle:**
* Identity Provider Single Sign-On URL 	-> SSO Entrypoint (IdP)
* X.509 																-> SSO Certificate (X509)

After adding them, click "Save", saving the configuration. After saving, log out of your user to verify the SSO configuration. If you don't see a button for "Use SSO", you most likely configured the wrong organization.

### Google SAML SSO
• Log in to your Google Workspace portal as admin -> Apps -> Web and mobile apps.

• Click Add app -> Add custom SAML app.

• In the popup window, enter shuffle as the name of the app, you can upload the app icon here as well. Then click continue.

• The next page will provide the IDP data. Download IdP metadata then click continue.

• Next page will be the SP information, this is where you should provide the Single Sign On URL, and SP Entity ID.

	- ACS URL : 
 		- For Cloud : https://shuffler.io/api/v1/login_sso
		- For On-prem: https://<your-ip>:3443/api/v1/login_sso	
	- Entity ID : shuffle-saml
	- Name ID: Basic Information > Primary Email
 ![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/7958a55b-c932-4b5c-8910-dfb42703b695)

 •	The next page is where you add the below attributes and click on Finish and the app is added to the Google Workspace.
 ![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/2bd0c217-de1c-41a4-82b9-7672ed2a4984)

 •	After completing the app creation on Google Workspace. You can select the shuffle app under the "Web and mobile apps". Click on the shuffle app, and note 
        the SPID in the URL, that is the SPID that will be needed.

 ![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/cfd1fc98-8efe-4aa2-a4af-4ea60d10a3d6)

 •	Now we configure the Google SAML SSO in shuffle portal. Log in to your Shuffle web portal.
 
 •	 Click on profile  -> Admin --> Edit Details --> Now add the Entrypoint (IdP) and SSO Certificate under the SAML SSO and click on save.

  **Note : The IdP metadata contains the Idp ID and certificate. Use this link as your SSO entry point, substituting your SP ID for "YourSPID" and your IDP ID for "YourIDPId."**
 
         - SSO Entrypoint (IdP) : https://accounts.google.com/o/saml2/initsso?idpid=C0ivw&spid=634181550209&forceauthn=false

### Auth0 
To use Auth0 SSO with Shuffle, first make an app on [https://manage.auth0.com](https://manage.auth0.com). Documentation can be found [here](https://auth0.com/docs/configure/saml-configuration/configure-auth0-saml-identity-provider).

After the app is made, click "Addons" > "SAML2 Web App". 
![Auth0 SSO setup](https://github.com/frikky/shuffle-docs/blob/master/assets/sso-4.png?raw=true)

**In the popup, move the data of these fields to Shuffle:**
* Identity Provider Login URL 				-> SSO Entrypoint (IdP)
* Identity Provider Certificate 			-> SSO Certificate (X509)

Open the Certificate file in a text editor, and copy it's contents.

After adding them, click "Save", saving the configuration. After saving, log out of your user to verify the SSO configuration. If you don't see a button for "Use SSO", you most likely configured the wrong organization.

### PingIdentity 
To use PingID SSO with Shuffle, first make an app on [https://console.pingone.eu/](https://docs.pingidentity.com/bundle/pingoneforenterprise/page/xsh1564020480660-1.html). Documentation can be found [here](https://docs.pingidentity.com/bundle/pingoneforenterprise/page/xsh1564020480660-1.html).

After the app is made, click the dropdown for it on the right side > Configuration > find these fields.
![PingID SSO setup Shuffle](https://github.com/frikky/shuffle-docs/blob/master/assets/sso-5.png?raw=true)

**In the view above, move the data of these fields to Shuffle:**
* INITIATE SINGLE SIGN-ON URL 			-> SSO Entrypoint (IdP)
* DOWNLOAD METADATA 								-> SSO Certificate (X509)

Open the Certificate file in a text editor, and copy it's contents in the field.

After adding them, click "Save", saving the configuration. After saving, log out of your user to verify the SSO configuration. If you don't see a button for "Use SSO", you most likely configured the wrong organization.

### Keycloak
Open ID SSO setup with Keycloak:
- Click on clients 
- Create new client
- Set client id 
- Ensure client protocol is openid-connect
- Hit save

You now have a client. Click on settings and configure them as follows
- Your client ID
- Set up a name
- Client Protocol set to openid-connect
- Access Type set to public
- Standard Flow Enabled toggled to ON
- Direct access grants toggled to ON 

![Valid redirect URI](https://user-images.githubusercontent.com/31187099/162692070-ccc54692-6793-4331-adc7-2356d0fd5397.jpg)

For the Valid Redirect URI https://shuffler.io/api/v1/login_openid

- Backchannel Logout URL https://shuffler.io/*
- Backchannel Logout Session toggled to ON

Under the Fine Grain OpenID Connect Configuration.

Valid Request URIs https://shuffler.io/login?autologin=true

![Auto login = true](https://user-images.githubusercontent.com/31187099/162692186-6ac71b93-01be-4cb1-83f4-b7cb17758378.jpg?raw=true)

Once this is done head over to your shuffle instance.
1. Click on Admin button
2. Scroll down and click on the downward facing arrow beneath Organization overview
3. Scroll down again to OpenID connect
4. Fill in the client ID (It should be the same as what you entered in Keycloak)
5. Authorization URL http://<Your_Keycloak_URL>:<port>/auth/realms/openid/protocol/openid-connect/auth
6. Token URL http://<Your_Keycloak_URL>:<port>/auth/realms/openid/protocol/openid-connect/token

![OIDC shuffle-side](https://user-images.githubusercontent.com/31187099/162689392-51fcb2e9-3d89-4066-8b99-6074065f9c2a.png?raw=true)

If you keep getting redirected to your backend url, head on to your Shuffle folder on your server.
1. Vim .env

![vim env](https://user-images.githubusercontent.com/31187099/164943744-981638cf-6149-42e1-a455-3d12927ec24c.png)

2. In vim change the BASE URL to your server link; i.e SSO_REDIRECT_URL=http://<URL>:<PORT>

![baseurl](https://user-images.githubusercontent.com/31187099/164943748-96217836-6b7d-42e7-8c25-fae3d3294b30.png)

Finally go back to shuffle and use SSO button to login.

![shuffle SSO](https://user-images.githubusercontent.com/31187099/162689445-8db0766c-6f18-4463-8a92-f6ae62213918.png?raw=true)

Assigning a Role from Keycloak to Shuffle for a New User

If you want to assign a Shuffle organization role (`admin`, `user`, `org-reader`) from your Keycloak client, you can achieve this using the following method:

Steps to Assign Roles

1. In your Keycloak client, create three new roles with the names `shuffle-admin`, `shuffle-user`, and `shuffle-org-reader`, as shown in the image below:

   ![image](https://github.com/user-attachments/assets/e8a1f344-73c9-453d-b119-aef4643610b4)

2. After creating the roles, assign them to the users you want. The `shuffle-admin`, `shuffle-user`, and `shuffle-org-reader` roles in Keycloak correspond to the `admin`, `user`, and `org-reader` roles in Shuffle.

3. Once the roles are assigned to users, navigate to:

   **Client Scopes** → **Roles** → **Mapper** → **Client Roles**

   On the **Client Roles** page:

   - Update the `Token Claim Name` to `roles`
   - Enable the option **"Add to ID Token"** so that the roles are included in the response.

   ![image](https://github.com/user-attachments/assets/09582542-efa1-429b-9d45-e0a3796c6fbd)

 Important Notes:

- After completing these settings, all newly created users will be assigned roles based on their Keycloak roles. If no role is assigned, the default role will be `user`.
- As of now, role assignment is only applied to newly generated users. If a user already exists in Shuffle, changing their role in Keycloak will **not** update their role in Shuffle.  
  In this case, you can manually change the user's role from the `https://shuffler.io/admin?tab=users` page.

  

### Azure AD
To use OpenID with Azure AD, Shuffle supports OpenID connect with the use of Client IDs and Client secrets. To set up OpenID Connect with Azure, we use "ID_token" authentication. This entails a few normal steps regarding app creation in Azure App Registration.

1. Set up an app in Azure AD with ID tokens enabled
Go to [app registrations and create a new app](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade). Make it use "Web" for redirect URI's and direct it to your Shuffle instance at /api/v1/login_openid. From here, make sure to go to "authentication" and enable "ID Tokens"
![image](https://user-images.githubusercontent.com/5719530/169712651-24f481bc-7d90-4b09-b25f-cd1ec6c52c20.png)

2. Get the Client ID, Client Secret and your Tenant
Start by generating a client secret. Keep it safe, as we'll use it later. 
![image](https://user-images.githubusercontent.com/5719530/169712756-a07ae08f-75a6-4174-8c8a-26700fd48654.png)

The client secret and tenant ID can be found in the "Overview" tab:
![image](https://user-images.githubusercontent.com/5719530/169712793-7173a2c5-3450-4a79-8f95-9363b940c293.png)

3. Go to the admin panel in Shuffle and put in the Client ID and Secret
![image](https://user-images.githubusercontent.com/5719530/169712842-83db0618-d1f2-4bcd-ad78-5276f0c0696a.png)

4. Put in your Tenant ID in the authorization URL
The URL is as such: `https://login.microsoftonline.com/TENANT_ID/oauth2/v2.0/authorize`. The Token URL is not strictly required for ID Token auth.
![image](https://user-images.githubusercontent.com/5719530/169712857-fe49855e-da3a-4dca-9fde-59bdc60eaa4d.png)

5. In the "Token Configuration" tab on the left, click "Add Optional Claim." Select the token type as "ID" and choose "email" as the claim, then click "Add."
![token_configuration](https://github.com/user-attachments/assets/2f3b62b9-23a6-4404-a6c6-2dfd796a0b2d)
	
7. Done! Click save and log out. Try your new login based on your Azure AD configuration. 
	
PS: When a user signs in, they are granted the access rights of a "user" within the designated organization. The username will be derived from the email address listed in the Azure users list. Therefore, when creating or adding a new user in Azure, ensure that the email field in their profile is populated. If this email field is empty, the user will not be able to log in to the organization.
	
### Other Platforms
As long as you can create an identity and acquire an Entrypoint (IdP) and X509, paste them into the Shuffle fields, and it should work with any SAML/SSO provider.

### Testing SSO

Testing Single Sign-On (SSO) ensures that your SSO setup is functioning correctly. When you click the "Test SSO" button, you will be redirected to your SSO authentication page. After authentication, you will be redirected to `https://shuffler.io/workflows` if you are using the cloud version, or `https://frontend-url/workflows` if you are using the on-premises version. There are two test cases to verify the SSO feature:

1. **User Change During Authentication**: If you log into your Shuffle account with username "A" and authenticate with username "B", your user will change to "B". If user "B" does not exist in the organization, they will be added. The video below demonstrates logging into Shuffle with "lalitdeore12@gmail.com" and authenticating with Azure username "lalitdeoretest@lalitdeore12gmail.onmicrosoft.com" (which has the email "lalit@shuffler.io"). After authentication, the user changes from "lalitdeore12@gmail.com" to "lalit@shuffler.io".

https://github.com/user-attachments/assets/8c3474a5-bfdd-4c68-bd59-0b7b1ddb2b0c

2. **User Remains the Same During Authentication**: If you log into Shuffle with user "A" and authenticate with the same user "A", your user will not change. The video below shows logging into Shuffle with "lalitdeore12@gmail.com" and authenticating with the same user in Azure. After authentication, the user remains unchanged.

https://github.com/user-attachments/assets/0a927283-d39e-4200-8ba3-654ef6f1b9c1

**Note**: Ensure that the "email" field is included in the SSO response from your SSO provider. If this field is empty, you may encounter errors. The email from your SSO provider will be assigned as the username in Shuffle.



### How to Assign a Role to a New User from an SSO Provider (OpenID Connect) in Shuffle  

If you want to assign a role to a user from an SSO provider, you can do so using the following method:  

1. Create three roles in your SSO application/client:  
   - `shuffle-admin`  
   - `shuffle-user`  
   - `shuffle-org-reader`  

2. Assign one of these roles to new users when granting them access to the application/client.  
   - The `shuffle-admin`, `shuffle-user`, and `shuffle-org-reader` roles in your SSO provider correspond to the `admin`, `user`, and `org-reader` roles in Shuffle.  

3. Ensure that the `roles` claim is included in the **ID token** response from your SSO provider.  

After completing these steps, all newly created users will be assigned roles in Shuffle based on their assigned role in the SSO provider.  

- If none of the specified roles are assigned, or if the `roles` claim is missing, the user will be assigned the default role: **`user`** in Shuffle.  

Important Notes  

1. Currently, this feature is only available for **OpenID Connect**. Support for **SAML SSO** may be added in the future.  
2. At this time, role assignments only apply to newly created users. If a user already exists in Shuffle, changing their role in the SSO provider **will not** update their role in Shuffle.  
   - To manually update an existing user’s role in Shuffle, please visit the **Shuffle Admin Page**:  
     [Shuffle Admin Page](https://shuffler.io/admin?tab=users)  

If you have any questions or need further assistance, please feel free to reach out to us at **[support@shuffler.io](mailto:support@shuffler.io)**. 


## Detection Manager
The Shuffle Detection Manager is a system introduced in beta in December 2024, allowing Shuffle to work with platforms like Tenzir and other systems to help with Detection Engineering. The goal of the system is not to replace actual detection systems themselves, but to offer a centralized way to control Detection rules across tenants and different tools. As an example, **below is a focus on Sigma rules with Tenzir**. The system is tested with Yara rules, Email detection rules and custom rule systems.  

### Testing Tenzir + Sigma
1. **Rule Manager:**      At least One Shuffle org
2. **Job Handler:**       An Orborus instance running
3. **Detection Handler:** A Tenzir instance running on the same server as Orborus **(no setup needed)**
4. **Log Forwarder:**     Any system that can forward logs to Tenzir

To test the Tenzir detection system, it is first important to ensure that your Orborus instance is attached to Shuffle, which can be found on the /admin?tab=Locations path. Below is a BAD instance, where Orborus both says "Stopped" AND Pipelines is crossed out. The first goal is to re-enable these.

<img width="791" alt="A bad instance that is not running" src="https://github.com/user-attachments/assets/263975bf-7e07-4675-bc67-ac308e69ec76" />

### Fixing the pipeline setup
To solve the pipeline issue shown in the previous image, we have to do two things:

1. Start Orborus and get it to the "Running" state. To do this, click the Location in question and copy the command to one of your servers. After this has been done, you should see a the Red "Stopped" part change to a Green "Running" box as in the image below. If this does not occur, reach out to support@shuffler.io. 
2. Go to /detections/Sigma in the UI, and click "Connect" in the top-right corner. Refresh the page after a minute or so, and the Pipeline system should be showing as green on the [Location page](https://shuffler.io/admin?tab=Locations) and in the top-right corner of the [Detection page](https://shuffler.io/detections/Sigma). If it does not, please reach out to support@shuffler.io.

<img width="791" alt="image" src="https://github.com/user-attachments/assets/ba35c94c-cedc-4ae5-8b38-0855f7cd5c11" />

Tenzir setup configuration:
- **Adding a custom storage folder for Sigma rules:** Mount in the folder you want to control into the Orborus command. Then add the environment variable `SHUFFLE_STORAGE_FOLDER=/tmp/foldername` to Orborus. The default is `/tmp/`. 
- **Connecting to an external Tenzir node:** Add the following environment variable to the Orborus command: ``. This requires that [the web API is enabled](https://docs.tenzir.com/rest-api) on the node.

```
If ran locally with systemd:
1. Open /etc/systemd/system/tenzir-node.service
2. Find the line that says "ExecStart" and add ' --commands=web server --mode=dev --bind=0.0.0.0' to the end of it

It should look like this: ExecStart=/opt/tenzir/bin/tenzir-node "--commands=web server --mode=dev --bind=0.0.0.0"

3. Save and close the file.
4. systemctl daemon-reload & systemctl restart tenzir-node
5. Try to connect to it: curl http://localhost:5158/api/v0/ping
```

- **Control the Shuffle Tenzir node from Tenzir Cloud**: Go to [Tenzir Cloud](https://app.tenzir.com) and create a node configuration. Download the configuration file, then add the variables found in it to the following environment variables to Orborus: `TENZIR_PLUGINS__PLATFORM__API_KEY=<apikey>`, `TENZIR_PLUGINS__PLATFORM__CONTROL_ENDPOINT=<url>`, `TENZIR_PLUGINS__PLATFORM__TENANT_ID=<tenant>`

### Mounting the Tenzir Sigma location into Orborus
1. You need to mount in the folder that is going to store the sigma rules, controlled from within Shuffle
2. The default location is /tmp/sigma_rules, so to mount it in, use `--volume "/tmp:/tmp"` in the Dockerfile.
3. If you end up changing the storage location, use the `SHUFFLE_STORAGE_FOLDER` environment variable with the full path.

### Running the Tenzir Detection pipeline
- [Sigma Pipelines with Tenzir](https://docs.tenzir.com/tql2/operators/sigma)

### Running a sample Detection
TBD

### Storing Tenzir logs in Opensearch
- [Tenzir -> Opensearch documentation](https://docs.tenzir.com/integrations/opensearch)

## KMS
Shuffle by default allows you to store authentication tokens within Shuffle itself, which are encrypted in the database. Since February 2024, we additionally support the use of external KMS systems to handle authentication, which is based on [Native Actions](https://shuffler.io/docs/extensions#native-actions) and [Schemaless](https://github.com/frikky/schemaless). Native Actions run in the background to perform the "Get KMS key" action, and the run of the app is NOT stored. 

The Shuffle KMS system is built as a third party Key:Value provider. You can reference keys from the KMS in any field marked as "Authentication" in the UI, or from within a Shuffle authentication itself (meaning you can authenticate the authentication..). The way you reference the keys is path-based, starting with `kms/`. Requirements:

* Have an Authentication called **kms shuffle storage** in Shuffle. On the [Auth page](/admin?tab=app_auth), it should clearly stand out as a different type of authentication.
* The Authentication needs to be associated with an App in the IAM category
* The App needs to have an action labeled as "Get KMS key"
* If it's the FIRST translation, it may fail out without internet access to github.com

When these requirements are fullfilled, you can do the following to use the KMS system:

* Find the required parameters for the action. The first image below shows the parameters IN ORDER for Hashicorp Cloud Platform Vault.
* Use the following format: `kms/field1/field2/field3/field4/...`. This NEEDS to start with `kms/`
* Make sure the Environment is correct. It uses your default environment to connect to the KMS if not otherwise specified on the [Auth page](/admin?tab=app_auth). 
<img width="919" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/ba69ec4a-2206-4f30-9ee2-0d94390a9dde">

* Example referencing the "username" in the app name "Jira": `kms/998067a9-33f2-4c4d-bbb6-4a997d784def/2e9a877f-1a89-4394-a242-f2c6d9dd2420/jira/username`
<img width="617" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/0b354dc6-1d8e-4366-9f38-2cff2fe94486">

If all of this is fulfilled, you can run the workflow, and Shuffle will automatically reference the KMS correctly. **If it fails to authenticate**, you should see a Notification show up like in the following image.

<img width="989" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/8a24c8f1-c00d-4481-bf56-ece2b7749fed">

### Failure handling and Debugging
During the initial configuration of KMS, there are many things that CAN go wrong. After the setup is initially completed and it works, it should not fail again, meaning spending time to set it up properly the first time is well worth it.

If you are using Shuffle onprem and have trouble with KMS translations, we suggest setting the environment variable `SHUFFLE_KMS_DEBUG=true` on the shuffle-backend container. This will allow you to test individual keys in ANY field, meaning you can e.g. print out the KMS value that it should translate to. This further means we will not be deleting the KMS execution, and you can see the execution on the [Workflow Runtime Debugger page.](/workflows/debug). **KMS debug mode is NOT enabled on shuffler.io**.

<img width="275" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/b93fd28d-cb92-4a56-a9f3-9b2cd7a96d32">

If your KMS translation fails, it is most likely due to network connectivity OR translation errors [for the standard](https://github.com/Shuffle/standards/blob/main/translation_standards/get_kms_key.json) in use. After running a translation, you should see the following three file categories in the admin panel:
- translation standards 	- The available translation standards
- translation input		- The data FROM the kms used for translation. Does NOT contain values, only keys.
- translation output		- The translation OUTPUT. Includes JSON paths to the correct keys

IF your translation fails, the first area to look at is the "[translation output](/admin?tab=files&category=translation_output)" file category, as this is where the translation for the schema happens. The hash will match the data you have sent in, which can be found in the "translation input" folder. Documentation about schemaless explains [how translations happen](https://github.com/frikky/schemaless?tab=readme-ov-file#example), and how they can be fixed. If you need further help, contact support@shuffler.io

A valid KMS translation file should be in the following format:
```
{
   "kms_value": "path.in.kms.json"
}
```

**The "kms_key" field is NOT relevant - the ONLY thing that is important is that the kms_value path is correct.**

### Using any KMS
KMS is supported for any system as long as the sections above are covered. It has been tested for the following:

- Microsoft Azure KMS 
- Hashicorp Vault
- Google Cloud Key Management
- AWS Key Management Service
- Hashicorp Cloud Platform
- Github
- AliCloud
- ... and more! Ask if you need help.

## Native Actions
Native Actions are a new way Shuffle interacts with data, built brick by brick since introducing Shuffle's Integration Layer API in late 2022. The goal of Native Actions is to enable ourselves and others to be able to perform actions towards a specific API, without necessarily know how to do it specifically for that system. 

As of early 2024, this system is in active development, and we will implement features with it and help third party platforms do the same throughout the next few years.

**Example usecases:**
- Listing assets from your asset management system/CMDB to make a list of assets, without needing to know the Assets' API
- Blocking an Endpoint without knowing how to use the EDR API. Add this as a button to the list from the previous usecase
- Shuffle Notification Workflow: Get notifications directly to your ticketing system with minimal configuration

<img width="736" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/d9c5831c-af53-4bd2-9b34-7dd8c2daab32">

The Native Actions system is based on [generative AI for automatic mapping of fields (Schemaless)](https://github.com/frikky/schemaless), uses Github to [store configurations (Standards)](https://github.com/shuffle/standards), and uses [Shuffle's Integration Layer API](https://shuffler.io/docs/API#integration-layer) to run the actions. 

## Inbound Webhooks
This section describes inbound webhooks to Shuffle, and how to set them up in many commonly used third-party systems. If your system support outbound Webhooks, it can also forward to Shuffle as a GET or POST request. [More about webhook triggers](/triggers/#webhooks)

### Wazuh
Wazuh is a SIEM platform for security operations. We've used it through their API multiple ways, but were missing an important component; alerting. That's why we've developed a simple alert forwarder from Wazuh to Shuffle. 

[Wazuh extension documentation](https://documentation.wazuh.com/current/user-manual/manager/manual-integration.html)

**PS: If you expect more than 10 alerts per second, you should add multiple workflows AND webhook forwarders to Wazuh**

These are the steps to set it up:
1. Create a Workflow which will receive alerts
2. Add a Webhook to the Workflow
3. Configure Wazuh with the Webhook URL
4. Test the integration

**1. Create a Workflow which will receive alerts**
This one is pretty easily explained. Go to Shuffle an make a new Workflow.

**2. Add a Webhook to the workflow**
[Add a webhook](/docs/triggers#webhook) and find the Webhook URL. Remember to start the Webhook!

![Extend Shuffle with Wazuh](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_1.png?raw=true)

Copy the URL and keep it for the next steps
![Extend Shuffle with Wazuh 2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_2.png?raw=true)

**3. Configure Wazuh with the Webhook URL**
Start by logging into your Wazuh management console with access to edit the ossec.conf file. We'll first start by adding the Shuffle webhook forwarder. 

1. Transfer [these integration files](https://github.com/frikky/Shuffle/tree/master/functions/extensions/wazuh) to the server. Ignore the file named "ossec.conf" for now.
2. Move the custom-\* files to the location /var/ossec/integrations

```
[root@wazuh]# pwd
/var/ossec/integrations
[root@wazuh]# ls -alh
total 76K
drwxr-x---.  2 root  ossec  187 Apr 25 04:34 .
drwxr-x---. 19 root  ossec  242 Dec 14 09:40 ..
-rwxr-x---   1 ossec ossec 1.1K Dec 20 04:50 custom-shuffle
-rwxr-x---   1 ossec ossec 4.5K Jan 19 09:32 custom-shuffle.py
-rwxr-x---.  1 root  ossec 4.3K Nov 30 08:41 pagerduty
-rwxr-x---.  1 root  ossec 1.1K Nov 30 08:42 slack
-rwxr-x---.  1 root  ossec 3.8K Nov 30 08:41 slack.py
-rwxr-x---.  1 root  ossec 1.1K Nov 30 08:42 virustotal
-rwxr-x---.  1 root  ossec 6.3K Nov 30 08:41 virustotal.py
```

3. Change the files' ownership and access rights. This MAY be necessary if Wazuh doesn't have root privileges (it shouldn't)
```
$ chown root:ossec custom-shuffle
$ chown root:ossec custom-shuffle.py
$ chmod 750 custom-shuffle
$ chmod 750 custom-shuffle.py
```

4. Configure ossec.conf to forward to Shuffle 

Go to the location /var/ossec/etc/ossec.conf (or where the ossec.conf file is). Take the information below (including <integration>) and paste it in. Find the webhook URL from earlier, copy it and add it to the <hook_url> section. 

Find more fields like [levels, groups and rule_id here](https://documentation.wazuh.com/current/user-manual/manager/manual-integration.html).

```
	<integration>
		<name>custom-shuffle</name>
		<level>5</level>
		<hook_url>http://IP:PORT/api/v1/hooks/webhook_hookid</hook_url>
		<alert_format>json</alert_format>
	</integration>
```

5. Restart ossec manager. Every time you change ossec.conf, you need to restart the ossec manager.
```
systemctl restart wazuh-manager.service
```

You should now start seeing data sent from Wazuh into Shuffle which can be used. If data is NOT sent, make sure of a few things:
- If https in the Shuffle URL: is the certificate of Shuffle signed? Default: no.
- Check /var/ossec/logs for logs: grep -R custom-shuffle

**4. Test the integration**
There are many ways to test the integration, but you can simplify it by setting the "level" part of the configuration to a lower number (3~), as that would trigger it in a lot of cases, including when you SSH into the Wazuh manager. After an alert is supposed to have triggered, go to Shuffle, and you'll see something like the image below.

![Extend Shuffle with Wazuh 3](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_3.png?raw=true)

#### Running custom commands with Wazuh
Active response can be used with the command "Run Command" in the Wazuh app in Shuffle. This requires an Agent (Agent list) and Command ([Active response](https://documentation.wazuh.com/current/getting-started/use-cases/active-response.html) command). Below, we will show how to set up the custom command "reboot".

- Wazuh API logs will be on the manager in: /var/ossec/logs/api.log
- Wazuh agent logs can be found in /var/ossec/logs

**Testing custom active response from Shuffle**:
The goal with this section is to set up a bash script that can run custom commands from within Shuffle.

1. Log into the Wazuh agent of choice (Linux), and add the following script to the active-response folder. Give it the name "shuffle.sh". Full path: /var/ossec/active-response/bin/shuffle.sh PS: Once done, make sure it's executable: chmod +x /var/ossec/active-response/bin/shuffle.sh
```
#!/bin/bash
# Extra arguments

# Installing jq
if ! command -v jq &> /dev/null
then
    echo "jq could not be found - installing"
    sudo apt install jq -y 
    sudo yum install jq -y 
fi


read -r INPUT_JSON
CMD=$(echo $INPUT_JSON | jq -r .parameters.alert.cmd)
CALLBACK=$(echo $INPUT_JSON | jq -r .parameters.alert.callback)
OUTPUT=$($CMD)
curl -XPOST $CALLBACK -d """$OUTPUT""" -k
``` 

2. Open /var/ossec/etc/shared/ar.conf and ADD the following line to the bottom of the file:
```
shuffle - shuffle.sh - 0
```

3. Restart the wazuh agent
```
/var/ossec/bin/wazuh-control restart 
```

4. Log into Shuffle and import [this public workflow](https://shuffler.io/workflows/44bc4e93-ba6e-4895-8294-424fd2a1d169). Make sure to change the following:
- Activate the Wazuh app if it's not already
- Add a Wazuh username & password to the HTTP node
- Add the Wazuh URL to the HTTP node, as well as Get_agents and other Wazuh nodes.
- Make sure the last block after "Get_agents" runs the command "shuffle" with the "Agent list" containing your specific agent's ID.

The default from this workflow is that it will reboot the server.

### TheHive
TheHive is a case management platform for and by security professionals. One of their key capabilities is webhooks, which can send realtime updates to a third party system whenever ANYTHING is changed within TheHive (e.g. a new alert or a case task is written). Shuffle has an ideal way of handling this, [outlined in this blogpost (TheHive4)](https://medium.com/shuffle-automation/indicators-and-webhooks-with-thehive-cortex-and-misp-open-source-soar-part-4-f70cde942e59).

**PS: There is a difference between TheHive3 and TheHive 4 on how to set this up. We are referring to TheHive4 in this section.**

1. Create a Workflow in Shuffle 
2. Add a Webhook to the Workflow
3. Configure TheHive with the Webhook URL
4. Test the integration

**1. Create a Workflow in Shuffle**
This one is pretty easily explained. Go to Shuffle an make a new Workflow.

**2. Add a Webhook to the workflow**
[Add a webhook](/docs/triggers#webhook) and find the Webhook URL. Remember to start the Webhook!

![Extend Shuffle with TheHive](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_1.png?raw=true)

Copy the URL and keep it for the next steps
![Extend Shuffle with TheHive 2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_2.png?raw=true)

**3. Configure TheHive with the Webhook URL**
Configuring TheHive is the only unique step here, and is different between versions. Full documentation about [TheHive4 webhooks can be found here](https://github.com/TheHive-Project/TheHiveDocs/blob/master/TheHive4/Administration/Webhook.md).

As can be seen in the documentation, there are three steps to setting up TheHive webhooks: 
1. Define the webhook forwarder:

Find the [application.conf](https://docs.thehive-project.org/thehive/installation-and-configuration/configuration/manage-configuration/) file and scroll to the webhook section. If it doesn't exist, add the following:
```
notification.webhook.endpoints = [
  {
    name: Shuffle
    url: "http://IP:PORT/api/v1/hooks/webhook_hookid"
    version: 0
    wsConfig: {}
    includedTheHiveOrganisations: ["*"]
    excludedTheHiveOrganisations: []
  }
]
```

Modify it to have the URL you found making the webhook in Shuffle. You can also use https by adding certificate references to wsConfig{}

2. Restart TheHive
```
systemctl restart THeHive
```

3. Activate the webhook
Run this curl command (change the URL, username and password), which activates TheHive forwarding to Shuffle. 
**PS: Make sure you have access to the organization you want the Webhook for**
```
curl -XPUT -u thehive_user:thehive_password -H 'Content-type: application/json' thehive_url/api/config/organisation/notification -d '
{
  "value": [
    {
      "delegate": false,
      "trigger": { "name": "AnyEvent"},
      "notifier": { "name": "webhook", "endpoint": "Shuffle" }
    }
  ]
}'
```

**4. Test the integration**
In TheHive UI (NOT CLI), create a new case, or add a comment to an existing case. This will then be seen within Shuffle. After the webhook is supposed to have triggered, go to Shuffle, and you'll see something like the image below.

![Extend Shuffle with TheHive 3](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_3.png?raw=true)

### Logzio 
**1. Create a Workflow which will receive alerts**
This one is pretty easily explained. Go to Shuffle an make a new Workflow.

**2. Add a Webhook to the workflow**
[Add a webhook](/docs/triggers#webhook) and find the Webhook URL. Remember to start the Webhook!

![Extend Shuffle with Wazuh](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_1.png?raw=true)

Copy the URL and keep it for the next steps
![Extend Shuffle with Wazuh 2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_2.png?raw=true)

**3. Configure Logz.io forwarding**
After logging into app.logz.io, hover Settings Icon > Settings > click Notifications Endpoint. This will make all rules send alerts to the assigned webhook target.

![Extend Shuffle with Logz.io](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_4.png?raw=true)

Once in the notification endpoint view, click "Add Endpoint". Configure the following elements:
* Type: Custom
* Name: Shuffle (or some other identifier)
* URL: The Webhook URL from step 2
* Method: POST
* Data (should be autofilled): 
```
{
    "alert_title": "{{alert_title}}",
    "alert_description": "{{alert_description}}",
    "alert_severity": "{{alert_severity}}",
    "alert_event_samples": "{{alert_samples}}"
}
```

Custom data will be parsed into the field "alert_event_samples"

![Extend Shuffle with Logz.io 2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_5.png?raw=true)

**4. Test the integration**
Click "Run the test" at the bottom before saving. This allows for it to send a sample payload to Shuffle.

If the data payload is configured as in step 3, the custom data will be available as such:
```
$exec.alert_event_samples
```

![Extend Shuffle with Logz.io 3](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_6.png?raw=true)

### MISP
MISP, short for Malware Information Sharing Platform, is one of the best Open Source alternatives for Threat Intelligence. For that reason, a lot of our users have wanted a way to handle data in realtime from MISP. What kind of data? Event updates, indicator updates, IDS flag edits, Organization edit etc.

That's why we released an extension for Shuffle which can read ZMQ messages from MISP in realtime and send them to a webhook.

[More information here](https://www.circl.lu/doc/misp/misp-zmq/)

**Steps to set it up:**
1. Enable ZMQ in MISP by going to Server Settings -> Plugins in MISP. Make sure to enable the options for forwarding Events and Attributes.
2. Install pyzmq and redis on the MISP server: 
```
pip3 install pyzmq redis
```
3. Go to Shuffle and create a new Webhook
4. [Install Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) on a host with access to ZMQ (localhost:50000 by default). This can be on the MISP server, but at scale, it preferably shouldn't be.
5. Copy the docker-compose [found here](https://github.com/frikky/Shuffle/tree/master/functions/extensions/misp/docker-compose.yml) and edit the environment variables to point to your ZMQ instance (PS: Don't use localhost, even if it's on the MISP server)
```
version: '3'
services:
  zmq:
    image: ghcr.io/frikky/shuffle-zmq:latest
    container_name: shuffle-zmq
    hostname: shuffle-zmq
    environment:
      - ZMQ_HOSTNAME=10.1.2.3
      - ZMQ_PORT=9000
      - ZMQ_FORWARD_URL=<WEBHOOK_URL>
    restart: unless-stopped
```
6. Run the docker-compose!
```
docker-compose up -d
```
7. Test it by going to your MISP instance and changing an event or attribute

### AWS S3 forwarder
Ever wanted to run an action as soon as something is uploaded to your S3 Bucket? Maybe you just want to build an S3 honeypot? If so, this part is for you. Herein we describe how you can get information about files being uploaded or changed from an S3 bucket into Shuffle.

**Basic overview:**
User -> Upload to S3 -> S3 triggers Lambda function -> Lambda function triggers Webhook -> File is downloaded from within Shuffle

Steps to set it up:
1. Create a Workflow with Webhook inside Shuffle
2. Create a Lambda function that triggers on S3 changes
3. Configure the workflow to download the file
4. **Optional**: Scan file with Yara

![AWS lambda overview](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-1.png?raw=true)

**1. Create a Workflow which will receive alerts**
This one is pretty easily explained. Go to Shuffle an make a new Workflow. [Add a webhook](/docs/triggers#webhook) and find the Webhook URL. Remember to start the Webhook!

![Extend Shuffle with webhook](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_1.png?raw=true)

Copy the URL and keep it for the next steps
![Extend Shuffle with webhook2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_2.png?raw=true)

**2. Create the lambda function**
- After logging into your AWS, go to [Lambda functions](https://console.aws.amazon.com/lambda/home) and click "Create function" in the top right corner. 

- Use "Author from scratch", and type in a name like "Shuffle-forwarding" and make sure to choose Runtime as Python 3.8. Click "Create function" in the bottom right corner.
![Author S3 from scratch](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-2.png?raw=true)

- Click "Add trigger" in the window, left of the function. In the next menu find "S3", before choosing the bucket you want and the "Event type". Click "Add trigger"
**PS: The bucket and cloud function have to be in the same location**
![Add trigger](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-3.png?raw=true)

- Under Configuration > Environment variables, click "Edit". Add variable with key "SHUFFLE_WEBHOOK", and the value from step 1. Click "Save".
![Configure s3 environment](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-4.png?raw=true)

- Time to add some code. Go to the "code" tab and paste in the code below. Click "deploy". This should now forward the request to Shuffle. 
```
import json
import urllib.parse
import requests
import os

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    #bucket = event['Records'][0]['s3']['bucket']['name']
    
    webhook = os.environ.get("SHUFFLE_WEBHOOK")
    if not webhook:
        return "No webhook environment defined: SHUFFLE_WEBHOOK"
        
    ret = requests.post(webhook, json=event["Records"][0])
    if ret.status_code != 200:
        return "Bad status code for webhook: %d" % ret.status_code
        
    print("Status code: %d\nData: %s" % (ret.status_code, ret.text))
```

**3. Configure and test the workflow**
To test the previous step, we have to upload a file to the chosen S3 bucket. If everything is connected correctly, this will trigger an event to come into Shuffle. If it doesn't, have a look at the Lambda function's logs, or [contact us](https://shuffler.io/contact).
![S3 data in Shuffle](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-6.png?raw=true)

Now all we need is to do is actually download the file. This requires access rights to the bucket itself from the API in use. The app we use for this is the "AWS S3" app, with the action "Download file from bucket". See the next image for how to configure this action after authenticating it. (We may add file uploads to webhooks in the future).
![Configure s3 environment](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-5.png?raw=true)

And that's it! All file updates should now come into Shuffle, including a way to download the file.


**4. Extra: Scan the file with Yara**
In a lot of cases you would want to analyze the files somehow. But how..? Shuffle has a built in way to run Yara on files, and get results based on built-in rules (or your own). Most of the time, you would also want a response to that search, hence we've created a way to also delete the file if it matches too many Yara rules.
![Basic s3 analysis](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-7.png?raw=true)

To do this, add in the "Yara" node with the action "Analyze file", and put "$get_s3_file.file_id" in the "File Id" field. This should match the file downloaded from the bucket.

After this, add another S3 node, and choose the action "Delete file from bucket" with these parameters:
- Bucket Name: $exec.s3.bucket.name
- Bucket Path: {{ "$exec.s3.object.key" | url_decode | replace: "+", " " }}

Last but not least, we need a way [to see IF](/docs/workflows#conditions) the file should be deleted. This can be done by clicking the branch between Yara and the S3 delete action > "New Condition" > with the following data: 
```
{{ $run_yara.matches | size }} > 3
```
![S3 condition yara](https://github.com/frikky/shuffle-docs/blob/master/assets/s3_function-8.png?raw=true)

Done! Whenever a file is downloaded, it will be analyzed by Yara, checking matches, then removing the file if it's more than 3.

### QRadar

**QRadar send offense webhook to Shuffle.**

#### STEP 1: Add the Script to QRadar & Config
> **Bash Code:**
```
#!/bin/bash
# Version 1.0.0

shuffle_url=$1
api_token=$2
offense_id=${3%.*}

auth_header="SAuthorization:$api_token"

output=$(curl --insecure -H $auth_header $shuffle_url -d "$(cat <<EOF
{
        "offense_id": $offense_id
}
EOF
)")
```

What you should do to use it:

1. Log In to QRadar;			
2. Go to Admin > Custom Actions > **Define Actions**;	
3. Click **Add**;
4. Fill the Basic Information (name & description);
5. In the Script Configuration set **bash** as interpreter, and import the bash script attached to this message;	
6.** For the Script Parameters, add the parameters in the following order:**

```
1. [Fixed Property] **shuffle_url** - As value insert the Shuffle Webhook URI, for example https://shuffle.local/api/v1/hooks/webhook_15acc....	
2. [Fixed Property] **authorization** - Insert the Required headers (**SAuthorization**), for example in Shuffle webhook if you set **SAuthorization=s873hn872n_s298ns2-98ns2ns** in the Required headers you authorization value will be "s873hn872n_s298ns2-98ns2ns". *If you change the token name, don't forget to change it in the bash code too*.			
3. [Network Event Property] **offense_id** - Insert **offense_id** as value
```

7. Save	
8. Deploy Changes

![image](https://user-images.githubusercontent.com/21691729/152444978-d360680a-a0b1-40b0-bd04-fa7395cf4d85.png)
![image](https://user-images.githubusercontent.com/21691729/152445000-0d2a1828-ee1d-41b1-a549-5417c9a48c75.png)


#### STEP 2: Create new offense alert rule
			
1. Go to Offenses > **Rules**;			
2. Click Actions > **New Event Rule**:
```
    Rule Description
      Apply Shuffle new offense alert on events which are detected by the Local system
and when the event QID is one of the following (28250369) Offense Created
 
    Rule Responses
      Execute Custom Action QRadar to Shuffle  (previous added script)

This Rule will be: Enabled
```

#### QRadar Overview			
- Easy, this way each time a new offense dispatches in QRadar it will send a webhook to Shuffle containing the offense_id, then the webhook node will receive this info and pass it to the next node (QRadar App) that will perform a **get offense** ~~data~~ action using the received offense id as key.
			
This way you won't need to execute an api call every x time and save the last offense id. This is a better solution and improves the SLA, coz if you set 1 minute as you x time, you may have 1 minute delay or less, besides you are getting all "ungotten" offenses at once, when you can use shuffle to handle with multiple at the same time if it happen to dispatch more than one offense in QRadar at the same time or with just some seconds of difference.
	

### FortiSIEM
FortiSiEM is the SIEM of Fortigate. It has the possibility of notifying Shuffle through a webhook when a rule triggers, which is exatly what this documentation section is for. The main caveat: all data is XML and needs to be transformed with the Shuffle Tools "XML to JSON" formatter.

**1. Create a Workflow which will receive alerts**
This one is pretty easily explained. Go to Shuffle an make a new Workflow.

**2. Add a Webhook to the workflow**
[Add a webhook](/docs/triggers#webhook) and get the Webhook URL. Remember to start the Webhook!

![Extend Shuffle with Wazuh](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_1.png?raw=true)

Copy the URL and keep it for the next steps
![Extend Shuffle with Wazuh 2](https://github.com/frikky/shuffle-docs/blob/master/assets/extensions_example_2.png?raw=true)

**3. Configure FortiSIEM forwarding**
Log into the UI. When inside, go to ADMIN > Settings > Incident Notification. In the "Incident HTTP Notification", paste in the webhook from the previous step. Click "save", then "Test". After the test, check the workflow in Shuffle whether it triggered. If it didn't, your FortiSIEM can't access the Shuffle instance.
	
![image](https://user-images.githubusercontent.com/5719530/162085936-58a44de4-0289-4cf9-8f72-7b3229857448.png)
	
With the Notification Endpoint specified in the previous step, we need to decide what rules to add. By default, we add all of them. To do this, go to ADMIN > Settings > Notification Policy, and add a new policy. In here, select the "Send XML file over HTTP(S) to the destination set in...". This will make sure all alerts are sent to Shuffle.
	
![image](https://user-images.githubusercontent.com/5719530/162086144-8bbfb6fa-d512-4c36-81db-f830bcf9c204.png)

That's it! It's now time to wait for an alert to actually trigger. When it has, make sure to send Execution Argument from the webhook ($exec) straight into an XML to JSON parser. That way you can use it easily in Shuffle.

	
	
### Splunk SIEM 
Splunk is a SIEM tool for security operations. There are multiple ways to forward the Splunk alerts to  external systems. Simplest way to forward splunk alerts to Shuffle is with using webhook.

**Step 1:** First we'll have to create a Shuffle workflow which will recieve alerts from Splunk. Go to /workflows in Shuffle and create a new worfklow. Then, inside workflow editor drag in the webhook from the trigger section in left pane.

![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-1.png)

**Step 2:** Click on the webhook node and then click on start. Copy the webhook url.
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-2.png)

**Now that we have webhook running in the Shuffle, Go to your Splunk deployment server and log in.**

**Step 3:** Now we'll have to configure Splunk with the webhook URL. Once logged in, go to the **search and reporting** app and type in the query you want to create an alert for.   
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-3.png)

**Step 4:** Save the search query as an alert.
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-4.png)

**Step 5:** Fill out all the form details for saving as an alert. At the very bottom of thr form in **Trigger action** section click on **Add actions** select Webhook.
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-5.png)

**Step 6:** Paste in the webhook URL in URL field and click Save.
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/splunk-alerts-6.png)

**You should now start seeing data sent from Splunk into Shuffle which can be used inside workflow for further actions.**

	
### Eventlog Analyzer
Note: API integration is unfortunately not supported with EventLog Analyzer. However, If you would like to forward logs from EventLog Analyzer to Shuffle. For more information please follow this [guide](https://www.manageengine.com/products/eventlog/help/StandaloneManagedServer-UserGuide/Configurations/log-forwarder.html)
	

### ServicePilot SIEM 
ServicePilot is a high-performance analytics platform that supports observability and full-stack monitoring: metrics, traces and logs. You can collect data from many services and sources across your entire IT stack (ITIM, NPM, APM, DEM, SIEM) as well as view details of historical data stored by ServicePilot. Webhook integration service is not provided by the ServicePilot platform. Here am gonna mentioned the steps for how to use ServicePilot app workflow.

#### - What this workflow do?
This workflow is help to get all the alerts, objects, events and logs. In this workflow there are two nodes of ServicePilot app. one is for getting all the records from the ServicePilot SIEM app and another one is searching for alerts, objects, events and logs for specific entry. As a result this workflow first excecute the Get_All_Data node and after that it excecute the Get_Specific_Record node and at the last return the result.

#### - How the seaching happens?
For searching records from the ServicePilot app we need to write SQL query to search the data. we need to write query as a query parameter in the request url.

#### - Steps to create a workflow
**Step 1:** First we'll have to create a Shuffle workflow which will search for events, objects, alerts, and logs from ServicePilot. Go to /workflows in Shuffle and create a new worfklow. Then, inside workflow editor drag in the node for the ServicePilot.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-0.0.png)

**Step 2:** Click on the ServicePilot node.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-1.0.png)

**Step 3:** Change the name of the node as Get_All_Data.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-1.1.png)

**Step 4:** Write Query for searching all the datas from the ServicePilot.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-1.2.png)

**Step 5:** Inside workflow editor drag in the another node for the ServicePilot and connect it with the existing node.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-2.0.png)

**Step 6:** Change the name of the node as Get_Specific_Record.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-2.1.png)

**Step 7:** Write Query for searching specific record from the ServicePilot.
	
![image](https://github.com/shuffle/Shuffle-docs/blob/master/assets/servicepilot-2.2.png)

**Finally, Click the excecution button and you should now start seeing data sent from ServicePilot into Shuffle which can be used inside workflow for further actions.**
	
	
### ELK/Elastic
Intergrating Elastic with Shuffle will first require you to set up a webhook in Elastic. Below are the steps you will need to follow to ensure your alerts are forwaded into Shuffle immediately.

1. Create a new workflow in Shuffle, bottom left on your screen head to the triggers tab and drag in the webhook into your workflow. Click on it and ensure that the webhook is started. Copy the provided webhook URI and head over to Elastic.
   
 ![image](https://github.com/user-attachments/assets/e708d1fd-8222-4c47-ac29-7a2d5f62024e)

 ![image](https://github.com/user-attachments/assets/98799857-7640-4cf7-aec4-31224a186320)

3. Follow Elastic's documentation on setting up the webhook [here](https://www.elastic.co/guide/en/kibana/current/webhook-action-type.html).
   - When setting up the webhook in Elastic you will have to provide a url to send the info to. Provide the Shuffle webhook URI you copied in step 1 above
   - You do not need to provide authentication in Elastic while setting up, but just incase you do, remember to do the same in your webhook in Shuffle

4. To finish setting up your connector in Elastic you will be required to provide the body of the webhook connector, we will need to provide a JSON body for the connector. Copy and paste the below in the connector body
    ```{"raw": {{context.alerts}}}```

5. Go ahead and test your connector and then check your workflow executions in Shuffle if you have an incoming execution.

	
### Cortex 
TBD: Responder executions
