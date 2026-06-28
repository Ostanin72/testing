def vote(votes):
    max_count_vote = 0
    for i in set(votes):
        if votes.count(i) > max_count_vote:
            max_count_vote = votes.count(i)
            max_vote = i
    return max_vote


if __name__ == '__main__':
    print(vote([1, 1, 1, 2, 3]))
    print(vote([1, 2, 3, 2, 2]))