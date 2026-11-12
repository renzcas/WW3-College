from simulation.network import InfluenceNetwork


def test_add_edge():

    net = InfluenceNetwork()

    net.add_edge(
        "USA",
        "NATO",
        0.8
    )

    assert (
        net.edge_weight(
            "USA",
            "NATO"
        ) == 0.8
    )

    assert (
        net.edge_weight(
            "NATO",
            "USA"
        ) == 0.8
    )


def test_neighbors():

    net = InfluenceNetwork()

    net.add_edge(
        "USA",
        "NATO",
        0.8
    )

    assert (
        "NATO"
        in net.neighbors("USA")
    )