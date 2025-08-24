import numpy as np
from logger_config import setup_logger
logger = setup_logger()

def getting_phase(data, aligned_data):
    pos_indices = np.where(~np.isnan(data) & (data > 0))[0]
    pos_occurance_deg = aligned_data[pos_indices]

    pos_mask_bot = pos_occurance_deg > 270
    pos_mask_top = pos_occurance_deg < 270

    neg_indices = np.where(~np.isnan(data) & (data < 0))[0]
    neg_occurance_deg = aligned_data[neg_indices]

    dict_phase = {}
    if np.any(pos_mask_bot):
        dict_phase["pos"] = {
            "bot": float(np.min(pos_occurance_deg[pos_mask_bot])),
            "top": float(np.max(pos_occurance_deg[pos_mask_top])),
        }
    else:
        dict_phase["pos"] = {
        "bot": float(np.min(pos_occurance_deg[pos_mask_top])),
        "top": float(np.max(pos_occurance_deg[pos_mask_top])),
    }
    dict_phase["neg"] = {
        "bot": float(np.min(neg_occurance_deg)),
        "top": float(np.max(neg_occurance_deg)),
    }

    print(dict_phase)
    return dict_phase

def getting_charge(data):
    pos_val = data[data > 0]
    pos_avg = np.nanmean(pos_val)
    pos_max_val = np.nanmax(pos_val)
    pos_min_val = np.nanmin(pos_val)

    neg_val = data[data < 0]
    neg_avg = np.nanmean(neg_val)
    neg_min_val = np.nanmax(neg_val)
    neg_max_val = np.nanmin(neg_val)
    
    dict_charge = {
        "pos": {
            "avg": float(pos_avg),
            "max": float(pos_max_val),
            "min": float(pos_min_val)
        },
        "neg": {
            "avg": float(neg_avg),
            "max": float(neg_max_val),
            "min": float(neg_min_val)
        }
    }

    print(dict_charge)
    return dict_charge

def getting_n(data):
    pos_count = np.sum(data > 0)
    neg_count = np.sum(data < 0)
    
    dict_count = {
        "pos": int(pos_count),
        "neg": int(neg_count)
    }

    print(dict_count)
    return pos_count, neg_count