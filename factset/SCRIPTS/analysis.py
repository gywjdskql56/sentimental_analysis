import pandas as pd
import os
import pickle
import finbert as fb
from googletrans import Translator
import certifi
certifi.where()
translator = Translator()
ticker_list = os.listdir('D:/XML')
file_list = list(filter(lambda x: 'pickle' in x, os.listdir('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US'))))
# with open('D:/XML/{}/{}'.format('AAPL-US',file_list[0])) as f:
#     data = f.read()
analysis_df = pd.DataFrame(columns=['type','sentence','kor_sentence','pos','neu','neg'])
for file in file_list[1:]:
    print(file)
    if True:#file.replace('.pickle','.xlsx') not in os.listdir('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US')):
        with open('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/{}'.format('AAPL-US',file), 'rb') as handle:
            data = pickle.load(handle)
            part_dict = dict()
            count = 0
            for key in data['participant'].keys():
                try:
                    part_dict[data['participant'][key]['id']] = data['participant'][key]['type']
                except:
                    part_dict[data['participant'][key]['id']] = 'NM_'+data['participant'][key]['content']

            for key in data['section']['MANAGEMENT DISCUSSION SECTION'].keys():
                if key == '0':
                    pass
                else:
                    sent_dict = data['section']['MANAGEMENT DISCUSSION SECTION'][key]
                    sent_list = sent_dict['content']
                    for sent in sent_list:
                        if len(sent) < 100:
                            if 'id' in sent_dict.keys():
                                analysis_df.loc[count, 'type'] = "MD_"+part_dict[sent_dict['id']]
                            analysis_df.loc[count, 'sentence'] = sent
                            kor_sent = translator.translate(sent, dest="ko")
                            analysis_df.loc[count, 'kor_sentence'] = kor_sent[0].text
                            score = fb.cal_finbert_score(sent)
                            analysis_df.loc[count, 'pos'] = score[0]
                            analysis_df.loc[count, 'neg'] = score[1]
                            analysis_df.loc[count, 'neu'] = score[2]
                            analysis_df.loc[count, 'sentiment'] = score[3]
                            count += 1
                        else:
                            for sen in sent.split('. '):
                                if 'id' in sent_dict.keys():
                                    analysis_df.loc[count, 'type'] = "MD_"+part_dict[sent_dict['id']]
                                analysis_df.loc[count, 'sentence'] = sen
                                kor_sent = translator.translate(sent, dest="ko")
                                analysis_df.loc[count, 'kor_sentence'] = kor_sent[0].text
                                score = fb.cal_finbert_score(sen)
                                analysis_df.loc[count, 'pos'] = score[0]
                                analysis_df.loc[count, 'neg'] = score[1]
                                analysis_df.loc[count, 'neu'] = score[2]
                                analysis_df.loc[count, 'sentiment'] = score[3]
                                count += 1
            if 'Q&amp;A' in data['section'].keys():
                for key in data['section']['Q&amp;A'].keys():
                    if key == '0':
                        pass
                    else:
                        sent_dict = data['section']['Q&amp;A'][key]
                        sent_list = sent_dict['content']
                        for sent in sent_list:
                            if len(sent) < 200:
                                if 'type' in sent_dict.keys():
                                    analysis_df.loc[count, 'type'] = "QA_"+ sent_dict['type']
                                else:
                                    analysis_df.loc[count, 'type'] = "QA_"+part_dict[sent_dict['id']]
                                analysis_df.loc[count, 'sentence'] = sent
                                kor_sent = translator.translate(sent, dest="ko")
                                analysis_df.loc[count, 'kor_sentence'] = kor_sent[0].text
                                score = fb.cal_finbert_score(sent)
                                analysis_df.loc[count, 'pos'] = score[0]
                                analysis_df.loc[count, 'neg'] = score[1]
                                analysis_df.loc[count, 'neu'] = score[2]
                                analysis_df.loc[count, 'sentiment'] = score[3]
                                count += 1
                            else:
                                for sen in sent.split('. '):
                                    if 'type' in sent_dict.keys():
                                        analysis_df.loc[count, 'type'] = "QA_" + sent_dict['type']
                                    else:
                                        analysis_df.loc[count, 'type'] = "QA_" + part_dict[sent_dict['id']]
                                    analysis_df.loc[count, 'sentence'] = sen
                                    kor_sent = translator.translate(sent, dest="ko")
                                    analysis_df.loc[count, 'kor_sentence'] = kor_sent[0].text
                                    score = fb.cal_finbert_score(sen)
                                    analysis_df.loc[count, 'pos'] = score[0]
                                    analysis_df.loc[count, 'neg'] = score[1]
                                    analysis_df.loc[count, 'neu'] = score[2]
                                    analysis_df.loc[count, 'sentiment'] = score[3]
                                    count += 1
            analysis_df.to_excel('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/{}'.format('AAPL-US',file.replace('.pickle','.xlsx')))
print(1)


