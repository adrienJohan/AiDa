from workflows.nutrition import route_nutrition_request

def route_nutrition_input( user_message, image_path=None) :
    if image_path is not None: 
        return "meal_image"
    
    return route_nutrition_request(user_message)