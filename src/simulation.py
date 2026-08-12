import random


def simulate(regime, seed, agents, steps, regimes):
    rng = random.Random(seed)
    tau = regimes[regime]["tau"]
    rho = regimes[regime]["rho"]
    trust = [rng.random() for _ in range(agents)]
    belief = [0] * agents
    evacuated = [0] * agents
    degree = 6
    neighbours = [[rng.randrange(agents) for _ in range(degree)] for _ in range(agents)]
    rows = []

    for tick in range(steps):
        official_active = tick >= tau
        for index in range(agents):
            if official_active and belief[index] != 1 and rng.random() < 0.15 * trust[index]:
                belief[index] = 1
            if rng.random() < 0.05 * rho:
                belief[index] = 2 if belief[index] != 1 or rng.random() > trust[index] else belief[index]

            linked = neighbours[index]
            rumour_neighbours = sum(1 for item in linked if belief[item] == 2)
            official_neighbours = sum(1 for item in linked if belief[item] == 1)
            if rumour_neighbours > official_neighbours and rng.random() < rho * rumour_neighbours / degree:
                belief[index] = 2
            elif official_neighbours > rumour_neighbours and rng.random() < trust[index] * official_neighbours / degree:
                belief[index] = 1

            if evacuated[index] == 0:
                if belief[index] == 1 and rng.random() < 0.3:
                    evacuated[index] = 1
                elif belief[index] == 2 and rng.random() < 0.1 * rho:
                    evacuated[index] = 1

        rows.append(
            (
                tick,
                sum(evacuated),
                sum(1 for item in belief if item == 2),
                sum(1 for item in belief if item == 1),
            )
        )

    return rows


def summarise(rows):
    final = rows[-1]
    peak_evacuation = max(row[1] for row in rows)
    peak_rumour = max(row[2] for row in rows)
    peak_official = max(row[3] for row in rows)
    stride = max(1, len(rows) // 8)
    samples = "; ".join(f"t{row[0]}:e{row[1]}/r{row[2]}/o{row[3]}" for row in rows[::stride])
    return (
        f"timeline t=[0,{rows[-1][0]}]; final (evacuated={final[1]}, "
        f"rumor_believers={final[2]}, official_reached={final[3]}); peaks "
        f"(evac={peak_evacuation}, rumor={peak_rumour}, official={peak_official}). "
        f"Sampled trajectory every ~10 ticks: {samples}"
    )

