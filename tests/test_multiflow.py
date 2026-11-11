from models.world import World

def test_multiple_flow_atomicity():

    world = World()

    world.add_node(
        "usa",
        {"food": 100.0}
    )

    world.add_node(
        "japan",
        {"food": 0.0}
    )

    world.add_node(
        "korea",
        {"food": 0.0}
    )

    world.add_flow(
        "usa",
        "japan",
        "food",
        10.0
    )

    world.add_flow(
        "usa",
        "korea",
        "food",
        20.0
    )

    world.step()

    assert (
        world.nodes["usa"]["state"]["food"]
        == 70.0
    )

    assert (
        world.nodes["japan"]["state"]["food"]
        == 10.0
    )

    assert (
        world.nodes["korea"]["state"]["food"]
        == 20.0
    )