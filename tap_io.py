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


def load_points(path):
  pts = []
  with open(path) as f:
    for line in f:
      line = line.strip().split(" ")
      pts.append([int(line[0]), int(line[1])])

  return pts


def load_solutions(path):
  opt_sol = {}
  with open(path) as f:
      skip = True
      sol_idx = 0
      z_idx = 0
      for line in f:
          if skip:
              skip = False
              line = line.strip().split(";")
              for idx, header in enumerate(line):
                if header == "z":
                  z_idx = idx
                if header == "solution":
                  sol_idx = idx
              continue
          line = line.strip().split(";")
          opt_sol[line[0] + "_" + line[1]] = (list(map(lambda x : int(x)-1, line[sol_idx].split(","))), float(line[z_idx]))
  return opt_sol

def load_filtering_report(path):
  report = dict()
  with open(path) as f:
    skip = True
    for line in f:
      if skip:
        skip = False
        continue
      line = line.strip().split(";")
      report[line[0] + "_" + line[1]] = list(map(int,line[2].strip(",").split(",")))

  return report
