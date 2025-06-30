def create_dict_calibration(title, data):
    dictionary = {
        "title": {"text": title, "left": "center"},
        "tooltip": {
            "trigger": "item",
            # "axisPointer": {"type": 'cross'}
            },
        "xAxis": {"type": "value", "name": "mV"},
        "yAxis": {"type": "value", "name": "pC"},
        "dataset": {"source": data, "dimensions": ['volt', 'charge']},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60,
            "borderWidth": 2
        },
        "series": [
            {
                "name": "Charge",
                "type": "scatter",
                "encode": {
                    "x": "volt",
                    "y": "charge"
                }
            }
        ]
    }
    return dictionary

def create_dict_timeline_chargeVal_3p(sines):
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {
            'textStyle': {'color': 'gray'},
            "data": ["chargePos-R", "chargeNeg-R", "chargePos-S", "chargeNeg-S", "chargePos-T", "chargeNeg-T"],
            "selected": {
                "chargePos-R": True,
                "chargeNeg-R": True,
                "chargePos-S": True,
                "chargeNeg-S": True,
                "chargePos-T": True,
                "chargeNeg-T": True,
            }
        },
        "xAxis": {"type": "value", "name": "t"},
        "yAxis": {"type": "value", "name": "Max Charge (pC)"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "chargePos-R",
                "type": "line",
                "showSymbol": False,
                "data": sines[0],
                "itemStyle": {"color": "#FF3F33"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "chargeNeg-R",
                "type": "line",
                "showSymbol": False,
                "data": sines[0],
                "itemStyle": {"color": "#FF9898"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "chargePos-S",
                "type": "line",
                "showSymbol": False,
                "data": sines[1],
                "itemStyle": {"color": "#FED16A"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "chargeNeg-S",
                "type": "line",
                "showSymbol": False,
                "data": sines[1],
                "itemStyle": {"color": "#FFEB00"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "chargePos-T",
                "type": "line",
                "showSymbol": False,
                "data": sines[2],
                "itemStyle": {"color": "#3a86ff"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "chargeNeg-T",
                "type": "line",
                "showSymbol": False,
                "data": sines[2],
                "itemStyle": {"color": "#8DD8FF"},
                "lineStyle": {"width": 4},
            },
        ]
    }
    return dictionary
    
def create_dict_timeline_chargeCount_3p(sines):
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {
            'textStyle': {'color': 'gray'},
            "data": ["countPos-R", "countNeg-R", "countPos-S", "countNeg-S", "countPos-T", "countNeg-T"],
            "selected": {
                "countPos-R": True,
                "countNeg-R": True,
                "countPos-S": True,
                "countNeg-S": True,
                "countPos-T": True,
                "countNeg-T": True,
            }
        },
        "xAxis": {"type": "value", "name": "t"},
        "yAxis": {"type": "value", "name": "Count"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "countPos-R",
                "type": "line",
                "showSymbol": False,
                "data": sines[0],
                "itemStyle": {"color": "#FF3F33"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "countNeg-R",
                "type": "line",
                "showSymbol": False,
                "data": sines[0],
                "itemStyle": {"color": "#FF9898"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "countPos-S",
                "type": "line",
                "showSymbol": False,
                "data": sines[1],
                "itemStyle": {"color": "#FED16A"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "countNeg-S",
                "type": "line",
                "showSymbol": False,
                "data": sines[1],
                "itemStyle": {"color": "#FFEB00"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "countPos-T",
                "type": "line",
                "showSymbol": False,
                "data": sines[2],
                "itemStyle": {"color": "#3a86ff"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "countNeg-T",
                "type": "line",
                "showSymbol": False,
                "data": sines[2],
                "itemStyle": {"color": "#8DD8FF"},
                "lineStyle": {"width": 4},
            },
        ]
    }
    return dictionary

def create_dict_prpd_3p(sines, sensors):
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {
            'textStyle': {'color': 'gray'},
            "data": ["Sine-R", "Sine-S", "Sine-T"],
            "selected": {
                "Sine-R": False,
                "Sine-S": False,
                "Sine-T": True,
            }
        },
        "xAxis": {"type": "value", "name": "Deg", "max": 360},
        "yAxis": {"type": "value", "name": "Charge (pC)"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "Sine-R",
                "type": "line",
                "showSymbol": False,
                "data": sines[0],
                "itemStyle": {"color": "#FF3F33"},
                # "itemStyle": {"color": "#FF9898"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "Sine-S",
                "type": "line",
                "showSymbol": False,
                "data": sines[1],
                "itemStyle": {"color": "#FED16A"},
                # "itemStyle": {"color": "#FFEB00"},
                "lineStyle": {"width": 4},
            },
            {
                "name": "Sine-T",
                "type": "line",
                "showSymbol": False,
                "data": sines[2],
                "itemStyle": {"color": "#3a86ff"},
                # "itemStyle": {"color": "#8DD8FF"},
                "lineStyle": {"width": 4},
            },
            # {
            #     "name": "Sensor-R",
            #     "type": "line",
            #     "data": sensors[0],
            #     "itemStyle": {
            #         "color": '#3a86ff'
            #     }
            # },
            # {
            #     "name": "Sensor-S",
            #     "type": "line",
            #     "data": sensors[1],
            #     "itemStyle": {
            #         "color": '#3a86ff'
            #     }
            # },
            # {
            #     "name": "Sensor-T",
            #     "type": "line",
            #     "data": sensors[2],
            #     "itemStyle": {
            #         "color": '#3a86ff'
            #     }
            # },
        ]
    }
    return dictionary

def create_dict_prpd(data_sine, data_sensor):
    data_sensor1 = data_sensor[0]
    data_sensor2 = data_sensor[1]
    data_sensor3 = data_sensor[2]

    data_sensor2[:, 0] += 10
    data_sensor3[:, 0] -= 10

    pos1 = data_sensor1[data_sensor1[:, 1] > 0]
    neg1 = data_sensor1[data_sensor1[:, 1] < 0]
    pos2 = data_sensor2[data_sensor2[:, 1] > 0]
    neg2 = data_sensor2[data_sensor2[:, 1] < 0]
    pos3 = data_sensor3[data_sensor3[:, 1] > 0]
    neg3 = data_sensor3[data_sensor3[:, 1] < 0]
    
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {'textStyle': {'color': 'gray'}},
        "xAxis": {"type": "value", "name": "Deg"},
        "yAxis": {"type": "value", "name": "Charge (pC)"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "Phase Ref",
                "type": "line",
                "data": data_sine,
                "itemStyle": {
                    "color": '#3a86ff'
                }
            },
            {
                "name": "(+)Sensor1",
                "type": "scatter",
                "data": pos1,
                "itemStyle": {
                    "color": '#e63946'
                }
            },   
            {
                "name": "(-)Sensor1",
                "type": "scatter",
                "data": neg1,
                "itemStyle": {
                    "color": '#3d348b'
                }
            },
            {
                "name": "(+)Sensor2",
                "type": "scatter",
                "data": pos2,
                "itemStyle": {
                    "color": '#e63946'
                }
            },   
            {
                "name": "(-)Sensor2",
                "type": "scatter",
                "data": neg2,
                "itemStyle": {
                    "color": '#3d348b'
                }
            },
            {
                "name": "(+)Sensor3",
                "type": "scatter",
                "data": pos3,
                "itemStyle": {
                    "color": '#e63946'
                }
            },   
            {
                "name": "(-)Sensor3",
                "type": "scatter",
                "data": neg3,
                "itemStyle": {
                    "color": '#3d348b'
                }
            },
        ]
    }
    return dictionary

def create_dict_stream(data_stream):
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {'textStyle': {'color': 'gray'}},
        "xAxis": {"type": "value", "name": "Time"},
        "yAxis": {"type": "value", "name": "Voltage (mV)"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "Streaming",
                "type": "scatter",
                "data": data_stream,
                "itemStyle": {
                    "color": '#e63946'
                }
            }
        ]
    }
    return dictionary

