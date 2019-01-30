


def data_extraction(myfile):
    """(file open for reading) -> list of lists of strs

    load_profiles helper function, returns the data from myfile into rows of
    list of lists of strings.
    """

    # extract the data from myfile and turn it to rows
    s = myfile.read()
    # make the data iterable
    new_s = s[:-1]
    # get rid of all /n and list out each name pair by double /n
    new_s = new_s.split("\n\n")
    new_l = []
    for item in new_s:
        new_l.append(item.split("\n"))
    return new_l

def switch_name(name):
    """
    Swaps surname and first name, removing the comma.
    Percondition: name has a comma
    """
    temp = name.split(',')
    return temp[1][1:] + ' ' + temp[0]


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def load_profiles(profiles_file, person_to_friends, person_to_networks):
    """ (file open for reading, dict of {str: list of str},
         dict of {str: list of str}) -> NoneType

    This function mutates two input dictionaries. Each dictionary uses the
    person's name as a key and its friends' name in a list and its relatated
    networks as a list for person_to_friends, and person_to_networks,
    respectively

    >>> profiles_file = open("profiles.txt")
    >>> person_to_friends = {}
    >>> person_to_networks = {}
    >>> load_profiles(profiles_file, person_to_friends, person_to_networks)
    """
    # use the helper function data_extraction to get the data
    # from profiles_file.
    profiles_list = data_extraction(profiles_file)
    for person_info in profiles_list:
        # we remove the first file of the list
        person_key = switch_name(person_info[0])
        person_to_friends[person_key] = []
        person_to_networks[person_key] = []
        for item in person_info[1:]:
            # if it has comma, its because its a person, else it will be a net.
            if "," in item:
                person_to_friends[person_key].append(switch_name(item))
            else:
                person_to_networks[person_key].append(item)


def invert_networks_dict(person_to_networks):
    """ (dict of {str: list of str}) -> dict of {str: list of str}

    The values in person_to_networks will become keys and each will only
    appear once. The keys in person_to_networks become values and each
    will be catagorized under their previous values.

    >>>b = {'Phil Dunphy': ['Real Estate Association'], 'Claire Dunphy':
    ['Parent Teacher Association'], 'Gloria Pritchett':
    ['Parent Teacher Association']}
    >>>invert_networks_dict(b)
    {'Real Estate Association': ['Phil Dunphy'], 'Parent Teacher Association':
    ['Claire Dunphy', 'Gloria Pritchett']}
    >>> a = {'Cameron Tucker': ['Clown School', 'Wizard of Oz Fan Club'],
    'Gloria Pritchett': ['Parent Teacher Association']}
    >>> invert_networks_dict(a)
    {'Clown School': ['Cameron Tucker'], 'Wizard of Oz Fan Club':
    ['Cameron Tucker'], 'Parent Teacher Association': ['Gloria Pritchett']}
    """
    # get the keys and values in person_to_networks so that we can swap them
    inverted_network_dict = {}
    for key in person_to_networks:
        for value in person_to_networks[key]:
            # turn names (key) that have the same networks to values
            # and turn the network to their key
            if value in inverted_network_dict:
                inverted_network_dict[value].append(key)
            # swap every other names and networks to values and keys
            else:
                inverted_network_dict[value] = [key]
    return inverted_network_dict



