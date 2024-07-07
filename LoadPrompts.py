import json
import os
from collections import OrderedDict

class LoadPrompts():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["append", "rewrite","clear"], {"default": "append"}),
            },
            "optional": {
                "Que": ("STRING", {"forceInput": True, "multiline": True}),
                "Res": ("STRING", {"forceInput": True, "multiline": True}),
                "Neg": ("STRING", {"forceInput": True, "multiline": True}),
                "load_index": ("INT", {"default": None, "min": 0}),
                "Positive": ("STRING", {"default": "", "multiline": True}),
                "Negative": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING")
    RETURN_NAMES = ("Question", "Positive", "Negative")
    FUNCTION = "load_prompts"
    OUTPUT_NODE = True
    CATEGORY = "ArteMoon"

    def load_prompts(self, mode, Que="", Res="", Neg="", load_index=None, Positive="", Negative=""):
        json_file = os.path.join(os.path.dirname(__file__), 'ai_prompts.json')

        if mode == "clear": 
            if os.path.exists(json_file):
                with open(json_file, 'w') as f:
                    json.dump([], f, indent = 4)

        if Que or Res or Neg:
            data = {"question": Que, "response": self.remove_duplicates(Positive + (',' if Positive and Res else '') + Res), "negative": self.remove_duplicates(Negative + (', ' if Negative and Neg else '') + Neg)}

            if os.path.exists(json_file):
                with open(json_file) as f:
                    existing_data = json.load(f)

                data['index'] = len(existing_data) if mode == 'append' else 0
                if mode == 'append':
                    existing_data.append(data)
                else:
                    existing_data = [data]
            else:
                data['index'] = 0
                existing_data = [data]

            with open(json_file, 'w') as f:
                f.write(json.dumps(existing_data, indent = 4))
        elif load_index is not None and os.path.exists(json_file):
            with open(json_file) as f:
                existing_data = json.load(f)
                if load_index < len(existing_data):
                    data = existing_data[load_index]
                    Que = data["question"]
                    Res = data["response"]
                    Neg = data["negative"]
        elif os.path.exists(json_file):
            with open(json_file) as f:
                existing_data = json.load(f)
                data = existing_data[-1]
                Que = data["question"]
                Res = data["response"]
                Neg = data["negative"]
        else:
            Que = ""
            Res = ""
            Neg = ""

        Positive_output = self.remove_duplicates(f"{Positive},{Res}" if Positive else Res)
        Negative_output = self.remove_duplicates(f"{Negative}, {Neg}" if Negative else Neg)

        return (Que, Positive_output, Negative_output)

    def remove_duplicates(self, input_string):
        trans = str.maketrans(",.", "..")
        items = [item.strip() for item in input_string.translate(trans).split('.')]
        unique_items = list(OrderedDict.fromkeys(items))
        return ", ".join(unique_items)