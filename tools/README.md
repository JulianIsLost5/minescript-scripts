## Usage

- Download the **itemhelper.py** file
- Place it directly in the minescript folder
- Import it into your script (must end on `.pyj`)

---
## Example Use
```py
from itemhelper import ItemHelper

myitem = ItemHelper([minecraft:diamond_sword, 1], {"minecraft:sharpness":5, "minecraft:mending":1, "minecraft:fire_aspect":1})
myitem.add_enchantment("minecraft:unbreaking", 3)
myitem.remove_enchantment("minecraft:fire_aspect", 1)

item_stack = myitem.get_item_stack() # returns the actual ItemStack instance
```
