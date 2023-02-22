Setting Environment
===============
conda activate cdss

Running FastAPI
==============
uvicorn api:app --reload

Running ML Model Prediction
==============
python mainV2.py -m predict < temp_inputs
