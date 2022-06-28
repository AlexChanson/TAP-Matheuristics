from tap_io import load_instance

folder = "/path/to/instance/folder/"

for size in [40, 60, 80, 100, 200, 300]:
    for series_id in range(30):
        n, I, T, D = load_instance(folder + "tap_" + str(series_id) + "_" + str(size) + ".dat")
        tsp_solution = []
        ks_solution = []
        with open(folder + "tap_" + str(series_id) + "_" + str(size) + ".tsp") as f:
            tsp_solution.extend(map(int, f.readlines()[0].split(" ")))
        with open(folder + "tap_" + str(series_id) + "_" + str(size) + ".ks") as f:
            ks_solution.extend(map(int, f.readlines()[0].split(" ")))
        z_ks = sum(map(lambda q : I[q],ks_solution))
        z_tsp = sum(map(lambda q : I[q],tsp_solution))
        best = tsp_solution if z_tsp > z_ks else ks_solution
        with open(folder + "tap_" + str(series_id) + "_" + str(size) + ".warm", mode="w") as out:
            out.write(str(best).replace(",","").lstrip("[").rstrip("]"))
