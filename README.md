## **1.	Overview**

missedSampleLib is a Python-based machine learning package developed for the automated detection of wrong blood in tube (WBIT) errors in hospitalized patients.
The model was built using the XGBoost algorithm and trained on real-world clinical data. It operates on a vector containing the normalized variation of multiple laboratory parameters relative to the patient’s previous sample (when collected within the preceding five days).

The training dataset consisted of 50% correctly identified samples and 50% WBIT cases, the latter including 25% confirmed errors and 25% simulated sample reorderings.
The model was validated in two independent external cohorts, demonstrating excellent discrimination, sound calibration, and robust generalizability across laboratories.

## **2.	Model description**

The model functions as a plug-and-play module designed for seamless integration into Clinical Decision Support (CDS) and Laboratory Information Systems (LIS).
It outputs a probability score (0–1) representing the likelihood of a WBIT event, based on a vector of normalized rate-of-change (NRC) values derived from standard hematology and biochemistry parameters.

By default, predictions are recalibrated to a 5% prevalence, ensuring interpretability even for rare events.
This setting can be customized through the parameter pi_target, enabling adjustment to alternative prevalence levels (for example, 1% or 2%) to reflect local epidemiology.

## **3.	Key features**

•	Validated in two independent external cohorts

•	Plug-and-play integration with existing LIS or CDS environments

•	Automatic prevalence recalibration via pi_target

•	Compatible with real-time deployment for error detection and reporting

•	Transparent and reproducible: includes model weights, documentation, and training scripts

## **4.	Repository contents**

•	 DataProcessor.py — handles data import, preprocessing, and normalization. Generates the input feature matrix from raw analytical data.

•	ModelTrainer.py — defines the training pipeline, including cross-validation, hyperparameter tuning (*GridSearchCV*), and performance evaluation (AUC, ROC).

•	OnTheFlyCalibrator.py — implements the in-the-large calibration module (adjustment of model intercepts). This allows real-time recalibration of predicted probabilities according to local prevalence without retraining the model.

•	utils.py — contains auxiliary functions (parameter grids, metric calculations, etc.) used across the project.

•	train_set.csv — example training dataset used to fit the model. It includes normalized laboratory parameter variations and the binary outcome (WBIT vs. correct).

•	init.py — initializes the package, enabling direct import of its modules.

## **5.	Input format**

The model takes as input a vector containing the normalized variation of the following laboratory parameters, in the specified order:

Mean corpuscular volume (MCV), mean corpuscular hemoglobin (MCH), mean corpuscular hemoglobin concentration (MCHC), red cell distribution width (RDW), mean platelet volume (MPV), hemoglobin (HGB), chloride (Cl⁻), hematocrit (Ht), potassium (K⁺), creatinine (Cr), platelets (PLT), lymphocytes (LYMPH), eosinophils (EO), red blood cells (RBC), sodium (Na⁺), and basophils (BASO).

It is recommended to first determine the optimal prediction cutoff, adjusting the model according to the true WBIT prevalence observed in the laboratory.
If prevalence is initially unknown, the default calibration at 5% can be used, and the cutoff can later be recalculated once the true prevalence becomes available.

## **6.	Interpretation**

•	The predicted probability represents the model-estimated likelihood of a WBIT event.

•	The default 5% calibration provides balanced interpretability for hospital datasets.

•	Adjusting the pi_target parameter allows alignment with different real-world prevalence levels.

## **7.	Citation**

This package accompanies the study: “*Development and Validation of a Machine Learning Model for Accurate Detection of Wrong Blood in Tube Errors in Hospitalized Patients.*”
