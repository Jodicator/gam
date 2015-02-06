import Jmap
import socket
Xspawn = 13
Yspawn = 37
user_info = [["player", Xspawn, Yspawn, 0]] #contains all player info

def server_talk(IP, port):
    #important server variables, also map
    global user_info
    input_string = ""
    output_string = ""
    user_string = ""
    user_id = 0
    game_map = Jmap.game_map
    
    def which_user(user_name):
        global user_info
        x_max = len(user_info)
        if (x_max != 0):
            for x in range(0, x_max):
                if (user_info[x][0] == user_name):
                    return x
        user_info.append([user_name, Xspawn, Yspawn, 0])        
        return len(user_info) - 1

    def server_calcs(action):
        def collision(X_pos, Y_pos):
            if (game_map[X_pos][Y_pos] == "#"): #add all symbols that are not possible to walk on.
                print "player collides with object"
                return 0
            else:
                #the following for loop checks if move would collide with any players' coords.
                x_max = len(user_info)
                for x in range(0, x_max):
                    if (user_info[x][1] == X_pos):
                        if(user_info[x][2] == Y_pos):
                            return 0
                return 1

        global user_info
        return_map = ""
    
        if (action == ".\r\n"):
            print "player does nothing"
        elif (action == "up\r\n"):
            print "up received"
            if (collision(user_info[user_id][1], (user_info[user_id][2] - 1))):
                user_info[user_id][2] -= 1
        elif (action == "down\r\n"):
            print "down received"
            if (collision(user_info[user_id][1], (user_info[user_id][2] + 1))):
                user_info[user_id][2] += 1
        elif (action == "left\r\n"):
            print "left received"
            if (collision((user_info[user_id][1] - 1), user_info[user_id][2])):
                user_info[user_id][1] -= 1
        elif (action == "right\r\n"):
            print "right received"
            if (collision((user_info[user_id][1] + 1), user_info[user_id][2])):
                user_info[user_id][1] += 1
        
        i = -5
        while (i < 6):
            j = -5
            while (j < 6):
                x_max = len(user_info)
                is_player = 0
                for x in range(0, x_max):
                    if (user_info[x][1] == user_info[user_id][1] + j):
                        if (user_info[x][2] == user_info[user_id][2] + i):
                            return_map += "@"
                            is_player = 1
                            break
                if (not is_player):
                    return_map += game_map[(user_info[user_id][1] + j)][(user_info[user_id][2] + i)]
                j += 1
            i += 1
            j = -5
            return_map += "n"
        return return_map
    

    IPlink = socket.socket()
    IPlink.connect((IP, port))
    print "Connected"
    
    looper = 1
    while (looper == 1):
        print "loop"
        user_string = IPlink.recv(4096) #first gets username, second gets action.
        input_string = IPlink.recv(4096)
        #run function for incoming user here
        user_id = which_user(user_string)
        
        if (input_string == "I quit\n"):
            output_string = "quitting player"
            print output_string
            user_info.pop(user_id)
            IPlink.send(output_string + "\n")
            #looper = 0
        else:
            output_string = server_calcs(input_string)
            print "sending back output"
            IPlink.send(output_string + "\n")
            print "coords are now at x =", user_info[user_id][1], "y =", user_info[user_id][2]

    IPlink.close()

server_talk("127.0.0.1", 6790)
print "server closed"
