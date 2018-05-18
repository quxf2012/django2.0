from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import TokenAuthentication

class PostTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if request.method.lower() != 'post':
            return None
        token = request.data.get('auth-token')
        # logger.info('auth-token'+request.POST['auth-token'])
        # logger.info('auth token POST')
        if not token:
            return None

        return self.authenticate_credentials(token)
