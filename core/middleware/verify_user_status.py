class VerifyUserStatus:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request, *args, **kwds):
        
        if request.user.is_authenticated:
            print(request.user.username, "middleware")
        else:
            print("Anonymous User", "middleware")

        response = self.get_response(request)

        return response