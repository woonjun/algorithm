def max_score(num_steps, step_scores):
    dp_table = [[0] * 2 for i in range(num_steps)]
    dp_table[0][0] = 0  
    dp_table[0][1] = step_scores[0] 
    if num_steps > 1:
        dp_table[1][0] = step_scores[1] 
        dp_table[1][1] = max(step_scores[0] + step_scores[1], step_scores[1])  
    for i in range(2, num_steps):
        dp_table[i][0] = max(dp_table[i-2][0], dp_table[i-2][1]) + step_scores[i]
        dp_table[i][1] = dp_table[i-1][0] + step_scores[i]  
    return max(dp_table[num_steps-1][0], dp_table[num_steps-1][1])

def main():
    num_steps = int(input("Enter the number of steps (N): "))
    step_scores = []
    for i in range(num_steps):
        score = int(input("Enter the score for each step: "))
        step_scores.append(score)
    result = max_score(num_steps, step_scores)
    print("Maximum score:", result)

if __name__ == "__main__":
    main()
