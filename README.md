### Custom Permission

Decorator IsWorker

```
permission_classes = (IsAuthenticated, IsWorker)
```

Decorator is_owner in methods

```
class ProjetcsView(generics.RetrieveUpdateDestroyAPIView):
    @is_owner('users', 'Project')
    def update(self, request, *args, **kwargs):
```
