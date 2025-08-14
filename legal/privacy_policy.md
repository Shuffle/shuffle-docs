# Privacy Policy
This is the initial privacy policy for Shuffle cloud. Valid as of this file's last change date on [Github](https://github.com/frikky/shuffle-docs/blob/master/docs/privacy_policy.md)

## Table of contents
* [Introduction](#introduction)
* [Protecting your data](#how_we_protect_your_personal_data)
* [Limited Use disclosure](#limited_use)
* [Analytics](#analytics)
* [Data Location](#data_location)
* [Infrastructure Monitoring](#infrastructure_monitoring)
* [External social media platforms](#external_social_media_platforms)
* [External platforms](#external_platforms)
* [User Data Management](#user_data_management)
* [Collection of Children Data](#collection_of_children_data)
* [Business Transfers (Acquisition or Bankruptcy Events)](#Business_Transfers)
* [Rights under GDPR](#Rights_under_GDPR)
* [Data Ownership and Control](#Data_Ownership_and_Control)
* [Contact Information](#contact_information)
* [Log retention](#log_retention)

## Introduction
We are Shuffle AS (and Shuffle LLC, the subsidiary), and this privacy policy will tell you how we use and protect your personal data.

## How we protect your personal data
We understand the importance of the data we collect on our customers, and the sensitivity of what our customers may want to use our platform for. The following explanations go into more detail on how your data is being processed and stored.  

### Encryption
Shuffle utilizes [Google Cloud Platform's Datastore](https://cloud.google.com/datastore/docs/concepts/encryption-at-rest) and [Google Cloud Storage](https://cloud.google.com/storage). We encrypt all your data by default, and have extra mechanisms for API-keys and secrets inserted. [All our code for encryption can be accessed here.](https://github.com/Shuffle/shuffle-shared)

### Session Management
Utilizing Google Cloud Platform and internal audit logs, we track all sessions and changes in Google Cloud's [Cloud Logging](https://cloud.google.com/logging). 

### Two-factor authentication and Single Sign-on
Shuffle has added SSO and Two-factor authentication to any user for free, protecting from fraudulent access of your Shuffle account. [Read more here on SSO and MFA](https://shuffler.io/docs/extensions#single_signon_sso).

### Organization data access
We do not permit our team direct access your organization or data within the Shuffle platform without your explicit consent. During support investigations, we may utilize internal tools to simulate your user, but will never directly get information about you or your organization from our data storage solutions. To learn more about organizations, [click here](https://shuffler.io/docs/organizations). 

### Data processing usage 
We store your data for 3 years by default, to be used in an anonymous and sanitized way, to create algorithms for better workflow autocompletion.

- We store your personal information for a period of time that is consistent with our business purposes.
- We will retain your personal information for the length of time needed to fulfill the purposes outlined in this privacy policy unless a longer retention period is required or permitted by law.
- When the data retention period expires for a given type of data, we will delete or destroy it.
- You may request for your data to be deleted by contacting us at [support@shuffler.io](mailto:support@shuffler.io)

### Sharing of data with 3rd parties
Shuffle does not share data with any 3rd parties, except our support partner [Infopercept](https://infopercept.com/). We do however have third party services where your data may be stored - all listed in the segmented details below.

## Limited Use 
Shuffle's use and transfer to and from any app in our ecosystem will adhere to the respective platform's user data policy, including their Limited Use requirements. If a breach of policy is discovered, please contact us at [support@shuffler.io](mailto:support@shuffler.io) to get the integration fixed or removed.

### Google API Services User Data Policy
All use of Google's API's within the Shuffle ecosystem adheres to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy#additional_requirements_for_specific_api_scopes), including Limited use requirements. All client credentials that give access to or distribute data to and from Google API's are saved in a secure way and kept strictly confidential.  

## Segmented details 
### Analytics
* Platforms: Google Analytics, Segment
* Personal data: Cookies, Usage Data, Browser storage

### Data Location
As of Q1 2023, we have added multiple datacenter locations around the world on the Google Cloud Platform infrastructure. [Google's europe-west2 location (London)](https://cloud.google.com/compute/docs/regions-zones) is our default region for everyone, but we move customers to the closest region for them. The following regions are available:

1. europe-west2 (London, England - Default)
2. europe-west3 (Frankfurt, Germany)
3. us-west2 (California, US)
4. na-northeast1 (Québec, Canada)
5. asia-south1 (Mumbai, India)

We may add more regions in the future. If you would like to retain your data in another region than the default one (even if the region doesn't exist), contact the Shuffle support team.

### Infrastructure Monitoring
* Snyk: Monitors for Infrastructure, Code and Container vulnerabilities.
* GitGuarding: Monitors for potential credentials lost within or outside our infrastructure.
* Google Cloud Platform: Alerts, Notifications and logs for up/downtime. 

### Payment processor
We use the third party payment processor [Stripe](https://stripe.com/us/privacy). We do not retain any of the information provided to them during a transaction.

### External Platforms 
1. Sendgrid: Emails used for email 
2. Twilio: Phone numbers used for SMS
3. Github: Apps and Workflows shared by our users
4. Stripe: Payments
5. Fiken: Accounting 
6. Google Drive: General storage
7. Discord: Community Communication
8. Drift: Support Chat

### User Data Management
* Collected data: Email addresses, Domains, Organization names, Firstname, Lastname, Authentication keys
* Usage: User signin and Email outreach 

### User Data Management
We do not knowingly collect, use, or disclose personal information from children under the age of 13 (or other applicable age threshold under local law) without verifiable parental consent. Any collection of such data is at the sole discretion of the user, and we do not have access to or control over any such information. Users are solely responsible for ensuring compliance with applicable laws, including but not limited to the Children's Online Privacy Protection Act (COPPA) in the United States or equivalent regulations in other jurisdictions, when collecting or processing children's data.

### Business Transfers

Business Transfers: In connection with any merger, acquisition, sale of company assets, or in the unlikely event that Shuffle goes out of business or enters bankruptcy, user information may be transferred to or acquired by a third party. If any of these events occur, you will retain all of your data and privacy rights even after the transfer. This Privacy Policy will continue to apply to your information, and any successor or acquiring entity must honor the same commitments they may only use and protect your information consistent with the terms of this Privacy Policy. In practical terms, this means that your rights (for example, the right to access or delete your data) remain intact and enforceable, regardless of any change in our ownership or corporate status.

### Rights under GDPR

Shuffle users in the EU/EEA regions have the following rights:

* Right to Be Informed (Articles 13-14)
* Right of Access (Article 15)
* Right to Rectification (Article 16)
* Right to Erasure ("Right to Be Forgotten") (Article 17)
* Right to Restrict Processing (Article 18)
* Right to Data Portability (Article 20)
* Right to Object (Article 21)
* Rights Related to Automated Decision-Making and Profiling (Article 22)
* Right to Lodge a Complaint (Article 77)

For requests related to upholding these rights, please reach out to support@shuffle.io.

### Data Ownership and Control
Ownership of Your Data: You (and your institution) retain ownership of all data that you enter, upload, or generate through our Services, including all inputs, outputs, and associated metadata. We do not claim any ownership rights over your content or data; it remains your property at all times. Shuffle will access and process your data solely for the purposes of providing and improving the Services (and for any other purposes you have authorized), in accordance with this Privacy Policy and our Terms of Service. We will never use, disclose, or transfer your data for any other purpose without your explicit consent. This provision ensures that your institution’s data, and any results or insights derived from it, remain under your control and ownership even as it resides on our platform.

### User Creations 
1. Apps: Optional sharing with everyone
2. Workflows: Optional sharing with everyone

### Customer detail storage
* Google Workspace: Google drive, Gmail

### Contact Information
Data Controller: Shuffle AS and Shuffle LLC

### Log retention
Our policy is to retain logs for 15 days on cloud, however this is subject to change. For on-prem users, this is up to the server administrators running shuffle (generally, it is the customer doing that).

Contact info: [privacy@shuffler.io](mailto:privacy@shuffler.io)
