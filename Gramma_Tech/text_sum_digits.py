import re
def shoppingList(items):
    #prices = list(map(float, re.findall(r'\d[0-9]*\.?\d+', items)))
    matches = re.findall(r'\d[0-9]*\.?\d*', items)
    print (matches)
    prices = []
    for match in matches:
        if len(match) > 0:
            prices.append(float(match))
    print (prices)
    return sum(prices)




def main():
    items = "wanna 22.2&15.3olo 0.00 and 12.12kk0.02 ..34"
    #items = "Doughnuts, 4; doughnuts holes, 0.08; glue, 3.4"
    print (shoppingList(items))

main()
