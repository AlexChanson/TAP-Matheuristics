import decimal
import random


def load_instance(file):
    with open(file) as f:
        n = int(f.readline())
        I = []
        for e in f.readline().split(" "):
            I.append(float(e))
        T = []
        for e in f.readline().split(" "):
            T.append(float(e))
        D = []
        for i in range(n):
            d = []
            for e in f.readline().split(" "):
                d.append(float(e))
            D.append(d)
    return n, I, T, D


def save_instance(file, instance):
    with open(file, mode="w") as f:
        print(instance['size'], file=f)
        print(str(instance["interest"]).replace('[', '').replace(']', '').replace(',', ''), file=f)
        print(str(instance["time"]).replace('[', '').replace(']', '').replace(',', ''), file=f)
        for i in range(instance["size"]):
            print(str(instance["distances"][i]).replace('[', '').replace(']', '').replace(',', ''), file=f)


def get_distances(ist):
    l = []
    for i, line in enumerate(ist["distances"]):
        l.extend(line[i+1:])
    return l


def find_bound_by_distance(ist):
    k = ist['size']
    used = set()
    dis = 0
    while True:
        best = float('inf')
        best_id = (-1, -1)
        for i in range(ist["size"]):
            if i not in used:
                for j in range(i, ist['size']):
                    if i != j and j not in used and ist["distances"][i][j] < best:
                        best_id = (i,j)
                        best = ist["distances"][i][j]
        if dis + best*2 <= ist["ed"]:
            used.add(best_id[0])
            used.add(best_id[1])
            dis += best*2
        else:
            break


    return min(k, len(used))


if __name__ == '__main__':

    opt_bound = {}
    opt_sol = {}
    with open("./data/exact_f4.csv") as f:
        skip = True
        for line in f:
            if skip:
                skip = False
                continue
            line = line.strip().split(";")
            #print(line)
            opt_bound[line[0] + "_" + line[1]] = len(line[7].split(","))
            opt_sol[line[0] + "_" + line[1]] = list(map(int, line[7].split(",")))

    instances = list()
    input_instances = "C:\\Users\\chanson\\Desktop\\instances\\"
    debug = False

    for size in [300]:
        for series_id in range(30):
            ist = dict()
            ist["id"] = series_id
            ist["size"] = size
            n, ist["interest"], ist["time"], ist["distances"] = load_instance(input_instances + "tap_" + str(ist["id"]) + "_" + str(ist["size"]) + ".dat")
            ist["ed"] = int(decimal.Decimal(str(0.3 * n * 4.5)).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))
            ist["et"] = int(decimal.Decimal(str(0.6 * n * 27.5)).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))

            instances.append(ist)

    print("Loading done")
    print("id,size,filtered_size")
    cnt = 0
    for ist in instances:
        # estimation of optimal solution size
        # By time
        at = 0
        k = 0
        for item in sorted(ist["time"]):
            if at + item > ist["et"]:
                break
            else:
                at += item
                k += 1
        # By distances
        k_ = 0
        ad = 0
        for item in sorted(get_distances(ist)):
            if item == 0.:
                continue
            if ad + item > ist["ed"]:
                break
            else:
                ad += item
                k_ += 1
        # Take the min
        #print(k,  find_bound_by_distance(ist), opt_bound[str(ist["id"]) + "_" + str(ist["size"])])
        N = min(k,  find_bound_by_distance(ist))#, opt_bound[str(ist["id"]) + "_" + str(ist["size"])])
        #print(N, 0.3 * n, 0.6 * n, find_bound_by_distance(ist), k)

        if N == k_:
            cnt += 1# dist bound is smaller

        idx = []
        moy_dom_set = 0
        dom_set_sizes = []
        for i in range(ist['size']):
            this_i = ist["interest"][i]
            this_t = ist["time"][i]
            dom_set = set()
            for j in range(ist['size']):
                if i != j and this_i < ist["interest"][j] and this_t > ist["time"][j]:
                    dom_set.add(j)
            moy_dom_set += len(dom_set)
            dom_set_sizes.append(len(dom_set))
            #print dom set and presence in opt
            print(len(dom_set), i in opt_sol[str(ist["id"]) + "_" + str(ist["size"])])
            if len(dom_set) <= N:
                idx.append(i)
            else:
                if debug:
                    print(str(ist["id"]) + "_" + str(ist["size"]), "removed", i+1)

        moy_dom_set = moy_dom_set / float(ist['size'])
        I = []
        T = []
        D = []

        for i in idx:
            I.append(ist["interest"][i])
            T.append(ist["time"][i])
            d = []
            for j in idx:
                d.append(ist["distances"][i][j])
            D.append(d)

        ni = {"size": len(idx), "interest": I, "time": T, "distances":D}

        save_instance("./filtered_instances/tap_"+ str(ist["id"]) + "_" + str(ist["size"]) + ".dat", ni)

        #print(str(ist["id"]) + "," + str(ist["size"]) + "," + str(len((idx))) + "," + str(N) + "," + str(moy_dom_set))
        #print(str(ist["id"]) + "," + str(ist["size"]) + "," + str(len((idx))))
        #print(dom_set_sizes)

        inv_dom_size = []
        for i in range(ist['size']):
            this_i = ist["interest"][i]
            this_t = ist["time"][i]
            dom_set = set()
            for j in range(ist['size']):
                if i != j and this_i > ist["interest"][j] and this_t < ist["time"][j]:
                    dom_set.add(j)
            inv_dom_size.append(len(dom_set))
        #print(inv_dom_size)
