

if __name__ == '__main__':
    dist = [10, 20, 50, 15, 7]
    time = [2, 5, 7, 3, 8]

    print ("Global Avg: ", sum(dist)/sum(time))

    local_avg = dist[0]/time[0]
    for i in range(len(dist)):
        if i > 0:
            local_avg = (local_avg*i + (dist[i]/time[i]))/(i+1)

    print ("Local Avg: ", local_avg)
