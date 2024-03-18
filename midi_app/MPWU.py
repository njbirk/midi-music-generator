import random

def algoMPWU():
    # e: reweighting factor
    e = 0.05
    # num: max number of possible melodies/songs
    num = 500
    # melody will be the array of all possible melodies
    # now, it's still up in the air of how many melodies there are, so I leave it empty for now.
    # TODO: finalize the melody array once everything is ironed out 
    melody =  ["Kevin"] * num
    # arr: array storing the probability / frequency distribution of the melodies
    # intialize it so that every melody has equal probability to be recommended
    arr = [1] * num

    choice = random.choices(melody, weights = arr, k = 1)

    # present the melody choice to the user and waiting for response
    # wait for reponse, denoted f = -1, 0, 1. -1 means dislike, 0 neutral, 1 likes
    # TODO: discuss with front-end team how this code will be written line 18 now is just a placeholder
    f = 0
    update = melody.index(choice[0])
    # update the distribution according to whether the user like the song or not
    # i.e if the user like it, we add more weight on it so that next time it has more chance being suggested; if not, suggest less often
    arr[update] = (1 + f*e)*arr[update]

