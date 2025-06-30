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
                "data": pos_val,
                "itemStyle": {
                    "color": '#e63946'
                }
            },   
            {
                "name": "(-)Sensor1",
                "type": "scatter",
                "data": neg_val,
                "itemStyle": {
                    "color": '#3d348b'
                }
            },   
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