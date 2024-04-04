import pitch_tracker
from strike_zone import strike_or_ball
import keyboard

######################################################################
# Run Loop with counters keep track of balls and strikes             #
#  - If pitch goes trough strike zone                                #
#    - Print "Strike"                                                #
#    - Add 1 strike to count                                         #
#    - In event the pitch is strike 3, print "Strike 3! You're Out!" #
#  - If pitch does not go through stike zone                         #
#    - Print "Ball"                                                  #
#    - Add 1 ball to count                                           #
#    - In event pitch is ball 4, print "Ball 4! Take your base"      #
######################################################################

def umpire():
    exec(open(pitch_tracker).read()) # Starts the tracking of the pitches

    strike_count = 0
    ball_count = 0

    ##########################################################################################
    # Uses keys on the keyboard to say if another outcome besides a ball or a strike happens #
    # - If key for foul is pressed, the count does not change                                #
    # - If key for hit, out, or hbp is pressed, the count resets to 0-0                      #
    ##########################################################################################
    def foul_hit_out_hbp(outcome):
        global strike_count, ball_count
        if outcome.event_type == keyboard.KEY_DOWN:
            if outcome.name == "F": #Foul
                if strike_or_ball() == True:
                    strike_count = strike_count - 1
                else:
                    ball_count = ball_count - 1
            elif outcome.name == "P": #HBP
                strike_count = 0
                ball_count = 0
            elif outcome.name == "H": #Hit
                strike_count = 0
                ball_count = 0
            elif outcome.name == "O": #Out
                strike_count = 0
                ball_count = 0

    keyboard.on_press(foul_hit_out_hbp)

    while True:
        if strike_or_ball() == True:
            if strike_count < 2:
                print("Strike")
                strike_count += 1
            elif strike_count == 2:
                print("Strike 3, You're Out!")
                strike_count = 0
        elif strike_or_ball() == False:
            if ball_count < 3:
                print("Ball")
                ball_count += 1
            elif ball_count == 3:
                print("Ball 4, Take your base!")
                ball_count = 0

umpire()