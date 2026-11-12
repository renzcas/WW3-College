def propagate_crisis(
    network,
    agents,
    source,
    severity
):
    """
    Propagate escalation across neighbors.
    """

    agents[source].escalation += severity

    for neighbor, weight in network.neighbors(source).items():

        spread = severity * weight * 0.5

        agents[neighbor].escalation += spread