def make_recommendations(person, person_to_friends, person_to_networks):
    """ (str, dict of {str: list of str}, dict of {str: list of str})
        -> list of (str, int) tuple
    Makes friends recommendation based on their friends in common and on their
    common networks. If they have a surname in common, recommendation score is
    higher.
    Returns a list of tuple with the recommended person and its score.
    +1 point for each friend in common,
    +1 point for each network in common,
    +1 point if they already have any point and have a surname in common.

    >>> profiles_file = open("profiles.txt")
    >>> person_to_friends = {}
    >>> person_to_networks = {}
    >>> load_profiles(profiles_file, person_to_friends, person_to_networks)
    >>> make_recommendations('Claire Dunphy', person_to_friends, person_to_networks)
    [('Gloria Pritchett', 2), ('Manny Delgado', 1), ('Luke Dunphy', 3), ('Cameron Tucker', 1)]
    """
    #
    if person in person_to_networks:
        targets_networks = person_to_networks[person]
    else:
        targets_networks = []
    if person in person_to_friends:
        targets_friends = person_to_friends[person]
    else:
        targets_friends = []

    recommendation_list = []

    for key_person in person_to_friends:

        # We don't want to search through the target person's info right now
        # nor take any info if they already  are friends
        if person != key_person and key_person not in targets_friends:
            # We check if each friend from the person we want to make
            # recommendation to, is in the list from the other persons
            for friend in targets_friends:
                if friend in person_to_friends[key_person]:
                    recommendation_list.append(key_person)


    for key_person in person_to_networks:
        # We don't want to search through the target person's info right now
        # nor take any info if they already  are friends
        if person != key_person and key_person not in targets_friends:
            for network in person_to_networks[key_person]:
                if network in targets_networks:
                    recommendation_list.append(key_person)



    output_list = []
    for name in recommendation_list:
        # Check how many times their name appear on the recommendation list
        score = recommendation_list.count(name)
        # Give an extra point if they have an extra point
        if person.split(' ')[1] == name.split(' ')[1]:
            score += 1
        flag_repetition = False
        # Check if we have already included that name
        for tup in output_list:
            if tup[0] == name:
                flag_repetition = True
        # If we haven't included the name yet, we append on the output list
        if not flag_repetition:
            output_list.append((name, score))



    return output_list


def sort_recommendations(recommendations):
    """ (list of (str, int) tuple) -> list of str

    This function returns a list of potential friend's names ordered by score
    from highest to lowest. If multiple potential friends have the same score,
    they should follow the alphabetical order instead.

    >>> d = [('Manny Delgado', 1), ('Cameron Tucker', 1)]
    >>> sort_recommendations(d)
    ['Cameron Tucker', 'Manny Delgado']
    >>> d = [('Gloria Pritchett', 2), ('Luke Dunphy', 3)]
    >>> sort_recommendations(d)
    ['Luke Dunphy', 'Gloria Pritchett']

    """

    names_by_score = []
    score = 0
    # need a list to sort before append the final list
    a_list = []
    while recommendations:
        for name_score in recommendations:
            if name_score[1] == score:
                a_list.append(name_score[0])
            elif name_score[1] > score:
                score = name_score[1]
                a_list = [name_score[0]]
        a_list.sort()
        names_by_score.extend(a_list)
        for name in recommendations[:]:
            if name[0] in a_list:
                recommendations.remove(name)
        score = 0
        a_list = []

    return names_by_score


if __name__ == '__main__':

    # Use these messages in your code below.
    prompt_msg = "Please enter a person (or press return to exit): "
    no_recommendations_msg = "There are no recommendations for this person."
    exit_msg = "Thank you for using the recommendation system!"

    # During testing, we may change the values of these variables to non-empty
    # dictionaries or to different files.
    friendships = {}
    networks = {}

    profiles_file = open('profiles.txt')
    load_profiles(profiles_file, friendships, networks)
    # query = input(prompt_msg)
    # recommendations =  make_recommendations(query, friendships, networks)
    # sorted_recommendations = sort_recommendations(recommendations)
    query = input(prompt_msg)
    while query != "":
        recommendations = make_recommendations(query, friendships, networks)
        sorted_recommendations = sort_recommendations(recommendations)
        if len(sorted_recommendations) == 0:
            print(no_recommendations_msg)
        else:
            for item in sorted_recommendations:
                print(item)
        query = input(prompt_msg)
    if query == "":
        print(exit_msg)
    profiles_file.close()
