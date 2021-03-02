# Zepazo :waning_crescent_moon:

## Description :collision:
Zepazo is a project that aims to facilitate the detection of lunar impacts in videos taken from telescopes and standard cameras by comparing the different frames of the videos, trying to minimize false positives as much as possible.

## Motivation :star:
This project originally arises for the completion of a Final Degree Project proposed by [Sergio Alonso Burgos](https://lsi.ugr.es/lsi/zerjioi) and is being carried out by [Antonio Cuadros Lapresta](https://github.com/antoniocuadros) with the help of Sergio with the aim of facilitating the detection of lunar impacts due to our great love for the astronomy. It is intended to carry out the implementation of a novel software due at present we have no record of such software exists and which will facilitate the work of astronomers.

## Tools
- **Programming language:** Python 3.8.2
- **Video library:** OpenCV
- **Dependency manager:** Poetry
- **Documentation Generator:** Sphinx
- **Task runner:** Taskipy 

## Install dependencies
`poetry install`

## Execute unit tests
`poetry run task test`

### Execute unit tests with Dockerfile
`docker build . -t zepazo`


`docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix zepazo`
# Additional documentation
- [OpenCV instalation](https://github.com/antoniocuadros/zepazo/blob/main/docs/Tools/opencv.md)