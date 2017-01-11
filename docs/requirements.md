# Requirements Document for PS-Locate

## Project Specifics
Manager: rapier@psc.edu  
Developer: blearn@psc.edu  
Last Updated: 12-8-2016  

## Goals
Given an IP address, identify the N closest registered perfSONAR nodes along with host-specific meta data.

## Background
Currently the perfSONAR community only has a manual solution for finding the closest perfSONAR nodes to a given host.

## Assumptions
* All interfaces on a given host map to the same geographical coordinates; Only one interface IP is looked up.
* Ignore fact that some interfaces may not be accessible (Most nodes are on R&E networks not open to the public).

## User Interaction/Stories
Title | Description | Priority | Notes
------|-------------|----------|------
  CLI | User or 3rd party program can use a CLI to input an IP and receive a list of the nearest perfSONAR nodes. | Must Have |

## Questions
* Should the user be able to select how many nearby perfSONAR nodes are returned?

## Not Doing


