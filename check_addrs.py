import time

import requests
from datetime import datetime, timedelta
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed


# 替换为你的API密钥
API_KEYS = {
    'ethereum': '2VQG8WZ51WTDHP8PAMIK7PIJI8CBRYIQ2C',
    'bsc': 'RFCSK8XXZS2XJVFDMURFQ5XM6SYTTSZXQC',
    #'avalanche': 'your_avaxscan_api_key',
    'polygon': 'UMEJFSRUIGZ88YVXW3V3JBTU8545VB9A8Q',
    'arbitrum': 'P6Y821ZG334FU3VGZXRJPDJQVKWZIGM62N',
    'optimism': 'AT9MIY9XMB5FUSY188S1P28ERZE5P3TEG8',
    'base': '4Q233M1B6CFJ9U1JEMCRDV3IMUYVEI756U',
    'ftm': 'RXPWTWTA63GVGH27RCCINDJ3CMTPT8IRZQ',
    #'celo': 'your_celoscan_api_key',
    'gnosis': 'UMEJFSRUIGZ88YVXW3V3JBTU8545VB9A8Q',
    'zksync': 'your_zksyncscan_api_key'
}

API_URLS = {
    'ethereum': 'https://api.etherscan.io/api',
    'bsc': 'https://api.bscscan.com/api',
    'avalanche': 'https://api.snowtrace.io/api',
    'polygon': 'https://api.polygonscan.com/api',
    'arbitrum': 'https://api.arbiscan.io/api',
    'optimism': 'https://api-optimistic.etherscan.io/api',
    'base': 'https://api.basescan.org/api',
    'ftm': 'https://api.ftmscan.com/api',
    'celo': 'https://api.celoscan.io/api',
    'gnosis': 'https://api.gnosisscan.io/api',
    'zksync': 'https://block-explorer-api.mainnet.zksync.io/api'
}

def loadaccounts(filename):
    accounts = []
    try:
        txt_file = open(filename, "r")
        accounts = txt_file.read().splitlines()
        txt_file.close()
        for i in range(len(accounts)):
            if accounts[i].count('\t') > 0:
                accounts[i] = accounts[i].replace('\t', ' ')
    except Exception as e:
        print('load error', e)
        txt_file.close()
    finally:
        return accounts

def get_internal_transactions(address, chain):
    tryCount = 0
    while tryCount < 5:
        try:
            url = API_URLS[chain]
            api_key = API_KEYS[chain]
            params = {
                'module': 'account',
                'action': 'txlistinternal',
                'address': address,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'asc',
                'apikey': api_key
            }
            if chain == 'zksync':
                del params['apikey']
            response = requests.get(url, params=params)
            data = response.json()
            if data['status'] == '1':
                return data['result']
            else:
                return []
        except Exception as e:
            print('retrive error:',e)
            tryCount += 1
            time.sleep(1.5)
    return []

def check_within_3_days(wallet_addresses, chain):
    first_tx_dates = []

    for address in wallet_addresses:
        transactions = get_internal_transactions(address, chain)

        if transactions:
            first_tx = transactions[0]
            timestamp = int(first_tx['timeStamp'])
            date = datetime.utcfromtimestamp(timestamp).date()
            formatted_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            value = int(first_tx['value']) / (10 ** 18)
            hash = first_tx['hash']
            first_tx_dates.append((address, date,formatted_time,first_tx['from'],value,hash))
        else:
            print(f"No internal transactions found for address: {address} on {chain}")
            break

    if not first_tx_dates:
        print(f"No internal transactions found for any address on {chain}.")
        return False, chain,[]

    # 找到最早的日期和最晚的日期
    min_date = min(date for _, date,_,_,_,_ in first_tx_dates)
    max_date = max(date for _, date,_,_,_,_ in first_tx_dates)

    # 检查是否在3天内
    within_3_days = (max_date - min_date).days <= 3

    if within_3_days:
        print(f"All first internal transactions occurred within 3 days on {chain}.")
    else:
        print(f"First internal transactions did not occur within 3 days on {chain}.")

    return within_3_days, chain,first_tx_dates

# 示例钱包地址集合

#wallet_addresses = loadaccounts('./cluster-1.txt')
df = pd.read_csv('./dune_1500k_group.csv')
chains = ['ethereum', 'bsc', 'avalanche', 'polygon', 'arbitrum', 'optimism', 'base', 'ftm', 'celo', 'gnosis', 'zksync']
chains = ['ethereum', 'bsc', 'polygon', 'arbitrum', 'optimism', 'base', 'ftm', 'gnosis', 'zksync']

# 根据groupid列进行分组
grouped = df.groupby('groupid')

# 创建一个空的DataFrame
columns = ['Group','Chain', 'Address', 'Time', 'From', 'Value','Hash']
df_result = pd.DataFrame(columns=columns)
# 遍历每个分组并提取ua列进行后续处理
for group_id, group in grouped:
    ua_list = group['ua'].tolist()
    executor = ThreadPoolExecutor(len(chains))
    threads = []

    for chain in chains:
        thread = executor.submit(check_within_3_days, ua_list, chain)
        threads.append(thread)

    for thread in threads:
        within_3_days, chain,first_tx_dates = thread.result()
        if within_3_days:
            for address, _, formatted_time, from_addr, value, hash in first_tx_dates:
                print(f"Group: {group_id}, Chain: {chain}, Address: {address}, Time: {formatted_time}, From: {from_addr}, Value: {value}, Hash: {hash}")
                # 创建一个包含当前数据的临时DataFrame
                temp_df = pd.DataFrame([{
                    'Group': group_id,
                    'Chain': chain,
                    'Address': address,
                    'Time': formatted_time,
                    'From': from_addr,
                    'Value': value,
                    'Hash': hash
                }])

                # 使用pd.concat将临时DataFrame添加到主DataFrame
                df_result = pd.concat([df_result, temp_df], ignore_index=True)
# 保存DataFrame为CSV文件
df_result.to_csv('check_first_2.csv', index=False)
