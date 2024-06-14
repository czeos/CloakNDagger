from maltego_trx.decorator_registry import TransformRegistry


registry = TransformRegistry(
        owner="CloakNDagger",
        author="Mike",
        host_url="gossip.monster",
        seed_ids=["demo"]
)

# metadata
registry.version = "0.1"

#settings
# registry.global_settings = [hunchly_api_path]