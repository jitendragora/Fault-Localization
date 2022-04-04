import pandas as pd
import csv
#df1 = pd.read_csv('RankingMetricsScore_tcasMutantLine72_V1.csv')
a = zip(*csv.reader(open("RankingMetricsScore_tcasMutantLine63_V4.csv", "r")))
csv.writer(open("RankingMetricsScore_tcasMutantLine63_V4.csv", "w")).writerows(a)

