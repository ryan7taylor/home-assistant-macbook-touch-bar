#!/usr/bin/env python3
"""Light slider widget

This is a "Custom Apple Script Slider Widget" type.
In the widget config add (*fix paths yourself*)
```
return do shell script ("~/miniconda3/bin/python ~/Downloads/home-assistant-macbook-touch-bar/widgets/light-slider.py --entity_id light.living_room_lights --state")
```
and in the "Action Configuration" add
```
on bttWidgetSliderMoved(sliderValue)
	set cmd to "~/miniconda3/bin/python ~/Downloads/home-assistant-macbook-touch-bar/widgets/light-slider.py --entity_id light.living_room_lights --set " & sliderValue
	do shell script cmd
end bttWidgetSliderMoved
```
"""
import argparse

from utils import entity, service

parser = argparse.ArgumentParser()
parser.add_argument("--entity_id", action="store", required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--state", action="store_true")
group.add_argument("--set", action="store")
args = parser.parse_args()

domain = args.entity_id.split(".")[0]

if args.state:
    state = entity(args.entity_id)
    brightness = state["attributes"]["brightness"] if state["state"] == "on" else 0
    print(brightness / 255)
else:  # setting the state
    brightness = round(255 * float(args.set.replace(",", ".")))
    response = service(domain, "turn_on", args.entity_id, brightness=brightness)
    print(f"Setting brightness={brightness}")
