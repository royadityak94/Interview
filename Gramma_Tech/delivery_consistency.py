def compute_min_index(arr, sub):
    arr.append(24)
    min = float('inf')
    min_idx = 0
    for idx in range(len(arr)-1):
        diff = arr[idx+1] - sub
        if diff > 0 and diff < min:
            min = diff
            min_idx = idx
    return min_idx

def deliveryFee(intervals, fees, deliveries):
    factors = float('inf')

    delivery_interval = [0] * len(intervals)

    for hr, _ in deliveries:
        interval = compute_min_index(intervals, hr)
        delivery_interval[interval] += 1

    factors = []
    print (delivery_interval)

    for idx, (fee, delivery_count) in enumerate(zip(fees, delivery_interval)):
        if delivery_count == 0:
            return False
        factors.append(fee/delivery_count)

        if idx > 0 and len(fees) < 3:
            if factors[idx] != factors[idx-1]:
                return False
        elif idx > 2 and not (factors[idx-2] == factors[idx-1] == factors[idx]):
            return False

    return True

def main():
    intervals = [0, 10, 23]
    fees = [3, 3, 3]
    deliveries = [[0,12], [0,13], [0,51], [9,17], [10,3], [10,59], [22,22], [22,23], [23,0], [23,17], [23,47], [23,48]]

    print (deliveryFee(intervals, fees, deliveries))

main()
