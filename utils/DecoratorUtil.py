from fastapi import Form


class DecoratorUtil:
    def form_body(self, cls):
        cls.__signature__ = cls.__signature__.replace(
            parameters=[
                arg.replace(default=Form(...))
                for arg in cls.__signature__.parameters.values()
            ]
        )

        return cls