import requests
import re
from bs4 import BeautifulSoup

proxies = {
	'HTTP': "http://117.65.1.222:3256",
	# 'HTTP': "http://47.99.201.206",

}
res = requests.get(
	'https://www.guazi.com/Detail?clueId=119465055',
	proxies=proxies,
	headers={
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
		"referer": "https://www.guazi.com/buy?search=%257B%2522minor%2522%253A%2522benz%2522%257D",
		"cookies": "platform=pc; gzSupportWebp=1; uuid=50966328-df09-4a13-aa2d-815b5f449b37; sessionid=bea7caf3-2eb5-4aa8-8579-60a53567ef61; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2250966328-df09-4a13-aa2d-815b5f449b37%22%7D; ca_s=self; ca_n=self; DATE=1658277875919; crystal=U2FsdGVkX19EKjTjusje4CF+JmQqMWY3Fs+e9/l0a/+c/VAH4zfffb/0dyS1e6NSO5v3zG7TjtLJBeTAOlnMJyeIocsynM15LSOqw6pHO0wzXu2Z3dopuIAX3JXoh4+QePoVLIsTC1+Uv2Ywdajn6EQHxGQK7cK7Blhj8PHwKRMgiejNsfGwgdc+RVXjIUGvuEmF4jBU1CQRrtMxJ1tudkKazPN45h/HIc5mz7QwMJI5+pIEV8lJ6Fo1HF/BxL9c; cityId=13; cityDomain=sh; cityName=%E4%B8%8A%E6%B5%B7; SECKEY_ABVK=QgJ3oAo3JnA5w0WOY+fBzfHxx0x2L/bY8v7IfYNSTis%3D; BMAP_SECKEY=_9jc8muYnGSPIM0ZQJzJYJEFTWx8wYfbIKE-HvzddOkfkXan6Zc2NiU3mJPCN5eq_QYDsa_VIOntQSRQbrgDn3YZYNs9q-Y20FzUNqP0zsAcHVsAwCU0Zn6OKNL8MGHm2cn4lAbhoKOtYDUMilIw3I9Pd0lYgSZyfnRkxECSEqT-jCd6JPUAsC4kMCyYfGi-"
	},
)

soup = BeautifulSoup(res.text, 'lxml')

div = soup.find_all(name='div', class_='container')
print(div)

# 找车名
# car_name_tag = soup.find(name='h1')
# car_name = car_name_tag.stripped_strings.__next__()
