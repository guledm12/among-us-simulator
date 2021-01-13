def load_map(file_path):                                                #Function that opens a file and returns a dictionary of rooms and their adjacent rooms.
    f = open(file_path, "r")                                            #Opens file.
    load_map.rooms = {}                                                 #Dictionary that tracks rooms and adjacent rooms.
    for i in f:
        adjacent_rooms = []                                             #List of adjacent rooms that will be added to each key.
        i = i.strip("\n").split(":")                                    #Splits the room and thr adjacent rooms and removes whitespace.
        i[1] = i[1].split(",")                                          #Splits the adjacent rooms.
        for j in i[1]:
            j = j.strip()                                               #Strips each adjacent room of it's whitespace
            adjacent_rooms.append(j)                                    #Adds stripped adjacent room to the full list.
        load_map.rooms[i[0]] = adjacent_rooms                           #Sets each key (room) and value (adjacent room)
    f.close()                                                           #Closes file.
    return load_map.rooms                                               #Returns dictionnary.

def simplify_testimony(chat,rooms):                                     #Function that returns simplfied versions of chat messages.
    COLORS = ["red","blue","green","yellow","brown","pink","orange"]    #Constant list of all possible user colours.
    chat_list = []                                                      #List that contains each message's word.
    chat_room = []                                                      #List that tracks the room mentionned in a message.
    chat_color = []                                                     #List that tracks the color mentionned in a message.
    rooms_list = []                                                     #List that contains all keys from rooms dictionary.
    for a in rooms.keys():                                              #Takes the keys from the rooms dictionnary and turns any multi-word room string into a list with all words in the name.
        if " " in a:
            a = a.split(" ")
        rooms_list.append(a)
    if ("voted" in chat) == False:                                      #Simplfies non-vote messages.
        chat = chat.rstrip("\n").split(":")                             #Splits speaker from message.
        chat[1] = chat[1].strip(" .").split(" ")                        #Splits each word.
        for c in chat[1]:
            c = c.strip(",.?")                                          #Strips punctuation from each word.
            chat_list.append(c)
        one_string = ""                                                 #String that will turn a multi-word room list into one string.
        for i in chat_list:                                             #Iterates over each word in message.
            for j in rooms_list:                                        #Iterates over each room name.
                if type(j) is list:                                     #If statement that handles multi-word room names.
                    for l in j:                                         #Iterates over each word in the multi-word room list.
                        if (i.find(l) != -1):                           #If word from chat matches any word from multi-word room list.               
                            if (i in one_string.strip().split(" ")) == False:   #If word has been mentionned (Also makes sure no duplicates are added)
                                one_string = one_string + " " + l       #Adds word to string.
                            a = one_string.strip().split(" ")                   
                            if a == j:                                  #Makes sure that the multi-word room name derived from the chat matches the room name from the keys dictionnary.
                                chat_room.append(one_string)
                else:
                    if i.find(j) != -1:                                 #Handles single-word room names. If word matches any room in room list
                        chat_room.append(j)
            for k in COLORS:                                            #Iterates over all possible user colors.
                if i.find(k) != -1:                                     #If word matches any color in color list.
                    chat_color.append(k)   
         
        if (len(chat_room) >= 1) and (len(chat_color) >= 1):            #If both a room and color have been mentionned.
            return( "%s: %s in %s" % (chat[0],chat_color[0],chat_room[0]))  #Returns a statement of a user talking about someone else and the room. 
        elif (len(chat_room) >= 1):                                     #If just a room has been mentionned.
            return( "%s: %s in %s" % (chat[0],chat[0],chat_room[0]))    #Returns statement of a user talking about him/herself and the room.
        else:                                                           #If no useful info has been mentionned.
            return("")                                                  #Returns an empty string

    else:                                                               #Simplfies vote messages.
        chat = chat.rstrip("\n")                                        
        return(chat)                                                    #Returns chat message without white-space.
            
def load_chat_log(file_path,rooms):                                     #Function that loads a chat from a file and simplifies the chat.
    load_chat_log.chat_log = []                                         #List (referred to as a chat log) that will keep track of simplfied messages
    f = open(file_path, "r")                                            #Opens file.                                    
    for i in f:                                                         #Iterates over file.
        if (simplify_testimony(i,load_map.rooms) != ""):                #Makes it so useless info isn't added to chat log.
            load_chat_log.chat_log.append(simplify_testimony(i,load_map.rooms))  #Adds useful info to chat log with the simplify_testimony function.
    f.close()                                                           #Closes file.
    return load_chat_log.chat_log                                       #Returns chat log

def tally_votes(chat_log):                                              #Function that takes in the chat log creates a dictionnary and keeps track of votes.
    votes = {"red" : 0,"blue" : 0,"green" : 0,"yellow" : 0,"brown" : 0,"pink" : 0,"orange" : 0,"skip": 0}   #Dictionnary that will be updated.
    for i in chat_log:                                                  
        if ("voted" in i):                                              #Iterates only over chat log vote messages 
            i = i.split(" ")
            votes[i[2]]+=1                                              #Takes in the part of the info that mentions whos been voted, and adds the corresponding info to the dictionnary.
    return votes                                                        #Returns the dictionnary.

def get_path(chat_log):                                                 #Function that takes in the chat log and creates a dictionnary which tracks each user's path.
    get_path.path_dict = {"red" : [],"blue" : [],"green" : [],"yellow" : [],"brown" : [],"pink" : [],"orange" : []} #Dictionnary that will be updated.
    for i in chat_log:                                                  
        one_string = ""                                                 #String that will turn a multi-word room list into one string.
        if ("in" in i):                                                 #Iterates only over chat log non-vote messages.
            j = i.split(" ")                                            #Splits simplified info into seperate words.
            if len(j) > 4:                                              #If statement that handles multi-word room manes (if the splitted word list > 4, we know the room has multiple words in it.)
                for x in range(3,len(j)):                               #Iterates over each of these multiple words.
                    one_string = one_string + " " + j[x]                #Adds each word to single-word string.
                j[3] = one_string.strip()                               #Turns multi-word room name into a single string.
            if j[1] + ":" == j[0]:                                      #If statement that makes sure that each user is talking about themselves.
                get_path.path_dict[j[1]].append(j[3])                   #Adds location in the chat log senten
    return get_path.path_dict                                           #Rerurns the dictionnary with each user's path.

def get_sus_paths(path_dict,rooms):                                     #Function that finds out which's user's path was suspicious and returns a list of suspects.
    suspicious = []                                                     #List that tracks suspects.
    for i in path_dict.items():
        if len(i[1]) != 0:                                              #Iterates over users' paths (only users who actually have a path).
            for j in range(len(i[1])):                                  #Iterates over each user's path
                if(j!=0) and ((i[1][j] in rooms[i[1][j-1]] ) == False): #If a room in a user's path isn't in the previous room's list of adjacent rooms, we have a suspect.
                    suspicious.append(i[0])                             #Add user's color to list of suspects.
    return(suspicious)                                                  #Returns list of suspects
  
def main():                                                            
    load_map("skeld.txt")
    load_chat_log("chatlog.txt",load_map.rooms)
    tally_votes(load_chat_log.chat_log)
    get_path(load_chat_log.chat_log)
    get_sus_paths(get_path.path_dict,load_map.rooms)

if (__name__ == "__main__"):
    main()