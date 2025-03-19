# PotassiumControl
Experiments for diet recommendations for Potassium Control

## Quantitative Evaluation of LLMs (in zero-shot and one-shot setting) and trained LLMs
![available LLMs](https://github.com/user-attachments/assets/8bd5a5b5-a0c3-4f4d-9be7-996725b2c976)
Realized the available LLMs do not achieve good quantitative performance compare to real dietician feedback.

To address this generated a synthetic dataset to give recommendation like dietician does using one same of actual recommendation. Synthetic data in `gmdt_synthetic_data.json`
Train a small LLM on this synthetic dataset.

![trained_LLM_synthetic_ds](https://github.com/user-attachments/assets/5db230e0-faa8-4d9c-b825-be30f1b2da80)
The trained model achieves better quantitative measures.

## Streamlit application for qualitative Evaluation
Built a streamlit application for qualitative evaluation from field experts
![image](https://github.com/user-attachments/assets/ce516ae3-8712-4722-b2bc-e01f9e944e59)

Qualitative analysis result **to be added**.
