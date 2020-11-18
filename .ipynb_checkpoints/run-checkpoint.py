import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from drill.flow.run_inference import run_inference

run_inference()
