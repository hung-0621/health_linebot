class health_assessment():
    
    def __init__(self,profile:tuple,answer:tuple) -> None:
        self.gender = profile[2]
        self.age = profile[3]
        self.height = profile[4]
        self.weight = profile[5]
        self.answer = answer