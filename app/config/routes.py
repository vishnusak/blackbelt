from system.core.router import routes

routes['default_controller'] = 'Login'
routes['/login'] = 'Login#get_login'
routes['/register'] = 'Login#get_register'
routes['/logout'] = 'Login#logout'
routes['POST']['/register'] = 'Login#register'
routes['POST']['/login'] = 'Login#login'
routes['/friends'] = 'Friends#home'
routes['/friends/<id>/add'] = 'Friends#add'
routes['/friends/<id>/remove'] = 'Friends#remove'
routes['/friends/<id>'] = 'Friends#profile'
