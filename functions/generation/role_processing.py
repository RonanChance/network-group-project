def convert_names(role):
        
    if 'Casting' in role:
        return 'Casting'
    elif 'Writing' in role:
        return 'Writing Credits'
    elif 'Costume' in role:
        return 'Costume Design'
    elif ('Production' in role) or ('Produced' in role):
        return 'Production'
    elif 'Music' in role:
        return 'Music'
    elif 'Art' in role:
        return 'Art'
    elif 'Cast' in role:
        # remove cast roles
        return None
    elif 'Additional' in role:
        # remove additional cast roles
        return None
    elif 'Thanks' in role:
        return None
    else: 
        return role
