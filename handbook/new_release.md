# New release
New releases are exciting, and requires broad collaboration across the entire team. Here is a basic overview of what it entails.

**Release Structure**
* Release version (1.4.0: Native Actions & Multiregion management)
  * Milestones
    * Issues
      * Title & Description
      * User assignment
      * Tags

## Overview
A new release happens about once every 4-6 months, with minor releases for important features and nightly builds inbetween. This is to allow power-users to try features immediately instead of waiting. 
Releases are meant to contain new features along with bug fixes. 

Tracking of the next release should be done in the [roadmap project](https://github.com/orgs/Shuffle/projects/8). 

**Ambitious deadlines with focus on innovation are VERY important**

## Milestones
When a new release is decided, it is important to outline the milestones of the release. As an example, 1.3.0 was a release about Usability/Ease of use. 
With this in mind, we made the following milestones:

- Onboarding Flow
- Recommendations
- Scaling Shuffle

These milestones should reflect the overarching goal of the release itself, and should be a maximum of 4 major objectives. 

[Milestones can be assigned to an issue](https://github.com/Shuffle/Shuffle/milestones), and when all milestones are fullfiled, that means the version should be completed and released.

## Product
Product is at the head of release, and someone from Engineering should always be in charge of the release itself. As an example, @frikky was in charge of 1.2.0, and @0x0elliot is in charge of release 1.3.0.

Each version has its own branch on Github, e.g. 1.3.0 is for the release of 1.3.0. The "Main" branch should always reflect the "latest" release of containers.

Here are the things to get done before any marketing material goes out:
1. Github: Merge the branch of the latest release into Main. E.g. 1.3.0 -> Main. This is to ensure builds automatically run in the CI/CD early.
2. GCP: Release the website (https://shuffler.io). **Make sure all new and old things work**. Workflows are critical.
3. GCP & Local: Test the images generated in step #1 in the following ways: Normal Shuffle setup (docker), Scale setup (docker swarm), Kubernetes setup.
4. GCP & Local: Test if the images run workflows correctly. Test if the containers work on **x86 AND ARM**. 
5. Local: If all is good, tag all the images you tested to be "latest" instead of "nightly". Also add the tag "1.3.0".
6. GCP: Release the backend to all other regions (canada, EU, Asia-pacific...)
7. Github: Make a release for the new version in the https://github.com/shuffle/shuffle repo. 
8. Tell marketing & sales that all is ready to release what they got :)

## Marketing
When a release is decided, it is important to know what should be shared. Here are the things we do regularly:

- Newsletter
- Social media posting
- In-product
- Webinar / Conferences
- Videos (Youtube/Tiktok)

This means it's vital to talk to the Marketing team about what we are building and why we are building it during the initial phases of a release. 

**During the release itself**, the marketing team should have something for the following ready:
- A blogpost (why is the release exciting and new? Hint about the future etc.) - [Articles](https://github.com/Shuffle/shuffle-docs/tree/master/articles), Medium & Linkedin crosspost?
- Discord information: Fred
- Release information Github: Fred

## Support & Security Development
Support goes along the same lines as marketing, and should be kept in the loop to not be blindsided.

## Customer Success
TBA

## Legal
TBA




