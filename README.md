# SANDRA
**S**onar side scan **A**I for **D**ebris **R**ecognition and Analysis (SANDRA) is an AI system designed to find debris using underwater Sonar Side Scan images (and live video from AUVs soon) which is edge deploy able due to its light weight underlying architecture of YOLO (currently version 8).
It consists of the
1. Data preprocessing pipeline
2. Data annotation pipeline
3. YOLO model (v8) trained on most of the real SSS images which can detect:
   a) Ghost Nets (Only Synthetic Data)
   b) Wrecked Ships
   c) Wrecked Planes 
   d) Pipelines
   e) Anomalies
   and determine the empty sea bed and marine life. 
4. Backend deployed using Render 
5. Front End (Web Dashboard)
