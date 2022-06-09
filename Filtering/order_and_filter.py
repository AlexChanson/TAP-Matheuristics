import decimal
import random
from main import load_instance, save_instance

if __name__ == '__main__':
    filter_ratio = 0.85

    instances = list()
    input_instances = "C:\\Users\\chanson\\Desktop\\instances_euc_coord\\"
    debug = False

    for size in [40, 60, 80, 100, 200, 300, 400]:
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

    with open ("./filtered_instances/filtering_report.csv", mode="w") as fr:
        print("id;size;removed", file=fr)
        for ist in instances:
            print(str(ist["id"]) + ";" + str(ist["size"]) + ";", file=fr, end="")
            idx = []
            for i in range(ist['size']):
                this_i = ist["interest"][i]
                this_t = ist["time"][i]
                dom_set = set()
                for j in range(ist['size']):
                    if i != j and this_i < ist["interest"][j] and this_t > ist["time"][j]:
                        dom_set.add(j)
                idx.append((i, len(dom_set)))

            idx.sort(key=lambda x: x[1], reverse=False)
            I = []
            T = []
            D = []
            cnt = 0
            for i in idx:
                i = i[0]
                if cnt > ist['size']* filter_ratio:
                    print(str(i) + ",", end="", file=fr)
                    continue
                I.append(ist["interest"][i])
                T.append(ist["time"][i])
                d = []
                cnt_ = 0
                for j in idx:
                    j = j[0]
                    if cnt_ > ist['size'] * filter_ratio:
                        continue
                    d.append(ist["distances"][i][j])
                    cnt_ += 1
                D.append(d)
                cnt += 1

            ni = {"size": cnt, "interest": I, "time": T, "distances":D}

            save_instance("./filtered_instances/tap_"+ str(ist["id"]) + "_" + str(ist["size"]) + ".dat", ni)

            #print(str(ist["id"]) + "," + str(ist["size"]) + "," + str(len((idx))) + "," + str(N) + "," + str(moy_dom_set))
            print(str(ist["id"]) + "," + str(ist["size"]) + "," + str(cnt))
            #print(dom_set_sizes)
            print("", file=fr)


