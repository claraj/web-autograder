from channels.routing import ProtocolTypeRouter, URLRouter
import autograder.routing

print('hello fm project routing')

application = ProtocolTypeRouter({
    'http': URLRouter(autograder.routing.urlpatterns)
})
