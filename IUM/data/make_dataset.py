from typing import List, Dict
import json

base_path = "/media/jzielins/SD/sem6/IUM/IUM/data"


def load_json_data(data_name : str) -> Dict :
    with open(base_path + "/raw/" +  data_name + "s.jsonl", "r") as file:
        lines = file.readlines()

    objects = {}
    id = data_name + "_id"

    for line in lines:
        object_v = json.loads(line)
        objects[object_v[id]] = object_v
    

    objects["meta_name"] = data_name

    return objects


def load_sessions(data_name):
    file = open(base_path + "/raw/" +  data_name + "s.jsonl", "r")
    lines = file.readlines()

    sessions = {"meta_name" : "sessions"}

    for line in lines:
        session : Dict[str, Dict] = json.loads(line)
        
        if session["event_type"] == "BUY_PRODUCT":
            sessions[session["purchase_id"]] = session
    return sessions


def aggregate_data(data_sets : List[Dict[int, Dict]], sessions : Dict):
    for data_set in data_sets:
        for key, session in sessions.items():
            if key != "meta_name":                
                id_key = data_set["meta_name"] + "_id"
                data = data_set[session[id_key]].copy()            
                del data[id_key]

                del session[id_key]
                session.update(data)


def save_aggregated_data(data : Dict):
    with open(base_path + "/processed/sessions.jsonl", "w") as file:
        for key, value in data.items():
            if key != "meta_name":
                json.dump(value, file)
                file.write("\n")


if __name__ == "__main__":
    users = load_json_data("user")
    products = load_json_data("product")
    purchases = load_json_data("purchase")
    sessions = load_sessions("session")
    
    aggregate_data([products, users, purchases], sessions)
    save_aggregated_data(sessions)