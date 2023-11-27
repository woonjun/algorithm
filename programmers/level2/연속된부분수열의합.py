def calculate_cumulative_sum(sequence):
    cumulative_sum = [0]
    total = 0
    for num in sequence:
        total += num
        cumulative_sum.append(total)
    return cumulative_sum

def solution(sequence, k):
    answer = []; distance = k//sequence[len(sequence)-1]-1

    camulative_sum = calculate_cumulative_sum(sequence)

    while(distance<len(sequence)):
        start = 0; end = len(sequence)
        while(start<=end):
            mid = (start+end)//2
            try:
                if(k>(camulative_sum[mid+1]-camulative_sum[mid-distance])):
                    start = mid+1
                elif(k<(camulative_sum[mid+1]-camulative_sum[mid-distance])):
                    end = mid-1
                else:
                    if(sequence[mid] == sequence[mid-distance]):
                        a = sequence.index(sequence[mid])
                        return[a,a+distance]
                    else:
                        return [mid-distance,mid]
            except:
                break     

        distance+=1
    return answer

test=[
[[1, 2, 3, 4, 5],7,[2, 3]],
[[1, 1, 1, 2, 3, 4, 5],	5,	[6, 6]],
[[2, 2, 2, 2, 2],	6,	[0, 2]],
[[2,2,2,2,2,10,10,10,10,10,10],30,[5,7]]
]
for i in range(len(test)):
    print(f'mine = {solution(test[i][0],test[i][1])} result = {test[i][2]}')
