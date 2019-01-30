import a2_functions


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
    profiles = load_profiles(profiles_file, friendships, networks)
    #query = input(prompt_msg)
    #recommendations =  make_recommendations(query, friendships, networks)
    #sorted_recommendations = sort_recommendations(recommendations)
    query = input(prompt_msg)
    while query != "":
        recommendations = make_recommendations(query, friendships, networks)
        sorted_recommendations = sort_recommendations(recommendations)
        if len(recommendations) == 0:
            print(no_recommendations_msg)
        else:
            for item in sorted_recommendations:
                print(item)
        query = input(prompt_msg)
    if query == "":
        print(exit_msg)
    profiles_file.close()
