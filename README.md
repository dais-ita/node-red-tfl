# node-red-tfl
A node red prototype of a service toolbox to answer questions concerning traffic in London

(Very much work in progress, code organisation, tidying, commenting needs to take place as well as actually creating many of the services required).

# TFL Node Red Overview - A Deep Dive in TFL Congestion to Explore Coalition SItuational Understanding

This node red implementation aims to provide a simple prototype for a service structure for a coalition concerned with traffic within london. 

The primary question being: “Is my route from point A to point B congested?”

In many cases, the services as individual components are not aiming to be at the cutting edge of their individual fields but instead this prototype brings them together to provide a sandbox to explore the dimensions of the situational understanding problem. 

To explore this fully,in most cases, services are considered to be pre existing and belong to a coalition partner, thus a deliberate choice has been made to separate the components into their own hosted services (primarily by wrapping python code in a simple flask web server). 

Within the node red dashboard, nodes are created that call the flask services.

In “reality” the front end UI would be hosted by each coalition partner and would be able to access the services of the coalition. 

For now you can run all the services and node red locally.

To do this you must:

- Install node.js & node red: https://nodered.org/docs/getting-started/installation
- Install node red dashboard : https://github.com/node-red/node-red-dashboard
- Install python 
- Install flask python module
- Install python dependencies for desired services
- Run node red locally
- Import Flow from TFL_flow.txt
- Run each service locally (you may need/wish to configure ip and port settings and then adjust the node red flow)




## Intended Available Services (High level summary)

*these services are composite services and are not intended to be used in the demonstration of “real” service chains
 
INPUTS => OUTPUTS

NOINPUT (request only) => Available TFL Camera IDs

TFL Camera ID => Camera Data (longitude, latitude etc)

TFL Camera ID => Camera Image (Current available image from TFL API)

TFL Camera ID => Camera Video (Current available video from TFL API)

TFL Camera ID => Camera Video - Frame by Frame (Current available video from TFL API)

*TFL Camera ID => Speed Limit (from estimate of subject road of camera using OSM)

*TFL Camera ID => Cars Detected in Image


Longitude, Latitude => Speed Limit (from estimate of subject road of camera using OSM) 

Longitude, Latitude => Daylight Ratio (using https://sunrise-sunset.org/api)


Image => Cars Detected in Image

Image => Congestion Classification


Stream of Frames => Blobs in motion and their pixel velocities

Stream of Camera Images with 5 minute timesteps => Predicted Car Volumes

## Current Available Services

### RCNN Car Detector

TFL Camera ID => Cars Detected in Image

https://github.com/dais-ita/Faster-RCNN_TF “hosted” branch

dais/car_detector_AAS.py


### OSM Speed Limit API

TFL Camera ID => Speed Limit (from estimate of subject road of camera using OSM)

Flask Services/OSM.py


### Get TFL Camera IDs

NOINPUT (request only) => Available TFL Camera IDs

Flask Services/GetCameraIDs.py





