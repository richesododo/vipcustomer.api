import wikipedia
from bs4 import BeautifulSoup
import unicodedata
from .vipcalcdata import data as data_, total_data_score


class Wiki_Source:
    '''
       This class is used for getting the data from Wikipedia \n
       Param - full_name -> str
    '''

    def scrape(self, full_name):
        '''
            This function is used to scrape the data with the help of Wikipedia and BeautifulSoup from the web
        '''

        result = {}
        try:
            result = wikipedia.page(title=f'{full_name}').html()
        except:
            return result

        soup = BeautifulSoup(result, "lxml")
        info_data = soup.select('.infobox-data')
        info_label = soup.select('.infobox-label')
        data_dict = {}

        for i in range(len(info_label)):
            data_dict[info_label[i].text] = info_data[i].text
        
        return data_dict


    def calculate_vip_score(self, data):
        '''rating is out of 100'''

        data_dict = data
        cleaned_data_dict = {}

        for x, y in data_dict.items():
            cleaned_data_dict[x.lower()] = y.lower()

        top_level_keys_in_mydata = data.keys() 
        vip_score = 22
        vip_key = []

        for i, key in enumerate(cleaned_data_dict):
            if key.lower() in top_level_keys_in_mydata: 
                vip_score += 2
                vip_key.append(key.lower())
            else:
                pass

        if vip_score > 12:
            for item in vip_key:
                data_from_key = cleaned_data_dict[item]
                check = type(data_from_key)
                if check == list:
                    for i in data_from_key:
                        if i in data_[item].keys():
                            vip_score += 3
                            vip_score += data_[item][i]
                elif check == str:
                    if i in data_[item].keys():
                            vip_score += 3
                            vip_score += data_[item][i]

        else:
            pass

        final_score = (vip_score / total_data_score) * 100 

        return final_score


    def clean_data(self, key, data_dict):
        # data_dict = self.scrape()
        data_val_str = data_dict.get(key)
        
        if data_val_str is not None:
            data_val_str = data_val_str.strip().replace('\n', ' ')
            born_list = data_val_str
            x = unicodedata.normalize('NFKD', born_list).encode('ascii', 'ignore')
            x = x.decode("utf-8")
            return x

        else:
            return data_val_str



    def process(self, dict_):
        full_name = dict_['name']
        data = self.scrape(full_name)
        is_vip = False
        cleaned_data = self.clean_data('Born', data)
        if cleaned_data is not None:
            details = cleaned_data.split(' ')
            name = f'{details[0]} {details[2]} {details[2]}'.lower()

            if len(data) == 0:
                return [data]

            elif not (dict_['name'].lower() in name.lower()):
                return []

            else:
                '''is_vip, First name, Last name, gender, occupation, age'''
                
                find_age = cleaned_data.find('age')
                age = ''
                for i, item in enumerate(cleaned_data):
                    if i == find_age + 4:
                        age += item
                    elif i > find_age and item == ')':
                        age += cleaned_data[i - 1]
                        break
                    else:
                        pass

                gender = self.clean_data('Gender', data)
                occupation = self.clean_data('Occupation', data)
                is_vip = True
                vip_score = self.calculate_vip_score(data) 
                if occupation is None:
                    return [
                        
                            {
                                'name': name,
                                'gender': gender,
                                'occupation': '',
                                'age': age,
                                'is_vip': is_vip,
                                'vip_score': vip_score,
                            }
                        
                    ]
                else:
                    if type(occupation) == list:
                        
                        for i in occupation:
                            i.lower()
                    else:
                        occupation.lower()
                    return [
                        {
                            'name': name,
                            'gender': gender,
                            'occupation': occupation,
                            'age': age,
                            'is_vip': is_vip,
                            'vip_score': vip_score,
                        }
                    ]
        else:
            return []