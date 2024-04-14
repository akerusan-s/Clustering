from models import KohonenClustering
from tools import load_2d_data, show

data = load_2d_data("2d_data.txt")

khn = KohonenClustering(k=4)

khn.fit(data)
ans = khn.predict_list(data)

show(data, ans, khn.centers)
