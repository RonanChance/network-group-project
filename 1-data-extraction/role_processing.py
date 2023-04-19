def Convert_Names(role):
        
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
        return 'Cast'
    else: 
        return role
