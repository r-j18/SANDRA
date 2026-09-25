# SANDRA
**S**onar side scan **A**I for **D**ebris **R**ecognition and Analysis (SANDRA) is an AI system designed to find debris using underwater Sonar Side Scan images (and live video from AUVs soon) which is edge deploy able due to its light weight underlying architecture of YOLO (currently version 26n). <br>
It consists of : <br>
1. Data preprocessing pipeline
2. Data annotation pipeline
3. YOLO model (v26n) trained on most of the real SSS images which can detect: <br>
   a) Ghost Nets <br>
   b) Wrecked Ships <br>
   c) Wrecked Planes<br>
   d) Pipelines  <br>
   e) Anomalies  <br>
   and determine the empty sea bed and marine life. <br>
4. Backend deployed using Render <br>
5. Front End (Web Dashboard) <br>
