import json
import requests as req
import pandas as pd
import xmltodict

class CurrencyConversion:
    BASE_URL = 'https://sdw-wsrest.ecb.europa.eu/service/data/'
    def __init__(self):
        pass

    @staticmethod
    def convert_xml_to_dataframe(xml_data):
        """
        Convert XML data into Pandas Dataframe

        :param xml_data:
        :return: DataFrame
        """
        dict_data = xmltodict.parse(xml_data)
        json_data = json.dumps(dict_data)
        data = json.loads(json_data)
        message_dataset = data.get('message:GenericData', {}).get('message:DataSet', {})
        generic_ops_data = message_dataset.get('generic:Series', {}).get('generic:Obs', {})
        dimension_value_lst = {'TIME_PERIOD': [], 'OBS_VALUE': []}
        for dataobj in generic_ops_data:
            dimension_value_lst['TIME_PERIOD'].append(dataobj['generic:ObsDimension']['@value'])
            dimension_value_lst['OBS_VALUE'].append(float(dataobj['generic:ObsValue']['@value']))
        df_minension_value = pd.DataFrame(dimension_value_lst)
        return df_minension_value

    @staticmethod
    def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
        """
        Provide monthly exchange rate of source and target

        :param source:
        :param target:
        :return: DataFrame
        """
        if source:
            url = CurrencyConversion.BASE_URL+'EXR/M.{source}.{target}.SP00.A?detail=dataonly'.format(\
                source=source, target=target)
            resp = req.get(url)
            if resp.status_code == 200:
                df_exchange_rate = CurrencyConversion.convert_xml_to_dataframe(resp.text)
                return df_exchange_rate
            else:
                raise Exception(resp.text)
        else:
            raise Exception("Source is required")

    @staticmethod
    def get_raw_data(identifier: str) -> pd.DataFrame:
        """
        Get indentifier detail

        :param identifier:
        :return: DataFrame
        """
        if identifier:
            url = CurrencyConversion.BASE_URL+'BP6/{identifier}?detail=dataonly'.format(\
                identifier=identifier)
            resp = req.get(url)
            if resp.status_code == 200:
                df_raw_data = CurrencyConversion.convert_xml_to_dataframe(resp.text)
                return df_raw_data
            else:
                raise Exception(resp.text)
        else:
            raise Exception('identifier is required')

    @classmethod
    def get_data(cls, identifier: str, target_currency: str = None) -> pd.DataFrame:
        """
        Data transformation of Exchange rate data and Identifier data

        :param identifier:
        :param target_currency:
        :return: DataFrame
        """
        df_raw_data = cls.get_raw_data(identifier)
        if not df_raw_data.empty:
            if target_currency:
                identifier_currency = identifier.split(".")[12]
                df_exchange_rate = cls.get_exchange_rate(target_currency, identifier_currency)
                if not df_exchange_rate.empty:
                    df_data = pd.merge(df_exchange_rate, df_raw_data, on=['TIME_PERIOD'], how='inner')
                    df_data['OBS_VALUE'] = df_data['OBS_VALUE_x'] * df_data['OBS_VALUE_y']
                    df_data = df_data[['TIME_PERIOD', 'OBS_VALUE']]
                    return df_data
                else:
                    raise Exception("No Exchange Data Available")
            else:
                return df_raw_data
        else:
            raise Exception("No Raw Data Available")
