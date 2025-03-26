
from django.http import HttpRequest, HttpResponse
import datetime

def set_useragent_on_request_middleware(get_response):
    
    print("init call")
    def middleware(request: HttpRequest):
        print("Before func get_response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("After func get_response")
        return response
    
    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.response_count = 0
        self.exceptions_count = 0
        
    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count:", self.requests_count)
        response = self.get_response(request)        
        self.response_count += 1
        print("response count:", self.response_count)
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("Num of exceptions:", self.exceptions_count)
        
        
class RequestLimiterMiddle:
    """
    Класс содержит словарь соответствий <br>
    { ip пользователя: время обращения }
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_dt_dict = {}
        self.time_limit: int = 3
        
    def __call__(self, request: HttpRequest):
        dt = datetime.datetime.now()
        client_ip = request.META["REMOTE_ADDR"] 
        old_dt = self.ip_dt_dict.setdefault(client_ip, dt)        
        dif: datetime.timedelta = dt - old_dt
        if (old_dt != dt) and (dif.seconds < self.time_limit):
            return HttpResponse(f"Sorry {client_ip}. Limit 1 request per {self.time_limit} seconds", status=429)
        #else
        self.ip_dt_dict[client_ip] = dt
        return self.get_response(request)
        