def create_dict_prpd_test(data_sine, data_sensor_pos, data_sensor_neg):
    dictionary = {
        "tooltip": {"trigger": "item"},
        "legend": {'textStyle': {'color': 'gray'}},
        "xAxis": {"type": "value", "name": "Deg"},
        "yAxis": {"type": "value", "name": "Charge (pC)"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "Phase Ref",
                "type": "line",
                "data": data_sine,
                "itemStyle": {
                    "color": '#3a86ff'
                }
            },
            {
                "name": "(+)Sensor1",
                "type": "scatter",
                "data": data_sensor_pos,
                "itemStyle": {
                    "color": '#e63946'
                }
            },   
            {
                "name": "(-)Sensor1",
                "type": "scatter",
                "data": data_sensor_neg,
                "itemStyle": {
                    "color": '#3d348b'
                }
            }
        ]
    }
    return dictionary

def create_dict_historical(title, yAxis, data):
    dictionary = {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "time", "name": "Time"},
        "yAxis": {"type": "value", "name": yAxis},
        "dataset": {"source": data, "dimensions": ['timestamp', 'pos', 'neg']},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60
        },
        "series": [
            {
                "name": "Positive",
                "type": "line",
                "encode": {
                    "x": "timestamp",
                    "y": "pos"
                }
            },
            {
                "name": "Negative",
                "type": "line",
                "encode": {
                    "x": "timestamp",
                    "y": "neg"
                }
            },

        ]
    }
    return dictionary

def create_dict_counter_background(title, yAxisLabel, data):
    dictionary = {
        "title": {"text": title, "left": "center"},
        # "backgroundColor": "#d1dfff",
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "value", "name": "Count"},
        "yAxis": {"type": "value", "name": yAxisLabel},
        "dataset": {"source": data, "dimensions": ['count', 'pos', 'neg']},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 60,
            "borderWidth": 2
        },
        "series": [
            {
                "name": "Positive",
                "type": "line",
                "encode": {
                    "x": "count",
                    "y": "pos"
                }
            },
            {
                "name": "Negative",
                "type": "line",
                "encode": {
                    "x": "count",
                    "y": "neg"
                }
            },

        ]
    }
    return dictionary
