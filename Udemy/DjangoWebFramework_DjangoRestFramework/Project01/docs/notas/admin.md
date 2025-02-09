# Listar usuarios Django

Para listar os usuários do Django, enter no terminal e execute o comando:

```bash
python mange.pu shell
```

Em seguida, execute os seguinte comandos:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
users
```

O comando `User.objects.all()` retorna todos os usuários do Django. O comando `users` exibe a lista de usuários.

# Criar usuário Django

```bash
python manage.py createsuperuser --username=admin --email=admin@gmail.com
```


# Alterar senha de usuário Django

```bash
python manage.py changepassword <user-name>
```


# Usuários

| User | Password |
| ---- | -------- |
| root | root     |
| admin | admin   |

