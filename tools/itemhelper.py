Registries = JavaClass("net.minecraft.core.registries.Registries")
ItemStack = JavaClass("net.minecraft.world.item.ItemStack")
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation")
Minecraft = JavaClass("net.minecraft.client.Minecraft")
ItemEnchantments = JavaClass("	net.minecraft.world.item.enchantment.ItemEnchantments")
EnchantmentHelper = JavaClass("net.minecraft.world.item.enchantment.EnchantmentHelper")
Mutable = JavaClass("net.minecraft.world.item.enchantment.ItemEnchantments$Mutable")
Holder = JavaClass("net.minecraft.core.Holder")
Predicate = JavaClass("java.util.function.Predicate")
ResourceKey = JavaClass("net.minecraft.resources.ResourceKey")

mc = Minecraft.getInstance()
level = mc.level

class ItemHelper():
    def __init__(self, item_stack: tuple[str, int]|ItemStack, enchantments: dict={}):
        if type(item_stack) is ItemStack:
            self.item_stack = item_stack
        else:
            self.item_stack = ItemStack(self._get_item_registry_entry(item_stack[0]), item_stack[1])
            for type,level in enchantments.items():
                self.add_enchantment(type, level)
    
    def add_enchantment(self, enchantment_id, level):
        item_enchantments = EnchantmentHelper.getEnchantmentsForCrafting(self.item_stack)
            
        mutable = Mutable(item_enchantments)
        mutable.upgrade(self._get_enchantment_registry_entry(enchantment_id), level)
        
        item_enchantments = mutable.toImmutable()
        EnchantmentHelper.setEnchantments(self.item_stack, item_enchantments)
        return self
    
    def remove_enchantment(self, enchantment_id, level):
        item_enchantments = EnchantmentHelper.getEnchantmentsForCrafting(self.item_stack)
            
        mutable = Mutable(item_enchantments)
        
        def check(entry):
            return entry.method_55838(self._get_enchantment_registry_entry(enchantment_id))
        
        mutable.removeIf(Predicate(check))
       
        item_enchantments = mutable.toImmutable()
        EnchantmentHelper.setEnchantments(self.item_stack, item_enchantments)
        return self
    
    def _get_registry_from_key(self, key):
        registry_access = level.registryAccess()
        registry = registry_access.lookupOrThrow(key)
        return registry
   
    def _get_item_registry_entry(self, item_id):
        item_registry = self._get_registry_from_key(Registries.ITEM)
        return item_registry.getValue(ResourceLocation.parse(item_id))
   
    def _get_enchantment_registry_entry(self, enchantment_id):
        enchantment_registry = self._get_registry_from_key(Registries.ENCHANTMENT)
        key = ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.parse(enchantment_id))
        return enchantment_registry.getOrThrow(key)
    
    def get_item_stack(self):
        return self.item_stack
