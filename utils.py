import torch
import numpy as np
import os
import cv2
import yaml
from pathlib import Path

here = Path(__file__).parent.resolve()

config_path = Path(here, "config.yaml")

if os.path.exists(config_path):
    config = yaml.load(open(config_path, "r"), Loader=yaml.FullLoader)

    annotator_ckpts_path = str(Path(here, config["annotator_ckpts_path"]))
    HF_MODEL_NAME = str(Path(here, config["HF_MODEL_NAME"]))
    DWPOSE_MODEL_NAME = str(Path(here, config["DWPOSE_MODEL_NAME"]))
else:
    annotator_ckpts_path = str(Path(here, "./ckpts"))
    HF_MODEL_NAME = "lllyasviel/Annotators"
    DWPOSE_MODEL_NAME = "yzd-v/DWPose"

def pad64(x):
    return int(np.ceil(float(x) / 64.0) * 64 - x)

def common_annotator_call(model, tensor_image, **kwargs):
    out_list = []
    for image in tensor_image:
        np_image = np.asarray(image * 255., dtype=np.uint8) 
        np_result = model(np_image, output_type="np", **kwargs)
        out_list.append(torch.from_numpy(np_result.astype(np.float32) / 255.0))
    return torch.stack(out_list, dim=0)
