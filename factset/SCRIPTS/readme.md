# XML cleaner

## xml file -> pickle

### 데이터 구조도

#### 0.상위 key
['title', 'date', 'company', 'participant', 'section']

#### 1. title -> str
#### 2. date -> str(yyyy-mm-dd)
#### 3. company -> list
#### 4. participant -> dict
* key : participant_id 
* value : dict (id: id/type/content + affiliation/affiliation_entity/entity/title)
#### 5. section -> dict
* key : section_name
* value : dict (num : id/content, 0은 전체 데이터)
