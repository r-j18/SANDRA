## Phase 1: Preprocessing & Acoustic Enhancement

Running the initial OpenCV scripts locally within your Fedora Conda environment keeps the heavy image processing off the edge devices.

* **CLAHE:** Balances illumination to pull details out of dark acoustic shadows without overexposing bright returns.
* **SRGR Correction:** Applies Slant-Range to Ground-Range flat-bottom correction using the AUV altitude ($H_{auv}$) to eliminate geometric distortion.
* **Later Stage**
* **Lee Filter:** Smooths multiplicative acoustic speckle noise without blurring sharp structural returns.
* **Bilateral Filter:** Flattens background seabed variations while preserving high-frequency target edges.

## Phase 2: SAM-Assisted Annotation

* **Platform Ingestion:** Upload the enhanced dataset into Roboflow.
* **Taxonomy & Pairs:** Define positive targets alongside paired shadow classes (e.g., `wreck_highlight`, `wreck_shadow`) to teach the model shadow boundaries.
* **Polygon Masking:** Utilize SAM's click-to-annotate feature to generate pixel-tight polygon masks.
* **Format Export:** Export masks downscaled into tight YOLO-formatted bounding boxes.

## Phase 3: Cloud Model Training

* **Hardware Setup:** Mount the labeled dataset from Google Drive into a Google Colab instance utilizing the free T4 GPU.
* **Training Loop:** Initialize `yolo26n.pt` and execute training using the MuSGD optimizer, 640x640 resolution, and mixed precision.
* **Evaluation Dump:** Run a custom evaluation script to export a CSV detailing every validation prediction's raw confidence score against its Intersection over Union (IoU).

## Phase 4: Accuracy Optimization & Edge Deployment

* **Platt Scaling Calibration:** Train a Logistic Regression model on the exported CSV to map raw confidence (against an IoU $\ge$ 0.50 threshold) into true statistical probabilities.
* **Sonar Analytics Engine:** Program the mathematical modules for inference:
* **Shadow Height:** Calculates physical height using $H_t = \frac{L_s \cdot H_{auv}}{R_s}$.
* **Kinematic Geotagging:** Translates frame durations and AUV velocity into physical lengths, fusing heading and ground range to project precise UTM/Lat-Lon coordinates.


* **Universal Export:** Convert the weights to an ONNX graph (`model.export(format="onnx")`) and deploy via ONNX Runtime for hardware-agnostic execution.

## Phase 5: FastAPI Backend Service

* **Ingestion Endpoint:** Create a `POST /detect` route accepting raw sonar image uploads and vehicle telemetry (speed, heading, altitude, ping rate, lat, lon).
* **Execution Pipeline:** The server routes images through the Phase 1 OpenCV pipeline, into the ONNX Runtime session, and passes raw scores through the Logistic Regression calibrator.
* **Response Payload:** Returns JSON containing the detected class, calibrated confidence, geographic coordinates, and calculated 3D dimensions.

## Phase 6: React & TypeScript Frontend

* **Upload Interface:** Build a drag-and-drop web dashboard for sonar tiles and telemetry.
* **Canvas Overlay:** Render JSON data on an HTML5 Canvas with color-coded bounding boxes and calibrated confidence percentages.
* **Interactive Mapping:** Integrate Leaflet or Mapbox to plot geotagged target pins on a real-world map, displaying shadow-derived heights alongside a toggle to compare raw versus CLAHE-enhanced feeds.
