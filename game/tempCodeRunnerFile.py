    if car.rect.bottom > road.bottom:
        car.y = road.bottom - car.rect.height/2
        car.rect.center = (car.x,car.y)