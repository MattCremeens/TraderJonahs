import json


def get_values(data):
    quantities = {}
    prices = {}
    cost = 0
    for tool_call in data['outputs']['tool_calls']:
        if tool_call['function']['name'] == 'create_an_order':
            qty = json.loads(tool_call['function']['arguments'])['qty']
            side = json.loads(tool_call['function']['arguments'])['side']
            symbol = json.loads(tool_call['function']['arguments'])['symbol']
            if side == 'buy':
                quantities[symbol] = qty
            else:
                quantities[symbol] = -qty

    for message in data['inputs']['messages']:
        if message.get('name') == 'get_snapshot':
            symbol = json.loads(message['content'])['symbol']
            price = json.loads(message['content'])['latestTrade']['p']
            prices[symbol] = price
    
    for symbol, quantity in quantities.items():
        if symbol in prices:
            cost += quantity * prices[symbol]
    
    return quantities, prices, cost


if __name__ == "__main__":
    f = open('../run.json', 'r')
    data = json.load(f)
    print(get_values(data))