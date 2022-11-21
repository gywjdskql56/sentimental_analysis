import pandas as pd
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import pickle


def remove_tag(str,tag):
    return re.sub("<[/]?{}[^<>]*>".format(tag),"",str)
def find_and_remove_tag(bs_data, tag):
    return list(map(lambda x:re.sub("<{}>|</{}>|\n".format(tag,tag), "", str(x)), list(bs_data.find_all(tag)))) #re.sub("<[^<>]*>", "", str(x))
def make_tag_desc_dict(content_dict, sub_tag, p_key):
    tag_desc_dict_total = dict()
    for i in range(len(content_dict[sub_tag])):
        try:
            tag_desc = re.findall('<{}[^<>]*>'.format(sub_tag), str(content_dict[sub_tag][i]))[0]
            tag_desc = re.sub('<|>', '', tag_desc)
            tag_desc = re.sub('^{} '.format(sub_tag), '', tag_desc)
            tag_desc_dict = eval('{' + '",'.join(list(map(lambda x: "\"" + x.split("=")[0] + "\":" + x.split("=")[1],
                                                          filter(lambda x: "=" in x, tag_desc.split("\" "))))) + '}')
            tag_content = remove_tag(str(content_dict[sub_tag][i]), sub_tag)
            # tag_content = BeautifulSoup(str(content_dict[sub_tag]['MANAGEMENT DISCUSSION SECTION']['content'].replace('\n', '')), 'xml')
            tag_desc_dict['content'] = tag_content
            pk = tag_desc_dict[p_key]
            tag_desc_dict_total[pk] = tag_desc_dict
        except:
            tag_desc_dict = dict()
            tag_content = remove_tag(str(content_dict[sub_tag][i]), sub_tag)
            tag_desc_dict['content'] = tag_content
            pk = tag_desc_dict[p_key]
            tag_desc_dict_total[pk] = tag_desc_dict


    return tag_desc_dict_total

def make_content(content_dict, sub_tag):
    for sec in list(content_dict[sub_tag].keys()):
        content = content_dict[sub_tag][sec]['content']
        content_no_tag = re.sub('<[^>]*>','',content).strip()
        speaker_ids = re.findall('<speaker[^>]*>', str(content))
        speaker_convers = re.sub('<speaker[^>]*>','||', str(content)).split('||')[1:]
        conver_dict = dict()
        conver_dict["0"] = content_no_tag
        count = 1
        for id, conver in zip(speaker_ids, speaker_convers):
            whole_conver = id + conver
            whole_conver = find_and_remove_tag(BeautifulSoup(whole_conver, 'xml'),'p')
            try:
                meta = eval("{" + ','.join(list(map(lambda x: "\"" + x.split("=")[0] + "\":" + x.split("=")[1],
                                             re.sub('<speaker |>', '', id).split(" ")))) + "}")
            except:
                meta = {}
            meta['content'] = whole_conver
            conver_dict[count] = meta
            count += 1
        content_dict[sub_tag][sec] = conver_dict
    return content_dict

def xml_pickle(file_nm):
    with open(work_dir + file_nm, 'r') as f:
        xml_data = f.read()
    bs_data = BeautifulSoup(xml_data.replace('\n', ''), 'xml')

    content_dict = dict()
    for tag in tag_list:
        content_dict[tag] = find_and_remove_tag(bs_data, tag)[0]
        if tag in tag_dict.keys():
            sub_tag = tag_dict[tag]
            content_dict[sub_tag] = bs_data.find_all(sub_tag)
            if sub_tag == 'company':
                content_dict[sub_tag] = find_and_remove_tag(
                    BeautifulSoup(str(content_dict['companies']), 'xml'),
                    'company')
                del content_dict[tag]
            elif sub_tag == 'participant':
                content_dict[sub_tag] = make_tag_desc_dict(content_dict, sub_tag, p_key='id')
                del content_dict[tag]
            elif sub_tag == 'section':
                content_dict[sub_tag] = make_tag_desc_dict(content_dict, sub_tag, p_key='name')
                content_dict = make_content(content_dict, sub_tag)
                del content_dict[tag]
                print(1)
    with open(work_dir + file_nm.replace('.xml', '.pickle'), 'wb') as handle:
        pickle.dump(content_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def make_xml_pickle_indir(work_dir):
    xml_file_list = list(map(lambda x:x.replace('.xml',''),list(filter(lambda x:'.xml' in x, os.listdir(work_dir)))))
    pkl_file_list = [] #list(map(lambda x:x.replace('.pickle',''),list(filter(lambda x:'.pickle' in x, os.listdir(work_dir)))))
    file_list = list(map(lambda x: x+'.xml', list(set(xml_file_list) - set(pkl_file_list))))
    for file_nm in (file_list):
        print(file_nm)
        xml_pickle(file_nm)

def make_xml_pickle_file(file_nm):
    print(file_nm)
    xml_pickle(file_nm)




tag_list = ['title','date','companies','participants','body']
tag_dict = {
    'companies':'company',
    'participants':'participant',
    'body':'section',
    'section':'speaker',
    'speaker':'plist'
}
tag_nm_list = {
    # 'company':[],
    'participant':['id','type','affiliation','affiliation_entity','title'],
    'section':[],
}

ticker_list = os.listdir('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/')
work_dir = 'C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US')
make_xml_pickle_file('20030416-5798-C.xml')
for ticker in ticker_list:
    print(ticker)
    work_dir = 'C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format(ticker)
    make_xml_pickle_indir(work_dir)




