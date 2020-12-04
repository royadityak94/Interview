
import statistics


if __name__ == '__main__':
    arr = list(range(1, 11))
    last_avg = arr[1]
    map = [arr[0], 1]

    print (">> ", arr)
    for idx in range(2, len(arr)+1):
        current_avg, current_cnt = map
        new_avg = (current_avg*current_cnt + arr[idx-1])/(idx)
        map = [new_avg, current_cnt+1]

        #last_avg = (last_avg*(idx-1) + arr[idx-1])/(idx)
        ws = arr[:idx]
        computed_sum = sum(ws)
        print (idx-1, ws, computed_sum,  statistics.mean(ws), new_avg)
