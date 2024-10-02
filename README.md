# Video_analysis
## Overview
This repository contains a Python script for analyzing video footage of bee interactions. The script tracks the trajectories of bees, calculates interaction probabilities, and provides insights into their behaviors.

## Table of Contents
1. Features
2. Technologies Used
3. Installation
4. Usage
   
## Features
- Analyzes video footage to track the trajectories of multiple bees.
- Calculates interaction probabilities based on tracked data.
- Generates visualizations to display bee movement patterns.
- Supports long video recordings for comprehensive analysis.
- 
## Technologies Used
- Programming Language: Python
- Video Analysis: OpenCV
- Data Manipulation: NumPy, Pandas

## Installation
1. Git clone using : `git clone https://github.com/harneet862/video_analysis.git`
2. cd video-analysis-bee
3. Install the required dependencies:
`pip install opencv-python numpy pandas matplotlib`
4. Prepare your video files in the appropriate format (e.g., MP4, AVI).

## Usage
1. Run the video analysis script:
`python video_analysis.py --input <path_to_your_video> --output <path_to_output_file>`
Replace <path_to_your_video> with the path to the video file and <path_to_output_file> with the desired output file name.
2. The script will process the video and generate output visualizations and interaction probabilities.

## Data Analysis
- The script processes video footage to derive interaction probabilities between tracked bees.
- Data is organized and visualized to highlight movement patterns and interactions.
