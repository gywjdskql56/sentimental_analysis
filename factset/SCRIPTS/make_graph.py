import pandas as pd
from matplotlib import pyplot as plt
import os
from datetime import datetime, timedelta
plt.rcParams["figure.figsize"] = (14,4)

pr_org = pd.read_excel('data/AAPL_PR.xlsx')
pr_org.columns = ['Date', 'AAPL US EQUITY']

file_list = list(filter(lambda x: '.xlsx' in x, os.listdir('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US'))))
file_date_list = sorted(list(map(lambda x: datetime.strptime((x.split('-')[0]), '%Y%m%d'), file_list)))
date_df = pd.DataFrame(file_date_list, columns=['Date'])
date_df['Date'] = file_date_list

pr_org = pd.merge(pr_org, date_df, left_on = 'Date', right_on = 'Date', how='outer')
pr_org = pr_org.set_index('Date')
date_list = sorted(list(pr_org.index))
pr_org = pr_org.loc['2002-01-01':]
pr = (pr_org.pct_change().fillna(0)+1).cumprod()

plt2 = plt
plt.plot(pr)

# for file in sorted(file_list):
#     print(file)
#     try:
#         score_df = pd.read_excel('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US') + file)
#         date = datetime.strptime((file.split('-')[0]), '%Y%m%d')
#         plt.vlines(date, 1, max(pr.values)+1, colors='red')
#         plt.savefig('result/{}.png'.format('ALL'))
#     except:
#         print('ERROR')
# plt.savefig('result/{}.png'.format('ALL'))
# plt.clf()


for year in sorted(list(map(lambda x: x[:4], file_list))):
    print(year)
    pr_2 = pr_org.loc['{}-01-01'.format(year): '{}-12-31'.format(year)]
    pr_2 = (pr_2.pct_change().fillna(0) + 1).cumprod()
    plt2.plot(pr_2, color='black')
    year_date = list(filter(lambda x: str(x)[:4] == year, file_list))
    year_date = list(map(lambda x: datetime.strptime((x.split('-')[0]), '%Y%m%d'), year_date))
    for y_date in year_date:

        y_date_pre = date_list[date_list.index(y_date)-1]
        y_date_aft = date_list[date_list.index(y_date)+1]
        pr_2_label = (pr_2.loc[y_date_aft] - pr_2.loc[y_date_pre]).values * 100
        if pr_2_label>0:
            plt2.vlines(y_date, min(pr_2.values), max(pr_2.values), color='blue', linewidth=pr_2_label, alpha=0.5)
        else:
            plt2.vlines(y_date, min(pr_2.values), max(pr_2.values), color='red', linewidth=pr_2_label, alpha=0.5)
    plt2.savefig('result/{}.png'.format(str(year)))
    plt2.clf()
print(1)