from simulation.network import InfluenceNetwork
from simulation.crises import propagate_crisis
from models.agent import Agent


def test_crisis_propagation():

    net = InfluenceNetwork()

    net.add_edge(
        "USA",
        "NATO",
        1.0
    )

    agents = {
        "USA": Agent("USA"),
        "NATO": Agent("NATO")
    }

    propagate_crisis(
        net,
        agents,
        "USA",
        50
    )

    assert (
        agents["USA"].escalation
        == 50
    )

    assert (
        agents["NATO"].escalation
        > 0
    )