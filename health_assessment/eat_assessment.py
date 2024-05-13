class eat:
    def __init__(self,user_id,age,height,weight,gender,activity_status):
        self.user_id = user_id
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity_status = activity_status
        
    def TDEE_Calculate(self)->float:
        #男性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) + 5
        #女性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) - 161
        TDEE = 10 * self.weight + 6.25 * self.height
        if self.gender == "male":
            TDEE -= (5 * self.age) + 5
        else:
            TDEE -= (5 * self.age) - 161
            
        match self.activity_status:
            case "活動趨於靜態（久坐、躺著不出門）":
                TDEE *= 1.2
            case "活動程度較低（開車、烹飪、散步）":
                TDEE *= 1.375
            case "活動程度正常（做家務、逛街、健走）":
                TDEE *= 1.55
            case "活動程度較高（打球、騎腳踏車、有氧運動）":
                TDEE *= 1.72
            case "活動程度激烈（運動訓練、運動競賽）":
                TDEE *= 1.9
                
        return TDEE
        