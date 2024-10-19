# myapp/context_processors.py
def user_profile_data(request):
    if request.user.is_authenticated:
        return {
            'user_name': request.user.name,  
            'user_profile_picture': request.user.profile_picture.url if request.user.profile_picture else None
        }
    return {'user_name': None, 'user_profile_picture': None}

